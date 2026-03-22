# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**taste** is a Python CLI tool that analyzes a researcher's "research taste" — the distinctive patterns in how they choose problems, design methods, and evolve over time. It uses the Semantic Scholar API to fetch papers and Claude (Anthropic) to perform two-phase LLM analysis across 7 taste dimensions.

## Development Commands

### Installation
```bash
pip install -e .              # Install in editable mode
pip install -e ".[dev]"       # Install with dev dependencies (pytest, ruff)
pip install -e ".[all]"       # Install all optional dependencies
```

### Running the Tool
```bash
# Set API key first
export ANTHROPIC_API_KEY=sk-ant-...

# Basic usage
taste --researcher "Kaiming He"

# Use Semantic Scholar author ID directly (skip disambiguation)
taste --researcher-id 39353098

# Save output to file
taste --researcher "Yann LeCun" --output-file lecun_taste.md

# Use different Claude model
taste --researcher "Ilya Sutskever" --llm.model claude-opus-4-20250514

# Verbose logging
taste --researcher "Geoffrey Hinton" --verbose
```

### Testing
```bash
pytest                        # Run all tests
pytest tests/test_selector.py  # Run specific test file
pytest -v                     # Verbose output
```

### Code Quality
```bash
ruff check .                  # Lint code
ruff format .                 # Format code
```

## Architecture

### Two-Phase LLM Analysis

The core insight is that analyzing 50+ papers in one LLM call doesn't work well. Instead:

**Phase 1: Per-Career-Phase Analysis** (`analysis/paper_analyzer.py`)
- Career is divided into phases (e.g., "PhD at MSRA 2009-2012", "FAIR 2016-2020")
- Each phase's papers are analyzed separately for 7 taste dimensions
- Produces phase-specific observations and representative papers
- These calls can be parallelized (currently sequential)

**Phase 2: Cross-Phase Synthesis** (`analysis/aggregator.py`)
- All phase analyses are combined into one final LLM call
- Identifies what's consistent, what evolved, and what's unique
- Produces the final `TasteProfile` with tags and key papers

### Data Flow

```
CLI (cli.py)
  ↓
Semantic Scholar API (data/semantic_scholar.py)
  → Fetch author + all papers
  ↓
Paper Selector (data/selector.py)
  → Select high-contribution papers (first/co-first/last author)
  → Fill year gaps to ensure timeline coverage
  ↓
Career Analyzer (analysis/career.py)
  → LLM infers career phases from paper metadata
  ↓
Phase Analyzer (analysis/paper_analyzer.py)
  → LLM analyzes each phase for 7 dimensions
  ↓
Aggregator (analysis/aggregator.py)
  → LLM synthesizes final taste profile
  ↓
Output (output/markdown.py, output/terminal.py)
  → Markdown file and/or Rich terminal display
```

### The 7 Taste Dimensions

Defined in `analysis/dimensions.py`:

1. **Problem Taste** — What problems they choose (fundamental vs applied, pioneer vs follower)
2. **Method Taste** — Methodological preferences (elegant/simple vs complex/engineered)
3. **Aesthetic Taste** — Value of beauty (naming, method complexity, ablation design)
4. **Narrative Taste** — How they tell the story (intuition-first vs formalism-first)
5. **Timing Taste** — When they enter/exit areas (early mover vs fast follower)
6. **Collaboration Taste** — How they work with others (solo vs team, mentorship)
7. **Evolution Taste** — How their direction evolves (gradual deepening vs sharp pivots)

### Paper Selection Strategy

Not just "top N by citations" — that misses crucial information. Instead (`data/selector.py`):

1. **Position-based selection**: Include all papers where the researcher was first, co-first (second), or last author (PI/corresponding)
2. **Year coverage guarantee**: Every active year must have representation — fill gaps with top-cited papers from missing years
3. **Time-ordered**: Papers are analyzed chronologically to track evolution

This reveals taste better than citation-based selection alone.

### Key Data Models

All in `data/models.py`:

- `Paper` — Paper metadata with author position and contribution level
- `Author` — Researcher profile (name, affiliations, h-index, etc.)
- `CareerPhase` — One phase of a career with papers and focus areas
- `CareerTimeline` — Complete career trajectory with phases and direction shifts
- `PhaseAnalysis` — LLM analysis of one career phase
- `TasteProfile` — Final output with dimensions, tags, and key papers

### Configuration

Uses `draccus` for dataclass-based CLI configuration:

- Main config: `cli.py:ShowConfig`
- LLM config: `cli.py:LLMArgs` (model, temperature, max_tokens)
- Semantic Scholar config: `data/semantic_scholar.py:SemanticScholarConfig`

All CLI flags follow the pattern `--config.subconfig.field`.

### Caching

Disk cache in `~/.cache/taste` (configurable via `--cache-dir`):
- Caches fetched author profiles (author + all papers)
- Keyed by Semantic Scholar author ID
- Disable with `--no-cache`

### LLM Backend

Currently supports Claude via Anthropic API (`llm/claude.py`). The backend interface (`llm/backend.py`) is designed to support other providers (OpenAI, etc.) but only Claude is implemented.

Prompts are in `llm/prompts.py` — three main prompts:
1. Career inference prompt (reconstruct career timeline)
2. Phase analysis prompt (analyze papers in one phase)
3. Aggregation prompt (synthesize across all phases)

## Important Notes

- **API Keys**: Requires `ANTHROPIC_API_KEY` environment variable. Optional `S2_API_KEY` for Semantic Scholar (higher rate limits).
- **Async**: Uses `httpx` + `asyncio` for API calls. All LLM and API calls are async.
- **Author Disambiguation**: When searching by name, picks the highest-cited match. Use `--researcher-id` to skip disambiguation.
- **Career Inference**: Uses LLM to infer career phases because paper metadata alone is insufficient (LLM knows famous researchers and their trajectories).
- **JSON Parsing**: LLM responses are expected to be JSON. Code handles markdown code blocks (```json) and strips them before parsing.

## Project Status

Early development (v0.1.0). Core pipeline works but prompt quality is still being tuned. See `docs/ROADMAP.md` for planned features.
