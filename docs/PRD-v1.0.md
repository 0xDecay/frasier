# Frasier v1.0 — Product Requirements Document

**Project:** Frasier (NERV) — Autonomous AI Organization  
**Version:** 1.0 (Reliability-First Redesign)  
**Author:** Claude (Lead Engineer) with Dhroov (Product Visionary)  
**Date:** 2026-02-25  
**Status:** Draft — Pending Founder Approval

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Current State Assessment](#2-current-state-assessment)
3. [Phase 1 — Reliability Overhaul](#3-phase-1--reliability-overhaul)
4. [Phase 2 — Pipeline Redesign](#4-phase-2--pipeline-redesign)
5. [Phase 3 — Parallel Execution](#5-phase-3--parallel-execution)
6. [Phase 4 — Build & Delivery Capabilities](#6-phase-4--build--delivery-capabilities)
7. [Infrastructure, Costs & Risks](#7-infrastructure-costs--risks)

---

## 1. Executive Summary

Frasier is not a chatbot, not a tool, not an assistant. It is an autonomous AI organization — seven specialized agents operating 24/7 on a DigitalOcean VPS as a functioning company. A founder posts a project vision to Discord. Frasier (COO) decomposes it into a mission plan. Edward researches. Spike engineers. Faye creates content. Vicious handles marketing. Julia curates knowledge. Ein runs quality assurance. The system executes without human intervention and delivers finished work product back through Discord.

That is the vision. The reality, after eleven versions shipped in ten days, is this: 507 tests pass, the architecture is genuinely sound, and not a single end-to-end deliverable has ever been completed. Twenty-nine bugs have been logged. Components work in isolation — the deep work pipeline produces quality output, capability-aware decomposition assigns the right agent to the right task, the PostgreSQL brain maintains state reliably — but the seams between components fail. Agent handoffs break. Steps get stuck. Research failures produce confident hallucinations instead of honest errors. One failed step kills an entire mission, discarding all completed work. Steps can complete with null output and the system calls it done. The system builds well but cannot finish.

Version 1.0 is a reliability-first redesign. The goal is not new features. The goal is that Frasier can take a project brief and autonomously deliver a sellable digital product, a working application or agent, or a comprehensive research deliverable — with accuracy, depth, and quality that meets professional standards. No human intervention between brief and delivery.

The redesign proceeds in four phases:

**Phase 1 — Reliability.** Eliminate the catastrophic failure modes. Zombie step detection and cleanup. Graceful degradation instead of binary pass/fail. Circuit breakers for API outages. Research integrity guards that refuse to synthesize from empty sources. A result validation gate that makes it structurally impossible for a step to be marked "completed" with no output. Context overflow protection so large missions don't silently drown the final step. This phase alone should take Frasier from zero completions to consistent partial completions.

**Phase 2 — Pipeline Redesign.** Rebuild the execution layer: agent handoffs that preserve context, a final assembly phase that composes individual step outputs into a coherent deliverable, a shared project workspace so agents can build on each other's work, mid-execution escalation when the system detects it is stuck. Replace Ein's per-step QA (which adds latency without substance) with meaningful quality gates at phase boundaries.

**Phase 3 — Parallel Execution.** Move from a single worker to a multi-worker architecture. Steps without dependencies execute concurrently. Mission-level parallelism so the system can run multiple projects simultaneously. Adaptive pipeline depth based on project complexity.

**Phase 4 — Build & Delivery.** Give the system the ability to produce real artifacts — generate files, scaffold applications, write and execute code, package deliverables. This is the phase where Frasier stops being a system that writes text about work and becomes a system that does work.

**What stays.** The PostgreSQL brain — it is the right choice and it works. The three-process architecture (orchestrator, worker, Discord gateway). The persona system that gives each agent distinct expertise and voice. The deep work pipeline concept (critique-revision cycles that measurably improve output quality). Capability-aware decomposition and DAG-based dependency resolution. The policy engine. The memory system.

**What changes.** The QA pipeline moves from per-step rubber-stamping to phase-boundary quality gates with teeth. Agent handoffs get explicit context transfer instead of implicit database reads. The single worker becomes a pool. Self-healing replaces silent failure — the system detects stuck states and recovers without human intervention. A final assembly phase stitches step outputs into deliverables. Build capabilities let agents produce artifacts, not just text.

**Success looks like this:** Dhroov posts "Build me a lead magnet PDF on AI automation for small businesses" to Discord. Frasier decomposes it. Edward researches the topic with real sources. Faye writes the content. Spike formats the PDF. Julia indexes the knowledge generated. Ein validates the final product against the original brief. The finished PDF — with accurate information, proper citations, professional structure, and genuine depth — appears in Discord. No human touched it between brief and delivery.

---

## 2. Current State Assessment

### 2.1 Architecture Overview

Frasier runs as three PM2-managed processes on a single DigitalOcean VPS:

1. **Orchestrator.** Receives project briefs from Discord, decomposes them into missions (a DAG of steps with dependencies and agent assignments), writes the plan to PostgreSQL, and monitors execution progress. It uses capability-aware decomposition to match steps to agents based on their defined expertise.

2. **Worker.** A single-threaded process that polls PostgreSQL for steps in `pending` status whose dependencies have been satisfied. It picks up one step at a time, loads the assigned agent's persona, executes the deep work pipeline (draft → critique → revision cycles), writes the result back to PostgreSQL, and moves to the next step. Heartbeats are written every 30 seconds to signal liveness.

3. **Discord Gateway.** Handles inbound commands from the founder and outbound delivery of results. Listens for project briefs, status queries, and control commands. Delivers completed mission outputs back to the appropriate Discord channel.

**Data flow:** Discord message → Orchestrator parses brief → Orchestrator writes mission plan (steps, dependencies, agent assignments) to PostgreSQL → Worker polls for executable steps → Worker runs deep work pipeline per step → Worker writes results to PostgreSQL → Orchestrator detects mission completion → Discord Gateway delivers output.

PostgreSQL is the single source of truth. All state — missions, steps, results, agent memories, heartbeats, policy decisions — lives in the database. There is no in-memory state that cannot be reconstructed from the database. This is a genuinely good architectural decision.

### 2.2 What Works Well

**The PostgreSQL brain is solid.** Using a relational database as the central nervous system was the right call. State is durable, queryable, and survives process restarts. The schema — missions, steps, results, memories, policies — models the domain accurately. There are no data races on writes because each step is owned by a single worker.

**Capability-aware decomposition produces good plans.** When the orchestrator breaks a project into steps, it correctly identifies which agent should handle which task. Edward gets research. Spike gets engineering. Faye gets content. The matching logic works, and the resulting DAG structures are sensible.

**The deep work pipeline produces measurably better output.** Critique-revision cycles are not theater. In v0.7.0 testing, critique scores ranged from 4.5 to 5.0 on a 5-point scale, and the revised output was demonstrably stronger than the initial draft. The pipeline concept — draft, critique against rubric, revise with specific feedback — is architecturally sound and produces real quality gains.

**The persona system creates genuinely differentiated agent behavior.** Each agent has a distinct voice, expertise domain, and working style that comes through in their output. This is not cosmetic. Edward's research reads differently from Faye's content, and both are better for being specialized.

**The policy engine enforces operational rules consistently.** Rate limits, approval requirements, escalation triggers — these are defined declaratively and enforced at the database level. The engine works as designed.

**The DAG dependency system correctly orders execution.** Steps that depend on other steps wait. Steps without dependencies are correctly identified as executable. The topological ordering is correct.

**507 tests pass.** The test suite is real, not decorative. Unit tests cover individual components. Integration tests verify cross-component behavior. The test infrastructure is mature for a system this young.

### 2.3 The 19 Failure Points

#### Tier 1 — Catastrophic Failures

These will cause mission failure every time they trigger. They are not edge cases. They occur under normal operating conditions.

**1. Zombie steps with no recovery.** When the worker crashes, hangs, or loses its database connection mid-execution, the step it was processing remains in `in_progress` status permanently. There is no timeout. There is no detection mechanism. There is no cleanup process. The step is simply stuck, and because downstream steps depend on it, the entire mission is blocked forever. This is the single most common failure mode. Every unattended overnight run has hit it. The heartbeat system exists but nothing reads it — the 30-second heartbeat is written to the database and never checked by any other process.

**2. Research failure produces confident hallucination.** When Edward's research step calls Brave Search and the API returns an error, times out, or returns zero results, the synthesis prompt still fires. The prompt includes the instruction "Use ONLY these sources" — but the source list is empty. The LLM, given an authoritative-sounding prompt with no sources to constrain it, generates plausible-sounding content fabricated entirely from training data. There is no check that validates whether sources were actually retrieved before synthesis begins. The system does not know the difference between "researched and synthesized" and "made it up." This is not a rare failure. Brave Search rate limits trigger regularly under sustained use.

**3. One failed step kills the entire mission.** Step completion is binary: success or failure. If a single step fails — for any reason, including transient API errors — the mission is marked as failed. All completed work from other steps is effectively discarded. There is no partial success. There is no ability to retry the failed step while preserving the successful ones. There is no concept of a mission being "80% complete with one gap." A ten-step mission where nine steps produced excellent work and one step hit a rate limit is treated identically to a mission where nothing worked.

#### Tier 2 — Data Loss and Silent Degradation

**4. Revision destroys original work.** When a step enters the revision cycle, the original result is set to `null` in the database before the revision attempt begins. If the revision then fails (API timeout, context overflow, malformed response), both the original and the revision are lost. The step has no result at all — not even the imperfect original.

**5. No cascade failure at step time.** When a step fails, its dependent steps should be immediately marked as blocked or failed. Instead, they remain in `pending` status for up to 30 seconds until the heartbeat catches them.

**6. No circuit breaker for API outages.** When an external API is down or rate-limited, the retry logic fires all attempts immediately with no backoff. Each step independently discovers the outage, burns through its retries, and fails.

#### Tier 3 — Missing Capabilities

**7. No step timeout detection.** No maximum execution time. No detection that a step has exceeded a reasonable duration.

**8. No partial success handling.** Everything is pass/fail.

**9. No mission cancellation or pause.** Once running, a mission cannot be stopped. The only way is to kill the worker process, which causes zombie steps.

**10. No Discord delivery retry.** If the delivery message fails, the result is lost.

**11. No observability.** No timing metrics, no performance dashboards, no way to answer basic operational questions.

#### Tier 4 — Design Gaps

**12. No shared project workspace.** Each step executes in isolation.

**13. No final assembly phase.** Step outputs are concatenated, not synthesized.

**14. No mid-execution escalation.** Steps can only succeed or fail. No path to flag issues for replanning.

**15. No adaptive pipeline depth.** Every step gets the same treatment regardless of complexity.

**16. Single worker, no parallel execution.**

**17. No build capabilities.** Agents produce text about code, not actual code.

**18. Ein's per-step QA adds latency without substance.**

**19. Null result completion — mission marked done without a deliverable.** A step can complete its pipeline execution, produce null or empty output, and still be marked `in_review` → `completed`. There is no validation at any point in the chain — not at step completion, not at approval, not at mission completion — that checks whether the step actually produced a result. The completion logic (`checkMissionCompletion()`) checks only that all steps have a terminal status (`completed` or `failed`). It does not inspect `mission_steps.result`. This means a mission can be marked `completed` with its most important step — including the final deliverable step — containing null in the result column. This is not theoretical. Mission #91 (the autonomous info product bake-off) completed 18 of 19 steps, producing 61,000 words of solid research. Step 14 (the final executive summary) returned null. The project was marked "completed" and Dhroov received nothing. The root cause is compound: (a) the final step received all 18 predecessor outputs as context (~61,000 words), which likely exceeded the model's context window, causing a silent failure in synthesis; (b) the pipeline did not treat "no output" as an error; (c) no downstream check verified the result existed before marking the step and mission as done.

### 2.4 Recurring Bug Patterns

**Built-but-not-wired (3 critical bugs).** Code implements features correctly in isolation but is never called from the runtime path.

**Cross-process desync (3 critical bugs).** The three PM2 processes make assumptions about each other's state that are not enforced.

**Schema mismatches (2 critical bugs).** Column names in queries do not match the schema. Fields expected non-null are null.

**Data integrity violations (4 bugs).** Steps reference nonexistent missions. Results written for already-failed steps. Memories saved with null agent IDs.

**Infinite loops (2 bugs).** No retry counter persists across requeuings. A step can be retried indefinitely.

### 2.5 Honest Assessment

The architecture is approximately 75% right. The fundamental decisions — PostgreSQL as central state, process separation for resilience, DAG-based execution planning, persona-driven agents, critique-revision quality loops — are sound and should be preserved. The remaining 25% is the execution layer: the glue between components, the error handling, the recovery mechanisms, the handoff protocols. This layer needs to be rebuilt, not patched.

The path to v1.0 is not "add features." It is "make what exists work reliably, then extend it." Phase 1 (reliability) must be complete and proven before any subsequent phase begins. A system that can execute five steps reliably in sequence is more valuable than one that can theoretically execute fifty steps in parallel but completes zero.

## 3. Phase 1 — Reliability Overhaul

This is the highest-priority phase. Nothing else ships until missions complete reliably end-to-end. Every item in this section addresses a documented failure mode or a gap that has caused lost work, stuck missions, or silent failures in production.

---

### 3.1 Self-Healing Heartbeat

The heartbeat process (`heartbeat.js`, running on a 30-second interval) is the system's immune system. It must detect and resolve every category of stuck state without human intervention.

**Zombie Step Detection**

A "zombie step" is a step stuck in `in_progress` because the worker crashed, the LLM call hung, or the process was killed mid-execution. There is no current mechanism to detect this. The step sits in `in_progress` forever, blocking all downstream dependents.

Detection query:

```sql
SELECT id, mission_id, agent_id, started_at
FROM mission_steps
WHERE status = 'in_progress'
  AND started_at < NOW() - INTERVAL '30 MINUTES';
```

Resolution:
1. Mark the step as `failed` with `error_reason = 'Step timed out after 30 minutes of inactivity'`.
2. Log a `CRITICAL` event: `{ event: 'zombie_step_detected', step_id, mission_id, agent_id, stuck_duration_minutes }`.
3. Trigger cascade failure evaluation for all downstream dependents (see below).

The 30-minute threshold is deliberately generous. The longest legitimate step execution observed in production is approximately 12 minutes (deep research with multiple Brave Search calls and a long synthesis pass). Thirty minutes provides a 2.5x safety margin. This threshold should be configurable via environment variable `ZOMBIE_STEP_TIMEOUT_MINUTES` to allow tuning without a code deploy.

**Zombie Mission Detection**

A "zombie mission" is a mission stuck in `in_progress` where no further progress is possible. This occurs when all remaining steps are either `failed` or depend on a failed step. The ISS-028 incident demonstrated this pattern: a mission sat in `in_progress` for over 14 hours, consuming a queue slot, because three of its steps had failed and the remaining steps all depended on them.

Detection query:

```sql
SELECT m.id AS mission_id
FROM missions m
WHERE m.status = 'in_progress'
  AND NOT EXISTS (
    SELECT 1
    FROM mission_steps ms
    WHERE ms.mission_id = m.id
      AND ms.status IN ('pending', 'in_progress', 'escalated')
      AND NOT EXISTS (
        SELECT 1
        FROM step_dependencies sd
        JOIN mission_steps dep ON dep.id = sd.depends_on_step_id
        WHERE sd.step_id = ms.id
          AND dep.status = 'failed'
      )
  );
```

This query finds missions where every non-terminal step either has already failed or has at least one failed dependency — meaning no step can ever make progress again.

Resolution:
1. Calculate the success ratio: `completed_steps / total_steps`.
2. Apply the partial success threshold (see Section 3.2) to determine final status.
3. Mark the mission accordingly and post a summary to Discord.
4. Log: `{ event: 'zombie_mission_resolved', mission_id, final_status, completed_ratio }`.

**Cascade Failure at Step Failure Time**

The existing `failBlockedSteps()` function (line 806 in `heartbeat.js`) correctly identifies steps whose dependencies have failed and marks them as `failed` with reason `'Dependency step [X] failed'`. However, it only runs on the heartbeat tick — every 30 seconds. This creates a window where dependent steps appear as `pending` and could theoretically be claimed by a worker, only to discover mid-execution that their input data does not exist.

Enhancement: Add an immediate cascade call in `worker.js` at the point where a step is marked `failed`. The function `cascadeFailDependents(stepId)` performs the same logic as `failBlockedSteps()` but scoped to a single step's direct dependents, then recurses. This eliminates the 30-second blind spot entirely.

```
cascadeFailDependents(failedStepId):
  dependents = SELECT step_id FROM step_dependencies WHERE depends_on_step_id = failedStepId
  for each dependent:
    if dependent.status == 'pending':
      mark dependent as 'failed', reason = 'Dependency step {failedStepId} failed'
      log event
      cascadeFailDependents(dependent.id)  // recurse
```

The heartbeat's `failBlockedSteps()` remains as a safety net for edge cases where the worker-level cascade missed something (e.g., worker crashed between marking the step failed and running the cascade).

---

### 3.2 Partial Success

Binary success/failure is too coarse. A mission that completed 9 of 10 steps successfully should not be treated identically to a mission where the very first step failed and nothing ran. Replace the binary model with graduated outcomes.

**Mission Outcome States**

| Status | Condition | Behavior |
|---|---|---|
| `completed` | 100% of steps succeeded | Full deliverable assembled and posted |
| `partial_success` | >= 70% of steps succeeded AND no critical-path step failed | Deliverable assembled from completed steps; gaps explicitly noted |
| `failed` | < 70% of steps succeeded OR any critical-path step failed | No deliverable assembled; failure summary posted |

**Critical-Path Steps**

During decomposition, Frasier marks certain steps as `is_critical_path = true`. These are steps without which the deliverable is fundamentally incomplete — for example, the core analysis step of a research mission, or the financial model step of a business plan. If any critical-path step fails, the mission fails regardless of the overall completion percentage.

The `mission_steps` table requires a new boolean column:

```sql
ALTER TABLE mission_steps ADD COLUMN is_critical_path BOOLEAN DEFAULT false;
```

Frasier sets this flag during decomposition based on the mission's acceptance criteria and the step's role in the dependency graph. Root steps (those with no dependents relying on them) are never critical-path. Steps that are upstream of 3+ other steps are strong candidates.

**Partial Success Assembly**

When a mission reaches `partial_success`:
1. Frasier receives the list of completed step results and the list of failed steps with their error reasons.
2. The assembly prompt includes an additional directive: `"The following sections could not be completed: [failed step descriptions]. Clearly note these gaps in the deliverable. Do not fabricate content for missing sections. Instead, state what was intended and why it is absent."`
3. The Discord notification includes a transparency block:

```
Mission: [name] — Partial Success (8/10 steps completed)

Completed sections: [list]
Missing sections:
  - [Step 6: Competitor pricing analysis] — Failed: Brave Search circuit breaker open
  - [Step 9: Executive summary revision] — Failed: Dependency on Step 6

The deliverable below reflects the completed work. Missing sections are noted inline.
```

The 70% threshold is stored as an environment variable `PARTIAL_SUCCESS_THRESHOLD` (default `0.7`) to allow adjustment without code changes. The rationale for 70%: below this level, the deliverable has too many gaps to be useful as a starting point; above it, the completed work has standalone value even with noted omissions.

---

### 3.3 Revision History

The current revision mechanism (line 554 in `missions.js`) sets a step's `result` column to `null` before re-executing the pipeline. This permanently destroys the previous work product. If the revision produces a worse result — or fails entirely — the original output is gone.

**New Table: `step_revisions`**

```sql
CREATE TABLE step_revisions (
  id SERIAL PRIMARY KEY,
  step_id INTEGER NOT NULL REFERENCES mission_steps(id) ON DELETE CASCADE,
  revision_number INTEGER NOT NULL,
  result TEXT NOT NULL,
  critique_score NUMERIC(3,1),
  critique_text TEXT,
  revised_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(step_id, revision_number)
);

CREATE INDEX idx_step_revisions_step_id ON step_revisions(step_id);
```

**Archive-Before-Clear Protocol**

Before clearing a step's result for revision, the worker executes:

```sql
INSERT INTO step_revisions (step_id, revision_number, result, critique_score, critique_text)
VALUES (
  $stepId,
  (SELECT COALESCE(MAX(revision_number), 0) + 1 FROM step_revisions WHERE step_id = $stepId),
  (SELECT result FROM mission_steps WHERE id = $stepId),
  (SELECT critique_score FROM mission_steps WHERE id = $stepId),
  (SELECT critique_text FROM mission_steps WHERE id = $stepId)
);
```

Only after this insert succeeds does the worker set `result = null` and re-execute the pipeline.

**Fallback on Revision Failure**

If the revision attempt fails (LLM error, timeout, circuit breaker open), the worker restores the best previous result:

```sql
SELECT result, critique_score
FROM step_revisions
WHERE step_id = $stepId
ORDER BY critique_score DESC NULLS LAST, revision_number DESC
LIMIT 1;
```

The step's `result` and `critique_score` are restored from this row. The step is marked `completed` (not `failed`), with a note in the log: `'Revision failed; restored best previous result (revision #X, score Y.Z)'`.

This guarantees the invariant: **no work product is ever permanently lost**.

---

### 3.4 Circuit Breaker Pattern

Every external API call is a potential point of failure. When an external service goes down, the system should degrade gracefully rather than burning through retries and timeouts. Implement the circuit breaker pattern for all external dependencies: Brave Search, OpenRouter (LLM provider), and Discord.

**Circuit Breaker States**

| State | Behavior |
|---|---|
| `closed` | Normal operation. Calls proceed. Failure counter tracked. |
| `open` | All calls short-circuited immediately (no network request made). Returns a predefined fallback response. |
| `half-open` | A single probe call is allowed through. Success closes the circuit; failure reopens it. |

**State Transitions**

- `closed` → `open`: Triggered when `consecutiveFailures >= 3` for a given API.
- `open` → `half-open`: Triggered after the cooldown period elapses (initial: 5 minutes).
- `half-open` → `closed`: Triggered when the probe call succeeds.
- `half-open` → `open`: Triggered when the probe call fails. Cooldown doubles (exponential backoff: 5m → 10m → 20m → capped at 60m).

**Implementation: `CircuitBreaker` Class**

Located in `src/utils/circuitBreaker.js`. Each external API gets its own instance:

```javascript
const braveSearchBreaker = new CircuitBreaker({
  name: 'brave_search',
  failureThreshold: 3,
  initialCooldownMs: 5 * 60 * 1000,   // 5 minutes
  maxCooldownMs: 60 * 60 * 1000,       // 1 hour cap
  backoffMultiplier: 2
});

const openRouterBreaker = new CircuitBreaker({
  name: 'openrouter',
  failureThreshold: 3,
  initialCooldownMs: 5 * 60 * 1000,
  maxCooldownMs: 60 * 60 * 1000,
  backoffMultiplier: 2
});

const discordBreaker = new CircuitBreaker({
  name: 'discord',
  failureThreshold: 3,
  initialCooldownMs: 5 * 60 * 1000,
  maxCooldownMs: 60 * 60 * 1000,
  backoffMultiplier: 2
});
```

Every external call is wrapped: `breaker.execute(async () => { /* actual API call */ })`. If the circuit is open, `execute()` throws a `CircuitOpenError` immediately without making the network request. The caller handles this error according to the API-specific fallback behavior.

**API-Specific Fallback Behavior**

- **Brave Search (circuit open):** The step's `researchFailed` flag is set to `true`. The synthesis prompt is modified per Section 3.5. The step continues without web research rather than failing entirely.
- **OpenRouter (circuit open):** The step cannot proceed without an LLM. Mark the step as `failed` with reason `'LLM provider circuit breaker open'`. The step will be retried when the circuit closes (see retry queue in Section 3.7).
- **Discord (circuit open):** The notification is saved to the `pending_notifications` table (Section 3.7). The step is still marked `completed` — delivery failure does not invalidate the work product.

**Observability**

Every state transition is logged: `{ event: 'circuit_breaker_state_change', api: 'brave_search', from: 'closed', to: 'open', consecutiveFailures: 3, cooldownMs: 300000 }`. The heartbeat's `logPerformanceMetrics()` function (Section 3.8) includes current circuit breaker states in its hourly report.

---

### 3.5 Research Failure Honesty

When a research step returns zero sources — whether because the Brave Search circuit breaker is open, the API returned no results, or results were filtered out as irrelevant — the system must ensure downstream synthesis does not confidently hallucinate facts that appear research-backed.

**Detection**

The `researchFailed` flag is set to `true` on the step record in two scenarios:
1. The Brave Search circuit breaker is in `open` state when the research phase executes.
2. The Brave Search API returns successfully but yields zero usable results after relevance filtering.

The flag is stored on the step: `ALTER TABLE mission_steps ADD COLUMN research_failed BOOLEAN DEFAULT false;`

**Prompt Modification**

When `researchFailed = true`, the synthesis prompt is modified before being sent to the LLM:

Remove the standard directive:
> "Use ONLY the following sources to support your analysis."

Replace with:
> "IMPORTANT: Web research was unavailable for this task. You MUST clearly label any claims as 'based on general knowledge — not verified by web research.' Do not present unverified claims as established fact. Where possible, recommend specific sources the reader should consult to verify your general-knowledge claims."

This modification is applied in the `buildSynthesisPrompt()` function in the pipeline module. The function checks `step.researchFailed` and swaps the directive block accordingly.

**Critique Score Penalty**

When `researchFailed = true`, the self-critique rubric is modified:
- The maximum possible score is capped at `3.0`, regardless of output quality.
- The critique prompt includes: `"Note: this step was completed without web research. The maximum score for any unverified output is 3.0. If the output presents unverified claims as fact, score 1.0."`

A score of 3.0 falls below the standard auto-approve threshold (currently 4.0), which guarantees the step either enters a revision pass or is flagged for human review. This prevents confidently wrong output from flowing into the final deliverable without scrutiny.

**Transparency in Deliverable**

When the final assembly step (Section 4.4) encounters workspace sections where `researchFailed = true`, it includes a notation:
> "[Note: This section was produced without web research and relies on the agent's general knowledge. Claims have not been independently verified.]"

---

### 3.6 Mission Lifecycle States

The `missions` table already supports `paused` and `cancelled` statuses in its schema, but no code paths implement these transitions. This creates a gap: Dhroov has no way to stop a runaway mission or temporarily freeze work without killing the entire worker process.

**State Machine**

```
                    !pause
  in_progress ──────────────► paused
       │                         │
       │                         │ !resume
       │                         ▼
       │                    in_progress
       │
       │         !cancel
       ├──────────────────► cancelled
       │
       ▼
  completed / partial_success / failed
```

**Command: `!pause <mission_id>`**

Triggered via Discord command. Implementation in `commands.js`:

1. Validate the mission exists and is `in_progress`.
2. Set `missions.status = 'paused'` and `missions.paused_at = NOW()`.
3. All `pending` steps for this mission are left as-is in the database but the worker's `claimNextStep()` query is modified to exclude steps belonging to paused missions:

```sql
SELECT ms.id
FROM mission_steps ms
JOIN missions m ON ms.mission_id = m.id
WHERE ms.status = 'pending'
  AND m.status = 'in_progress'
  AND NOT EXISTS (
    SELECT 1 FROM step_dependencies sd
    JOIN mission_steps dep ON dep.id = sd.depends_on_step_id
    WHERE sd.step_id = ms.id AND dep.status != 'completed'
  )
ORDER BY ms.priority ASC, ms.created_at ASC
LIMIT 1
FOR UPDATE SKIP LOCKED;
```

The `m.status = 'in_progress'` condition naturally excludes paused missions. Steps that are already `in_progress` (actively being worked on by a worker) are allowed to finish — pausing does not abort running work.

4. Respond in Discord: `"Mission [name] paused. [X] steps were in progress and will complete. [Y] pending steps are frozen."`

**Command: `!resume <mission_id>`**

1. Validate the mission exists and is `paused`.
2. Set `missions.status = 'in_progress'`, clear `paused_at`.
3. Respond in Discord: `"Mission [name] resumed. [Y] pending steps are now available for processing."`

**Command: `!cancel <mission_id>`**

1. Validate the mission exists and is `in_progress` or `paused`.
2. All `pending` steps: set status to `cancelled`.
3. All `in_progress` steps: set status to `cancelled` (worker detects cancellation on next checkpoint — see below).
4. Set `missions.status = 'cancelled'` and `missions.cancelled_at = NOW()`.
5. Respond in Discord: `"Mission [name] cancelled. [X] steps were cancelled. [Y] steps had already completed — their work is preserved in the project workspace."`

**Worker Cancellation Checkpoint**

The worker checks for cancellation at two points during step execution: (1) after the research phase completes, and (2) after the synthesis phase completes. At each checkpoint:

```javascript
async function checkCancellation(stepId) {
  const step = await db.query('SELECT status FROM mission_steps WHERE id = $1', [stepId]);
  if (step.rows[0].status === 'cancelled') {
    throw new StepCancelledException(stepId);
  }
}
```

If cancelled, the worker logs the event and moves to the next available step. This provides sub-minute cancellation responsiveness without the complexity of true mid-execution abort.

---

### 3.7 Discord Delivery Retry

A completed deliverable must never be lost because of a transient Discord API failure. The current implementation makes a single `channel.send()` call with no retry logic. If Discord returns a 500, 502, or rate-limit error, the deliverable is gone — the step is marked complete but nothing is posted.

**Retry Strategy**

Wrap all `channel.send()` calls in `sendWithRetry(channel, content, options)`:

1. Attempt 1: immediate.
2. Attempt 2: wait 1 second, retry.
3. Attempt 3: wait 5 seconds, retry.
4. Attempt 4: wait 15 seconds, retry.
5. All attempts failed: save to `pending_notifications` table.

The retry delays follow an exponential pattern (1s, 5s, 15s) to respect Discord rate limits while providing reasonable responsiveness.

**Pending Notifications Table**

```sql
CREATE TABLE pending_notifications (
  id SERIAL PRIMARY KEY,
  channel_id TEXT NOT NULL,
  content TEXT NOT NULL,
  embed_data JSONB,
  mission_id INTEGER REFERENCES missions(id),
  step_id INTEGER REFERENCES mission_steps(id),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  retry_count INTEGER DEFAULT 0,
  last_retry_at TIMESTAMP WITH TIME ZONE,
  status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'delivered', 'abandoned'))
);

CREATE INDEX idx_pending_notifications_status ON pending_notifications(status);
```

**Heartbeat Retry Loop**

The heartbeat adds a new function `retryPendingNotifications()` that runs every tick (30 seconds):

```sql
SELECT id, channel_id, content, embed_data, retry_count
FROM pending_notifications
WHERE status = 'pending'
  AND (last_retry_at IS NULL OR last_retry_at < NOW() - INTERVAL '5 MINUTES')
ORDER BY created_at ASC
LIMIT 5;
```

For each pending notification:
1. Attempt `channel.send()`.
2. If successful: set `status = 'delivered'`.
3. If failed: increment `retry_count`, set `last_retry_at = NOW()`.
4. If `retry_count >= 10`: set `status = 'abandoned'`, log a `CRITICAL` event, notify Dhroov via a different channel or DM if possible.

The 5-minute cooldown between retries and the limit of 5 per tick prevent the heartbeat from hammering a downed Discord API.

---

### 3.8 Observability

The system currently operates with minimal visibility into performance characteristics. Step durations are not consistently tracked, there is no aggregate reporting, and diagnosing slowdowns requires manual database queries. This section adds structured timing data and automated performance reporting.

**Step Timing Enforcement**

The `mission_steps` table already has `started_at` and `completed_at` columns. Ensure they are populated at every state transition:

- `started_at`: set when the worker claims the step (`status` transitions from `pending` to `in_progress`). Currently set in the `claimStep()` function — verify this is not bypassed in any code path.
- `completed_at`: set when the step reaches any terminal state (`completed`, `failed`, `cancelled`). Add this to the `completeStep()`, `failStep()`, and `cancelStep()` functions if not already present.

**New Column: Pipeline Phase Timing**

Add a JSONB column to track duration of each pipeline phase within a step:

```sql
ALTER TABLE mission_steps ADD COLUMN phase_timings JSONB DEFAULT '{}';
```

The worker populates this as each phase completes:

```json
{
  "decompose": { "started_at": "...", "completed_at": "...", "duration_ms": 3200 },
  "research": { "started_at": "...", "completed_at": "...", "duration_ms": 8500, "sources_found": 6 },
  "synthesize": { "started_at": "...", "completed_at": "...", "duration_ms": 12300, "tokens_generated": 2400 },
  "critique": { "started_at": "...", "completed_at": "...", "duration_ms": 4100, "score": 4.2 },
  "revise": { "started_at": "...", "completed_at": "...", "duration_ms": 9800, "final_score": 4.6 }
}
```

**Hourly Performance Metrics**

New heartbeat function `logPerformanceMetrics()`, scheduled to run every 60 minutes (tracked by a `lastMetricsRun` timestamp compared against `NOW()`):

```sql
-- Average step duration by agent role (last hour)
SELECT agent_id, AVG(EXTRACT(EPOCH FROM (completed_at - started_at))) AS avg_seconds
FROM mission_steps
WHERE completed_at > NOW() - INTERVAL '1 HOUR'
GROUP BY agent_id;

-- Average phase duration (last hour, from JSONB)
SELECT
  phase.key AS phase_name,
  AVG((phase.value->>'duration_ms')::int) AS avg_duration_ms
FROM mission_steps,
  jsonb_each(phase_timings) AS phase
WHERE completed_at > NOW() - INTERVAL '1 HOUR'
GROUP BY phase.key;

-- Steps completed vs. failed in last hour
SELECT status, COUNT(*) AS count
FROM mission_steps
WHERE completed_at > NOW() - INTERVAL '1 HOUR'
  AND status IN ('completed', 'failed')
GROUP BY status;

-- Current queue depth
SELECT COUNT(*) AS pending_steps
FROM mission_steps
WHERE status = 'pending';

-- Circuit breaker states (from in-memory state, not SQL)
```

The output is logged as a structured JSON object and optionally posted to a `#frasier-metrics` Discord channel.

**Daily Summary**

At midnight UTC (or the first heartbeat tick after midnight), `logPerformanceMetrics()` generates an expanded daily summary:

- Total missions completed / partial_success / failed.
- Total steps completed / failed / cancelled.
- Average mission completion time (end-to-end).
- Slowest step (by total duration) with its mission and agent.
- Most-revised step (highest revision count from `step_revisions` table).
- Circuit breaker trip count per API.
- Pending notification backlog count.

This summary is posted to Dhroov's Discord DM and logged to the application log.

---

### 3.9 Result Validation Gate

**Failure Point Addressed:** #19 — Null result completion.

A step that produces no output is not a completed step. It is a failed step. The current system has zero checks for this condition at any point in the lifecycle — the pipeline can return null content, `completeStep()` saves it without inspection, the approval chain processes it without checking, and `checkMissionCompletion()` marks the mission done based solely on status, not substance.

This section introduces a three-layer validation gate that makes it structurally impossible for a null-result step to be marked as completed.

**Layer 1: Pipeline Output Guard**

Immediately after the pipeline returns, before calling `completeStep()`, the worker validates the result:

```javascript
// In worker.js, after pipeline execution
const finalContent = pipelineResult.content;

if (!finalContent || finalContent.trim().length === 0) {
  const errorReason = pipelineResult.error
    ? `Pipeline error: ${pipelineResult.error}`
    : 'Pipeline returned null or empty content — no result produced';
  await missions.failStep(step.id, errorReason);
  logEvent('CRITICAL', {
    event: 'null_result_detected',
    step_id: step.id,
    mission_id: step.mission_id,
    agent_id: step.assigned_agent_id,
    pipeline_phases: pipelineResult.phaseTimings || null,
    error: errorReason
  });
  return; // Do not proceed to completeStep
}
```

This is the primary gate. If the pipeline produces nothing, the step fails immediately with a clear error reason. No silent passes.

**Layer 2: Database-Level Constraint**

Add a CHECK constraint to prevent null results from being stored on completed steps:

```sql
ALTER TABLE mission_steps ADD CONSTRAINT result_required_when_completed
  CHECK (
    status != 'completed' OR result IS NOT NULL AND LENGTH(TRIM(result)) > 0
  );
```

This is a safety net. If any code path bypasses the worker guard and attempts to mark a step as `completed` with a null or empty result, the database rejects the update. This constraint should never fire in normal operation — if it does, it means the worker guard was bypassed, and the database just prevented data corruption.

**Layer 3: Mission Completion Deliverable Check**

Before `checkMissionCompletion()` marks a mission as `completed` or `partial_success`, verify that the critical-path steps and the final step actually contain results:

```javascript
async function checkMissionCompletion(missionId) {
  const { data: steps, error } = await supabase
    .from('mission_steps')
    .select('id, status, result, is_critical_path, step_order')
    .eq('mission_id', missionId);

  if (error || !steps || steps.length === 0) return false;

  const allDone = steps.every(s => s.status === 'completed' || s.status === 'failed');
  if (!allDone) return false;

  const completedSteps = steps.filter(s => s.status === 'completed');
  const failedSteps = steps.filter(s => s.status === 'failed');

  // NEW: Verify completed steps actually have content
  const emptyCompletedSteps = completedSteps.filter(
    s => !s.result || s.result.trim().length === 0
  );

  if (emptyCompletedSteps.length > 0) {
    // These steps are lying — they claim completion but have no result.
    // Fail them with explanation, then re-evaluate.
    for (const emptyStep of emptyCompletedSteps) {
      await failStep(emptyStep.id, 'Step marked completed but contains no result');
      logEvent('CRITICAL', {
        event: 'phantom_completion_detected',
        step_id: emptyStep.id,
        mission_id: missionId
      });
    }
    // Re-run completion check with corrected statuses
    return checkMissionCompletion(missionId);
  }

  // Existing logic continues: evaluate success ratio, critical path, etc.
  // ...
}
```

This is the backstop. Even if Layers 1 and 2 are somehow circumvented, the mission-level check catches phantom completions before they reach the founder. The re-evaluation means the success ratio is recalculated with the corrected step statuses, so a phantom completion properly counts as a failure.

**Context Overflow Prevention**

Failure Point #19's root cause includes context overflow — 61,000 words of predecessor output injected into the final step's prompt exceeded the model's context window, causing a silent failure. This is addressed by the token budget mechanism in Section 4.3 (Agent Handoff Protocol) and Section 4.4 (Final Assembly Phase), but a worker-level safeguard is added here:

```javascript
// In worker.js, when building predecessor context
const MAX_PREDECESSOR_TOKENS = 40000; // ~30K words — leaves room for system prompt + task

const predecessorOutputs = await missions.getPredecessorOutputs(step.id);
let totalTokenEstimate = 0;
const truncatedOutputs = [];

for (const p of predecessorOutputs) {
  const outputTokens = Math.ceil(p.result.length / 4); // rough char-to-token estimate
  if (totalTokenEstimate + outputTokens > MAX_PREDECESSOR_TOKENS) {
    // Summarize instead of including full output
    const summaryTokenBudget = 2000; // ~1500 words per predecessor summary
    const truncatedResult = p.result.substring(0, summaryTokenBudget * 4)
      + '\n\n[... output truncated due to context budget. Key findings above.]';
    truncatedOutputs.push({ ...p, result: truncatedResult, truncated: true });
    totalTokenEstimate += summaryTokenBudget;
    logEvent('WARNING', {
      event: 'predecessor_output_truncated',
      step_id: p.stepId,
      original_length: p.result.length,
      truncated_to: summaryTokenBudget * 4
    });
  } else {
    truncatedOutputs.push(p);
    totalTokenEstimate += outputTokens;
  }
}
```

This prevents the context window overflow that caused Mission #91's Step 14 to fail silently. When predecessor outputs are too large, they are truncated with an explicit marker rather than blowing out the model's context and producing nothing. The 40,000-token budget is conservative — the model's actual context window is larger, but leaving ample room for system prompt, task description, and generation ensures reliable output.

---

### 3.10 Integration Test Suite

Unit tests verify individual functions in isolation. Integration tests verify that the complete system behaves correctly through multi-step workflows that cross module boundaries. The following test suite covers every critical path in the reliability overhaul.

**Test Infrastructure**

Test directory: `tests/integration/`

All integration tests share a common setup:
- A dedicated test database (same schema as production, created fresh per test run via `beforeAll` hook).
- Mock implementations for external APIs:
  - `MockBraveSearch`: returns configurable search results or errors.
  - `MockOpenRouter`: returns configurable LLM responses or errors.
  - `MockDiscord`: captures sent messages in an in-memory array for assertion.
- A real heartbeat instance and worker instance pointed at the test database and mocks.
- `afterAll` tears down the test database.

**Test: Full Mission Lifecycle** (`tests/integration/missionLifecycle.test.js`)

1. Create a mission via `createMission({ name: 'Test Mission', brief: '...' })`.
2. Call `decomposeMission(missionId)` — verify it creates 3+ steps with proper DAG dependencies.
3. Start the worker. Verify it claims the first step (one with no dependencies).
4. Verify the step passes through all pipeline phases: decompose → research → synthesize → critique.
5. Verify the step is marked `completed` with a non-null result and a critique score.
6. Verify the worker automatically claims the next available step (dependency resolved).
7. Allow all steps to complete. Verify the mission is marked `completed`.
8. Verify the assembly step was created and executed.
9. Verify the Discord mock received the final deliverable message.

**Test: Zombie Step Recovery** (`tests/integration/zombieRecovery.test.js`)

1. Insert a step directly into the database with `status = 'in_progress'` and `started_at = NOW() - INTERVAL '45 MINUTES'`.
2. Run one heartbeat tick.
3. Assert the step's status is now `failed` with `error_reason LIKE '%timed out%'`.
4. Assert a `CRITICAL` log event was emitted.

**Test: Cascade Failure** (`tests/integration/cascadeFailure.test.js`)

1. Create a mission with a three-step DAG: A → B → C (B depends on A, C depends on B).
2. Mark step A as `failed`.
3. Call `cascadeFailDependents(stepA.id)`.
4. Assert step B is `failed` with reason referencing step A.
5. Assert step C is `failed` with reason referencing step B.
6. Assert the mission's zombie detection query now identifies this mission.

**Test: Partial Success** (`tests/integration/partialSuccess.test.js`)

1. Create a mission with 10 steps, none marked `is_critical_path`.
2. Complete 8 steps successfully. Fail 2 steps.
3. Trigger the heartbeat's zombie mission detection.
4. Assert the mission is marked `partial_success` (80% >= 70% threshold).
5. Assert the assembly step was created with the partial success prompt modification.
6. Repeat with 6 completed and 4 failed. Assert the mission is marked `failed` (60% < 70%).
7. Repeat with 9 completed and 1 failed, where the 1 failed step is `is_critical_path = true`. Assert the mission is marked `failed` despite 90% completion.

**Test: Circuit Breaker** (`tests/integration/circuitBreaker.test.js`)

1. Configure `MockBraveSearch` to return errors.
2. Execute 3 consecutive research calls. Assert all fail normally (circuit still closed).
3. Assert the circuit breaker is now in `open` state.
4. Execute a 4th research call. Assert it returns immediately without hitting the mock (circuit open).
5. Assert `researchFailed = true` is set on the step.
6. Assert the synthesis prompt contains the general-knowledge disclaimer.
7. Advance time by 5 minutes. Configure `MockBraveSearch` to succeed.
8. Execute a research call. Assert the circuit transitions to `half-open`, then `closed`.

**Test: Revision History Preservation** (`tests/integration/revisionHistory.test.js`)

1. Complete a step with result "Version 1" and critique score 3.5.
2. Trigger a revision. Assert `step_revisions` contains one row with "Version 1" and score 3.5.
3. Complete the revision with result "Version 2" and critique score 4.2.
4. Trigger another revision. Configure the LLM mock to fail.
5. Assert the step's result is restored to "Version 2" (highest score from revisions).
6. Assert the step is marked `completed`, not `failed`.

**Test: Discord Delivery Retry** (`tests/integration/discordRetry.test.js`)

1. Configure `MockDiscord` to fail on the first 3 send attempts, then succeed.
2. Complete a step that triggers a Discord notification.
3. Assert 4 send attempts were made (1 initial + 3 retries).
4. Assert the notification was delivered.
5. Reconfigure `MockDiscord` to fail on all attempts.
6. Complete another step. Assert a row exists in `pending_notifications` with `status = 'pending'`.
7. Reconfigure `MockDiscord` to succeed. Run a heartbeat tick. Assert the pending notification is now `status = 'delivered'`.

**Test: Mission Pause/Resume/Cancel** (`tests/integration/missionLifecycle.test.js`)

1. Create a mission with 5 steps. Start the worker. Let 1 step begin processing.
2. Execute `!pause`. Assert the mission is `paused`. Assert the in-progress step completes normally. Assert no new steps are claimed.
3. Execute `!resume`. Assert the mission is `in_progress`. Assert the worker claims the next step.
4. Execute `!cancel`. Assert all pending steps are `cancelled`. Assert the mission is `cancelled`.

**Test: Null Result Validation Gate** (`tests/integration/nullResultGate.test.js`)

1. Configure `MockPipeline` to return `{ content: null, error: null }` — a silent null result (no explicit error).
2. Assign a step to the worker. Let the pipeline execute.
3. Assert the step is marked `failed` (not `in_review` or `completed`).
4. Assert `error_reason` contains `'Pipeline returned null or empty content'`.
5. Assert a `CRITICAL` log event with `event: 'null_result_detected'` was recorded.
6. Create a second mission where all steps succeed except the final step, which returns null.
7. Assert the final step is marked `failed`. Assert the mission is evaluated as `partial_success` or `failed` (not `completed`).
8. Assert no deliverable posting occurs for the null final step.

**Test: Context Overflow Prevention** (`tests/integration/contextOverflow.test.js`)

1. Create a mission with 10 steps, each producing 8,000 words of output (~80,000 words total).
2. Let all 10 steps complete. The 11th (assembly) step receives predecessor outputs.
3. Assert that predecessor outputs were truncated to fit within `MAX_PREDECESSOR_TOKENS`.
4. Assert `WARNING` log events with `event: 'predecessor_output_truncated'` were recorded.
5. Assert the assembly step still produces a non-null, non-empty result.
6. Assert the mission completes successfully with a deliverable.

**CI Integration**

These tests run in the CI pipeline (GitHub Actions) before every deploy to production. The CI configuration:
1. Spin up a PostgreSQL service container.
2. Run database migrations.
3. Execute `npm run test:integration`.
4. If any test fails, the deploy is blocked.

The `package.json` script:
```json
{
  "scripts": {
    "test:integration": "jest --config jest.integration.config.js --runInBand --forceExit"
  }
}
```

The `--runInBand` flag ensures tests run sequentially (they share a database). The `--forceExit` flag handles cleanup of any lingering async handles from the heartbeat or worker.

---

## 4. Phase 2 — Pipeline Redesign

Phase 1 makes missions reliable. Phase 2 makes them intelligent. The current pipeline treats each step as an isolated unit — agents execute without knowledge of what other agents have produced, leading to redundant work, contradictory outputs, and deliverables that read like stapled-together fragments rather than coherent documents. This phase introduces shared context, structured handoffs, and adaptive execution depth.

---

### 4.1 Remove Per-Step QA (Ein)

The current pipeline runs a full QA review by Ein (the quality assurance agent) on every individual step. This was originally intended to catch errors early but has proven to be the single largest contributor to pipeline latency. Each Ein review requires an LLM call, adds 20-40 seconds of execution time, and produces feedback that is rarely actionable at the step level — Ein's strengths lie in cross-step coherence, not within-step quality.

**What Changes**

- Remove Ein from the per-step approval chain in `executePipeline()` within `worker.js`. The pipeline phases become: decompose → research → synthesize → self-critique → (conditional) revise.
- Self-critique remains. It is fast (same LLM call that generated the output evaluates it), cheap (no additional API call to a separate model), and domain-aware (the generating agent knows the task context better than a generic QA prompt).
- The `agents` table retains Ein's record. Ein's `agent_type` is updated from `'qa'` to `'coherence_auditor'` to reflect the new role.

**Ein's New Role: Project-Level Coherence Auditor**

Ein reviews the assembled deliverable once per mission (Section 4.4), not once per step. This is a dramatically better use of the QA agent:

- Ein sees the complete output, enabling detection of contradictions between sections.
- Ein evaluates whether the deliverable as a whole addresses the original brief.
- Ein checks for formatting consistency, logical flow, and completeness.
- One high-value review replaces N low-value reviews.

**Performance Impact**

For a mission with 8 steps, this removes 8 LLM calls and 8 approval waits. At an average of 30 seconds per Ein review, this eliminates approximately 4 minutes of pipeline time per mission. For missions with revision loops that previously triggered additional Ein reviews, the savings compound further.

---

### 4.2 Shared Project Workspace

The fundamental problem with the current architecture is information isolation. Each step executes with only its own task description and (if lucky) the direct output of its parent step. Agent B has no idea what Agent A discovered. Agent C duplicates work that Agent A already completed. The final deliverable is assembled from pieces that were written in mutual ignorance.

The shared project workspace solves this by giving every agent read access to everything the team has produced so far.

**New Table: `project_workspace`**

```sql
CREATE TABLE project_workspace (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  mission_id INTEGER NOT NULL REFERENCES missions(id) ON DELETE CASCADE,
  section_key TEXT NOT NULL,
  agent_id TEXT NOT NULL,
  content TEXT NOT NULL,
  version INTEGER NOT NULL DEFAULT 1,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(mission_id, section_key)
);

CREATE INDEX idx_project_workspace_mission_id ON project_workspace(mission_id);
```

The `UNIQUE(mission_id, section_key)` constraint ensures each section has exactly one current version. When an agent updates a section, the `version` column increments and `updated_at` is refreshed via an `ON CONFLICT ... DO UPDATE` upsert.

**Section Keys**

Section keys are short, descriptive identifiers for the deliverable component that a step produces. Examples:

| Step Description | Section Key |
|---|---|
| "Research the competitive landscape for AI writing tools" | `competitor_analysis` |
| "Build a financial model for Year 1 operations" | `financial_model` |
| "Identify the target customer persona" | `customer_persona` |
| "Draft the executive summary" | `executive_summary` |

Frasier assigns section keys during decomposition. The `mission_steps` table gets a new column:

```sql
ALTER TABLE mission_steps ADD COLUMN section_key TEXT;
```

The decomposition prompt includes: `"For each step, assign a concise section_key that identifies what part of the deliverable this step contributes to. Use snake_case. Examples: 'market_research', 'revenue_model', 'risk_analysis'."` The decomposition output parser extracts the section key and stores it on the step record.

**Write Protocol**

When a step completes with status `completed`:

```sql
INSERT INTO project_workspace (mission_id, section_key, agent_id, content, version)
VALUES ($missionId, $sectionKey, $agentId, $stepResult, 1)
ON CONFLICT (mission_id, section_key)
DO UPDATE SET
  content = EXCLUDED.content,
  agent_id = EXCLUDED.agent_id,
  version = project_workspace.version + 1,
  updated_at = NOW();
```

This upsert means if two steps share a section key (e.g., an initial research step and a deeper follow-up step), the later step's output overwrites the earlier one. The version counter tracks how many times the section has been updated. Previous versions are not stored in the workspace table (the `step_revisions` table preserves historical step outputs; the workspace always reflects the latest state).

**Read Protocol**

Before executing a step, the worker loads relevant workspace sections:

```sql
SELECT section_key, agent_id, content, version, updated_at
FROM project_workspace
WHERE mission_id = $missionId
ORDER BY updated_at ASC;
```

All sections are loaded (not just those from direct dependencies) because agents benefit from broad context. The worker injects the workspace into the agent's prompt as a structured block:

```
=== PROJECT WORKSPACE (Current State) ===

--- Section: market_research (by Maya, Researcher | v2, updated 3 min ago) ---
[content truncated to 3000 chars if longer]

--- Section: customer_persona (by Niles, Strategist | v1, updated 8 min ago) ---
[content truncated to 3000 chars if longer]

=== END PROJECT WORKSPACE ===

Your task: [step description]
```

**Token Budget Management**

The total workspace injection is capped at 12,000 tokens (approximately 9,000 words). If the workspace exceeds this, sections are prioritized:
1. Sections from direct dependency steps (always included in full, up to 4,000 tokens each).
2. Sections with the most recent `updated_at` (included next, truncated to 2,000 tokens each).
3. Remaining sections summarized to 500 tokens each via a fast LLM call.
4. If still over budget, oldest and least-related sections are dropped with a note: `"[Additional workspace sections omitted for brevity. Full workspace available.]"`

The truncation strategy ensures agents always see the most relevant and recent context while staying within model context limits.

---

### 4.3 Agent Handoff Protocol

The shared workspace provides broad context. The handoff protocol provides focused context — the specific output from the step(s) that this step directly depends on. Together, they give the executing agent both a panoramic view (workspace) and a close-up view (handoff) of the project state.

**Handoff Block Construction**

When the worker prepares to execute step B, which depends on step A (via the `step_dependencies` table):

1. Load step A's result from `mission_steps.result`.
2. Load step A's agent assignment from `mission_steps.agent_id`, joined to `agents.name` and `agents.role`.
3. Load relevant workspace sections for additional context.
4. Construct the handoff block:

```
=== HANDOFF FROM Maya (Senior Researcher) ===
TASK COMPLETED: Research the competitive landscape for AI writing tools
KEY FINDINGS:
[Step A's result, truncated to 4,000 characters if longer. Truncation preserves
the first 2,000 characters and the last 2,000 characters, with a note in between:
"[...middle section truncated for brevity — full output available in project workspace...]"]
WORKSPACE CONTEXT:
[Relevant workspace sections that step B might need beyond step A's direct output]
=== END HANDOFF ===
```

If step B depends on multiple steps (A and C), multiple handoff blocks are included, ordered by the dependency steps' completion time (earliest first, so the narrative builds chronologically).

**Prompt Assembly Order**

The full prompt for step B's executing agent is assembled in this order:

1. **System prompt**: Agent's capability manifest and behavioral directives.
2. **Project workspace**: Current state of all workspace sections (Section 4.2).
3. **Handoff block(s)**: Direct dependency outputs (this section).
4. **Task description**: Step B's description and acceptance criteria.
5. **Pipeline phase directive**: Phase-specific instructions (e.g., "You are now in the synthesis phase. Produce the deliverable content.").

This order is intentional. The agent reads its identity first, then sees the broad project context, then the specific inputs from upstream agents, then its own task. This mirrors how a human team member would be briefed: role → context → inputs → assignment.

**Handling Missing Handoffs**

If a dependency step's result is `null` (should not happen with Section 3.3's revision history, but defensively handled):
- Log a `WARNING` event: `{ event: 'missing_handoff', step_id: stepB.id, missing_from: stepA.id }`.
- Include a reduced handoff block: `"=== HANDOFF FROM [Agent] === TASK COMPLETED: [description]. NOTE: Output from this step was not available. Proceed with the information in the project workspace. === END HANDOFF ==="`.

---

### 4.4 Final Assembly Phase

Individual step outputs, even with shared workspace context and handoffs, are written from each agent's perspective. The final deliverable needs a single authorial voice, consistent formatting, no redundancy, and a coherent narrative arc. The assembly phase provides this.

**Automatic Assembly Trigger**

When the last step of a mission reaches a terminal state (`completed`, `failed`, or `cancelled`), the worker evaluates the mission's outcome:

- If `completed` or `partial_success`: create an assembly step.
- If `failed`: skip assembly, post failure summary to Discord.

The assembly step is created programmatically (not during decomposition) with the following properties:

```sql
INSERT INTO mission_steps (
  mission_id, agent_id, description, status, is_critical_path, section_key,
  step_order, complexity
)
VALUES (
  $missionId,
  'frasier',              -- Frasier (COO) handles assembly
  'Assemble final deliverable from all team outputs',
  'pending',
  true,                   -- Assembly is always critical path
  'final_deliverable',
  (SELECT MAX(step_order) + 1 FROM mission_steps WHERE mission_id = $missionId),
  'standard'
);
```

The assembly step has no dependencies in the `step_dependencies` table — its trigger is the completion of all other steps, not a DAG edge. The worker detects this by checking: after completing any step, are all non-assembly steps in a terminal state? If yes, the assembly step's status is set to `pending` and it becomes eligible for claiming.

**Assembly Context Budget**

The assembly step must handle missions with potentially massive total output — Mission #91 produced 61,000 words across 18 steps, far exceeding any model's effective context window. Without explicit context management, the assembly step will either fail silently (producing null output) or produce a shallow summary that loses the depth of the underlying research.

The assembly step uses a tiered context loading strategy:

1. **Primary context (always included, full text):** The original mission brief, the workspace sections from `project_workspace`, and any step marked `is_critical_path = true`. These are the structural backbone. Token budget: up to 30,000 tokens.

2. **Secondary context (summarized if necessary):** Completed step results that are NOT critical-path. These provide supporting detail. If the total token estimate for all secondary results exceeds 20,000 tokens, each is truncated to its first 1,500 words and last 500 words with an explicit `[... middle section omitted for context budget — full content available in workspace ...]` marker. Token budget: up to 20,000 tokens.

3. **Metadata only (when context is exhausted):** If even after summarization the context exceeds 50,000 tokens, remaining non-critical steps are represented as one-line summaries only: `"Step N ([agent]): [description] — [critique_score]/5"`. This ensures the assembly step knows what exists even if it cannot read the full content.

The assembly prompt explicitly tells Frasier: `"Some step outputs have been summarized for context management. Use workspace sections as the primary source of truth. Step outputs are supplementary. If you need more detail from a summarized step, note the gap in the deliverable rather than fabricating content."`

Token estimation uses a conservative 4-characters-per-token ratio. The 50,000-token total budget leaves approximately 30,000 tokens for the system prompt, assembly instructions, and generated output within a 128K-token context window.

**Assembly Prompt**

Frasier's assembly prompt receives:

1. The original mission brief (from `missions.brief`).
2. All workspace sections (from `project_workspace`), ordered by section key to match the deliverable structure.
3. All completed step results (from `mission_steps.result`), subject to the context budget above — full text for critical-path steps, summarized or metadata-only for others.
4. A list of failed steps with their error reasons (if `partial_success`).

The prompt:

```
You are assembling the final deliverable for the project: "[mission name]".

ORIGINAL BRIEF:
[mission.brief]

PROJECT WORKSPACE (all sections):
[workspace sections, in order]

COMPLETED STEP OUTPUTS:
[step results, for reference]

FAILED STEPS (if any):
[list of failed step descriptions and reasons]

INSTRUCTIONS:
1. Synthesize all team outputs into a single, coherent, professional document.
2. Ensure consistency of tone, terminology, and formatting across all sections.
3. Remove redundancy — if multiple agents covered the same ground, merge into one definitive treatment.
4. Fill minor gaps where one section references information that another section elaborates on.
5. If any sections were produced without web research (marked in the workspace), preserve the general-knowledge disclaimer.
6. If this is a partial success, explicitly note which sections are missing and why.
7. Format the deliverable for the founder's review: clear headings, actionable conclusions, no jargon without definition.
8. The deliverable should read as if written by one expert, not stapled together from multiple authors.
```

**Ein's Coherence Review**

After the assembly step completes, a final review step is created and assigned to Ein:

```sql
INSERT INTO mission_steps (
  mission_id, agent_id, description, status, section_key, step_order, complexity
)
VALUES (
  $missionId,
  'ein',
  'Coherence review of assembled deliverable',
  'pending',
  'coherence_review',
  (SELECT MAX(step_order) + 1 FROM mission_steps WHERE mission_id = $missionId),
  'simple'                -- Review is a single-pass evaluation
);
```

A dependency edge is added from the assembly step to the review step.

Ein's review prompt:

```
You are performing a coherence review on the final deliverable for: "[mission name]".

ORIGINAL BRIEF:
[mission.brief]

ASSEMBLED DELIVERABLE:
[assembly step result]

Evaluate the deliverable against these criteria:
1. COMPLETENESS: Does it address every requirement in the original brief? List any gaps.
2. INTERNAL CONSISTENCY: Are there any contradictions between sections? Any place where one section says X and another implies not-X?
3. LOGICAL FLOW: Does the document progress logically? Are transitions between sections smooth?
4. FORMATTING: Is the formatting consistent (heading levels, list styles, terminology)?
5. ACTIONABILITY: Does the deliverable give the founder clear, actionable conclusions?

Produce a review in this format:
- Overall Score: [1-5]
- Issues Found: [list, or "None"]
- Suggested Fixes: [list, or "None"]

If Overall Score >= 4.0: Approve the deliverable as-is.
If Overall Score 3.0-3.9: List specific fixes. The assembly step will be re-run with your feedback.
If Overall Score < 3.0: Flag for human review. The deliverable has fundamental problems.
```

If Ein's score is below 4.0, the assembly step is re-queued with Ein's feedback injected into the prompt. This loop runs at most twice — if the second assembly attempt still scores below 4.0, the deliverable is posted with Ein's review notes attached so Dhroov can see both the deliverable and the identified issues.

**Deliverable Posting**

The final deliverable (post-review) is posted to Discord by Frasier. If the content exceeds Discord's 2,000-character message limit:
1. Split into multiple messages at section boundaries (not mid-paragraph).
2. First message includes the mission name and brief summary.
3. Subsequent messages are prefixed with `"[continued — part X of Y]"`.
4. If total content exceeds 10,000 characters, attach as a formatted text file instead.

---

### 4.5 Mid-Execution Escalation

Some problems cannot be solved by retrying harder. When an agent's self-critique identifies a fundamental issue — the task is infeasible, the brief contradicts itself, or the approach is wrong — the system needs an escalation path rather than burning through revision loops that will never converge.

**Escalation Trigger**

During the self-critique phase, if BOTH conditions are met:
1. Critique score < 2.0.
2. Critique text contains one or more of these keywords: `"impossible"`, `"infeasible"`, `"contradicts"`, `"wrong approach"`, `"cannot be completed"`, `"fundamentally flawed"`, `"outside scope"`.

The keyword check is case-insensitive and uses substring matching (not exact word matching), so "this approach is fundamentally contradictory" would trigger on "contradict".

**New Step Status: `escalated`**

```sql
-- Add to the CHECK constraint on mission_steps.status
ALTER TABLE mission_steps DROP CONSTRAINT IF EXISTS mission_steps_status_check;
ALTER TABLE mission_steps ADD CONSTRAINT mission_steps_status_check
  CHECK (status IN ('pending', 'in_progress', 'completed', 'failed', 'cancelled', 'escalated'));
```

When escalation triggers:
1. Set the step's status to `escalated`.
2. Store the critique details: `escalation_reason = critique_text` (new column on `mission_steps`, type TEXT).
3. Create an escalation event in the application log: `{ event: 'step_escalated', step_id, mission_id, agent_id, critique_score, critique_text }`.
4. Notify Frasier (the COO agent) via an internal escalation mechanism (described below).

**Frasier's Escalation Response**

Frasier receives the escalation as a special prompt:

```
ESCALATION ALERT — Step [id] in Mission "[name]" has been flagged by [agent name].

STEP DESCRIPTION: [description]
CRITIQUE SCORE: [score]
CRITIQUE DETAILS: [critique text]
PROJECT WORKSPACE STATE: [current workspace sections summary]

You have three options:
1. RE-DECOMPOSE: Break this step into different sub-steps with a revised approach. Explain the new approach.
2. SKIP: Mark this step as skipped and adjust downstream steps. Explain why skipping is acceptable.
3. FAIL MISSION: This problem is insurmountable. The mission cannot deliver value. Explain why.

Choose one option and provide your reasoning.
```

Frasier's response is parsed for the chosen option:

- **RE-DECOMPOSE**: The escalated step is marked `failed`. New replacement steps are created with revised descriptions. Dependencies are rewired: anything that depended on the escalated step now depends on the new steps.
- **SKIP**: The escalated step is marked `cancelled` with `error_reason = 'Skipped by Frasier: [reasoning]'`. Dependent steps are evaluated — if they can proceed without this input, they continue; if not, they are also cancelled.
- **FAIL MISSION**: The mission is marked `failed` with `failure_reason = 'Escalation: [Frasier's reasoning]'`. All pending steps are cancelled.

**Human Escalation Timeout**

If Frasier's automated escalation response does not resolve the issue (the replacement steps also escalate, or Frasier's response cannot be parsed), the system falls back to human notification:

- After 10 minutes with no resolution: post to Discord: `"@Dhroov — Mission [name] has a step that cannot be resolved automatically. Step [id]: [description]. The agent reported: [critique excerpt]. I need your guidance on how to proceed."`
- The mission is paused (Section 3.6 pause behavior) until Dhroov responds with `!resume`, `!cancel`, or manual instructions.

---

### 4.6 Adaptive Pipeline Depth

The current pipeline applies identical processing to every step: decompose → research → synthesize → critique → revise. This is wasteful. A step that formats data into a table does not need web research. A step that produces a competitive analysis needs more research depth than the default. Adaptive pipeline depth matches processing intensity to task complexity.

**Complexity Levels**

New column on `mission_steps`:

```sql
ALTER TABLE mission_steps ADD COLUMN complexity TEXT DEFAULT 'standard'
  CHECK (complexity IN ('simple', 'standard', 'deep'));
```

| Complexity | Pipeline Phases | Use Cases |
|---|---|---|
| `simple` | synthesize → critique | Coordination tasks, formatting, data reorganization, summaries of already-available workspace content, status updates |
| `standard` | decompose → research → synthesize → critique → (conditional) revise | Analysis, writing, design, most knowledge work |
| `deep` | decompose → extended research → synthesize → critique → mandatory revise | Financial modeling, technical architecture, competitive analysis, legal review, anything requiring high factual accuracy |

**Phase Behavior by Complexity**

**Simple:**
- Skip the decompose phase entirely (the step is already atomic).
- Skip the research phase (no web search needed — the workspace provides all necessary context).
- Execute synthesize with the workspace context and handoff blocks.
- Execute self-critique. If score >= 3.5, mark complete. If score < 3.5, execute one revision pass. No further revisions.

**Standard (current behavior, unchanged):**
- Decompose: break the task into sub-components if complex enough.
- Research: standard Brave Search budget (up to 5 queries, 10 results per query).
- Synthesize: produce the output.
- Self-critique: evaluate against acceptance criteria.
- Revise: if critique score < 4.0, revise once. If still < 4.0 after revision, accept as-is (the improvement from further revisions exhibits diminishing returns at standard complexity).

**Deep:**
- Decompose: break the task into sub-components with explicit acceptance criteria per sub-component.
- Extended research: doubled budget (up to 10 queries, 15 results per query). Research phase also attempts to find primary sources (academic papers, official documentation, regulatory filings) rather than relying solely on general web results. The research prompt is augmented: `"Prioritize primary sources: official documentation, peer-reviewed research, regulatory filings, and direct company disclosures. Secondary sources (news articles, blog posts) are supplementary."`
- Synthesize: produce the output with explicit source citations for every factual claim.
- Self-critique: evaluate with a stricter rubric. The critique prompt adds: `"Apply rigorous standards. Every factual claim must have a cited source. Logical arguments must be watertight. Unsupported conclusions are scored as errors."`
- Mandatory revise: regardless of critique score, the revision phase always runs for deep-complexity steps. Even a score of 4.5 triggers a revision pass with the directive: `"Your output scored [X]. Even at high scores, identify any remaining weaknesses and strengthen them."`
- Maximum two revision passes for deep complexity (vs. one for standard).

**Complexity Assignment During Decomposition**

Frasier assigns complexity during the decomposition phase. The decomposition prompt includes:

```
For each step, assign a complexity level:
- "simple": The step is coordination, formatting, summarization of existing content, or data reorganization. No external research needed.
- "standard": The step requires analysis, original writing, or synthesis of new information. Standard research depth.
- "deep": The step requires high factual accuracy, involves financial modeling, technical architecture, legal analysis, or competitive intelligence. Extended research and mandatory revision.

Base your assessment on: the step's description, its acceptance criteria, the type of deliverable it contributes to, and the domain expertise required. When in doubt, choose "standard" — it is better to over-process than to under-process a critical step.
```

The decomposition output parser extracts the complexity value and stores it on the `mission_steps.complexity` column. If the parser fails to extract a valid complexity value, it defaults to `'standard'`.

**Pipeline Router**

The worker's `executePipeline()` function uses the step's complexity to determine which phases to run. Implementation is a configuration map:

```javascript
const PIPELINE_PHASES = {
  simple: ['synthesize', 'critique'],
  standard: ['decompose', 'research', 'synthesize', 'critique', 'revise'],
  deep: ['decompose', 'extendedResearch', 'synthesize', 'critique', 'mandatoryRevise']
};

async function executePipeline(step) {
  const phases = PIPELINE_PHASES[step.complexity] || PIPELINE_PHASES.standard;
  for (const phase of phases) {
    await checkCancellation(step.id);
    const startTime = Date.now();
    await executePhase(phase, step);
    recordPhaseTiming(step.id, phase, startTime);
  }
}
```

The `extendedResearch` phase calls the same Brave Search integration as `research` but with doubled query and result limits. The `mandatoryRevise` phase bypasses the score threshold check and always executes.

**Observability Impact**

The `phase_timings` JSONB column (Section 3.8) naturally captures which phases ran for each step. The hourly performance metrics can break down average duration by complexity level:

```sql
SELECT complexity, AVG(EXTRACT(EPOCH FROM (completed_at - started_at))) AS avg_seconds
FROM mission_steps
WHERE completed_at > NOW() - INTERVAL '1 HOUR'
GROUP BY complexity;
```

This data enables future tuning: if `simple` steps average 15 seconds and `deep` steps average 180 seconds, the system is correctly differentiating. If they converge, the complexity assignment logic needs refinement.

## 5. Phase 3 — Parallel Execution

### 5.1 Multi-Worker Architecture

The current system runs a single `worker.js` process that polls `getPendingSteps()` every 5 seconds and executes one step at a time. The DAG dependency system introduced in Phase 2 already identifies which steps are unblocked and eligible for execution. Phase 3 closes the gap between "knowing what can run in parallel" and "actually running it in parallel."

**Architecture:**

PM2 manages N identical worker processes, each running the same `worker.js` code. The only difference between workers is their unique identifier, passed as an environment variable (`WORKER_ID=worker-1`, `WORKER_ID=worker-2`). There is no coordinator process — each worker independently polls the database, claims work, and executes it.

**Claim Mechanism:**

The core of parallel execution is an atomic claim query that prevents two workers from executing the same step:

```sql
UPDATE mission_steps
SET status = 'in_progress',
    claimed_by = $1,
    started_at = NOW()
WHERE id = (
  SELECT id FROM mission_steps
  WHERE status = 'pending'
    AND mission_id IN (SELECT id FROM ops_missions WHERE status = 'in_progress')
    AND id NOT IN (
      SELECT step_id FROM step_dependencies
      WHERE depends_on_step_id IN (
        SELECT id FROM mission_steps WHERE status != 'completed'
      )
    )
  ORDER BY step_order ASC
  LIMIT 1
  FOR UPDATE SKIP LOCKED
)
RETURNING *;
```

Key details:
- `FOR UPDATE SKIP LOCKED` ensures that if Worker-1 is in the process of claiming a row, Worker-2's query skips that row entirely rather than blocking. This eliminates lock contention.
- If the `UPDATE` returns zero rows, no work is available. The worker sleeps for its poll interval and tries again.
- The `claimed_by` column is a `TEXT` field storing the worker's ID. It serves as an audit trail (which worker ran which step) and as a diagnostic tool when investigating failures.
- On step completion or failure, the worker updates `status`, clears `claimed_by`, and sets `completed_at` or `failed_at`.

**Schema Change:**

```sql
ALTER TABLE mission_steps ADD COLUMN claimed_by TEXT DEFAULT NULL;
ALTER TABLE mission_steps ADD COLUMN started_at TIMESTAMPTZ DEFAULT NULL;
CREATE INDEX idx_mission_steps_status_mission ON mission_steps(status, mission_id);
CREATE INDEX idx_mission_steps_claimed ON mission_steps(claimed_by) WHERE claimed_by IS NOT NULL;
```

The `started_at` column enables timeout detection. If a step has been `in_progress` for longer than a configurable threshold (default: 10 minutes), the heartbeat process marks it as `failed` with reason `timeout`, clears `claimed_by`, and the step becomes eligible for retry or cascade-failure per Phase 1 rules.

**PM2 Configuration:**

```javascript
// ecosystem.config.js — worker section
{
  name: 'worker',
  script: './src/worker.js',
  instances: 2,
  exec_mode: 'fork',        // Not cluster — each is an independent process
  max_memory_restart: '200M',
  env: {
    NODE_ENV: 'production'
  },
  instance_var: 'WORKER_ID', // PM2 sets WORKER_ID=0, WORKER_ID=1, etc.
  watch: false,
  autorestart: true,
  max_restarts: 10,
  restart_delay: 5000
}
```

Each worker process uses `WORKER_ID` to construct its identifier string (`worker-${process.env.WORKER_ID || process.env.NODE_APP_INSTANCE || 0}`). PM2's `NODE_APP_INSTANCE` environment variable is automatically set in multi-instance mode, providing the fallback.

**Worker Lifecycle:**

1. Worker starts, logs its ID, connects to database via connection pool.
2. Polls for claimable steps every 5 seconds (configurable via `WORKER_POLL_INTERVAL_MS`).
3. Claims a step via the atomic query. If no rows returned, sleeps and retries.
4. Executes the step through the standard pipeline (prompt construction → LLM call → result storage → critique if applicable).
5. On completion: updates step status, stores result, triggers any downstream dependency checks.
6. On failure: updates step status to `failed`, stores error, triggers cascade-failure logic from Phase 1.
7. Returns to polling.

Workers share no in-memory state. All coordination happens through the database. This means a worker can crash and restart without affecting any other worker. PM2's `autorestart` ensures crashed workers come back within 5 seconds.

### 5.2 Parallel Step Groups

The DAG system from Phase 2 implicitly defines which steps can run in parallel: any steps whose dependencies are all satisfied are eligible simultaneously. Phase 3 makes this explicit in the decomposition output so that both the system and Dhroov can understand the execution plan.

**Decomposition Enhancement:**

During mission decomposition, Frasier's planning prompt includes an instruction to organize steps into numbered execution groups. The decomposition output schema adds a `parallel_groups` array:

```json
{
  "steps": [
    { "id": 1, "title": "Research market size", "agent": "edward", "dependencies": [] },
    { "id": 2, "title": "Analyze top 5 competitors", "agent": "edward", "dependencies": [] },
    { "id": 3, "title": "Profile target audience", "agent": "faye", "dependencies": [] },
    { "id": 4, "title": "Synthesize competitive landscape", "agent": "vicious", "dependencies": [1, 2] },
    { "id": 5, "title": "Map audience-product fit", "agent": "faye", "dependencies": [3, 4] },
    { "id": 6, "title": "Assemble final deliverable", "agent": "frasier", "dependencies": [4, 5] }
  ],
  "parallel_groups": [
    { "group": 1, "step_ids": [1, 2, 3], "description": "Independent research tasks" },
    { "group": 2, "step_ids": [4, 5], "depends_on_groups": [1], "description": "Analysis requiring research results" },
    { "group": 3, "step_ids": [6], "depends_on_groups": [2], "description": "Final synthesis and assembly" }
  ]
}
```

The `parallel_groups` field is informational — it does not override the DAG. The DAG remains the source of truth for execution order. The groups exist for two purposes:

1. **Discord visibility.** When a mission starts, Frasier posts the execution plan in human-readable form: "Phase 1 (3 parallel tasks): Edward researches market size, Edward analyzes competitors, Faye profiles audience → Phase 2 (2 tasks): Vicious synthesizes competitive landscape, Faye maps audience fit → Phase 3: Frasier assembles deliverable." This gives Dhroov a clear mental model of what's happening and how long it should take.

2. **Progress reporting.** The heartbeat process uses group boundaries to report meaningful progress: "Group 1 complete (3/3). Starting Group 2." rather than raw step counts that obscure the structure.

**Validation:** During decomposition, the system validates that `parallel_groups` is consistent with `dependencies`. If a step in Group 2 has no dependency on any step in Group 1, the validator flags it — the step should be in Group 1. This catches decomposition errors before execution begins.

### 5.3 Resource Contention

Parallel execution multiplies pressure on every external dependency. Two workers executing research steps simultaneously send twice the API calls in half the time. Without centralized tracking, free-tier limits can be exhausted mid-mission with no warning.

**Brave Search Budget Tracker:**

A `research_budget` table provides centralized, real-time tracking of search API usage:

```sql
CREATE TABLE research_budget (
  id SERIAL PRIMARY KEY,
  month TEXT NOT NULL UNIQUE,            -- Format: '2026-03'
  queries_used INTEGER NOT NULL DEFAULT 0,
  queries_limit INTEGER NOT NULL DEFAULT 200,
  fetches_used INTEGER NOT NULL DEFAULT 0,
  fetches_limit INTEGER NOT NULL DEFAULT 2000,
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

Before any Brave Search call, the worker executes an atomic increment-and-check:

```sql
UPDATE research_budget
SET queries_used = queries_used + 1,
    updated_at = NOW()
WHERE month = TO_CHAR(NOW(), 'YYYY-MM')
  AND queries_used < queries_limit
RETURNING queries_used, queries_limit;
```

If zero rows returned, the budget is exhausted. The worker skips the search call and passes a modified prompt to the LLM: "Research budget exhausted. Synthesize the best answer you can from your training data. State clearly which claims are from verified sources vs. general knowledge." This produces an honest, lower-confidence output rather than a hallucinated one disguised as researched fact.

At 80% budget utilization (160 queries), the heartbeat posts a Discord warning: "Research budget at 80% (160/200 queries). Remaining missions this month will have reduced research depth." This gives Dhroov the option to prioritize remaining budget or upgrade to a paid Brave Search tier ($5/month for 2,000 queries).

**Row initialization:** The heartbeat process checks on startup and at midnight UTC whether a row exists for the current month. If not, it inserts one with default limits. This avoids race conditions between workers trying to create the initial row.

**OpenRouter Rate Limiting:**

OpenRouter returns rate limit headers on every response:
- `X-RateLimit-Remaining` — requests remaining in the current window
- `X-RateLimit-Reset` — Unix timestamp when the window resets

The LLM client module (`src/lib/llm.js`) parses these headers after every call. Behavior:

| Remaining | Action |
|-----------|--------|
| > 20 | Normal execution |
| 10–20 | Log warning, continue |
| 1–10 | Add 2-second delay between calls |
| 0 | Sleep until reset timestamp + 5-second buffer, then retry |

This logic lives in the shared LLM client, so all workers respect it independently. Since each worker makes its own API calls, the rate limit state is per-response — no shared in-memory counter needed.

Additionally, the LLM client implements exponential backoff for 429 (Too Many Requests) responses: wait 5 seconds, then 15, then 45, then fail the step. Three consecutive 429s on different steps within 60 seconds triggers the circuit breaker from Phase 1, pausing all LLM calls for 2 minutes.

**Supabase Connection Pooling:**

Supabase's free tier provides a connection pooler (PgBouncer) at a separate connection string. The current system connects directly to the database. With parallel workers, each process holding its own connections risks hitting the 60-connection limit.

Configuration change in `src/lib/database.js`:

```javascript
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,  // Use pooler URL, not direct
  max: 5,                                       // Max 5 connections per process
  idleTimeoutMillis: 30000,                     // Release idle connections after 30s
  connectionTimeoutMillis: 10000                // Fail if can't connect in 10s
});
```

Connection budget at N=2 workers:
- Worker-1: 5 connections
- Worker-2: 5 connections
- discord_bot: 3 connections
- heartbeat: 2 connections
- **Total: 15 connections** (well within the 60-connection limit)

This leaves ample headroom for scaling to N=3 or N=4 workers in the future without hitting connection limits.

**VPS Memory Management:**

With parallel workers, total memory consumption on the 1GB VPS becomes:

| Process | Estimated RSS |
|---------|--------------|
| discord_bot.js | 80–120 MB |
| heartbeat.js | 40–60 MB |
| worker-0 | 100–180 MB (spikes during LLM response parsing) |
| worker-1 | 100–180 MB |
| PM2 daemon | 30–50 MB |
| OS + PostgreSQL client libs | 100–150 MB |
| **Total** | **450–740 MB** |

On a 1GB VPS, this works under normal conditions but leaves dangerously thin margins during load spikes. The PM2 `max_memory_restart: 200M` setting prevents any single worker from consuming unbounded memory, but a simultaneous spike across both workers could still trigger OOM kills.

**Recommendation:** Upgrade to the 2GB DigitalOcean droplet ($12/month, a $4/month increase) before enabling the second worker. This provides comfortable headroom and eliminates OOM risk as the primary failure mode. The upgrade is a one-command operation via the DigitalOcean control panel (requires a brief reboot).

---

## 6. Phase 4 — Build & Delivery Capabilities

Phase 4 transforms Frasier from a system that produces text documents into one that produces shippable products: formatted digital goods, working software, and configured external services. This is the phase where Frasier becomes a revenue-generating operation.

### 6.1 Execution Modes

Every mission is assigned a `mode` during decomposition. The mode determines which tools are available to agents, what the output format looks like, and which pipeline stages apply. The mode is stored on the `ops_missions` table and is immutable after decomposition (changing mode mid-mission would invalidate the step structure).

**Four modes:**

**Research Mode** (default, current behavior)
- Tools: Brave Search, web fetch, LLM synthesis
- Output: Structured text stored in `step_results` and assembled via Phase 2 workspace
- Agents involved: Primarily Edward (research), Vicious (analysis), Frasier (assembly)
- Use cases: Market research, competitive analysis, financial modeling, strategic planning, due diligence
- Cost profile: $0.50–$2.00 per mission (dominated by LLM calls and search queries)

**Content Mode**
- Tools: Research mode tools + formatting directives + document structure templates
- Output: Publishable documents with title pages, tables of contents, section headers, formatted body text, citations, and appendices
- Agents involved: Edward (research), Faye (writing and tone), Spike (technical accuracy review if applicable), Frasier (assembly and formatting)
- Use cases: Info products (PDF guides, playbooks, frameworks), email sequences, course outlines, blog post series, documentation
- Cost profile: $1.00–$5.00 per mission (more LLM calls for writing, revision, and formatting)

**Build Mode**
- Tools: Research mode tools + file system operations (`write_file`, `read_file`, `list_files`) + command execution (`run_command`) + Git operations
- Output: A working codebase in a sandboxed directory with passing tests, a README, and deployment instructions
- Agents involved: Edward (technical research), Spike (architecture, code generation, debugging), Ein (testing, security review), Frasier (spec and coordination)
- Use cases: REST APIs, CLI tools, web apps, AI agents, automation scripts, data pipelines
- Cost profile: $2.00–$10.00 per mission (iterative code generation, test-fix cycles, multiple LLM calls per file)

**Operations Mode**
- Tools: External service API clients (Gumroad, Google Docs, Notion, email platforms)
- Output: Configured external resources (product listings, published documents, created pages) with confirmation URLs
- Agents involved: Vicious (copywriting, listing optimization), Faye (audience-facing content), Julia (execution of API calls)
- Use cases: Product launches, content distribution, storefront setup, marketing campaigns
- Cost profile: $0.25–$1.00 per mission (few LLM calls, primarily API integration work)

**Mode Selection Logic:**

During decomposition, Frasier's planning prompt includes the mission description and asks the LLM to select a mode based on the desired output. The prompt includes examples:

- "Research the top 10 AI newsletter monetization strategies" → `research`
- "Create a comprehensive guide to building AI agents" → `content`
- "Build a REST API for tracking newsletter subscribers" → `build`
- "List our AI Agents Guide on Gumroad at $29" → `operations`

Compound missions (e.g., "Research AI agents, write a guide, and list it on Gumroad") are decomposed into sub-missions with different modes, linked by dependencies. The decomposer creates:
1. Mission A (research mode): Research AI agents
2. Mission B (content mode): Write guide, depends on Mission A
3. Mission C (operations mode): List on Gumroad, depends on Mission B

Each sub-mission follows its own pipeline independently.

**Schema Change:**

```sql
ALTER TABLE ops_missions ADD COLUMN mode TEXT NOT NULL DEFAULT 'research'
  CHECK (mode IN ('research', 'content', 'build', 'operations'));
ALTER TABLE ops_missions ADD COLUMN cost_cap DECIMAL(10,2) DEFAULT 2.00;
ALTER TABLE ops_missions ADD COLUMN parent_mission_id INTEGER REFERENCES ops_missions(id);
```

The `parent_mission_id` column enables compound missions. Sub-missions reference their parent so that the system can track overall progress and Frasier can report "Mission #91: 2 of 3 sub-missions complete."

### 6.2 Content Delivery Pipeline

The content pipeline converts research into a formatted, sellable digital product. Each stage is a mission step executed by the appropriate agent.

**Stage 1: Research & Structure (Edward, research mode)**

Standard deep work pipeline from Phase 2. Edward receives the topic and produces structured research output: key findings organized by section, data points with source attribution, relevant quotes and statistics, and a recommended document outline. The outline is stored in the project workspace under the key `research_outline`.

The decomposition prompt instructs Edward to produce an outline with:
- 5–12 sections (depending on topic depth)
- 2–4 key points per section
- Source citations for every factual claim
- Suggested word count per section (total target: 5,000–15,000 words for a guide)

**Stage 2: Content Production (Faye, content mode)**

Faye receives Edward's research via the handoff protocol (Phase 2). Her system prompt is configured for long-form content writing with these constraints:
- Write in the specified tone (professional, conversational, academic — set in mission parameters)
- Each section must be self-contained but flow naturally into the next
- Include actionable takeaways (not just information, but "here's what to do with it")
- Maintain consistent voice across all sections
- Target reading level: 8th grade (Flesch-Kincaid) unless specified otherwise

Faye writes one section per step. Each section step receives:
1. The full outline (from workspace key `research_outline`)
2. Edward's research for that specific section (from the corresponding research step result)
3. Previously written sections (from workspace, for voice consistency)

Self-critique for content steps evaluates:
- Completeness: Does this section cover everything in the outline?
- Readability: Is the language clear and accessible?
- Actionability: Does the reader know what to do after reading this?
- Tone consistency: Does this match the voice of previous sections?
- Citation integrity: Are claims backed by Edward's research?

Sections scoring below 4.0 on any criterion trigger revision (Phase 2 adaptive depth logic applies).

**Stage 3: Technical Review (Spike, conditional)**

If the mission is flagged as containing technical content (detected during decomposition by keywords: "tutorial," "how-to," "implementation," "code," "technical"), Spike receives the assembled draft and reviews for:
- Factual accuracy of technical claims
- Correctness of any code snippets or command examples
- Logical consistency of technical explanations
- Missing prerequisites or assumed knowledge that should be stated

Spike's output is a structured review: a list of issues with line references, severity (critical, suggestion), and proposed corrections. Critical issues are sent back to Faye for revision. Suggestions are incorporated during final assembly.

**Stage 4: Final Assembly (Frasier, content mode)**

Frasier receives all completed sections from the workspace and assembles them into one coherent document. Assembly includes:

1. **Front matter:** Title page, subtitle, author attribution ("Produced by NERV"), date, version
2. **Table of contents:** Auto-generated from section headers with page estimates
3. **Introduction:** Written by Frasier to frame the document's purpose, audience, and what the reader will learn
4. **Body:** All sections in order, with transition sentences between major sections if needed
5. **Conclusion:** Summary of key takeaways, recommended next steps, call to action
6. **Appendix:** Source list, methodology notes, glossary (if technical terms used)

The assembled document is stored as Markdown in the workspace under key `final_document`. Markdown is the canonical format — conversion to PDF or other formats happens in the delivery step.

**Markdown-to-PDF Conversion:**

The system uses `md-to-pdf` (an npm package wrapping Puppeteer) to convert the final Markdown to a styled PDF. A base CSS template (`src/templates/document.css`) controls:
- Font: Inter for body text, JetBrains Mono for code blocks
- Margins: 1 inch on all sides
- Headers: Styled with consistent sizing hierarchy
- Page breaks: Before each major section
- Footer: Page numbers, document title

The conversion runs as a build step command:
```bash
npx md-to-pdf /home/frasier/builds/{mission_id}/final_document.md \
  --stylesheet /home/frasier/src/templates/document.css
```

Output: a PDF file at `/home/frasier/builds/{mission_id}/final_document.pdf`.

**Stage 5: Listing & Publish Preparation (Vicious, operations mode)**

Vicious receives the assembled document and produces listing copy:
- **Product title:** Concise, benefit-driven (e.g., "The AI Agent Playbook: Build Autonomous Systems That Work")
- **Subtitle:** Expanding on the title's promise
- **Short description:** 1–2 sentences for search results and social sharing
- **Long description:** 300–500 words for the sales page — problem, solution, what's inside, who it's for, social proof hooks
- **Pricing recommendation:** Based on content depth, market research (from Edward's data), and comparable products
- **Tags/categories:** For platform discoverability

This output is stored as structured JSON in the workspace:
```json
{
  "title": "...",
  "subtitle": "...",
  "short_description": "...",
  "long_description": "...",
  "suggested_price": 29,
  "currency": "USD",
  "tags": ["ai", "automation", "agents"],
  "category": "Technology"
}
```

Until Gumroad API integration is built (see Section 6.5), the Discord notification includes:
1. The PDF file (attached if under 25MB, otherwise a file path on the VPS)
2. The listing copy (formatted for easy copy-paste into Gumroad's product creation form)
3. A checklist: "To publish: 1. Go to gumroad.com/products/new, 2. Paste this title, 3. Paste this description, 4. Upload the attached PDF, 5. Set price to $29, 6. Publish."

### 6.3 Build Pipeline (Code Generation)

The build pipeline enables Frasier to produce working software — from simple scripts to multi-file applications with tests and documentation.

**Tool Definitions:**

Spike (and Ein, for testing) interact with the filesystem and shell through a set of tools defined in the LLM call's tool schema. The worker intercepts tool_use responses from the LLM and executes them against the sandboxed build directory.

```javascript
const buildTools = [
  {
    name: 'write_file',
    description: 'Write content to a file. Creates parent directories if needed.',
    input_schema: {
      type: 'object',
      properties: {
        path: { type: 'string', description: 'Relative path from project root' },
        content: { type: 'string', description: 'Full file content' }
      },
      required: ['path', 'content']
    }
  },
  {
    name: 'read_file',
    description: 'Read the contents of a file.',
    input_schema: {
      type: 'object',
      properties: {
        path: { type: 'string', description: 'Relative path from project root' }
      },
      required: ['path']
    }
  },
  {
    name: 'run_command',
    description: 'Execute a shell command in the project directory. Returns stdout, stderr, and exit code.',
    input_schema: {
      type: 'object',
      properties: {
        command: { type: 'string', description: 'Shell command to execute' }
      },
      required: ['command']
    }
  },
  {
    name: 'list_files',
    description: 'List files and directories. Returns an array of paths.',
    input_schema: {
      type: 'object',
      properties: {
        path: { type: 'string', description: 'Directory path relative to project root. Defaults to "."' }
      }
    }
  }
];
```

**Execution Flow:**

1. **Spec Creation (Frasier):** Frasier decomposes the build mission into a technical specification: project type (Node.js API, Python script, static site, etc.), file structure, database schema if applicable, API endpoints or CLI commands, and acceptance criteria. This spec is stored in the workspace.

2. **Directory Setup (Worker):** The worker creates a sandboxed project directory at `/home/frasier/builds/{mission_id}/`. It initializes a Git repository in this directory (`git init`) for version tracking.

3. **Scaffolding (Spike, Step 1):** Spike receives the spec and produces the initial project structure. The LLM responds with a sequence of `write_file` tool calls to create `package.json`, directory structure, config files, and stub implementations. The worker executes each tool call sequentially, collecting results.

4. **Implementation (Spike, Steps 2–N):** Each subsequent step implements one component of the spec (e.g., one API endpoint, one database model, one utility module). Spike receives the spec, the current file listing, and the content of relevant existing files. The LLM responds with `write_file` and `run_command` calls. After each implementation step, the worker runs `npm test` (or equivalent) and passes the output back to the LLM.

5. **Test-Fix Loop (Spike):** If tests fail, the worker sends the test output back to the LLM as a follow-up message in the same conversation. Spike analyzes the failure, produces corrected `write_file` calls, and the worker re-runs tests. This loop repeats up to 3 times per step. If tests still fail after 3 attempts, the step is marked as `failed` with the last test output stored as the error.

6. **Security Review (Ein):** After all implementation steps complete, Ein receives the full file listing and contents of all source files. Ein's prompt checks for:
   - Hardcoded secrets (API keys, passwords, connection strings)
   - SQL injection vulnerabilities (string concatenation in queries)
   - Path traversal risks (user input in file paths)
   - Missing input validation
   - Insecure dependencies (known CVEs in package.json versions)
   Ein produces a structured report. Critical findings block delivery. Warnings are included in the final output.

7. **Commit & Deliver (Worker):** The worker runs `git add -A && git commit -m "Build complete: {mission_title}"` in the project directory. The Discord notification includes: project path, test results summary, Ein's security report, and instructions for reviewing and deploying the code.

**Conversation Management:**

Each build step is a multi-turn LLM conversation. The initial message contains the spec and context. Each tool result is appended as an assistant/tool response pair. This means a single build step may involve 5–15 LLM calls (tool call → execution → result → next tool call). The worker manages this conversation loop:

```javascript
async function executeBuildStep(step, buildDir) {
  let messages = [
    { role: 'user', content: step.prompt }  // Includes spec, context, instructions
  ];

  for (let turn = 0; turn < 20; turn++) {  // Max 20 tool-use turns per step
    const response = await callLLM(messages, { tools: buildTools });

    if (response.stop_reason === 'end_turn') {
      // LLM is done — extract final text response as step result
      return response.content;
    }

    if (response.stop_reason === 'tool_use') {
      const toolResults = [];
      for (const toolCall of response.tool_use_blocks) {
        const result = await executeToolCall(toolCall, buildDir);
        toolResults.push({ tool_use_id: toolCall.id, content: result });
      }
      messages.push({ role: 'assistant', content: response.content });
      messages.push({ role: 'user', content: toolResults });
    }
  }

  throw new Error('Build step exceeded maximum tool-use turns (20)');
}
```

**Model Selection for Build Mode:**

Code generation requires higher capability than research synthesis. The tiered model system from Phase 2 applies:
- **Scaffolding and simple files:** T1 (Claude Sonnet) — sufficient for boilerplate, config files, and straightforward CRUD
- **Complex implementation:** T2 (Claude Sonnet with extended thinking) — for algorithms, data structures, and non-trivial logic
- **Debugging failed tests:** T2 — analyzing test output and producing targeted fixes requires reasoning
- **Escalation:** If a build step fails 3 times on T2, escalate to T3 (Claude Opus via OpenRouter) for a fresh attempt with maximum capability

The step complexity field (`simple`, `standard`, `deep`) from Phase 2 maps directly: scaffolding steps are `simple` (T1), implementation steps are `standard` (T2), and debugging/escalation steps are `deep` (T3).

### 6.4 Sandboxing

Code execution on the production VPS is the highest-risk capability in the entire system. A malicious or buggy LLM output could delete files, exfiltrate data, or compromise the server. Sandboxing must be defense-in-depth: multiple independent layers, any one of which prevents catastrophic failure.

**Layer 1: Filesystem Isolation**

Every build runs in `/home/frasier/builds/{mission_id}/`. The `executeToolCall` function validates all file paths:

```javascript
function validatePath(requestedPath, buildDir) {
  const resolved = path.resolve(buildDir, requestedPath);
  if (!resolved.startsWith(buildDir)) {
    throw new Error(`Path traversal blocked: ${requestedPath} resolves outside build directory`);
  }
  return resolved;
}
```

The `write_file` and `read_file` tools only operate within the build directory. Any attempt to write to `/home/frasier/.env`, `/etc/passwd`, or `../../src/worker.js` is rejected before execution.

**Layer 2: Command Allowlist**

The `run_command` tool does not execute arbitrary shell commands. It validates against an allowlist of permitted command prefixes:

```javascript
const ALLOWED_COMMANDS = [
  'npm install',
  'npm test',
  'npm run',
  'node ',
  'npx ',
  'python ',
  'pip install',
  'pytest',
  'git init',
  'git add',
  'git commit',
  'ls',
  'cat',
  'mkdir',
  'cp',
  'mv'
];
```

Commands not matching any prefix are rejected. Shell operators (`|`, `&&`, `;`, `$(...)`, backticks) are stripped or cause rejection. Commands are executed with `child_process.execFile` (not `exec`) to prevent shell injection.

**Layer 3: Resource Limits**

Each `run_command` execution has enforced limits:
- **Timeout:** 10 minutes per command (kills the child process via SIGTERM, then SIGKILL after 5 seconds)
- **Disk:** Build directory has a 500MB quota (checked before each `write_file` call: sum total file sizes, reject if limit exceeded)
- **Memory:** Commands run with `ulimit` constraints where supported
- **No network:** Commands execute with `NODE_OPTIONS=--dns-result-order=ipv4first` and the build user has no outbound network rules (configured via iptables for the `frasier-build` system user, or via Docker in a future hardening pass)

**Layer 4: Credential Isolation**

Build commands execute as a separate system user (`frasier-build`) with no access to:
- `/home/frasier/.env` (Frasier's credentials)
- `/home/frasier/src/` (Frasier's codebase)
- `/home/frasier/.ssh/` (SSH keys)
- Any directory outside `/home/frasier/builds/`

The worker process (running as the `frasier` user) creates the build directory, chowns it to `frasier-build`, and then executes commands via `sudo -u frasier-build` with the build directory as the working directory.

**Layer 5: Output Sanitization**

Command output (stdout + stderr) is captured and truncated to 50KB before being sent back to the LLM. This prevents the LLM from receiving sensitive information that might leak into step results or Discord messages. The truncation also controls token consumption — a runaway `npm install` that dumps thousands of lines of output won't blow the context window.

### 6.5 Deployment Pipeline

**Stage 1 (v1.0): Manual Deploy**

Build mode produces a self-contained project directory with:
- All source code, properly structured
- `package.json` with dependencies and scripts
- Passing test suite
- `README.md` with setup and deployment instructions (generated by Frasier during assembly)
- Ein's security review report

The Discord notification provides everything Dhroov needs to deploy:
```
Build complete for Mission #91: "Subscriber Tracking API"
Repository: /home/frasier/builds/91/

Test results: 14/14 passing
Security review: 0 critical, 1 warning (no rate limiting on POST endpoints)
Files: 12 source files, 8 test files, 1 migration

To deploy:
1. SSH into VPS: ssh frasier@{ip}
2. cd /home/frasier/builds/91
3. cp .env.example .env && nano .env  (fill in database URL)
4. npm install --production
5. node src/index.js

Or: ask Claude Code to review and deploy.
```

No automated deployment in v1.0. Every build requires human review before going live. This is a deliberate safety constraint — until the build pipeline has proven reliable over dozens of missions, no code should reach production without Dhroov's (or Claude Code's) explicit approval.

**Stage 2 (Post-v1.0): Assisted Deploy**

After the build pipeline has demonstrated reliability (20+ successful builds with passing tests and clean security reviews), add optional deployment targets:
- DigitalOcean App Platform (for Node.js APIs)
- Vercel (for static sites and Next.js apps)
- Railway (for quick deploys with database provisioning)

The system deploys to a staging URL, posts it in Discord for review, and waits for explicit approval before promoting to production. This is documented here for future reference but is explicitly out of scope for v1.0.

### 6.6 Operations Pipeline

Operations mode enables Frasier to interact with external services on Dhroov's behalf — publishing products, creating documents, and managing platforms.

**MVP Integrations (v1.0):**

| Service | Capability | API | Auth |
|---------|-----------|-----|------|
| Gumroad | Create product listing, upload file, set price | Gumroad API v2 | OAuth token in .env |
| Google Docs | Create document, write content, share | Google Docs API | Service account JSON in .env |
| Notion | Create page, update content | Notion API | Integration token in .env |

Each integration lives in its own module under `src/lib/integrations/`:

```
src/lib/integrations/
├── gumroad.js       // createProduct, uploadFile, updateProduct
├── google-docs.js   // createDocument, writeContent, shareDocument
├── notion.js        // createPage, updatePage
└── index.js         // Registry: maps action types to handler functions
```

**Agent-to-Integration Pattern:**

Agents never call external APIs directly. An agent in operations mode produces a structured action request:

```json
{
  "action": "gumroad.createProduct",
  "params": {
    "name": "The AI Agent Playbook",
    "description": "...",
    "price": 2900,
    "currency": "usd",
    "tags": ["ai", "automation"]
  },
  "files": [
    { "workspace_key": "final_document_pdf", "filename": "ai-agent-playbook.pdf" }
  ]
}
```

The worker receives this action request as the step result, parses it, and executes it through the integration module. This separation provides:

1. **Security:** The LLM never sees API credentials. Credentials are only loaded by the integration module at execution time.
2. **Validation:** The worker validates the action request schema before executing. Missing required fields, invalid action types, or unexpected parameters are caught before any API call.
3. **Retry and error handling:** The integration module handles retries, rate limits, and error responses according to the standard patterns from Phase 1 (retry once after 5 seconds, circuit breaker on repeated failures).
4. **Audit trail:** Every integration call is logged with the full request (minus credentials), response, and timestamp. Stored in a `integration_log` table for debugging and cost tracking.

**Gumroad Integration Detail:**

The Gumroad integration is the highest-priority operations capability because it directly enables revenue.

```javascript
// src/lib/integrations/gumroad.js
class GumroadClient {
  constructor() {
    this.accessToken = process.env.GUMROAD_ACCESS_TOKEN;
    this.baseUrl = 'https://api.gumroad.com/v2';
  }

  async createProduct({ name, description, price, currency, tags }) {
    const response = await fetch(`${this.baseUrl}/products`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        access_token: this.accessToken,
        name,
        description,
        price,                    // In cents
        currency: currency || 'usd',
        tags: tags || []
      })
    });
    // Error handling, retry logic, response parsing...
    return { product_id: data.product.id, url: data.product.short_url };
  }

  async uploadFile(productId, filePath, fileName) {
    // Multipart upload to Gumroad's file endpoint
    // ...
  }
}
```

The full Gumroad flow for a content mission:
1. Content pipeline produces PDF at `/home/frasier/builds/{mission_id}/final_document.pdf`
2. Vicious produces listing copy (title, description, price, tags)
3. Operations step creates the product via `gumroad.createProduct`
4. If product creation succeeds, uploads the PDF via `gumroad.uploadFile`
5. Posts the product URL to Discord: "Product listed: https://dhroov.gumroad.com/l/ai-agent-playbook — Price: $29. Review and publish when ready."

Note: Gumroad products are created in draft state by default. Dhroov must manually publish after reviewing. This is another deliberate safety valve — no product goes live without human approval.

---

## 7. Infrastructure, Costs & Risks

### 7.1 Infrastructure Requirements

**Current State:**

| Component | Specification | Monthly Cost |
|-----------|--------------|-------------|
| VPS | DigitalOcean Basic Droplet, 1 vCPU, 1GB RAM, 25GB SSD | $8.00 |
| Database | Supabase free tier, 500MB storage, 60 connections via pooler | $0.00 |
| LLM | OpenRouter, Claude 3.5 Sonnet, pay-per-token | $25–$110 (usage-dependent) |
| Search | Brave Search API free tier, 200 queries/month | $0.00 |
| Discord Bot | Discord.js, bot hosted on VPS, no API cost | $0.00 |
| Domain/DNS | None currently | $0.00 |
| **Total** | | **$33–$118/month** |

**Required for v1.0:**

| Component | Specification | Monthly Cost | Change Reason |
|-----------|--------------|-------------|---------------|
| VPS | DigitalOcean Basic Droplet, 1 vCPU, 2GB RAM, 50GB SSD | $12.00 | Parallel workers (Phase 3) require additional memory. Build pipeline (Phase 4) requires additional disk for project directories. |
| Database | Supabase free tier, 500MB storage | $0.00 | No change. New tables (7 total) add minimal storage overhead. Even with revision history, 500MB is sufficient for 12+ months of operation at projected mission volume. |
| LLM | OpenRouter, Claude Sonnet (T1) + Sonnet Extended Thinking (T2) + Opus (T3) | $50–$200 | Build mode generates 5–15x more LLM calls per mission. Extended thinking and Opus escalation cost 2–5x more per call than Sonnet. Estimated: 60% T1, 30% T2, 10% T3 by call volume. |
| Search | Brave Search API free tier, 200 queries/month | $0.00 | Centralized budget tracker (Phase 3) prevents overuse. If consistently hitting limits, upgrade to Pro tier ($5/month for 2,000 queries) is available but not required at launch. |
| Git | GitHub free tier, private repositories | $0.00 | Build pipeline stores project repos. Free tier supports unlimited private repos. |
| Gumroad | Gumroad free tier, 10% transaction fee | $0.00 base | No monthly cost. Gumroad takes 10% of each sale. This is the revenue engine — the fee is acceptable. |
| **Total** | | **$62–$212/month** |

**Net increase: $29–$94/month.** The only guaranteed fixed cost increase is the VPS upgrade ($4/month). All other increases are proportional to usage — more missions, more LLM spend.

### 7.2 Cost Controls

Uncontrolled LLM spending is the primary financial risk. Build mode, extended thinking, and Opus escalation can each multiply costs by 3–5x. Three layers of cost control prevent runaway spending.

**Layer 1: Per-Mission Cost Cap**

Every mission has a `cost_cap` field set during decomposition. Default caps by mode:

| Mode | Default Cap | Rationale |
|------|------------|-----------|
| Research | $2.00 | Typical research mission: 5–8 steps × 1–2 LLM calls × $0.01–0.05 per call |
| Content | $5.00 | More steps, more revision cycles, larger prompts |
| Build | $10.00 | Iterative code generation, test-fix loops, multi-turn conversations |
| Operations | $1.00 | Few LLM calls, primarily structured output |

Dhroov can override the default cap when issuing a mission: "Build a subscriber API, budget $15."

**Tracking mechanism:** The `model_usage` table (already exists) stores `input_tokens`, `output_tokens`, `model`, and `cost_usd` for every LLM call. After each call, the worker sums `cost_usd` for the current mission. If total exceeds 80% of cap, the worker downgrades all remaining steps to T1 (cheapest model). If total exceeds 100%, the worker pauses the mission and posts to Discord: "Mission #91 has reached its $10.00 cost cap ($10.23 spent). Reply `!resume 91` to add $5.00 budget, or `!cancel 91` to stop."

**Layer 2: Monthly Cost Cap**

A global monthly cap (default: $200/month, configurable in .env as `MONTHLY_COST_CAP`) prevents aggregate overspend across all missions.

The heartbeat process checks total monthly LLM spend once per hour:

```sql
SELECT SUM(cost_usd) as total
FROM model_usage
WHERE created_at >= DATE_TRUNC('month', NOW());
```

| Threshold | Action |
|-----------|--------|
| 80% ($160) | Discord warning: "Monthly LLM budget at 80%. Switching to T1-only mode for remaining missions." All new steps default to T1 regardless of complexity. |
| 95% ($190) | Discord alert: "Monthly budget nearly exhausted. Only critical missions will proceed." Pause all missions except those flagged as `priority: critical`. |
| 100% ($200) | Hard stop. All missions paused. Discord: "Monthly budget exceeded. All work paused until next month or budget increase. Reply `!budget 300` to increase." |

**Layer 3: Research Budget**

Detailed in Section 5.3. The `research_budget` table tracks Brave Search usage. At 80% utilization, research steps degrade gracefully to LLM-only synthesis. This prevents a research-heavy month from burning through the search quota in the first week.

**Cost Visibility:**

Every mission completion Discord message includes a cost breakdown:
```
Mission #91 complete: "Market Research: AI Newsletter Monetization"
Cost: $1.47 / $2.00 cap
  - LLM calls: 12 (8 × Sonnet $0.72, 3 × Extended $0.61, 1 × Opus $0.14)
  - Search queries: 8 / 200 monthly
  - Duration: 14 minutes
