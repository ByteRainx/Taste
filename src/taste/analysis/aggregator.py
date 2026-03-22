"""Phase 2: Aggregate per-phase analyses into a complete taste profile."""

from __future__ import annotations

import json
import logging

from taste.data.models import Author, CareerTimeline, DimensionAnalysis, Paper, PhaseAnalysis, TasteProfile
from taste.llm.backend import LLMBackend
from taste.llm.prompts import build_aggregation_prompt

log = logging.getLogger(__name__)


def _format_phase_analysis(pa: PhaseAnalysis) -> str:
    lines = [f"### {pa.phase.name} ({pa.phase.years})"]
    if pa.phase.affiliations:
        lines.append(f"Affiliations: {', '.join(pa.phase.affiliations)}")
    lines.append(f"Papers in phase: {len(pa.phase.papers)}")
    if pa.representative_papers:
        lines.append("Representative papers: " + ", ".join(p.title for p in pa.representative_papers))
    lines.append("")
    for key, obs in pa.observations.items():
        lines.append(f"**{key}**: {obs}")
    return "\n".join(lines)


async def aggregate(
    author: Author,
    career: CareerTimeline,
    phase_analyses: list[PhaseAnalysis],
    all_selected_papers: list[Paper],
    llm: LLMBackend,
) -> TasteProfile:
    """Synthesize all phase analyses into a final taste profile."""
    # Build institution trajectory
    all_affiliations = []
    for phase in career.phases:
        for aff in phase.affiliations:
            if aff and aff not in all_affiliations:
                all_affiliations.append(aff)
    institutions = " → ".join(all_affiliations) if all_affiliations else "Unknown"

    # Career span
    years = [p.year for p in all_selected_papers if p.year]
    career_span = f"{min(years)}-{max(years)}" if years else "Unknown"

    # Format phase analyses
    phases_text = "\n\n".join(_format_phase_analysis(pa) for pa in phase_analyses)

    system, user = build_aggregation_prompt(
        author_name=author.name,
        author_citations=author.citation_count or 0,
        h_index=author.h_index or 0,
        n_papers=len(all_selected_papers),
        career_span=career_span,
        institutions=institutions,
        phase_analyses_text=phases_text,
    )

    log.info("Generating final taste profile...")
    raw = await llm.complete(system, user)

    # Parse JSON
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1]
        if raw.endswith("```"):
            raw = raw[:-3]
    data = json.loads(raw)

    # Build dimension analyses
    dimensions = []
    for d in data.get("dimensions", []):
        dimensions.append(
            DimensionAnalysis(
                key=d.get("key", ""),
                name=d.get("name", ""),
                summary=d.get("summary", ""),
                evidence=d.get("evidence", []),
            )
        )

    # Match key paper titles to Paper objects
    key_paper_titles = data.get("key_papers", [])
    key_papers = []
    for title in key_paper_titles:
        title_lower = title.lower().strip()
        for p in all_selected_papers:
            if title_lower in p.title.lower():
                key_papers.append(p)
                break

    return TasteProfile(
        author=author,
        one_liner=data.get("one_liner", ""),
        career=career,
        phase_analyses=phase_analyses,
        dimensions=dimensions,
        tags=data.get("tags", []),
        key_papers=key_papers,
        papers_analyzed=len(all_selected_papers),
    )
