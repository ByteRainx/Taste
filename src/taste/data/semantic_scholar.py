"""Semantic Scholar API fetcher."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field

import httpx

from taste.data.fetcher import Fetcher, FetcherConfig
from taste.data.models import Author, Paper, PaperAuthor

BASE_URL = "https://api.semanticscholar.org/graph/v1"
AUTHOR_FIELDS = "name,affiliations,citationCount,hIndex,paperCount,homepage,url"
PAPER_FIELDS = "title,abstract,year,citationCount,venue,authors"


@dataclass
class SemanticScholarConfig(FetcherConfig):
    api_key: str | None = None

    def build(self) -> SemanticScholarFetcher:
        return SemanticScholarFetcher(api_key=self.api_key)


class SemanticScholarFetcher(Fetcher):
    def __init__(self, api_key: str | None = None):
        headers = {}
        if api_key:
            headers["x-api-key"] = api_key
        self._client = httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=30.0)

    async def search_author(self, query: str) -> list[Author]:
        resp = await self._client.get(
            "/author/search",
            params={"query": query, "fields": AUTHOR_FIELDS, "limit": 10},
        )
        resp.raise_for_status()
        data = resp.json()
        authors = []
        for item in data.get("data", []):
            authors.append(
                Author(
                    id=item["authorId"],
                    name=item.get("name", ""),
                    affiliations=item.get("affiliations") or [],
                    homepage=item.get("homepage"),
                    paper_count=item.get("paperCount"),
                    citation_count=item.get("citationCount"),
                    h_index=item.get("hIndex"),
                )
            )
        # Sort by citation count descending for disambiguation
        authors.sort(key=lambda a: a.citation_count or 0, reverse=True)
        return authors

    async def get_author(self, author_id: str) -> Author:
        resp = await self._client.get(f"/author/{author_id}", params={"fields": AUTHOR_FIELDS})
        resp.raise_for_status()
        item = resp.json()
        return Author(
            id=item["authorId"],
            name=item.get("name", ""),
            affiliations=item.get("affiliations") or [],
            homepage=item.get("homepage"),
            paper_count=item.get("paperCount"),
            citation_count=item.get("citationCount"),
            h_index=item.get("hIndex"),
        )

    async def get_author_papers(self, author_id: str) -> list[Paper]:
        """Fetch all papers for an author with pagination."""
        papers = []
        offset = 0
        limit = 100
        while True:
            resp = await self._client.get(
                f"/author/{author_id}/papers",
                params={"fields": PAPER_FIELDS, "limit": limit, "offset": offset},
            )
            resp.raise_for_status()
            data = resp.json()
            batch = data.get("data", [])
            if not batch:
                break
            for item in batch:
                authors = [
                    PaperAuthor(id=a.get("authorId"), name=a.get("name", ""))
                    for a in item.get("authors") or []
                ]
                papers.append(
                    Paper(
                        id=item["paperId"],
                        title=item.get("title") or "",
                        abstract=item.get("abstract"),
                        year=item.get("year"),
                        citation_count=item.get("citationCount") or 0,
                        venue=item.get("venue"),
                        authors=authors,
                    )
                )
            if data.get("next") is None:
                break
            offset = data["next"]
            # Rate limit: be nice
            await asyncio.sleep(0.2)
        return papers

    async def close(self):
        await self._client.aclose()
