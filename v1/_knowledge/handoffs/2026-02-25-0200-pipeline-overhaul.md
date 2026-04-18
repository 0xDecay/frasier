---
date: 2026-02-25
category: handoff
project: frasier
priority: critical
tags: [handoff, decomposition, pipeline, quality, v0.11.0]
---

# Handoff: Pipeline Overhaul — Projects Can't Complete

## Objective

Fix the Frasier multi-agent system so projects can be handed off and completed autonomously to Manus-level quality. Currently, projects fail because tasks are scoped too broadly for agent capabilities, agents can't iterate on research, and reviewers reject work that was structurally impossible to complete.

## What Was Completed This Session

### v0.10.0 — Capability-Aware Decomposition (DEPLOYED)
- Created `src/lib/capabilities.js` — structured capability manifest for 7 agent roles (tools, strengths, cannot arrays) + global execution constraints
- Modified `src/lib/decomposition.js` — manifest injected into planning prompt + T1 feasibility validation gate with one re-decomposition retry
- 488 tests, 34 suites, all green
- Deployed to VPS, commit `1701404`
- **Result: Partially worked.** Feasibility gate caught 6 issues on first real project and re-decomposed. BUT the re-decomposed plan still created tasks that are too broad (e.g., "analyze demand signals for 15 niches" as a single step when agents can only do ~8 web fetches per task).

