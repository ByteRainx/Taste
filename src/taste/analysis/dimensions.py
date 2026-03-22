"""Taste dimension definitions."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class TasteDimension:
    key: str
    name: str
    description: str
    signals: list[str] = field(default_factory=list)


DIMENSIONS = [
    TasteDimension(
        key="problem",
        name="Problem Taste",
        description="What problems does this researcher choose to work on?",
        signals=[
            "fundamental vs applied",
            "well-established vs emerging fields",
            "originality of problem formulation",
            "whether they open new directions or deepen existing ones",
        ],
    ),
    TasteDimension(
        key="method",
        name="Method Taste",
        description="What methodological approaches do they prefer?",
        signals=[
            "elegant/simple vs complex/engineered",
            "theoretical vs empirical",
            "first-principles vs incremental",
            "core idea expressible in one sentence or not",
        ],
    ),
    TasteDimension(
        key="aesthetic",
        name="Aesthetic Taste",
        description="How much do they value beauty and simplicity in their work?",
        signals=[
            "naming style (iconic vs generic)",
            "method complexity (few components vs many)",
            "ablation thoroughness",
            "figure/diagram clarity",
        ],
    ),
    TasteDimension(
        key="narrative",
        name="Narrative Taste",
        description="How do they tell the story of their research?",
        signals=[
            "motivation style (intuition-first vs formalism-first)",
            "how they frame the problem in introduction",
            "related work attitude (respectful survey vs critical positioning)",
            "use of visual explanations vs equations",
        ],
    ),
    TasteDimension(
        key="timing",
        name="Timing Taste",
        description="When do they enter and exit research areas?",
        signals=[
            "early mover vs fast follower vs late optimizer",
            "anticipating trends before they peak",
            "knowing when to move on",
            "publishing rhythm",
        ],
    ),
    TasteDimension(
        key="collaboration",
        name="Collaboration Taste",
        description="How do they work with others?",
        signals=[
            "solo vs team player",
            "recurring collaborators vs diverse network",
            "cross-domain collaborations",
            "mentorship patterns (student first-author frequency)",
        ],
    ),
    TasteDimension(
        key="evolution",
        name="Evolution Taste",
        description="How does their research direction evolve over time?",
        signals=[
            "gradual deepening vs sharp pivots",
            "building on own prior work vs fresh starts",
            "self-correction (revising earlier views)",
            "concept transfer across domains",
        ],
    ),
]
