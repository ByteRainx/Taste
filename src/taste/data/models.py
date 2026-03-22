"""Core data models."""

from __future__ import annotations

from pydantic import BaseModel


class PaperAuthor(BaseModel):
    id: str | None = None
    name: str


class Paper(BaseModel):
    id: str
    title: str
    abstract: str | None = None
    year: int | None = None
    citation_count: int = 0
    venue: str | None = None
    authors: list[PaperAuthor] = []
    # Contribution metadata (filled by selector)
    author_position: str = "unknown"  # "first" | "second" | "last" | "middle" | "sole"
    contribution_level: str = "normal"  # "high" | "normal"
    is_selected: bool = False


class Author(BaseModel):
    id: str
    name: str
    affiliations: list[str] = []
    homepage: str | None = None
    paper_count: int | None = None
    citation_count: int | None = None
    h_index: int | None = None


class AuthorProfile(BaseModel):
    """Complete fetched data for a researcher."""
    author: Author
    papers: list[Paper]


class CareerPhase(BaseModel):
    name: str
    years: str  # "2009-2012"
    affiliations: list[str] = []
    focus_areas: list[str] = []
    papers: list[Paper] = []


class CareerTimeline(BaseModel):
    phases: list[CareerPhase] = []
    total_years: int = 0
    direction_shifts: list[str] = []


class DimensionAnalysis(BaseModel):
    key: str
    name: str
    summary: str
    evidence: list[str] = []


class TasteProfile(BaseModel):
    author: Author
    one_liner: str = ""
    career: CareerTimeline = CareerTimeline()
    phase_analyses: list[PhaseAnalysis] = []
    dimensions: list[DimensionAnalysis] = []
    tags: list[str] = []
    key_papers: list[Paper] = []
    papers_analyzed: int = 0


class PhaseAnalysis(BaseModel):
    phase: CareerPhase
    observations: dict[str, str] = {}  # dimension_key -> observation
    representative_papers: list[Paper] = []


# Fix forward reference
TasteProfile.model_rebuild()
