# Design Document: taste

> Paper is cheap, show me the taste.

## What is Research Taste?

Richard Hamming once said: *"The great scientists have tremendous taste in picking problems — they pick problems that are important and ripe."*

Research taste is not about productivity (paper count), impact (citation count), or prestige (affiliation). It's about **the distinctive patterns in how a researcher chooses problems, designs solutions, tells stories, and evolves over time**.

Every great researcher has a recognizable "signature" — you can often tell a Kaiming He paper from the title alone (simple method, fundamental question), or an Ilya Sutskever bet from the timing (scaling before anyone else believed in it).

`taste` makes this signature visible and analyzable.

## The 7 Dimensions of Research Taste

### 1. Problem Taste
**What problems do they choose to work on?**

- Fundamental vs applied problems
- Opening new directions vs deepening existing ones
- The "why doesn't this work?" question vs the "how to make this better?" question
- Example: Kaiming He asking "why do deeper networks perform worse?" → ResNet

### 2. Method Taste
**What methodological approaches do they prefer?**

- Elegant simplicity vs complex engineering
- Theory-driven vs experiment-driven
- Can the core idea be explained in one sentence?
- Example: Dropout — one simple idea (randomly turn off neurons) that changed everything

### 3. Aesthetic Taste
**How much do they value beauty in their work?**

- Naming: iconic names (ResNet, Attention Is All You Need) vs generic (XYZGAN-v2)
- Method complexity: few clean components vs many interacting parts
- Ablation design: does every experiment answer a clear question?

### 4. Narrative Taste
**How do they tell the story of their research?**

- Intuition-first (lead with a figure) vs formalism-first (lead with equations)
- How they frame "why this problem matters" in the introduction
- Related work: respectful survey vs critical positioning
- Whether the paper "teaches" the reader something

### 5. Timing Taste
**When do they enter and exit research areas?**

- Early mover (before the trend) vs fast follower vs late optimizer
- Anticipating paradigm shifts
- Knowing when a direction is exhausted and moving on
- Publishing rhythm and cadence

### 6. Collaboration Taste
**How do they work with others?**

- Solo thinker vs team builder
- Recurring collaborators vs constantly expanding network
- Cross-domain collaborations
- Mentorship: do their students become independent leaders?

### 7. Evolution Taste
**How does their research direction evolve over time?**

- Gradual deepening within one area vs sharp pivots to new areas
- Building on their own prior work vs fresh starts
- Self-correction: willingness to revise earlier positions
- Transferring core concepts across domains

## Paper Selection Philosophy

The most common mistake in researcher profiling is grabbing "top N papers by citation count." This misses crucial information:

### What we select instead

**All high-contribution papers** — where the researcher had significant involvement:
- First author (primary contributor)
- Co-first / second author (shared primary contribution)
- Last author (PI/corresponding — chose the direction)

**Year coverage guarantee** — every active year must have representation:
- A researcher's "quiet years" or "transition years" reveal as much taste as their blockbuster years
- Filling gaps ensures we can track evolution continuously

**Time ordering** — papers are analyzed chronologically:
- This reveals how taste evolves, what stays constant, and where pivots happen

### What we skip

- Middle-author papers (contribution unclear)
- Papers where the researcher was a minor contributor

## Architecture

### Two-Phase LLM Analysis

**Phase 1: Per-Career-Phase Analysis**

For each career phase (e.g., "Early Career at MSRA, 2009-2012"), we send all papers from that phase to the LLM and extract 7-dimension observations. This gives us:
- Phase-specific taste signals
- Representative papers per phase
- Local patterns within each period

**Phase 2: Cross-Phase Synthesis**

All phase analyses are combined into one final LLM call that identifies:
- What's **consistent** across the entire career (core taste)
- What **evolved** (taste maturation)
- What's **unique** compared to typical researchers in the field
- Taste tags and key representative papers

### Why Two Phases?

1. **Context limits**: 50+ papers with abstracts would overflow most model contexts
2. **Parallelization**: Phase 1 calls can run concurrently
3. **Cacheability**: Adding a new paper only re-runs one phase, not everything
4. **Quality**: Focused analysis per phase produces better observations than one giant prompt

### Career Timeline Inference

We reconstruct the researcher's career trajectory from paper metadata:
- Institutional affiliations over time
- Research topic shifts (detected from venue/keyword changes)
- Major direction pivots

This provides crucial context for the LLM — knowing "this was their PhD work at MSRA" vs "this was their work as a lead at FAIR" changes the interpretation entirely.

## Data Flow

```
Input: researcher name or Semantic Scholar ID
  │
  ├─ Semantic Scholar API
  │   ├─ Author search + disambiguation (by citation count)
  │   └─ Fetch ALL papers with metadata
  │
  ├─ Paper Selector
  │   ├─ Classify author position (first/second/last/middle)
  │   ├─ Select high-contribution papers
  │   └─ Fill year gaps
  │
  ├─ Career Analyzer (LLM-assisted)
  │   └─ Infer career phases, institutions, direction shifts
  │
  ├─ Phase Analyzer (LLM Phase 1)
  │   └─ Per-phase 7-dimension observations
  │
  ├─ Aggregator (LLM Phase 2)
  │   └─ Cross-phase synthesis → TasteProfile
  │
  └─ Output
      ├─ Markdown report
      └─ Rich terminal display
```

## Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Data source | Semantic Scholar API | Free, structured, reliable. No scraping needed. |
| Paper selection | Position-based + year coverage | Better than top-N citations; reveals evolution |
| LLM strategy | Two-phase (per-phase → aggregate) | Handles scale, enables caching, better quality |
| Career inference | LLM-assisted | Paper metadata alone is insufficient; LLM knows famous researchers |
| Config system | draccus | User preference; clean dataclass-based CLI |
| Async | httpx + asyncio | API calls and LLM calls benefit from async |
| Output | Markdown + Rich | Markdown is shareable; Rich is beautiful in terminal |
