"""Career timeline reconstruction from paper metadata + LLM inference."""

from __future__ import annotations

import json
import logging

from taste.data.models import Author, CareerPhase, CareerTimeline, Paper
from taste.llm.backend import LLMBackend
from taste.llm.prompts import build_career_prompt

log = logging.getLogger(__name__)


async def build_career_timeline(
    author: Author,
    papers: list[Paper],
    llm: LLMBackend,
) -> CareerTimeline:
    """Use LLM to infer career phases from paper list."""
    if not papers:
        return CareerTimeline()

    sorted_papers = sorted(papers, key=lambda p: (p.year or 0, -p.citation_count))

    system, user = build_career_prompt(
        author_name=author.name,
        current_affiliations=", ".join(author.affiliations) if author.affiliations else "",
        homepage=author.homepage or "",
        papers=sorted_papers,
    )

    log.info("Inferring career timeline with LLM...")
    raw = await llm.complete(system, user)

    # Parse JSON from response (handle markdown code blocks)
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1]
        if raw.endswith("```"):
            raw = raw[:-3]
    data = json.loads(raw)

    # Build phases and assign papers to each phase
    phases = []
    for pd in data.get("phases", []):
        years_str = pd.get("years", "")
        # Parse "2009-2012" -> (2009, 2012)
        parts = years_str.replace("–", "-").split("-")
        try:
            start = int(parts[0].strip())
            end = int(parts[-1].strip()) if len(parts) > 1 and parts[-1].strip() else 9999
        except (ValueError, IndexError):
            start, end = 0, 9999

        # Assign papers to this phase by year
        phase_papers = [p for p in sorted_papers if p.year is not None and start <= p.year <= end]

        phases.append(
            CareerPhase(
                name=pd.get("name", ""),
                years=years_str,
                affiliations=pd.get("affiliations", []),
                focus_areas=pd.get("focus_areas", []),
                papers=phase_papers,
            )
        )

    # Assign any unassigned papers to the nearest phase
    assigned_ids = {p.id for phase in phases for p in phase.papers}
    unassigned = [p for p in sorted_papers if p.id not in assigned_ids]
    if unassigned and phases:
        phases[-1].papers.extend(unassigned)

    years = [p.year for p in sorted_papers if p.year]
    total_years = (max(years) - min(years) + 1) if years else 0

    direction_shifts = [pd.get("direction_shift", "") for pd in data.get("phases", []) if pd.get("direction_shift", "N/A") != "N/A"]

    return CareerTimeline(phases=phases, total_years=total_years, direction_shifts=direction_shifts)
