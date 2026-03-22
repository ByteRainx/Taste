"""Phase 1: Analyze papers within each career phase."""

from __future__ import annotations

import json
import logging

from taste.data.models import Author, CareerPhase, Paper, PhaseAnalysis
from taste.llm.backend import LLMBackend
from taste.llm.prompts import build_phase_prompt

log = logging.getLogger(__name__)


async def analyze_phase(
    author: Author,
    phase: CareerPhase,
    llm: LLMBackend,
) -> PhaseAnalysis:
    """Analyze all papers in a career phase, extracting taste observations."""
    if not phase.papers:
        return PhaseAnalysis(phase=phase)

    system, user = build_phase_prompt(
        author_name=author.name,
        author_citations=author.citation_count or 0,
        h_index=author.h_index or 0,
        phase=phase,
    )

    log.info(f"Analyzing phase: {phase.name} ({len(phase.papers)} papers)...")
    raw = await llm.complete(system, user)

    # Parse JSON
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1]
        if raw.endswith("```"):
            raw = raw[:-3]
    data = json.loads(raw)

    observations = data.get("observations", {})
    rep_titles = data.get("representative_papers", [])

    # Match representative paper titles to actual Paper objects
    rep_papers = []
    for title in rep_titles:
        title_lower = title.lower().strip()
        for p in phase.papers:
            if title_lower in p.title.lower():
                rep_papers.append(p)
                break

    return PhaseAnalysis(
        phase=phase,
        observations=observations,
        representative_papers=rep_papers,
    )


async def analyze_all_phases(
    author: Author,
    phases: list[CareerPhase],
    llm: LLMBackend,
) -> list[PhaseAnalysis]:
    """Analyze all career phases sequentially."""
    results = []
    for phase in phases:
        result = await analyze_phase(author, phase, llm)
        results.append(result)
    return results
