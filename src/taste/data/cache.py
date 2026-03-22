"""Disk cache for API responses."""

from __future__ import annotations

import json
import time
from pathlib import Path

from taste.data.models import Author, AuthorProfile, Paper


class DiskCache:
    def __init__(self, cache_dir: str = "~/.cache/taste", ttl_days: int = 7):
        self._dir = Path(cache_dir).expanduser()
        self._dir.mkdir(parents=True, exist_ok=True)
        self._ttl_seconds = ttl_days * 86400

    def _path(self, key: str) -> Path:
        return self._dir / f"{key}.json"

    def get_profile(self, author_id: str) -> AuthorProfile | None:
        path = self._path(f"author_{author_id}")
        if not path.exists():
            return None
        data = json.loads(path.read_text())
        if time.time() - data.get("_ts", 0) > self._ttl_seconds:
            path.unlink(missing_ok=True)
            return None
        return AuthorProfile(
            author=Author(**data["author"]),
            papers=[Paper(**p) for p in data["papers"]],
        )

    def set_profile(self, author_id: str, profile: AuthorProfile) -> None:
        path = self._path(f"author_{author_id}")
        data = {
            "_ts": time.time(),
            "author": profile.author.model_dump(),
            "papers": [p.model_dump() for p in profile.papers],
        }
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2))
