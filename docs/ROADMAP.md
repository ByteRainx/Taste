# Roadmap

> taste is in early development. This document tracks our planned milestones.

## Current Status: v0.1.0-dev (MVP)

🚧 **In Development**

### What's Done

- [x] Project structure and packaging
- [x] Semantic Scholar API integration (fetch author + all papers)
- [x] Smart paper selection (position-based + year coverage)
- [x] Claude LLM backend
- [x] Career timeline inference (LLM-assisted)
- [x] Two-phase taste analysis pipeline
- [x] 7 taste dimensions defined
- [x] Markdown report generation
- [x] Rich terminal output
- [x] Disk caching
- [x] draccus CLI

### What's Left for v0.1.0

- [ ] End-to-end testing with real API key
- [ ] Prompt tuning (iterate on output quality)
- [ ] Error handling for API failures / rate limits
- [ ] Handle edge cases (authors with few papers, missing abstracts)

---

## v0.2.0 — Multi-Backend & Compare

- [ ] OpenAI backend (`--llm.provider openai`)
- [ ] Google Scholar support via `scholarly` library
- [ ] `taste compare "Kaiming He" "Yann LeCun"` — side-by-side comparison
- [ ] Interactive author disambiguation (prompt user to pick from candidates)
- [ ] YAML config presets for common settings
- [ ] Better progress reporting during long LLM calls

## v0.3.0 — Deep Analysis

- [ ] PDF upload for full-text analysis (not just abstracts)
- [ ] Per-paper deep dive mode (`taste paper <paper_id>`)
- [ ] Citation network analysis (who do they cite most? who cites them?)
- [ ] Taste evolution timeline visualization (chart)
- [ ] JSON export for programmatic use

## v0.4.0 — Web Interface

- [ ] Web UI (FastAPI + frontend)
- [ ] Shareable taste profile pages (like DeepWiki pages)
- [ ] Batch analysis mode (multiple researchers)
- [ ] Pre-generated profiles for famous researchers
- [ ] API endpoint for integrations

## v0.5.0 — Community & Polish

- [ ] `pip install taste` on PyPI
- [ ] Community-contributed taste dimensions (plugin system)
- [ ] Multiple language support for output (English/Chinese)
- [ ] Taste comparison leaderboard / gallery
- [ ] Research group taste analysis (analyze a lab, not just a person)

---

## Long-term Vision

- **taste as a standard tool** for understanding researchers, like Google Scholar is for finding papers
- **"Show me the taste"** as a cultural phrase in academia — when evaluating potential collaborators, advisors, or hires
- **Taste-based paper recommendations** — "you might like this paper because it matches your taste in X"
- **Field-level taste analysis** — what's the collective taste of the NLP community vs the CV community?

## Contributing

This project is open source and in early development. If you find it interesting:

1. Try it out and report issues
2. Suggest new taste dimensions
3. Help improve prompts for better analysis quality
4. Contribute support for additional LLM providers or data sources
