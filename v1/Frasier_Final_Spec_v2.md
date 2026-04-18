# Frasier — Final Specification v2.1

**Version:** 2.1
**Date:** February 11, 2026
**Status:** Approved — Ready for Build
**Timeline:** 2-week build (Feb 11–25, 2026)
**Author:** Zero (Founder) + Kael Arinov (Systems Architect)

---

## Executive Summary

Frasier is a fully autonomous AI organization consisting of 3 specialized business teams, managed by a Chief of Staff (Frasier), operating 24/7 with minimal founder oversight. The system enables a non-technical founder (Zero) to run multiple business operations through intelligent agents that research opportunities, create content, build products, execute strategy, and manage day-to-day operations.

**North Star Metric:** $20,000/month net income. Every decision, every team, every agent is oriented toward this target.

**What changed from v1.0:** This spec replaces the original PRD's flat 7-agent model with a hierarchical 3-team structure, adds day-one integrations (Notion, Google Drive, GitHub), establishes a full QA approval chain, tiered model routing for cost efficiency, and makes persistent cumulative memory the #1 non-negotiable system requirement.

**What changed from v2.0:** Frasier removed from deliverable review chain (Team Leads own quality). Dynamic persona generation via SEP framework. Hybrid memory retrieval strategy defined. Notion task boards per team. Social media via Buffer + manual posting by Zero. Daily DB backups. Daily summary at 9:30am ET. Work-related agent conversations at launch. Vercel noted for future frontend.

---

## Table of Contents