### Project #7 Submitted — "Autonomous Info Product Business" (Phase 1)
- Classified as `full_project` (0.95 confidence)
- Decomposed into 10 steps (#156-165), synced to Linear (NERV-84 through NERV-93)
- Steps #158 and #159 hit 3-strike revision cap and FAILED
- Step #158: "Conduct demand signal analysis for top 15 niches" — rejected 3x by Toji (scores: 1.6, 1.4, 2.6)
- Step #159: "Perform competitor analysis for top 10 niches" — rejected 3x by Rei/test-memory-agent (scores: 3.0, 2.4, 2.4)

## Root Causes Identified (Not Yet Fixed)

### 1. Decomposition Still Too Coarse
Even after the feasibility gate, tasks like "analyze 15 niches" are assigned to a single step. The agent can only do ~4-10 web searches and ~8 page fetches per step. You can't meaningfully research 15 niches with 8 fetches. The planner needs to understand QUANTITATIVE tool limits, not just qualitative capabilities.

**Fix needed:** The decomposition engine must right-size tasks based on tool budget. "15 niches x 4 searches each = 60 searches needed, agent can do 8, so split into ~8 steps of 2 niches each."

### 2. Agents Output Placeholder Commands Instead of Executing Searches
Reviewer feedback shows agents writing `[WEB_SEARCH: "property tax appeal" Google Trends]` as TEXT in their output instead of actually executing searches. The worker pipeline DOES run a RESEARCH phase that finds sources, but either:
- The RESEARCH phase queries are too generic / not aligned with the task
- The agent doesn't know how to use the pipeline's search results effectively
- The DECOMPOSE phase (which generates search queries) doesn't create enough/targeted queries

**Investigation needed:** Read `src/worker.js`, `src/lib/pipeline.js`, `src/lib/web.js` to understand how DECOMPOSE -> RESEARCH -> SYNTHESIZE -> CRITIQUE actually works.

### 3. `test-memory-agent` in Review Rotation
Step #159 was reviewed by `test-memory-agent` as a team_lead. This is not a real agent — it's likely a leftover test record in the agents table. It should not be in the review rotation.

**Fix needed:** Check agents table, remove test agents or filter them from review selection.

### 4. Reviewer Expectations Exceed Agent Capabilities
Toji demands "60+ web searches" and "15 niches x 4 search types" — which is correct for the acceptance criteria but physically impossible for the agent. The QA is calibrated correctly; the TASKS are wrong.

**This is a decomposition problem, not a review problem.** If tasks are right-sized, reviewers will pass them.

### 5. No Iterative Research Capability
The pipeline appears to be single-pass: DECOMPOSE -> RESEARCH -> SYNTHESIZE -> CRITIQUE. There's no mechanism for "search -> analyze -> identify gaps -> search more." Production research systems (Manus, etc.) iterate until sufficient depth.

### 6. Acceptance Criteria Not Tool-Budget-Aware
Even after v0.10.0, acceptance criteria like "3-5 Reddit thread summaries per niche x 15 niches = 45-75 threads" are written. Agents can fetch ~8 pages total. The acceptance criteria must be scoped to what a single step can deliver.

## Quality Bar — Manus Comparison

Dhroov had another LLM (Manus AI) execute the exact same Phase 1 roadmap. It produced:
- 18-page comprehensive research report with all 7 sections
- Real competitor analysis with actual products, prices, and quality assessments
- Audience profiling with 3 personas per niche, each with data-backed audience sizes
- Revenue modeling with conversion benchmarks from real sources
- State opportunity rankings with composite scoring methodology
- Supporting data files (SBA data, regulatory burden stats, etc.)

THIS is the quality bar. The Frasier team couldn't even complete a single research step.

Documents provided by Dhroov (attached to Discord and this session):
- `Phase_1_Market_Research_Report.md` — Full Manus output
- `Audience Profiling — Top 3 Niches.md`
- `Detailed Competitor Analysis — Top 3 Niches.md`
- `Niche Research Summary — Consolidated Data.md`
- `Revenue Modeling — Conversion Benchmarks & Projections.md`
- `SBA National Data & State Opportunity Ranking.md`
- `State Opportunity Data — Compiled Rankings.md`
- `Small Business Regulatory Compliance Burden Data.md`
- `Gumroad Case Study.md`
- `2025 Small Business Profile — United States.md`
- `niche_deep_research.csv` and `.json`
- `state_business_growth.md`
- `tweet_context.md` (original @whotfiszackk thread)

## Dhroov's Expectations (Product Requirements)
- Hand off a project and walk away. Get pinged when it's done.
- Intermediate Discord updates are fine (already working).
- Final output must match or exceed Manus quality.
- All technical design decisions are under Lead Engineer jurisdiction — don't ask Dhroov about architecture.
- Projects include: research, code generation, content gen, digital product creation, faceless YouTube, autonomous AI business.
- Agents are NOT advisors — they DO the work and produce deliverables.
- Frasier has full autonomy on personnel and project decisions.

## Files To Investigate (Not Yet Read This Session)
- `src/worker.js` — Worker pipeline, step processing, review handling
- `src/lib/pipeline.js` (or similar) — DECOMPOSE/RESEARCH/SYNTHESIZE/CRITIQUE phases
- `src/lib/web.js` — Brave API, DuckDuckGo, URL fetching, actual limits
- `src/heartbeat.js` — Review routing, domain expert selection
- `src/lib/agents.js` — Agent selection, findBestAgentAcrossTeams
- `src/lib/context.js` — How agent prompts are constructed

## Failed Approaches
- v0.10.0 capability manifest + feasibility gate: Partially worked (caught 6 issues, re-decomposed) but didn't solve the core scoping problem. Tasks were still too broad.
- The feasibility gate design is sound and should be KEPT, but augmented with quantitative tool budget awareness.

## Key Decisions Made
- D-041: Capability-aware decomposition (v0.10.0)

## Issue Log History (Patterns)
- ISS-026: Infeasible tasks (PARTIALLY fixed by v0.10.0)
- ISS-025: Attachment-only messages dropped (fixed v0.9.6)
- ISS-021: Snake_case vs camelCase broke step creation (fixed v0.9.5)
- ISS-017: Classification built but never wired (fixed v0.9.4)
- ISS-016: Completion notifications broken — race condition (fixed v0.9.3)
- ISS-015: Decomposition engine built but never wired (fixed v0.9.2)
- ISS-014: Infinite review loop — no revision cap (fixed v0.9.1)
- ISS-013: Linear cache never initialized in worker (fixed v0.9.1)
- ISS-012: Wrong model IDs — T2/T3 always fell back to T1 (fixed)
- ISS-008: T2 (Manus) never worked — everything ran on cheapest tier (fixed v0.4.0)
- ISS-007: Agents produce meta-instructions instead of deliverables (fixed v0.4.0)
- ISS-005: QA rubber-stamps everything (fixed v0.4.0)
- Recurring pattern: things get built but never wired end-to-end

## Pending Work (Next Session)
1. **Technical autopsy** — Read worker pipeline, web search, review routing, agent roster
2. **Online research** — How production systems (Manus, Devin, OpenHands) handle:
   - Iterative research execution
   - Tool-budget-aware planning
   - MapReduce research patterns
   - Adaptive decomposition
   - Self-reflection and gap analysis
3. **Design comprehensive fix** — Likely involves:
   - Tool-budget-aware decomposition (quantitative limits in planning)
   - Iterative research capability (search -> analyze -> gap-fill -> search more)
   - Right-sized acceptance criteria per step
   - Clean up test agents from review rotation
   - MapReduce pattern for research (parallel agents research slices, synthesis agent merges)
4. **Present plan to Dhroov for approval** (Rule #3: questions first)
5. **TDD implementation** (Rule #8: tests before code)
6. **Deploy and test with real project**

## Resume Instructions
Paste this into your next session:
`continue from _knowledge/handoffs/2026-02-25-0200-pipeline-overhaul.md`

Read the handoff, then:
1. Read the 6 investigation files listed above
2. Research online: how Manus/Devin/OpenHands handle iterative research, tool-budget-aware planning, MapReduce research patterns
3. Design the comprehensive fix
4. Present to Dhroov for approval before building
