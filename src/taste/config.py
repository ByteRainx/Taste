"""Central configuration for taste."""

from __future__ import annotations

from dataclasses import dataclass, field

from taste.data.fetcher import FetcherConfig
from taste.llm.backend import LLMConfig


@dataclass
class TasteConfig:
    """Main configuration for taste analysis."""

    # Input
    researcher: str = ""
    researcher_id: str | None = None

    # Sub-configs
    fetcher: FetcherConfig = field(default_factory=FetcherConfig.get_default)
    llm: LLMConfig = field(default_factory=LLMConfig.get_default)

    # Output
    output_format: str = "markdown"  # "markdown" | "terminal"
    output_file: str | None = None

    # Cache
    cache_dir: str = "~/.cache/taste"
    no_cache: bool = False

    verbose: bool = False