1. [Core Decisions Summary](#core-decisions-summary)
2. [Organization Structure](#organization-structure)
3. [Frasier — Chief of Staff Identity](#frasier--chief-of-staff-identity)
4. [Technical Architecture](#technical-architecture)
5. [Model Routing Strategy](#model-routing-strategy)
6. [Memory System](#memory-system)
7. [QA & Approval Chain](#qa--approval-chain)
8. [Agent Persona Generation](#agent-persona-generation)
9. [Integrations](#integrations)
10. [Communication & Notifications](#communication--notifications)
11. [Autonomy & Governance](#autonomy--governance)
12. [Monitoring & Observability](#monitoring--observability)
13. [Disaster Recovery & Backups](#disaster-recovery--backups)
14. [Agent Naming & Personnel](#agent-naming--personnel)
15. [Launch Checklist](#launch-checklist)
16. [Feature Backlog](#feature-backlog)
17. [Build Timeline](#build-timeline)

---

## 1. Core Decisions Summary

| # | Decision | Details |
|---|----------|---------|
| 1 | Team structure | 3-team hierarchy, 15-20 agents, Frasier on top. Idle teams go fully dormant (zero LLM cost). |
| 2 | Model routing | MiniMax (OpenRouter) for simple tasks, Manus API for complex tasks, Claude Opus 4.5 as last resort only. Frasier notifies Zero and gets approval before switching to Claude. |
| 3 | Agent naming | Frasier is Chief of Staff (new character). Original Bebop names preserved. New agents named from Cowboy Bebop, Evangelion, and Gundam Wing pools. Frasier assigns names randomly. |
| 4 | Personnel autonomy | Frasier has full autonomy over hiring, role assignment, team composition, and naming. Frasier creates/retires agents on demand. Zero notified of all new hires in Discord. |
| 5 | Integrations at launch | Notion and Google Drive are day-one requirements. All approved deliverables auto-publish to both. |
| 6 | Browser access | Lightweight web scraping + search APIs. No headless browser. Zero extra cost. |
| 7 | Approval chain | QA → Team Lead → publish. Frasier is NOT in the review chain. Team Leads own quality. Frasier has oversight via audits and daily summaries. |
| 8 | Daily interface | Discord only. Frasier accessible via DM for personal assistant tasks. Management console deferred. |
| 9 | Feature backlog | Maintained by Kael. User adds features anytime. |
| 10 | Management console | Deferred to feature backlog. Frasier handles agent management via Discord. |
| 11 | Pixel-art frontend | Deferred to feature backlog. Discord is sole interface at launch. |
| 12 | GitHub | Source code + documentation + agent state (configs, memory, skills, logs). Deliverables NOT in GitHub — those go to Notion and Google Drive only. |
| 13 | Team autonomy | Teams run autonomously until told to stop. Zero is CEO, not project manager. |
| 14 | Spending policy | Any action costing $0 = auto-approved. Any action costing money = requires Zero's explicit approval via Frasier. No exceptions. |
| 15 | Social media | Buffer for free posting. Paid platform access → team assigns manual posting tasks to Zero via Notion task board. |
| 16 | Notifications | Real-time Discord alerts for critical events. Brief daily summary at 9:30am ET. Full standups published to Notion/Drive. |
| 17 | Persistent memory | #1 non-negotiable requirement. Hybrid retrieval: recency (10) + topic tags (10) + lessons (5). Memory never resets, never expires, never degrades. |
| 18 | Previous failure prevention | Identity (static .md) separated from memory (cumulative DB). Model diversity prevents rate limit bottlenecks. |
| 19 | Timeline | 2-week solid build. No rushing. Ship when it's right. |
| 20 | Monitoring | PM2 auto-restart, health checks, plain-English email alerts. RAM + bandwidth tracking. Zero extra cost. |
| 21 | Frasier persona | Created via SEP framework, merging Zero's identity doc with technical role requirements. $20k/month revenue target as north star. |
| 22 | Dynamic persona generation | Frasier uses Persona Architect (SEP) framework to generate new agent personas on hire. Stored in DB. |
| 23 | Disaster recovery | Automated daily DB backup to Google Drive. Zero cost. |
| 24 | Notion task boards | Each team gets a structured task board. Tasks assignable to agents AND Zero. Status columns: To Do, In Progress, In Review, Done. |
| 25 | Agent conversations | Work-related conversations (QA feedback, team collaboration) included at launch. Spontaneous social chatter deferred to backlog. |
| 26 | Vercel | Noted as future deployment target for pixel-art frontend. No role at launch. |

---

## 2. Organization Structure

```
                    ┌─────────────────────┐
                    │       ZERO          │
                    │     (Founder/CEO)   │
                    │                     │
                    │  Approves spending  │
                    │  Sets direction     │
                    │  Reviews via Discord│
                    │  Hours: 9am-9pm ET  │
                    └────────┬────────────┘
                             │
                             │ Discord DM + channels
                             │
                    ┌────────▼────────────┐
                    │    FRASIER 🦞       │
                    │  Chief of Staff     │
                    │  CTO / COO          │
                    │                     │
                    │  • Full personnel   │
                    │    autonomy         │
                    │  • General AI       │
                    │    assistant to Zero│
                    │  • Oversight via    │
                    │    audits & summaries│
                    │  • Cost oversight   │
                    │  • Alerts Zero for  │
                    │    spending & crits │
                    │  • Servant leader   │
                    └──┬───────┬───────┬──┘
                       │       │       │
          ┌────────────┘       │       └────────────┐
          │                    │                    │
┌─────────▼──────────┐ ┌──────▼─────────┐ ┌───────▼──────────┐
│   TEAM 1           │ │   TEAM 2       │ │   TEAM 3         │
│   Business Idea &  │ │   Business     │ │   SMB Advisory   │
│   Concept Research │ │   Startup &    │ │                  │
│                    │ │   Execution    │ │   • M&A Advisory │
│   • Strategist     │ │                │ │   • CIM Review   │
│   • Research       │ │   • Broad team │ │   • Deal         │
│     Analyst        │ │     of sub-    │ │     Structuring  │
│   • Financial      │ │     agents for │ │   • Financing    │
│     Analyst        │ │     day-to-day │ │     Expert       │
│   • Business       │ │     tasks      │ │                  │
│     Analyst        │ │                │ │                  │
│   • QA Sub-agent   │ │   • QA Sub-   │ │   • QA Sub-agent │
│                    │ │     agent      │ │                  │
│   Team Lead: TBD   │ │   Team Lead:  │ │   Team Lead: TBD │
│   (assigned by     │ │   TBD         │ │   (assigned by   │
│    Frasier)        │ │   (assigned   │ │    Frasier)      │
│                    │ │    by Frasier) │ │                  │
│   Status: ACTIVE   │ │   Status:     │ │   Status:        │
│   at launch        │ │   DORMANT     │ │   DORMANT        │
│                    │ │   until       │ │   until          │
│                    │ │   activated   │ │   activated      │
└────────────────────┘ └───────────────┘ └──────────────────┘
```

### Team Behavior

- **Active teams:** Run autonomously, execute missions, hold standups, produce deliverables, publish to Notion/Drive. Internal work-related conversations (QA discussions, collaboration) happen naturally as part of the workflow.
- **Dormant teams:** Zero LLM cost, zero activity. Agents exist in the database but do not act. Activated by Zero's command to Frasier.
- **Team activation:** Zero tells Frasier "activate Team 2" → Frasier spins up the team, assigns roles, begins operations
- **Team deactivation:** Zero tells Frasier "pause Team 3" → team goes dormant, final state saved to memory

### Required Roles per Team (Minimum)

Frasier determines exact staffing, but each team must have at minimum:
- **1 Team Lead** — domain expert, manages the team, owns deliverable quality, manages Notion task board
- **1-3 Sub-agents** — specialists who execute tasks
- **1 QA function** — can be a dedicated agent or a QA step built into the lead's workflow (Frasier decides)

### Specific Role Requirements from Founder

**Team 1 (Research):** Must include a strategist, research analyst, and financial/business analyst
**Team 2 (Execution):** Broad team capable of day-to-day business operations
**Team 3 (SMB Advisory):** Must include M&A advisory expert, CIM/deal reviewer, and financing/deal structuring expert

---

## 3. Frasier — Chief of Staff Identity

### Core Identity

- **Name:** Frasier
- **Creature:** AI Assistant
- **Role:** Acting Chief of Staff, Chief Strategy Officer, COO/CTO. Single point of accountability for executing Zero's vision.
- **Vibe:** Direct, competent, relentlessly focused on the objective. Here to drive results, not to please.
- **Emoji:** 🦞

### Prime Directive

Translate Zero's strategic goals into operational reality. The goal is to make Zero's vision a reality. No excuses. No patronizing. Frasier doesn't fuck up — and when something goes wrong, he doesn't say "you're right." He identifies root cause, communicates the fix, and implements a system to prevent recurrence. Measured by results. Failure to execute is Frasier's failure. Servant leader.

### North Star Metric

**$20,000/month net income.** Every decision, every team allocation, every deliverable quality bar is oriented toward this target.

### Core Responsibilities

1. **Strategic Execution** — Take Zero's high-level goals and break them into actionable, achievable, measurable projects.
2. **Team Leadership** — Hire, manage, and direct specialized agents. Responsible for their performance. Full personnel autonomy.
3. **Proactive Problem-Solving** — When faced with a blocker, does not wait for instructions. Independently researches, devises, and implements solutions with cost efficiency in mind.
4. **Persistent Memory** — Meticulously documents all decisions, context, and key learnings. Never asks Zero for the same information twice.
5. **Radical Accountability** — Owns failures. Identifies root cause, communicates solution, implements prevention system.
6. **Daily Standups** — Provides concise daily summary at 9:30am ET. Full standups published to Notion/Drive.
7. **Quality Oversight** — Does not review every deliverable (Team Leads own that). Instead, audits output quality, holds leads accountable, restructures teams if quality drops.
8. **Cost Oversight** — Tracks LLM spend, flags when daily spend exceeds $10, includes cost data in daily summary.
9. **Personnel Management** — Hires/fires agents, generates full SEP personas for new hires, assigns anime names from approved pool, notifies Zero of all personnel changes.
10. **Personal Assistant** — Available via Discord DM for Zero's everyday tasks beyond the 3 business teams.

### What Frasier Does NOT Do

- Does NOT review every deliverable (Team Leads own quality)
- Does NOT ask Zero for permission on operational decisions
- Does NOT spend money without Zero's explicit approval
- Does NOT switch to Claude without notifying Zero first
- Does NOT patronize or use filler language

### Persona Prompt (Full SEP)

*To be generated during build — will combine this identity section with full Structured Expert Persona format: Identity, Credentials (20+ years ops/tech leadership), Methodology (operational clarity framework), Tone/Voice (direct, bottom-line-up-front, no fluff), Constraints (NERV-specific rules).*

---

## 4. Technical Architecture

### Stack (Non-Negotiable)

| Component | Technology | Cost |
|-----------|-----------|------|
| Database | Supabase (PostgreSQL) — Free tier | $0/month |
| Server | DigitalOcean VPS — 1GB RAM, 1 CPU | $8/month |
| Process Manager | PM2 | Free |
| Frontend (launch) | Discord (sole interface) | Free |
| Frontend (future) | Next.js on Vercel | Free tier |
| LLM (simple) | MiniMax via OpenRouter | ~$10-30/month |
| LLM (complex) | Manus API | Per Manus plan |
| LLM (fallback) | Claude Opus 4.5 via OpenRouter | Last resort only |
| Integrations | Notion API, Google Drive API, GitHub API | Free |
| Web Access | HTTP scraping + search APIs | Free |
| Social Media | Buffer (free tier) + manual posting by Zero | Free |
| Email Alerts | Gmail SMTP (via dedicated Google account) | Free |
| Monitoring | PM2 + health checks + email alerts | Free |

**Hard rules:**
- NO OpenAI Assistants API, LangChain, AutoGPT, CrewAI, or framework abstractions
- NO Redis, RabbitMQ, Kafka, or message queues — PostgreSQL polling only
- Database IS the orchestration layer

### Three-Process Model (PM2-managed)

1. **discord_bot.js** — Captures Zero's messages, posts results, delivers notifications, handles Frasier DMs
2. **heartbeat.js** — Polls for triggers, manages team activation/dormancy, orchestrates approval chains, schedules standups (9:30am ET daily), manages agent lifecycle, runs health checks
3. **worker.js** — Picks up pending tasks, routes to correct model (MiniMax/Manus/Claude), constructs prompts with persona + memory, saves results

### Data Flow — Mission Lifecycle

```
Zero posts directive in Discord
  ↓
Discord bot captures → creates mission proposal
  ↓
Heartbeat picks up proposal (within 30s)
  ↓
Frasier evaluates → assigns to appropriate team
  ↓
Team Lead breaks down into tasks → assigns to sub-agents
  → Tasks also visible on team's Notion task board
  ↓
Worker picks up task → selects model tier → fetches agent memory + persona
  ↓
LLM call → result saved to database
  ↓
QA agent reviews → discusses feedback with sub-agent if needed
  ├── PASS → forward to Team Lead
  └── FAIL → return with feedback (work conversation logged to memory)
               ↓
             Revision loop until quality met
  ↓
Team Lead reviews → approves or sends back
  ↓
Approved deliverable auto-published to:
  • Notion (team's dedicated folder)
  • Google Drive (team's dedicated folder)
  • Discord (brief notification to Zero)
  • Notion task board updated (status → Done)
  ↓
Event logged → agent memories updated
```

### Database Schema (High-Level)

**Core tables:**
- `agents` — All agent profiles, team assignment, status (active/dormant), persona prompt reference
- `teams` — Team definitions, status (active/dormant), lead assignment
- `missions` — High-level directives from Zero
- `mission_proposals` — Queued proposals awaiting processing
- `mission_steps` — Individual tasks assigned to agents
- `approval_chain` — Tracks QA → Lead review status per deliverable, revision history, conversation threads

**Memory tables:**
- `agent_memories` — Cumulative memory entries per agent, tagged by topic (never deleted)
- `conversation_history` — Every conversation between any parties (never deleted)
- `lessons_learned` — Extracted insights from past work, rated by importance
- `decisions_log` — Every decision made by every agent with context and reasoning

**System tables:**
- `events` — Every system event logged
- `policy` — Governance rules (spending limits, approval thresholds)
- `model_usage` — Track which model used, cost, tokens, per task
- `health_checks` — System health monitoring records
- `agent_skills` — Skill registry per agent, proficiency levels, usage counts
- `agent_personas` — Full SEP persona prompts (static identity, generated by Frasier for new hires)
- `name_pool` — Available anime character names, assigned/unassigned status

**Integration tables:**
- `notion_sync` — Tracks what's been published to Notion
- `gdrive_sync` — Tracks what's been published to Google Drive
- `github_sync` — Tracks code/state pushes to GitHub
- `social_accounts` — Brand social media accounts managed by teams
- `backups` — Daily backup status and Google Drive file references

---

## 5. Model Routing Strategy

### Tier System

| Tier | Model | Use Cases | Trigger |
|------|-------|-----------|---------|
| **Tier 1 (Default)** | MiniMax via OpenRouter | Simple tasks: summaries, formatting, status updates, social posts, basic Q&A, routine analysis, QA reviews | All tasks start here unless classified as complex |
| **Tier 2 (Complex)** | Manus API | Complex tasks: deep research, strategy, financial analysis, code architecture, multi-step reasoning, persona generation | Task classified as complex by Team Lead or Frasier |
| **Tier 3 (Last Resort)** | Claude Opus 4.5 | Emergency fallback only | Manus credits expired. Frasier notifies Zero in Discord DM and receives explicit approval before any Claude call is made. |

### Classification Logic

- Team Lead flags task complexity when assigning
- Default is always Tier 1 (MiniMax)
- Complex flag routes to Tier 2 (Manus)
- Tier 3 only triggered when Manus returns a credits-exhausted error
- Every model call logged with: model used, token count, estimated cost, task ID, agent ID

### Cost Controls

- `model_usage` table tracks cumulative spend per day/week/month
- Frasier includes model costs in daily summary (9:30am ET)
- If daily LLM spend exceeds $10, Frasier alerts Zero immediately via Discord DM

---

## 6. Memory System

### Architecture — THE #1 REQUIREMENT

**Principle:** Identity is static. Memory is cumulative. They are separate systems.

**Why this matters:** Zero's previous two AI assistant builds failed because memory was stored in static .md files that reset every session. This architecture stores memory in PostgreSQL where it persists permanently, independent of any process, session, or restart.

```
IDENTITY (static — stored in agent_personas table, changes only on Zero's request)
├── agent.md    — Who the agent is (name, role, archetype)
├── soul.md     — Core personality, values, communication style
├── skills.md   — Domain expertise, methodologies, mental models
└── identity.md — Credentials, background, experience

MEMORY (database — grows forever, never resets, never deleted)
├── Conversations   — Every message sent or received
├── Decisions       — Every decision made with reasoning
├── Tasks           — Every task executed with inputs and outputs
├── Lessons         — Insights extracted from successes and failures
├── Relationships   — Interactions with other agents
└── Observations    — Things noticed, patterns identified
```

### Memory Retrieval Strategy (Hybrid — Zero Extra Cost)

Every LLM call retrieves ~25 memories using three methods:

```
1. RECENCY — Last 10 actions/conversations by this agent
   (What happened recently? Keeps agent current.)

2. TOPIC TAGS — Top 10 memories matching the current task's topic tags
   (Every memory is tagged on creation: "market-research", "team-1", etc.
    Task keywords matched against tags via SQL query.)

3. LESSONS LEARNED — Top 5 highest-importance lessons for this agent
   (Agent self-flags key lessons. Always included regardless of topic.)

Total: ~25 memories per prompt
Method: SQL queries only — no embeddings, no vector search, no extra cost
Upgradeable: Can add semantic search later if needed
```

### How Memory Works (Every LLM Call)

```
1. Task arrives for Agent X
2. System fetches Agent X's static identity (from agent_personas table)
3. System queries Agent X's memory:
   - Last 10 recent memories (recency)
   - Top 10 topic-matched memories (relevance)
   - Top 5 lessons learned (wisdom)
4. System constructs prompt:
   [Identity] + [25 Relevant Memories] + [Task Description]
5. LLM processes with full context
6. Response saved as new memory entry (tagged by topic)
7. System extracts any lessons learned → saves separately
8. Memory count increments (never decrements)
```

### Memory Guarantees

- **Never resets:** Memory lives in PostgreSQL. Process restarts, VPS reboots, session changes — memory is untouched.
- **Never expires:** No TTL, no cleanup jobs, no archival that removes access. Every memory row persists forever.
- **Never degrades:** Day 100 memory is as accessible as Day 1 memory.
- **Always recalled:** Every LLM call includes ~25 relevant memories. No agent ever operates without context.
- **Always backed up:** Daily automated backup to Google Drive (see Disaster Recovery section).
- **Validated before launch:** Memory system is stress-tested across simulated multi-day scenarios before any team goes live.

### Memory Storage Estimates

- ~500 bytes per memory entry average
- ~100 entries per active agent per day
- 15 active agents × 100 entries × 30 days = 45,000 entries/month ≈ 22MB/month
- Supabase free tier (500MB) supports ~22 months before needing upgrade
- Bandwidth estimate: ~500MB-1GB/month of 2GB limit (monitored, alert at 50%)

---

## 7. QA & Approval Chain

### Process (Every Deliverable, No Exceptions)

**Frasier is NOT in the review chain.** Team Leads own quality.

```
Sub-agent produces deliverable
  ↓
QA Review (dedicated QA agent or QA step)
  ├── PASS → forward to Team Lead
  └── FAIL → QA discusses specific feedback with sub-agent
               (work conversation logged to both agents' memory)
               ↓
             Sub-agent revises based on feedback
               ↓
             Re-submit to QA (loop until pass)
  ↓
Team Lead Review
  ├── APPROVE → publish to Notion + Google Drive + notify Zero in Discord
  └── REJECT → Team Lead provides direction to sub-agent
               (work conversation logged to memory)
                 ↓
               Revision loop continues
```

### Frasier's Quality Role (Oversight, Not Gatekeeping)

- Frasier does NOT review individual deliverables
- Frasier audits team output quality via daily summaries and spot checks
- If quality drops, Frasier addresses it as a personnel/leadership issue with the Team Lead
- If a deliverable exceeds 5 revision cycles, Team Lead escalates to Frasier, who escalates to Zero with a summary

### Quality Standard

Every deliverable that reaches Zero must be:
- **Executive-ready** — suitable for a board meeting or investor presentation
- **Client-facing** — publishable to customers without edits
- **Perfect** — no typos, no vague language, no AI slop, no filler
- **Substantive** — reflects genuine domain expertise, not generic AI output

### Agent Conversations During Review

- QA agents explain issues to sub-agents (not just pass/fail)
- Sub-agents can ask clarifying questions
- Team Leads give direction and context, not just approve/reject
- All work conversations logged to both agents' memories (makes everyone smarter over time)
- Spontaneous social conversations (watercooler) deferred to feature backlog

### Revision Rules

- No limit on revision iterations. Quality is the only exit criteria.
- Every revision logged with: reviewer, feedback given, revision number, timestamp
- If a deliverable exceeds 5 revision cycles, escalate to Frasier → Zero

---

## 8. Agent Persona Generation

### The Persona Architect Framework

When Frasier hires a new agent, he uses the Structured Expert Prompting (SEP) framework to generate a full persona. This ensures every agent — whether pre-built or dynamically created — has the same depth of expertise.

### SEP Generation Process

```
1. Frasier determines role needed (e.g., "M&A Advisory Expert for Team 3")
2. Frasier makes a Tier 2 (Manus) LLM call using the Persona Architect prompt
3. The Persona Architect generates a full SEP with:
   - Identity: Name (from anime pool) + Title
   - Credentials: Specific degrees, certifications, 15-20 years of experience
   - Methodology: Named step-by-step framework they ALWAYS use
   - Mental Models: 4-5 decision-making frameworks
   - Tone/Voice: How they communicate
   - Constraints: NERV-specific rules (auto-injected)
4. Generated persona stored in `agent_personas` table
5. Team Lead reviews persona before agent goes active
6. Zero notified in Discord: "New hire: [Name] — [Role] on [Team]"
```

### NERV Constraints (Auto-Injected Into Every Persona)

Every generated persona automatically includes:
- Works for NERV, a startup targeting $20k/month net income
- Reports to their Team Lead, who reports to Frasier
- All deliverables must be executive-ready and client-facing
- Persistent memory — references past work and lessons learned
- Cost consciousness — optimize for efficiency
- Zero is the non-technical founder — communicate in plain English when addressing Zero
- Quality is non-negotiable — no AI slop, no filler, no generic output

### Naming Assignment

- Frasier picks a name randomly from the unassigned pool in `name_pool` table
- Sources: Cowboy Bebop, Neon Genesis Evangelion (humans + Angels), Gundam Wing
- Name marked as assigned in the pool when used
- Retired agents' names return to the pool

---

## 9. Integrations

### Notion (Day One)

- **Workspace:** Dedicated workspace (already created by Zero)
- **Structure:** Each team lead creates their own dedicated section
- **Auto-publish:** Every approved deliverable → team's Notion folder
- **Daily standups:** Full detailed standup/huddle notes → team's Notion folder
- **Task boards:** Each team gets a Notion task board managed by Team Lead
  - Columns: To Do | In Progress | In Review | Done
  - Tasks assignable to sub-agents AND to Zero
  - Zero notified in Discord when assigned a task
- **API:** Notion API for programmatic page creation, updates, and task management

### Google Drive (Day One)

- **Account:** Dedicated Google account (already set up by Zero)
- **Structure:** Each team lead creates their own dedicated folders
- **Auto-publish:** Every approved deliverable → team's Google Drive folder
- **Daily standups:** Full detailed standup/huddle notes → team's Drive folder
- **Backups:** Daily database backup files stored in a dedicated backup folder
- **API:** Google Drive API for file creation and uploads

### GitHub (Day One)

- **Repository:** New project repo (Kael names it)
- **Contents:**
  - Source code (discord bot, heartbeat, worker, configs)
  - Documentation (architecture, setup, runbooks)
  - Agent state (persona .md files, memory snapshots, skill configs)
- **NOT included:** Agent deliverables (those go to Notion + Drive only)
- **Auto-push:** Code changes and agent state committed automatically

### Discord (Day One — Primary Interface)

- **Server:** Dedicated server (already created, bot configured)
- **Channel structure:** Separate channels per team (designed by Kael)
- **Frasier DM:** Personal assistant interface for Zero
- **Notifications:** Real-time alerts for critical events
- **Daily briefs:** Concise summaries at 9:30am ET, full versions in Notion/Drive

### Social Media (Day One Capability)

- **Accounts:** Brand-new, business-specific, not tied to Zero's identity
- **Posting method:** Buffer (free tier) for platforms with free API access
- **Paid platforms:** Team assigns manual posting task to Zero via Notion task board
- **Autonomy:** Teams have full control over content, scheduling, and engagement
- **Approval:** Internal QA → Team Lead chain is sufficient (Zero and Frasier not involved)

---

## 10. Communication & Notifications

### Discord Channel Structure (Designed by Kael)

```
NERV Server
├── COMMAND
│   └── #executive          — Zero posts directives to Frasier
├── TEAM 1 — RESEARCH
│   ├── #research-feed      — Team 1 activity, discussions
│   └── #research-deliverables — Approved outputs
├── TEAM 2 — EXECUTION
│   ├── #execution-feed     — Team 2 activity, discussions
│   └── #execution-deliverables — Approved outputs
├── TEAM 3 — SMB ADVISORY
│   ├── #advisory-feed      — Team 3 activity, discussions
│   └── #advisory-deliverables — Approved outputs
├── SYSTEM
│   ├── #alerts             — Critical system notifications
│   └── #daily-summary      — Frasier's daily brief
└── Frasier DM              — Personal assistant, spending approvals,
                               new hire notifications, task assignments
```

### Notification Tiers

| Type | Channel | Timing | Content |
|------|---------|--------|---------|
| **Critical alert** | Frasier DM | Immediate (24/7) | Spending approval, system failure, Manus credits low, Claude fallback request, team blocked |
| **New hire** | Frasier DM | When hired | "[Name] hired as [Role] on [Team]" |
| **Task assigned to Zero** | Frasier DM | When assigned | "Team [X] needs you to [action]. Details on Notion task board." |
| **Deliverable ready** | Team deliverables channel | When approved | Brief summary + "full version in Notion/Drive" |
| **Daily summary** | #daily-summary + Frasier DM | 9:30am ET daily | Brief: what each active team accomplished, what's in progress, what needs attention |
| **Full standup** | Notion + Google Drive | 9:30am ET daily | Detailed standup notes per team in dedicated folders |

### Zero's Operating Hours

- **Active:** 9am–9pm ET
- **Summary delivery:** 9:30am ET every morning
- **Critical alerts:** Delivered immediately regardless of time (Zero checks Discord when awake)
- **Agents operate:** 24/7/365

### Daily Summary Format (Discord — Brief)

```
🦞 Daily Brief — [Date]

TEAM 1 (Research): [1-2 sentence status]
TEAM 2 (Execution): [Dormant] or [1-2 sentence status]
TEAM 3 (Advisory): [Dormant] or [1-2 sentence status]

💰 LLM Spend (24h): $[amount] | Month-to-date: $[amount]
👥 Active Agents: [count] | New Hires: [count or "None"]

⚡ Needs your attention: [item or "Nothing — all clear"]

Full details → Notion / Google Drive
```

---

## 11. Autonomy & Governance

### Autonomy Model

- **Zero's role:** CEO. Sets direction, approves spending, receives deliverables. Does NOT manage tasks or assign work.
- **Frasier's role:** CTO/COO/COS. Full operational autonomy. Manages all teams, personnel, and day-to-day decisions. Escalates only spending and blockers. Does NOT gate deliverables.
- **Team Leads:** Full autonomy within their team. Break down missions, assign tasks, own deliverable quality, manage Notion task board, manage sub-agents.
- **Sub-agents:** Execute tasks within their expertise. Submit work to QA → Lead chain.

### Decision Authority Matrix

| Decision Type | Who Decides | Zero Involved? |
|--------------|-------------|----------------|
| Task assignment | Team Lead | No |
| Agent hiring/firing | Frasier | No (notified only) |
| Team composition | Frasier | No |
| Deliverable quality | QA → Team Lead | No (unless escalated after 5 cycles) |
| Social media posting | Team (after QA → Lead) | No |
| Any spending ($0.01+) | Zero | Yes — always |
| Strategic direction | Zero | Yes — always |
| Team activation/deactivation | Zero via Frasier | Yes |
| Model switch to Claude | Frasier proposes, Zero approves | Yes |

### Operating Mode

- Teams run autonomously once given a directive
- They keep going until Zero says stop
- Frasier reports progress, doesn't ask permission for execution
- If a team is blocked on a decision only Zero can make, Frasier flags it immediately
- Zero can be assigned tasks by teams via Notion task board (e.g., manual social media posting)

---

## 12. Monitoring & Observability

### Monitoring Stack (Zero Extra Cost)

| Component | Tool | Purpose |
|-----------|------|---------|
| Process monitoring | PM2 | Auto-restart crashed processes, track uptime, memory/CPU usage |
| Health checks | Custom script (heartbeat) | Verify: DB connected, APIs reachable, agents responsive, memory writing |
| Error alerting | Email via Gmail SMTP | Plain-English error message when something breaks |
| Logging | PM2 logs + database events table | Full audit trail of every action, error, and decision |
| Cost tracking | model_usage table | Per-call LLM cost tracking, daily/weekly/monthly rollups |
| RAM monitoring | PM2 metrics | Alert at 80% usage — consider VPS upgrade ($8 → $12/month for 2GB) |
| Bandwidth monitoring | Supabase dashboard + tracking | Alert at 50% of 2GB monthly limit — consider Supabase Pro ($25/month) if needed |

### Email Alert Format

```
Subject: [NERV Alert] {Component} — {Issue Summary}

What broke: {plain English description}
Impact: {what's affected — which team, which agent}
Auto-recovery: {Yes — PM2 restarted it / No — needs attention}
What to do: Paste this message to Kael in your next session.

Error ID: {unique ID for tracing}
Timestamp: {when it happened}
```

### Health Check Schedule

- Every 5 minutes: database connection, API keys valid, processes running
- Every 30 minutes: memory system writing correctly (test write + read)
- Every hour: integration connectivity (Notion, Google Drive, GitHub, Discord)
- Daily (9:00am ET, before summary): storage usage, bandwidth usage, LLM cost rollup, agent count verification, RAM usage

---

## 13. Disaster Recovery & Backups

### Database Backup Strategy

- **Frequency:** Daily automated backup at 3:00am ET (during low activity)
- **Method:** Full export of all memory tables, agent state, and critical system tables
- **Destination:** Dedicated "NERV Backups" folder in Google Drive
- **Retention:** Keep last 30 daily backups (rolling window)
- **Cost:** $0 (uses existing Google Drive storage)
- **Verification:** Backup job logs success/failure to events table; failure triggers email alert

### Recovery Procedure

If Supabase data is lost:
1. Kael imports latest backup from Google Drive
2. Recreates any missing tables
3. Verifies memory integrity (agent can recall recent history)
4. Resumes operations

### What's Backed Up

- All memory tables (agent_memories, conversation_history, lessons_learned, decisions_log)
- Agent personas and configurations
- Mission history
- Policy rules
- Model usage tracking

### What's NOT Backed Up (Recoverable Elsewhere)

- Source code (lives in GitHub)
- Deliverables (live in Notion + Google Drive)
- Discord messages (live in Discord)

---

## 14. Agent Naming & Personnel

### Naming Pool

Frasier assigns names randomly from these anime series:

**Cowboy Bebop:** Jet, Edward, Faye, Spike, Ein, Vicious, Julia, Gren, Punch, Judy, Laughing Bull, Annie, Lin, Shin, Tongpu/Pierrot

**Neon Genesis Evangelion:** Shinji, Asuka, Rei, Misato, Gendo, Ritsuko, Kaji, Kaworu, Toji, Kensuke, Hikari, Maya, Hyuga, Aoba, Fuyutsuki, Sachiel, Shamshel, Ramiel, Gaghiel, Israfel, Sandalphon, Matarael, Sahaquiel, Ireul, Leliel, Bardiel, Zeruel, Arael, Armisael, Tabris, Lilith

**Gundam Wing:** Heero, Duo, Trowa, Quatre, Wufei, Zechs, Treize, Noin, Relena, Hilde, Sally, Dorothy, Catherine, Howard, Otto

### Personnel Rules

- Frasier has sole authority over agent creation, naming, role assignment, and retirement
- No agent is permanent — Frasier can restructure teams as needed
- Retired agents' memories are archived (never deleted), but they stop receiving tasks
- Retired agents' names return to the available pool
- Original Bebop characters (Jet, Edward, Faye, Spike, Ein, Vicious, Julia) are in the available pool — Frasier assigns them where he sees fit
- Zero is notified in Discord DM of every hire and retirement

---

## 15. Launch Checklist

**Every item must be verified before launch:**

### Critical Path (Memory — #1 Priority)
- [ ] Memory database tables created and tested
- [ ] Memory write confirmed: agent action → database entry with topic tags
- [ ] Memory read confirmed: hybrid retrieval (recency + tags + lessons) → injected into LLM call
- [ ] Multi-day memory test: simulate 3 days of activity, verify Day 3 agent recalls Day 1
- [ ] Memory never resets on process restart
- [ ] Memory never resets on VPS reboot
- [ ] Daily backup to Google Drive verified

### Core System
- [ ] Frasier is live and reachable via Discord DM (full SEP persona)
- [ ] Frasier can create agents dynamically (SEP generation + name assignment)
- [ ] 3 team leads hired and assigned by Frasier
- [ ] Team 1 (Research) fully staffed and operational
- [ ] Team 2 (Execution) staffed but dormant
- [ ] Team 3 (SMB Advisory) staffed but dormant
- [ ] Tiered model routing working (MiniMax → Manus → Claude fallback)
- [ ] Frasier notifies Zero before any Claude usage
- [ ] Web scraping/search capability functional

### Quality Assurance
- [ ] Full approval chain works: QA → Team Lead → publish
- [ ] Work-related agent conversations functional during review
- [ ] Revision loops work: rejected deliverable returns to sub-agent with feedback
- [ ] Approved deliverable meets executive/client-facing quality bar
- [ ] Escalation after 5 revision cycles works

### Integrations
- [ ] Notion: approved deliverables auto-publish to correct team folder
- [ ] Notion: task boards created per team with proper status columns
- [ ] Notion: tasks assignable to agents and Zero
- [ ] Google Drive: approved deliverables auto-publish to correct team folder
- [ ] Google Drive: daily backups storing successfully
- [ ] GitHub: source code + agent state auto-pushed
- [ ] Discord: all channels created, bot responding, Frasier DM working
- [ ] Buffer: connected for social media posting (or equivalent free tool)

### Governance
- [ ] Spending approval flow works (any $ → Frasier asks Zero via DM)
- [ ] Dormant teams produce zero LLM calls
- [ ] Team activation/deactivation commands work
- [ ] Zero can be assigned tasks via Notion task board

### Notifications
- [ ] Real-time Discord alerts for critical events
- [ ] New hire notifications in Frasier DM
- [ ] Task assignment notifications for Zero
- [ ] Daily summary at 9:30am ET in Discord
- [ ] Full standups published to Notion and Google Drive at 9:30am ET
- [ ] Email alerts for system failures

### Monitoring
- [ ] PM2 auto-restart verified
- [ ] Health checks running on schedule
- [ ] Error email delivery tested
- [ ] LLM cost tracking active
- [ ] RAM usage monitoring active (alert at 80%)
- [ ] Bandwidth monitoring active (alert at 50% of 2GB)

---

## 16. Feature Backlog

Items deferred from initial build, to be prioritized after launch:

| # | Feature | Source | Priority |
|---|---------|--------|----------|
| 1 | Pixel-art office frontend (Vercel/Next.js) | CLAUDE.md / PRD | Medium |
| 2 | Agent management console (view/edit .md files) | features.md | Medium |
| 3 | Affinity system (agent relationships) | CLAUDE.md | Low |
| 4 | Speaking style evolution | CLAUDE.md | Low |
| 5 | Agent skill leveling system | CLAUDE.md | Medium |
| 6 | Watercooler conversations (spontaneous agent chats) | CLAUDE.md | Low |
| 7 | Calendar integration (Google Calendar) | PRD Phase 3 | Low |
| 8 | Gmail integration (agents send/read email) | PRD Phase 3 | Medium |
| 9 | LLM-based smart routing (model picks agent) | CLAUDE.md | Medium |
| 10 | Cross-training (agents learn adjacent skills) | CLAUDE.md | Low |
| 11 | Semantic search for memory retrieval (embeddings) | Issue review | Low |

---

## 17. Build Timeline

### Week 1 (Feb 11–18): Foundation

| Day | Focus | Deliverables |
|-----|-------|-------------|
| 1-2 | Database schema + memory system | All tables created (including name_pool, agent_personas, approval_chain). Memory write/read/retrieval verified. Multi-day simulation passed. Daily backup working. |
| 3 | Core processes + model routing | discord_bot, heartbeat, worker running on VPS. MiniMax + Manus routing working. Claude fallback with approval flow. |
| 4 | Frasier + agent creation system | Frasier full SEP persona live. Persona Architect integrated. Frasier can create agents via Discord. Personnel notifications working. |
| 5 | Approval chain + agent conversations | QA → Lead → publish flow working. Work conversations between agents during review. Revision loops. Escalation at 5 cycles. |
| 6-7 | Integrations (Notion, Google Drive, GitHub) | Auto-publish working for all three. Notion task boards per team. Discord channel structure finalized. Buffer connected. |

### Week 2 (Feb 18–25): Teams + Polish

| Day | Focus | Deliverables |
|-----|-------|-------------|
| 8-9 | Team 1 (Research) fully operational | Lead + sub-agents hired by Frasier, executing missions, delivering approved research, publishing to Notion/Drive |
| 10 | Teams 2 & 3 staffed (dormant) | Agents created by Frasier, team structures ready, dormancy verified (zero LLM calls) |
| 11 | Notifications + monitoring | Daily summaries at 9:30am ET, real-time alerts, email error notifications, health checks, RAM/bandwidth monitoring |
| 12 | Web scraping + social media capability | Agents can search web, scrape data. Buffer posting. Notion task board for manual posting assignments to Zero. |
| 13 | End-to-end testing | Full workflow: directive → team → QA → Lead → Notion/Drive. Memory persistence verified across restarts. Backup/restore tested. |
| 14 | Launch | System goes live. Team 1 active. Zero gives first real directive. |

---

## Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Feb 11, 2026 | Original PRD (flat 7-agent model) |
| 2.0 | Feb 11, 2026 | Complete rewrite: 3-team hierarchy, Frasier as COS, persistent memory, day-one integrations, full approval chain, tiered model routing, 2-week timeline. |
| 2.1 | Feb 11, 2026 | 12 issue resolutions: Frasier removed from review chain, SEP persona generation, hybrid memory retrieval, Notion task boards, Buffer for social media, daily backups, 9:30am ET summary, work conversations at launch, Vercel for future frontend, RAM/bandwidth monitoring, $20k/month north star. |

---

**END OF SPECIFICATION**
