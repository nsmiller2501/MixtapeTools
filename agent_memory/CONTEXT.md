# MixtapeTools Skill Architecture

Shared language for skill workflows that process academic papers and hand work between parent sessions, subagents, and cached artifacts.

## Language

**Bulky source**:
An intermediate input too large to read safely in one tool call or one unbounded agent turn.
_Avoid_: Large file, huge markdown

**Extraction substrate**:
Reusable structural machinery that turns a **Bulky source** into bounded chunks, indexes, and handoff artifacts without interpreting the paper's substantive claims.
_Avoid_: Chunking hack, splitter

**Structural manifest**:
A compact, mechanically derived index of chunks, boundaries, headings, and source references used to navigate a **Bulky source**.
_Avoid_: Summary, reading notes

**Chunk worker**:
A bounded reading subagent that reads one chunk or a small chunk group and writes extraction notes for that source segment.
_Avoid_: Mini-wiki writer

**Synthesis bottleneck**:
A single reasoning step that reads chunk-level notes and produces the coherent paper-level extract and downstream wiki edits.
_Avoid_: Final cleanup

**Fanout-first extraction**:
The default academic-paper extraction shape where chunk workers read bounded source segments before a synthesis bottleneck writes paper-level artifacts.
_Avoid_: Large-paper fallback

**Sequential fanout**:
A fanout execution policy that runs chunk workers one at a time while preserving bounded worker assignments.
_Avoid_: Parallel by default

**Worker bundle**:
One or more adjacent chunks assigned to a chunk worker and read together within a hard source-size ceiling.
_Avoid_: Batch, shard

**Front-matter worker**:
The chunk worker assigned to the opening bundle and responsible for bibliographic candidates, abstract, introduction framing, and stated contributions.
_Avoid_: Metadata agent

**Body worker**:
The default chunk worker assigned to main-text bundles and responsible for local evidence while skipping bibliographic reconstruction unless new or contradictory metadata appears.
_Avoid_: Generic reader

**Back-matter worker**:
The chunk worker assigned to appendices, references, or supplemental trailing material and responsible for appendix evidence, robustness material, and replication/data availability clues.
_Avoid_: References reader

**Citation-overlap scan**:
A mechanical comparison between a paper's references and the project's existing `references/references.bib` entries to produce candidate related ingested papers.
_Avoid_: Related-papers judgment

**Deterministic match label**:
A rule name emitted by a script to explain why a citation-overlap candidate matched, such as DOI exact match or author-year string match.
_Avoid_: Relevance reason

**Project-neutral extract**:
A paper-level extract that records generally useful research details without filtering them through a specific project focus.
_Avoid_: Generic summary

**Project-relevance gate**:
A wiki-update filtering rule that gives full treatment to material directly relevant to the current project's focus and compresses less relevant material.
_Avoid_: Omit irrelevant sections

**Formal-object inventory**:
A complete local list of tables, figures, equations, specifications, algorithms, propositions, and similar formal objects encountered by chunk workers, with source references and compact surrounding context.
_Avoid_: Important figures only

**Clean chunk boundary**:
A chunk boundary placed at a natural structural break in the paper, usually a section or subsection heading, while preserving bounded chunk size.
_Avoid_: Semantic summary boundary

**Hard chunk ceiling**:
The maximum chunk size allowed before the **Extraction substrate** must split the source, even if no clean section boundary is available.
_Avoid_: Best-effort limit

**read-pdf**:
The owning context for marker conversion and reusable extraction machinery over converted paper text.
_Avoid_: PDF helper

**wiki-update**:
The wiki-ingest context that consumes paper extracts and extraction substrates to update project reference wikis.
_Avoid_: PDF reader

**Prompt cache amplification**:
Repeated subagent turns rereading an accumulated prompt and tool-result cache, making multi-turn extraction expensive even when cache hits are discounted.
_Avoid_: Token bug, chunking issue

## Relationships

- A **Bulky source** should pass through an **Extraction substrate** before deep extraction.
- An **Extraction substrate** creates structural access to source material; reasoning agents own reading and interpretation.
- A **Structural manifest** helps agents navigate chunks but must not contain scholarly interpretation.
- A **Chunk worker** extracts local evidence; the **Synthesis bottleneck** owns paper-level interpretation and final write products.
- **Fanout-first extraction** is preferred for academic PDFs because long, dense papers are the expected case, not an exception.
- **Sequential fanout** is the default execution policy so usage-limit failures lose at most one worker's active work.
- A **Worker bundle** should be read in one tool turn when possible to avoid intermediate **Prompt cache amplification** within that worker.
- A **Chunk worker** receives a bundle-specific assignment excerpt; the **Synthesis bottleneck** receives the full **Structural manifest**.
- **Front-matter workers**, **Body workers**, and **Back-matter workers** use position-specific instructions to reduce predictable duplication without asking scripts to interpret paper content.
- A **Citation-overlap scan** is non-authoritative; the **Synthesis bottleneck** decides whether candidate overlaps deserve wiki links or backlinks.
- A **Deterministic match label** records mechanical provenance, not scholarly relatedness.
- `read-pdf` writes a **Project-neutral extract**; `wiki-update` applies a **Project-relevance gate** before writing wiki-facing material.
- A **Formal-object inventory** is unfiltered at worker stage; importance and relevance decisions belong to the **Synthesis bottleneck**.
- A **Clean chunk boundary** is preferred when it does not violate bounded-size constraints.
- A **Hard chunk ceiling** overrides a **Clean chunk boundary**; oversized sections are split at the safest available paragraph, table, equation, or figure boundary.
- **Prompt cache amplification** increases with each subagent tool turn and with each chunk added to subagent context.
- **read-pdf** owns the **Extraction substrate**; **wiki-update** consumes it rather than duplicating marker-output handling.

## Example dialogue

> **Dev:** "Should `wiki-update` read marker output directly?"
> **Domain expert:** "No. Marker output can be a **Bulky source**, so it should go through the shared **Extraction substrate** before any subagent tries deep extraction."

## Flagged ambiguities

- "chunking issue" was used for both Read tool size limits and high cached-token spend. Resolution: use **Bulky source** for size-limit risk and **Prompt cache amplification** for repeated-turn cost.
