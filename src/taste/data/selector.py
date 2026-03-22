"""Smart paper selection: pick papers that best reveal research taste."""

from __future__ import annotations

from collections import defaultdict

from taste.data.models import Paper


def classify_author_position(author_id: str, paper: Paper) -> str:
    """Determine the target author's position in a paper's author list."""
    if not paper.authors:
        return "unknown"
    n = len(paper.authors)
    idx = None
    for i, a in enumerate(paper.authors):
        if a.id == author_id:
            idx = i
            break
    if idx is None:
        # Fallback: might be a name mismatch across sources
        return "unknown"
    if n == 1:
        return "sole"
    if idx == 0:
        return "first"
    if idx == 1:
        return "second"
    if idx == n - 1:
        return "last"
    return "middle"


def classify_contribution(position: str, num_authors: int) -> str:
    """Determine contribution level from author position."""
    if position in ("sole", "first", "second", "last"):
        return "high"
    # For small author lists, even middle positions indicate significant contribution
    if num_authors <= 3:
        return "high"
    return "normal"


def select_papers(author_id: str, papers: list[Paper]) -> list[Paper]:
    """Select papers that best represent the researcher's taste.

    Strategy:
    1. Classify every paper by author position and contribution level
    2. Select ALL high-contribution papers
    3. Ensure every active year has coverage (fill gaps with top-cited normal papers)
    4. Sort by year
    """
    # Step 1: classify all papers
    for p in papers:
        p.author_position = classify_author_position(author_id, p)
        p.contribution_level = classify_contribution(p.author_position, len(p.authors))

    # Step 2: select all high-contribution papers
    selected_ids = set()
    for p in papers:
        if p.contribution_level == "high":
            p.is_selected = True
            selected_ids.add(p.id)

    # Step 3: ensure year coverage
    # Find all active years (years where the author has any paper)
    papers_by_year: dict[int, list[Paper]] = defaultdict(list)
    for p in papers:
        if p.year is not None:
            papers_by_year[p.year].append(p)

    if papers_by_year:
        min_year = min(papers_by_year.keys())
        max_year = max(papers_by_year.keys())
        for year in range(min_year, max_year + 1):
            year_papers = papers_by_year.get(year, [])
            # Check if this year already has selected papers
            has_selected = any(p.id in selected_ids for p in year_papers)
            if not has_selected and year_papers:
                # Pick top 1-2 by citation from this year's unselected papers
                unselected = [p for p in year_papers if p.id not in selected_ids]
                unselected.sort(key=lambda p: p.citation_count, reverse=True)
                for p in unselected[:2]:
                    p.is_selected = True
                    selected_ids.add(p.id)

    # Step 4: collect and sort
    result = [p for p in papers if p.is_selected]
    result.sort(key=lambda p: (p.year or 0, -p.citation_count))
    return result
