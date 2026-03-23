"""Tests for paper selection logic."""

import pytest

from taste.data.models import Paper, PaperAuthor
from taste.data.selector import classify_author_position, classify_contribution, select_papers


def test_classify_author_position_sole():
    """Test sole author classification."""
    paper = Paper(
        id="1",
        title="Test Paper",
        authors=[PaperAuthor(id="author1", name="Author One")],
    )
    assert classify_author_position("author1", paper) == "sole"


def test_classify_author_position_first():
    """Test first author classification."""
    paper = Paper(
        id="1",
        title="Test Paper",
        authors=[
            PaperAuthor(id="author1", name="Author One"),
            PaperAuthor(id="author2", name="Author Two"),
        ],
    )
    assert classify_author_position("author1", paper) == "first"


def test_classify_author_position_second():
    """Test second author classification."""
    paper = Paper(
        id="1",
        title="Test Paper",
        authors=[
            PaperAuthor(id="author1", name="Author One"),
            PaperAuthor(id="author2", name="Author Two"),
            PaperAuthor(id="author3", name="Author Three"),
        ],
    )
    assert classify_author_position("author2", paper) == "second"


def test_classify_author_position_last():
    """Test last author classification."""
    paper = Paper(
        id="1",
        title="Test Paper",
        authors=[
            PaperAuthor(id="author1", name="Author One"),
            PaperAuthor(id="author2", name="Author Two"),
            PaperAuthor(id="author3", name="Author Three"),
        ],
    )
    assert classify_author_position("author3", paper) == "last"


def test_classify_author_position_middle():
    """Test middle author classification."""
    paper = Paper(
        id="1",
        title="Test Paper",
        authors=[
            PaperAuthor(id="author1", name="Author One"),
            PaperAuthor(id="author2", name="Author Two"),
            PaperAuthor(id="author3", name="Author Three"),
            PaperAuthor(id="author4", name="Author Four"),
            PaperAuthor(id="author5", name="Author Five"),
        ],
    )
    # Author at index 2 (third position) in a 5-author paper is middle
    assert classify_author_position("author3", paper) == "middle"


def test_classify_contribution_high():
    """Test high contribution classification."""
    assert classify_contribution("sole", 1) == "high"
    assert classify_contribution("first", 3) == "high"
    assert classify_contribution("second", 3) == "high"
    assert classify_contribution("last", 5) == "high"


def test_classify_contribution_normal():
    """Test normal contribution classification."""
    assert classify_contribution("middle", 5) == "normal"


def test_select_papers_basic():
    """Test basic paper selection."""
    papers = [
        Paper(
            id="1",
            title="Paper 1",
            year=2020,
            citation_count=100,
            authors=[
                PaperAuthor(id="target", name="Target Author"),
                PaperAuthor(id="other", name="Other Author"),
            ],
        ),
        Paper(
            id="2",
            title="Paper 2",
            year=2021,
            citation_count=50,
            authors=[
                PaperAuthor(id="other", name="Other Author"),
                PaperAuthor(id="target", name="Target Author"),
            ],
        ),
        Paper(
            id="3",
            title="Paper 3",
            year=2022,
            citation_count=10,
            authors=[
                PaperAuthor(id="other1", name="Other Author 1"),
                PaperAuthor(id="target", name="Target Author"),
                PaperAuthor(id="other2", name="Other Author 2"),
                PaperAuthor(id="other3", name="Other Author 3"),
            ],
        ),
    ]

    selected = select_papers("target", papers)

    # Should select all three papers:
    # Paper 1: first author (high contribution)
    # Paper 2: second author in 2-author paper (high contribution)
    # Paper 3: second author in 4-author paper (high contribution)
    assert len(selected) == 3
    assert selected[0].id == "1"  # First author, 2020
    assert selected[1].id == "2"  # Second author (co-first), 2021
    assert selected[2].id == "3"  # Second author, 2022


def test_select_papers_year_coverage():
    """Test that year gaps are filled."""
    papers = [
        Paper(
            id="1",
            title="Paper 1",
            year=2020,
            citation_count=100,
            authors=[PaperAuthor(id="target", name="Target Author")],
        ),
        Paper(
            id="2",
            title="Paper 2",
            year=2021,
            citation_count=50,
            authors=[
                PaperAuthor(id="other1", name="Other 1"),
                PaperAuthor(id="target", name="Target Author"),
                PaperAuthor(id="other2", name="Other 2"),
                PaperAuthor(id="other3", name="Other 3"),
            ],
        ),
        Paper(
            id="3",
            title="Paper 3",
            year=2022,
            citation_count=200,
            authors=[PaperAuthor(id="target", name="Target Author")],
        ),
    ]

    selected = select_papers("target", papers)

    # Should select all three: 2020 and 2022 are high-contribution (sole author)
    # 2021 should be filled as it's a gap year
    assert len(selected) == 3
    assert {p.year for p in selected} == {2020, 2021, 2022}
