"""Abstract fetcher interface."""

from __future__ import annotations

import abc
from dataclasses import dataclass

from taste.data.models import Author, Paper


class Fetcher(abc.ABC):
    @abc.abstractmethod
    async def search_author(self, query: str) -> list[Author]:
        ...

    @abc.abstractmethod
    async def get_author_papers(self, author_id: str) -> list[Paper]:
        ...

    @abc.abstractmethod
    async def get_author(self, author_id: str) -> Author:
        ...

    async def close(self):
        pass


@dataclass
class FetcherConfig:
    """Base fetcher config. Subclass for specific sources."""

    @classmethod
    def get_default(cls) -> FetcherConfig:
        from taste.data.semantic_scholar import SemanticScholarConfig
        return SemanticScholarConfig()

    def build(self) -> Fetcher:
        raise NotImplementedError("Use a specific FetcherConfig like SemanticScholarConfig")
