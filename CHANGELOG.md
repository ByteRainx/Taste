# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-03-23

### Added
- Initial release of taste
- Semantic Scholar API integration for fetching researcher papers
- Smart paper selection based on author position and year coverage
- LLM-driven career timeline inference
- Two-phase taste analysis (per-phase → cross-phase synthesis)
- 7 taste dimensions: Problem, Method, Aesthetic, Narrative, Timing, Collaboration, Evolution
- Markdown report generation with Rich terminal output
- Disk caching for API responses
- Comprehensive test suite (9 unit tests)
- Complete documentation (README, CLAUDE.md, CONCEPT, DESIGN, ROADMAP, PROJECT_STATUS)
- Example analysis (Xiaodan Liang)
- GitHub Actions CI workflow

### Fixed
- Robust JSON parsing to handle markdown code blocks and mixed text
- Optimized LLM prompts to avoid triggering safety restrictions
- Correct CLI parameter syntax in documentation

### Technical Details
- Python 3.10+ support
- Async I/O with httpx
- Pydantic data models
- draccus for CLI configuration
- Claude API (Anthropic) for LLM analysis
- pytest for testing
- ruff for code formatting

[0.1.0]: https://github.com/yourusername/taste/releases/tag/v0.1.0
