"""Prompt templates for taste analysis."""

from __future__ import annotations

from taste.analysis.dimensions import DIMENSIONS
from taste.data.models import CareerPhase, Paper

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _format_paper(p: Paper, idx: int) -> str:
    pos = p.author_position if p.author_position != "unknown" else ""
    pos_str = f" [{pos}]" if pos else ""
    return (
        f"{idx}. {p.title} ({p.year or '?'}, {p.venue or 'N/A'}, "
        f"{p.citation_count:,} citations{pos_str})\n"
        f"   Abstract: {p.abstract or 'N/A'}"
    )


def _dimensions_description() -> str:
    lines = []
    for d in DIMENSIONS:
        signals = ", ".join(d.signals)
        lines.append(f"- **{d.name}** ({d.key}): {d.description} Signals: {signals}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Phase 1: per-phase analysis
# ---------------------------------------------------------------------------

PHASE_ANALYSIS_SYSTEM = """\
You are a research taste analyst. You study a researcher's papers to identify \
their unique research "taste" — the distinctive patterns in how they choose \
problems, design methods, write papers, and evolve over time.

You will analyze a batch of papers from one phase of a researcher's career. \
Extract observations for each of these taste dimensions:

{dimensions}

Return a JSON object with this exact structure:
{{
  "observations": {{
    "<dimension_key>": "<2-3 sentence observation for this phase>",
    ...
  }},
  "representative_papers": ["<title of 1-3 most taste-revealing papers>"],
  "phase_summary": "<1 sentence summary of this phase's taste>"
}}

Be specific. Cite paper titles. Identify patterns, not just list papers. \
Write in English."""

PHASE_ANALYSIS_USER = """\
Researcher: {author_name} ({author_citations:,} total citations, h-index {h_index})
Career Phase: {phase_name} ({phase_years})
Affiliations during this phase: {affiliations}

Papers in this phase ({n_papers} papers):

{papers}"""


def build_phase_prompt(author_name: str, author_citations: int, h_index: int, phase: CareerPhase) -> tuple[str, str]:
    papers_text = "\n\n".join(_format_paper(p, i + 1) for i, p in enumerate(phase.papers))
    system = PHASE_ANALYSIS_SYSTEM.format(dimensions=_dimensions_description())
    user = PHASE_ANALYSIS_USER.format(
        author_name=author_name,
        author_citations=author_citations,
        h_index=h_index or 0,
        phase_name=phase.name,
        phase_years=phase.years,
        affiliations=", ".join(phase.affiliations) if phase.affiliations else "Unknown",
        n_papers=len(phase.papers),
        papers=papers_text,
    )
    return system, user


# ---------------------------------------------------------------------------
# Phase 2: cross-phase aggregation
# ---------------------------------------------------------------------------

AGGREGATION_SYSTEM = """\
You are synthesizing a researcher's complete "taste profile" from per-phase \
analyses of their career. Your job is to identify:

1. **Consistent patterns** — what taste elements stay the same across phases
2. **Evolution** — how their taste has changed or deepened over time
3. **Unique signature** — what makes this researcher's taste distinctive

The taste dimensions are:
{dimensions}

Return a JSON object:
{{
  "one_liner": "<one sentence capturing their core research taste>",
  "dimensions": [
    {{
      "key": "<dimension_key>",
      "name": "<dimension name>",
      "summary": "<3-5 sentence analysis spanning their whole career>",
      "evidence": ["<paper title that best illustrates this>", ...]
    }},
    ...
  ],
  "tags": ["<3-7 short taste tags like #minimalist, #root-cause-hunter>"],
  "key_papers": ["<3-5 paper titles that best represent their overall taste>"]
}}

Be insightful. Go beyond surface-level observations. A great taste profile \
should make the reader think "yes, that captures something real about how \
this person does research." Write in English."""

AGGREGATION_USER = """\
Researcher: {author_name}
Total citations: {author_citations:,} | h-index: {h_index} | Papers analyzed: {n_papers}
Career span: {career_span}
Institution trajectory: {institutions}

Per-phase analyses:

{phase_analyses}"""


def build_aggregation_prompt(
    author_name: str,
    author_citations: int,
    h_index: int,
    n_papers: int,
    career_span: str,
    institutions: str,
    phase_analyses_text: str,
) -> tuple[str, str]:
    system = AGGREGATION_SYSTEM.format(dimensions=_dimensions_description())
    user = AGGREGATION_USER.format(
        author_name=author_name,
        author_citations=author_citations,
        h_index=h_index or 0,
        n_papers=n_papers,
        career_span=career_span,
        institutions=institutions,
        phase_analyses=phase_analyses_text,
    )
    return system, user


# ---------------------------------------------------------------------------
# Career inference (optional LLM assist)
# ---------------------------------------------------------------------------

CAREER_INFERENCE_SYSTEM = """\
You are an academic career analyst. Given a researcher's papers sorted by year, \
infer their career trajectory: institution changes, role progression, and \
major research direction shifts.

Return a JSON object:
{{
  "phases": [
    {{
      "name": "<descriptive phase name>",
      "years": "<start_year>-<end_year>",
      "affiliations": ["<institution>"],
      "focus_areas": ["<research topic>", ...],
      "direction_shift": "<what changed from previous phase, or 'N/A' for first>"
    }},
    ...
  ]
}}

Use your knowledge of this researcher if available. Be concise."""

CAREER_INFERENCE_USER = """\
Researcher: {author_name}
Current affiliations: {current_affiliations}
Homepage: {homepage}

All papers sorted by year ({n_papers} total):

{papers}"""


def build_career_prompt(author_name: str, current_affiliations: str, homepage: str, papers: list[Paper]) -> tuple[str, str]:
    papers_text = "\n".join(
        f"- [{p.year or '?'}] {p.title} ({p.venue or 'N/A'}, {p.citation_count:,} cit, pos={p.author_position})"
        for p in papers
    )
    user = CAREER_INFERENCE_USER.format(
        author_name=author_name,
        current_affiliations=current_affiliations or "Unknown",
        homepage=homepage or "N/A",
        n_papers=len(papers),
        papers=papers_text,
    )
    return CAREER_INFERENCE_SYSTEM, user
