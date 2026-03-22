# taste

**Paper is cheap, show me the taste.**

Analyze a top researcher's "research taste" — their distinctive patterns in choosing problems, designing methods, and evolving over time.

Like [DeepWiki](https://deepwiki.com/) generates wikis for code repositories, `taste` generates taste profiles for researchers.

## Install

```bash
pip install -e .
```

## Usage

```bash
# Set your Anthropic API key
export ANTHROPIC_API_KEY=sk-ant-...

# Analyze a researcher
taste --researcher "Kaiming He"

# Use Semantic Scholar author ID directly (skip disambiguation)
taste --researcher-id 39353098

# Save to file
taste --researcher "Yann LeCun" --output-file lecun_taste.md

# Use a different model
taste --researcher "Ilya Sutskever" --llm.model claude-opus-4-20250514
```

## How It Works

```
taste --researcher "Kaiming He"
       │
       ▼
 ┌─────────────┐  Semantic Scholar API
 │  Fetcher    │──► Search author → Disambiguate → Fetch ALL papers
 └──────┬──────┘
        │
        ▼
 ┌─────────────┐  Smart selection
 │  Selector   │──► First/co-first/last author → high contribution
 └──────┬──────┘   Every year covered → no timeline gaps
        │
        ▼
 ┌─────────────┐  LLM inference
 │  Career     │──► Institutional trajectory, research direction shifts
 └──────┬──────┘
        │
        ▼
 ┌─────────────┐  LLM Phase 1: per-phase analysis
 │  Analyzer   │──► 7 taste dimensions × each career phase
 └──────┬──────┘
        │
        ▼
 ┌─────────────┐  LLM Phase 2: cross-phase synthesis
 │ Aggregator  │──► Patterns, evolution, unique signature
 └──────┬──────┘
        │
        ▼
 ┌─────────────┐
 │  Output     │──► Markdown report + Rich terminal output
 └─────────────┘
```

## 7 Taste Dimensions

| Dimension | What it captures |
|-----------|-----------------|
| **Problem Taste** | What problems they choose — fundamental vs applied, pioneer vs follower |
| **Method Taste** | Elegant/simple vs complex/engineered, theory vs empirics |
| **Aesthetic Taste** | Naming style, method complexity, figure clarity |
| **Narrative Taste** | How they tell the story — intuition-first vs formalism-first |
| **Timing Taste** | When they enter/exit fields, trend anticipation |
| **Collaboration Taste** | Solo vs team, recurring vs diverse collaborators |
| **Evolution Taste** | How their direction evolves — deepening vs pivoting |

## Paper Selection Strategy

Not just top-N by citations. We select papers that reveal taste:

- **All high-contribution papers**: first author, co-first, second author, last author (PI/corresponding)
- **Year coverage guarantee**: every active year has at least 1-2 papers, no timeline gaps
- **Time-ordered**: enables career evolution analysis

## Status

🚧 **Early development** — the core pipeline works, but prompt quality is still being tuned.

See [ROADMAP.md](docs/ROADMAP.md) for planned features.

## Documentation

- [CONCEPT.md](docs/CONCEPT.md) — Why research taste matters and who this is for
- [DESIGN.md](docs/DESIGN.md) — Technical design: the 7 dimensions, paper selection, two-phase LLM analysis
- [ROADMAP.md](docs/ROADMAP.md) — Development milestones and long-term vision

## License

MIT