Monthly total: $47.23 / $200.00 cap
```

This gives Dhroov full transparency into what each mission costs and how the monthly budget is tracking.

### 7.3 Database Schema Changes

**New Tables:**

```sql
-- 007_reliability.sql
CREATE TABLE step_revisions (
  id SERIAL PRIMARY KEY,
  step_id INTEGER NOT NULL REFERENCES mission_steps(id) ON DELETE CASCADE,
  revision_number INTEGER NOT NULL DEFAULT 1,
  result TEXT,
  critique_score DECIMAL(3,1),
  critique_feedback TEXT,
  revised_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(step_id, revision_number)
);

CREATE TABLE pending_notifications (
  id SERIAL PRIMARY KEY,
  channel_id TEXT NOT NULL,
  message TEXT NOT NULL,
  embed_data JSONB,
  retry_count INTEGER NOT NULL DEFAULT 0,
  max_retries INTEGER NOT NULL DEFAULT 3,
  next_retry_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  delivered_at TIMESTAMPTZ
);

CREATE TABLE circuit_breaker_state (
  api_name TEXT PRIMARY KEY,                    -- 'openrouter', 'brave_search', 'supabase', 'discord', 'gumroad'
  state TEXT NOT NULL DEFAULT 'closed'
    CHECK (state IN ('closed', 'open', 'half_open')),
  consecutive_failures INTEGER NOT NULL DEFAULT 0,
  last_failure_at TIMESTAMPTZ,
  last_failure_reason TEXT,
  reopens_at TIMESTAMPTZ,                       -- When to transition from open → half_open
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 008_workspace.sql
CREATE TABLE project_workspace (
  id SERIAL PRIMARY KEY,
  mission_id INTEGER NOT NULL REFERENCES ops_missions(id) ON DELETE CASCADE,
  section_key TEXT NOT NULL,                    -- e.g., 'research_outline', 'section_3', 'final_document'
  agent_id TEXT NOT NULL,                       -- Which agent wrote this
  content TEXT NOT NULL,
  version INTEGER NOT NULL DEFAULT 1,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(mission_id, section_key, version)
);

CREATE INDEX idx_workspace_mission ON project_workspace(mission_id);
CREATE INDEX idx_workspace_lookup ON project_workspace(mission_id, section_key);

-- 009_parallel.sql
CREATE TABLE research_budget (
  id SERIAL PRIMARY KEY,
  month TEXT NOT NULL UNIQUE,                   -- '2026-03'
  queries_used INTEGER NOT NULL DEFAULT 0,
  queries_limit INTEGER NOT NULL DEFAULT 200,
  fetches_used INTEGER NOT NULL DEFAULT 0,
  fetches_limit INTEGER NOT NULL DEFAULT 2000,
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 010_build_pipeline.sql
CREATE TABLE integration_log (
  id SERIAL PRIMARY KEY,
  mission_id INTEGER REFERENCES ops_missions(id),
  step_id INTEGER REFERENCES mission_steps(id),
  service TEXT NOT NULL,                        -- 'gumroad', 'google_docs', 'notion'
  action TEXT NOT NULL,                         -- 'createProduct', 'uploadFile', etc.
  request_params JSONB,                         -- Full request (credentials stripped)
  response_data JSONB,                          -- Full response
  status TEXT NOT NULL DEFAULT 'pending'
    CHECK (status IN ('pending', 'success', 'failed', 'retried')),
  error_message TEXT,
  duration_ms INTEGER,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_integration_log_mission ON integration_log(mission_id);
CREATE INDEX idx_integration_log_service ON integration_log(service, created_at);
```

**Schema Changes to Existing Tables:**

```sql
-- mission_steps modifications
ALTER TABLE mission_steps ADD COLUMN claimed_by TEXT DEFAULT NULL;
ALTER TABLE mission_steps ADD COLUMN started_at TIMESTAMPTZ DEFAULT NULL;
ALTER TABLE mission_steps ADD COLUMN complexity TEXT DEFAULT 'standard'
  CHECK (complexity IN ('simple', 'standard', 'deep'));
ALTER TABLE mission_steps ADD COLUMN escalated_at TIMESTAMPTZ DEFAULT NULL;
ALTER TABLE mission_steps ADD COLUMN revision_count INTEGER DEFAULT 0;
ALTER TABLE mission_steps ADD COLUMN timeout_seconds INTEGER DEFAULT 600;

CREATE INDEX idx_mission_steps_status_mission ON mission_steps(status, mission_id);
CREATE INDEX idx_mission_steps_claimed ON mission_steps(claimed_by) WHERE claimed_by IS NOT NULL;

-- ops_missions modifications
ALTER TABLE ops_missions ADD COLUMN mode TEXT NOT NULL DEFAULT 'research'
  CHECK (mode IN ('research', 'content', 'build', 'operations'));
ALTER TABLE ops_missions ADD COLUMN cost_cap DECIMAL(10,2) DEFAULT 2.00;
ALTER TABLE ops_missions ADD COLUMN cost_spent DECIMAL(10,2) DEFAULT 0.00;
ALTER TABLE ops_missions ADD COLUMN parent_mission_id INTEGER REFERENCES ops_missions(id);
ALTER TABLE ops_missions ADD COLUMN parallel_groups JSONB;
```

### 7.4 Migration Strategy

All schema changes are purely additive. No existing columns are modified, renamed, or removed. No existing data requires transformation. This guarantees backward compatibility: the current v0.7 codebase continues to function against the v1.0 schema without modification.

**Migration file structure:**

```
src/migrations/
├── 001_initial.sql           (existing)
├── 002_agents.sql            (existing)
├── 003_missions.sql          (existing)
├── 004_steps.sql             (existing)
├── 005_model_usage.sql       (existing)
├── 006_deep_work.sql         (existing)
├── 007_reliability.sql       (new: step_revisions, pending_notifications, circuit_breaker_state)
├── 008_workspace.sql         (new: project_workspace)
├── 009_parallel.sql          (new: research_budget, mission_steps modifications)
├── 010_build_pipeline.sql    (new: integration_log, ops_missions modifications)
```

Each migration is idempotent — uses `IF NOT EXISTS` for table creation and `ADD COLUMN IF NOT EXISTS` for alterations. Migrations run in order on startup via the existing migration runner. Rollback is not automated; if a migration fails, the system logs the error and refuses to start (forcing manual investigation rather than running on an inconsistent schema).

**Deployment order:**

Migrations align with phase rollout. Migration 007 deploys with Phase 1, 008 with Phase 2, 009 with Phase 3, and 010 with Phase 4. Each migration can be deployed independently — no migration depends on a later one.

### 7.5 Risk Assessment

**Critical Risks (must mitigate before deployment):**

| Risk | Description | Likelihood | Impact | Mitigation |
|------|-------------|-----------|--------|------------|
| Build pipeline code execution compromises VPS | A malicious or hallucinated LLM output executes destructive commands on the production server | Medium | Critical | Five-layer sandboxing (Section 6.4): filesystem isolation, command allowlist, resource limits, credential isolation, output sanitization. No auto-deploy. Manual review required for all builds. |
| Parallel workers corrupt shared state | Two workers modify the same mission or step simultaneously, producing inconsistent data | Medium | High | Atomic claim via `UPDATE ... WHERE` with `FOR UPDATE SKIP LOCKED`. No shared in-memory state. All coordination through database. Integration tests specifically covering race conditions. |
| LLM costs exceed budget | Build mode, extended thinking, and Opus escalation generate unexpectedly high costs | Medium | Medium | Three-layer cost control (Section 7.2): per-mission cap, monthly cap, T1 fallback mode. Cost visibility in every Discord notification. Hard stop at 100% monthly cap. |

**High Risks (must monitor actively):**

| Risk | Description | Likelihood | Impact | Mitigation |
|------|-------------|-----------|--------|------------|
| Build pipeline produces insecure code | Generated code contains vulnerabilities (SQL injection, hardcoded secrets, XSS) | High | High | Ein's security review catches common patterns. No auto-deploy in v1.0. All builds require human review. Known limitation: Ein's review is LLM-based and not a substitute for a security audit on production-critical code. |
| Brave Search free tier exhausted | 200 queries/month is consumed by first week of parallel research missions | High | Medium | Centralized budget tracker with atomic increment. 80% warning threshold. Graceful degradation to LLM-only synthesis with honest confidence labeling. Upgrade path: $5/month for 2,000 queries. |
| VPS OOM with parallel workers | Two workers processing simultaneously plus Discord bot exceeds 1GB RAM | Medium | High | PM2 `max_memory_restart: 200M` per worker. Upgrade to 2GB VPS ($12/month) before enabling second worker. Memory monitoring via PM2 metrics. |
| Extended thinking tokens inflate costs | T2 model produces excessive reasoning tokens that are billed but not visible in output | Medium | Medium | Monitor `thinking_tokens` in model_usage. Set `max_tokens` on thinking budget. If thinking costs exceed 40% of total call cost, flag for review. |

**Medium Risks (acceptable with monitoring):**

| Risk | Description | Likelihood | Impact | Mitigation |
|------|-------------|-----------|--------|------------|
| Supabase connection exhaustion | Parallel workers + bot + heartbeat exceed 60-connection pooler limit | Low | High | Connection pooling with max 5 connections per process. Current total: 15 connections (25% of limit). Monitored by heartbeat. |
| Gumroad API changes or rate limits | Gumroad updates their API, breaking the integration module | Low | Medium | Integration module isolates all Gumroad-specific code. API version pinned. Error handling logs full response for debugging. Manual fallback: Vicious produces listing copy for Dhroov to paste. |
| Compound mission coordination failure | Sub-missions with dependencies fail to pass context correctly, producing incoherent final output | Medium | Medium | Integration tests covering full compound mission lifecycle. Workspace provides shared state between sub-missions. Assembly step explicitly checks for missing sections. |
| Revision loops consume excessive budget | A step repeatedly fails critique, burning through revision attempts and LLM budget | Low | Medium | Hard cap of 3 revisions per step. After 3 failures, accept best result with a quality warning rather than continuing to iterate. Revision costs count against mission cost cap. |

### 7.6 Success Criteria

Each phase has concrete, testable acceptance criteria. A phase is not complete until every criterion passes in a production environment (not just local testing).

**Phase 1: Reliability — "Frasier survives failure gracefully"**

1. A worker process can be killed (`kill -9`) mid-step execution. The heartbeat detects the orphaned step (status `in_progress`, no worker heartbeat) within 60 seconds and marks it `failed`. Dependent steps cascade-fail. The mission produces partial results from completed steps. No manual intervention required.
2. A step that depends on a failed step is marked `blocked` within 1 second of the dependency failing (not on the next 30-second poll cycle). The cascade is triggered by the failing step's completion handler, not by polling.
3. When Brave Search returns an error (simulated by temporarily invalidating the API key), the research step produces an honest synthesis with explicit confidence labeling: "Based on general knowledge (no web sources available)." The output does not contain fabricated citations or hallucinated statistics.
4. A 10-step mission with 2 failed steps (one in Group 1, one in Group 2) delivers a partial result containing output from the 8 successful steps, assembled coherently with notes indicating which sections are missing and why.
5. When Discord is unreachable (simulated by blocking outbound traffic to Discord's API), notifications queue in `pending_notifications` and deliver successfully when connectivity is restored. No notifications are lost.
6. The circuit breaker trips after 5 consecutive failures to a single API, pauses calls for 2 minutes, then allows a single test call (half-open). If the test succeeds, normal operation resumes. If it fails, the breaker stays open for another 2 minutes.
7. An integration test suite of at least 20 tests covers: step failure, cascade failure, partial success assembly, circuit breaker state transitions, notification retry, and orphaned step recovery.

**Phase 2: Pipeline — "Frasier produces professional deliverables"**

1. Agent handoffs include the predecessor step's full result, relevant workspace context, and a structured handoff summary. The receiving agent's output demonstrates awareness of the predecessor's work (references specific findings, builds on prior analysis).
2. The project workspace stores and versions all intermediate artifacts. The assembly step retrieves all sections for a mission and produces a single coherent document with introduction, body sections, and conclusion.
3. Ein's quality review evaluates the assembled deliverable (not individual steps) and produces a structured assessment: coherence score, completeness check (all planned sections present), factual consistency between sections, and tone consistency.
4. A research project comparable in scope to the Phase 1 bakeoff (5+ research steps, 3+ agents involved) completes end-to-end and produces a deliverable that Dhroov rates as "professional quality" — meaning he would be comfortable sharing it externally without significant editing.
5. Adaptive depth correctly routes: a simple factual query completes in 1 step with no critique cycle; a complex analysis goes through 2–3 revision rounds before meeting the 4.0 quality threshold.
6. Model escalation triggers correctly: a step that fails twice on T1 escalates to T2, and a step that fails twice on T2 escalates to T3. The escalation is logged and visible in the mission cost breakdown.

**Phase 3: Parallel Execution — "Frasier does two things at once"**

1. Two worker processes running simultaneously claim different steps from the same mission. Verified by checking `claimed_by` values in the database — no step is ever claimed by two workers.
2. A purpose-built race condition test: 100 iterations of two workers attempting to claim the same step simultaneously. Zero double-claims across all iterations.
3. The research budget table accurately reflects total queries used across both workers. A test mission that would exceed the monthly limit is correctly throttled — the worker skips the search call and uses the honest synthesis fallback.
4. A 7-step mission organized into 3 parallel groups (3 steps, 2 steps, 2 steps) completes in measurably less wall-clock time than the same mission run sequentially. Target: at least 1.5x faster (accounting for the overhead of parallel coordination).
5. PM2 reports stable memory usage for both workers over a 24-hour period with continuous mission processing. No OOM kills, no memory leaks (RSS stays within 50MB of baseline after garbage collection).

**Phase 4: Build & Delivery — "Frasier ships products"**

1. Spike can scaffold a new Node.js project: create `package.json`, install dependencies, write source files, write test files, and run `npm test` with all tests passing. Verified by inspecting the build directory.
2. A simple application (REST API with 3 CRUD endpoints, input validation, and error handling) can be built from a natural-language spec. The resulting code compiles, tests pass, and the API responds correctly to manual curl requests.
3. A digital product (a 5,000+ word guide with 5+ sections) can be produced end-to-end: researched, written, reviewed, assembled into Markdown, converted to PDF, and listing copy generated. The PDF is well-formatted with consistent styling, proper headers, and page numbers.
4. All build pipeline file operations are contained within the sandboxed build directory. A test that attempts path traversal (`../../.env`) is blocked. A test that attempts a disallowed command (`curl`, `wget`, `rm -rf /`) is rejected.
5. Ein's security review catches at least: hardcoded API keys (test: inject `const API_KEY = "sk-..."` into generated code), SQL injection (test: string concatenation in a query), and missing input validation (test: endpoint accepts arbitrary input without sanitization).
6. Integration log captures every external API call with timing, request parameters (credentials stripped), response data, and status. A failed Gumroad API call is retried once after 5 seconds, and the failure is logged with the full error response.

### 7.7 Phase Timeline and Dependencies

| Phase | Scope | Dependencies | Estimated Effort | Priority |
|-------|-------|-------------|-----------------|----------|
| Phase 1: Reliability | Self-healing workers, partial success delivery, circuit breakers, revision history, notification retry queue, integration test suite | None — builds on existing v0.7 architecture | 3–5 days of focused implementation + 1–2 days testing | **First**. All other phases depend on the reliability foundation. |
| Phase 2: Pipeline | Handoff protocol, project workspace, final assembly, Ein quality review, adaptive depth, model escalation, tiered model routing | Phase 1 (revision history, circuit breakers required for safe escalation and retry) | 4–6 days implementation + 2 days testing | **Second**. Enables professional-quality output. |
| Phase 3: Parallel Execution | Multi-worker PM2 config, atomic step claiming, research budget tracker, OpenRouter rate limit handling, connection pooling, VPS upgrade | Phase 1 (self-healing required — parallel workers amplify failure scenarios) | 2–3 days implementation + 1–2 days testing | **Third**. Performance improvement; valuable but not blocking. |
| Phase 4: Build & Delivery | Execution modes, content pipeline (Markdown → PDF), build pipeline (tool-use code generation), sandboxed execution, Ein security review, Gumroad integration, operations mode | Phase 2 (workspace and assembly required for content and build pipelines) | 5–8 days implementation + 2–3 days testing | **Fourth**. Revenue capability; highest long-term value. |

**Total estimated effort: 17–29 days of focused implementation.**

Each phase delivers independently valuable improvements. The system is usable after each phase:
- After Phase 1: Frasier is reliable — missions don't silently fail, partial results are delivered, APIs are protected by circuit breakers.
- After Phase 2: Frasier produces professional deliverables — handoffs work, assembly is coherent, quality is enforced.
- After Phase 3: Frasier is faster — parallel execution reduces wall-clock time for multi-step missions.
- After Phase 4: Frasier generates revenue — builds products, publishes them, and handles external service interactions.

Phases 2 and 3 can be partially parallelized: the workspace system (Phase 2) and the multi-worker system (Phase 3) have no code-level dependencies on each other. However, Phase 3's value is limited without Phase 2's handoff protocol (parallel workers processing steps that don't share context produce fragmented output). The recommended approach is to complete Phase 2 first, then Phase 3, unless VPS performance becomes a blocking issue.

Phase 4 is the largest phase and can be broken into sub-phases if needed:
- 4a: Content pipeline (research → writing → assembly → PDF) — depends on Phase 2
- 4b: Build pipeline (spec → code generation → testing → security review) — depends on Phase 2
- 4c: Operations pipeline (Gumroad, Google Docs, Notion integrations) — independent of 4a/4b

Sub-phases 4a and 4b can be built in parallel. Sub-phase 4c can be built at any time after Phase 1, as it only requires the integration module pattern and does not depend on the workspace or assembly systems.
