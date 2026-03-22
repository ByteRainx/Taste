"""CLI entry point for taste."""

import asyncio
import logging
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path

import draccus

from taste.data.cache import DiskCache
from taste.data.models import AuthorProfile
from taste.data.selector import select_papers
from taste.data.semantic_scholar import SemanticScholarConfig

log = logging.getLogger("taste")


@dataclass
class LLMArgs:
    """LLM configuration."""
    model: str = "claude-sonnet-4-20250514"
    temperature: float = 0.3
    max_tokens: int = 8192
    api_key: str = ""

    def build(self):
        from taste.llm.claude import ClaudeBackend
        key = self.api_key or os.environ.get("ANTHROPIC_API_KEY", "")
        if not key:
            raise ValueError("Set ANTHROPIC_API_KEY env var or pass --llm.api_key")
        return ClaudeBackend(model=self.model, api_key=key, temperature=self.temperature, max_tokens=self.max_tokens)


@dataclass
class ShowConfig:
    """taste: Paper is cheap, show me the taste."""

    researcher: str = ""
    researcher_id: str | None = None

    # Data source
    s2_api_key: str | None = None

    # LLM
    llm: LLMArgs = field(default_factory=LLMArgs)

    # Output
    output_file: str | None = None

    # Cache
    cache_dir: str = "~/.cache/taste"
    no_cache: bool = False

    verbose: bool = False


async def _run_show(cfg: ShowConfig) -> None:
    from rich.console import Console
    from rich.progress import Progress, SpinnerColumn, TextColumn

    from taste.analysis.aggregator import aggregate
    from taste.analysis.career import build_career_timeline
    from taste.analysis.paper_analyzer import analyze_all_phases
    from taste.output.markdown import render_markdown
    from taste.output.terminal import print_profile

    console = Console()

    if not cfg.researcher and not cfg.researcher_id:
        console.print("[red]Error:[/red] Provide --researcher 'Name' or --researcher-id ID")
        sys.exit(1)

    # Build components
    fetcher = SemanticScholarConfig(api_key=cfg.s2_api_key).build()
    llm = cfg.llm.build()
    cache = DiskCache(cfg.cache_dir) if not cfg.no_cache else None

    try:
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
            # --- Resolve author ---
            if cfg.researcher_id:
                task = progress.add_task("Fetching author info...")
                author = await fetcher.get_author(cfg.researcher_id)
                progress.update(task, description=f"Found: {author.name} ({author.citation_count:,} citations)")
                progress.remove_task(task)
            else:
                task = progress.add_task(f"Searching for '{cfg.researcher}'...")
                candidates = await fetcher.search_author(cfg.researcher)
                progress.remove_task(task)
                if not candidates:
                    console.print(f"[red]No authors found for '{cfg.researcher}'[/red]")
                    return
                author = candidates[0]  # Pick highest-cited match
                console.print(
                    f"  Found: [bold]{author.name}[/bold] "
                    f"({author.citation_count:,} citations, h-index {author.h_index})"
                )

            # --- Fetch papers (with cache) ---
            profile = cache.get_profile(author.id) if cache else None
            if profile:
                console.print(f"  Using cached data ({len(profile.papers)} papers)")
                all_papers = profile.papers
            else:
                task = progress.add_task("Fetching all papers...")
                all_papers = await fetcher.get_author_papers(author.id)
                progress.update(task, description=f"Fetched {len(all_papers)} papers")
                progress.remove_task(task)
                if cache:
                    cache.set_profile(author.id, AuthorProfile(author=author, papers=all_papers))

            # --- Select papers ---
            selected = select_papers(author.id, all_papers)
            high = sum(1 for p in selected if p.contribution_level == "high")
            console.print(f"  Selected {len(selected)} papers ({high} high-contribution, {len(selected) - high} fill)")

            # --- Build career timeline ---
            task = progress.add_task("Inferring career timeline...")
            career = await build_career_timeline(author, selected, llm)
            progress.remove_task(task)

            for phase in career.phases:
                console.print(f"    {phase.name} ({phase.years}): {len(phase.papers)} papers")

            # --- Phase 1: Per-phase analysis ---
            for i, phase in enumerate(career.phases):
                task = progress.add_task(f"Analyzing phase {i+1}/{len(career.phases)}: {phase.name}...")
                progress.remove_task(task)

            task = progress.add_task(f"Analyzing {len(career.phases)} phases...")
            phase_analyses = await analyze_all_phases(author, career.phases, llm)
            progress.remove_task(task)

            # --- Phase 2: Aggregation ---
            task = progress.add_task("Generating taste profile...")
            taste_profile = await aggregate(author, career, phase_analyses, selected, llm)
            progress.remove_task(task)

        # --- Output ---
        print_profile(taste_profile)

        if cfg.output_file:
            md = render_markdown(taste_profile)
            Path(cfg.output_file).write_text(md, encoding="utf-8")
            console.print(f"\n[green]Report saved to {cfg.output_file}[/green]")

    finally:
        await fetcher.close()


@draccus.wrap()
def main(cfg: ShowConfig) -> None:
    level = logging.DEBUG if cfg.verbose else logging.WARNING
    logging.basicConfig(level=level, format="%(name)s | %(message)s")
    asyncio.run(_run_show(cfg))
