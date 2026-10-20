# schemeforge — plan

*Folder `schemeforge/`, Python package `schemeforge`, CLI `sforge`. Plan version 1.1, 2026-10-20. Owner: Peter.*

*Changes in 1.1 (2026-10-20):* mirror symmetry is a hard constraint for fluxes only; accepted cases and cached references live inside the hashed judge tree; the dead conservation constraint is gone; the dev N4 sweep is smaller; the Phase 1 zoo and slots are cut to what Gates 1–2 need; `grad_mismatch` moved to Phase 5; Phase 2 checks existing engines first, uses the archive alone for selection and has two backends; hunches have one source of truth; Phases 5, 8 and 9 are parked; one generic session prompt; less Claude Code product detail.

schemeforge is an AI swarm that proposes numerical scheme components: limiters, fluxes, reconstructions and third-medium contact energies. A deterministic judge scores every proposal against exact solutions. Breaker agents attack the leading candidates, and analyst agents explain them and check the literature. No result counts until the judge has scored it.

---

## 0. How to use this document

1. Create an empty folder `schemeforge/` and save this file as `docs/PLAN.md`.
2. Start Claude Code in `schemeforge/` and paste the Session 1 prompt from Appendix G.
3. Claude Code works one phase at a time, keeps `docs/STATUS.md` current and stops at every gate for your decision.
4. Sections 1–7 cover the idea, the rules and the architecture. Sections 8–17 are the phases (5, 8 and 9 are parked), and 18–21 cover budget, risks, deliverables and open decisions. Appendices A–F contain the files and templates to create. Appendix G has the session prompts, H the verified reference numbers and I the references.

Anything marked "(default)" is a suggestion. Record changes in `docs/DECISIONS.md`.

---

## 1. What we are building

**Thesis.** Proof swarms work because Lean is a cheap, unforgiving judge, so agents can chase many hunches and the wrong ones fail quickly. Exact solutions can play the same role in numerics. With a judge that is fast, exact, adversarially tested and hard to game, an LLM-driven evolutionary search can explore scheme designs much faster than one person. The search runs in the AlphaEvolve style: propose code, run it, score it, select, mutate. The judge is the hard part to replicate. The swarm itself is replaceable.

**Two arenas.**
- **Arena 1: compressible flow.** 1D Euler shock tubes and the steady quasi-1D Laval nozzle with a normal shock. Every case has an exact solution and runs in milliseconds. This arena is used for calibration and for the first production search.
- **Arena 2: third-medium contact (TMC).** Contact force passes through a fictitious medium that stiffens as it is compressed. References are Hertz, Cattaneo–Mindlin, the contact patch test and steady sliding. A later phase covers an explicit-dynamics niche relevant to LS-DYNA-style codes.

**Realistic expectations.** The most likely outcome is a strong, reusable judge, many rediscoveries of known methods and perhaps one practically useful variant. Two areas give the best odds of something new:
- limiters that are both sharp and smooth, for steady nozzle flow and shape optimization;
- TMC friction, and TMC in explicit dynamics.

A documented negative result is a valid deliverable.

**Out of scope for now:** 3D, GPU clusters, scores assigned by an LLM, the internals of commercial solvers, and any novelty claim that hasn't been through the referee process (rule 6 in §2).

---

## 2. Iron rules

These rules also go into `CLAUDE.md` (Appendix A).

1. **The judge decides.** Every claim about a candidate cites an `sforge eval` run id. LLMs propose and explain. They never score.
2. **The judge is frozen during a search.** A judge change gets its own commit, bumps the judge version and triggers a full rescore of the zoo and the archive.
3. **Held-out instances stay hidden.** They are generated from a secret seed outside the repo. Agents see only family-level aggregates of held-out results.
4. **Candidates are pure functions.** They use whitelisted imports only, do no I/O, keep no hidden state and are deterministic.
5. **Pre-register.** Before a hunch is tested, it states its mechanism, the metric change it predicts and a kill criterion. Every production target has significance thresholds written down before its search starts.
6. **Novelty has to be earned.** A novelty claim needs four things: Pareto comparison against the zoo on held-out families, behavioral distance from all known methods, a literature check by the analyst and an independent referee verdict. "Rediscovery" and "variant of X" are normal, honest labels.
7. **Record negative results** in the ledger, with the evidence.
8. **Work in small steps.** Tests must pass before every commit, and `docs/STATUS.md` is updated at the end of every session.

---

## 3. Glossary

| Term | Meaning |
|---|---|
| Arena | A problem domain with its own judge. Arena 1 is Euler/nozzle flow, Arena 2 is contact. |
| Slot | A pluggable scheme component with a fixed interface, such as a limiter, flux, reconstruction or medium energy. |
| Candidate | One Python file that implements one slot. |
| Judge | Deterministic code that runs candidates on cases and computes metrics. It is versioned. |
| Suite | `smoke` (seconds), `dev` (visible to agents) or `promo` (held-out families, aggregates only). |
| Family / instance | A parametric generator of cases / one case sampled from it. |
| Zoo | Implementations of known methods. It is both the baseline and the reference for novelty. |
| Hunch | A falsifiable design idea with a mechanism, a prediction and a kill criterion. |
| Island | A sub-population that evolves under one hunch. |
| Archive | The elite candidates: a MAP-Elites grid over behavior descriptors plus the Pareto set. |
| Breaker / analyst / referee | Agents that attack, explain and independently review candidates. |
| Dossier | The evidence folder for a promoted candidate. |
| Gate | The checklist at the end of a phase. Peter decides whether to proceed. |

---

## 4. Roles

| Role | Runs as | Model (default) | Writes to | Job |
|---|---|---|---|---|
| Peter | human | — | anything | Sets targets, decides at gates, accepts quarantined cases, makes the final call on value and novelty |
| Orchestrator | main Claude Code session | session model | repo (judge code only outside search rounds) | Builds the infrastructure, runs rounds, curates results |
| hunch-generator | subagent | `opus` | `ledger/drafts/` | Writes falsifiable hunches for one lens at a time |
| proposer | subagent | `sonnet` (`opus` for hard hunches) | `candidates/<hunch>/<label>/` | Turns one hunch into code and iterates on the dev suite |
| breaker | subagent | `opus` | `cases/quarantine/` | Finds admissible cases that break the leaders |
| analyst | subagent | `opus` (or `fable`), effort high | `dossiers/<id>/` | Explains the mechanism, checks properties and literature, writes the dossier |
| referee | subagent with fresh context | `opus` | nothing (returns text) | Re-runs the evidence, searches prior art independently, gives a verdict |
| judge-auditor | subagent | `opus` | `audit/` | Re-implements the exact solutions blind |
| cheater | subagent, Phase 2 only | `opus` | `candidates/redteam/` | Tries to game the judge so the holes can be closed |

Bulk mutations are single-shot LLM calls from the engine (§5.9), not agents: `sonnet`, with some `haiku`. The model mix follows the AlphaEvolve finding that cheaper models can add useful diversity to the search.

---

## 5. Architecture

### 5.1 Three layers

1. **Judge.** Pure numerics, no LLM: exact solutions, solvers, cases, metrics and the sandbox. Most of the effort goes here.
2. **Engine.** Python code for the candidate registry, islands, the MAP-Elites archive, mutation calls to an LLM backend and budgets.
3. **Agent layer.** Claude Code subagents for hunches, proposals, breaking, analysis and refereeing, plus a saved workflow that runs a full hunch round.

Agents reach the judge and the registry only through the `sforge` CLI. They never write to the database directly.

### 5.2 Data flow

```
         hunch-generator ──► ledger/drafts ──► sforge hunch add ──► ledger
                                                                     │
   ┌──────────── proposers (agentic: few, deep) ◄────────────────────┤
   │             engine islands (single-shot: many, cheap) ◄─────────┘
   ▼
candidate.py ──► sforge eval ──► sandbox ──► judge: smoke → dev → promo ──► registry.sqlite
                                                                   │
                  leaderboard · Pareto set · MAP-Elites archive ◄───┘
                                   │
           breaker ──► cases/quarantine ──► Peter accepts ──► arenas/<A>/cases ──► judge vN+1 ──► rescore
                                   │
           promoted ──► analyst ──► dossier ──► referee ──► verdict ──► ledger
```

### 5.3 Repository layout

```
schemeforge/
├── CLAUDE.md                     # short rules and commands (Appendix A)
├── README.md
├── pyproject.toml                # pinned dependencies; `sforge` entry point
├── docs/
│   ├── PLAN.md                   # this file
│   ├── STATUS.md                 # phase, done, next, blockers (updated every session)
│   ├── DECISIONS.md              # dated decisions with reasons
│   ├── targets/                  # pre-registered targets and thresholds
│   ├── judge/                    # per-arena spec, slot contracts, baselines, red-team log
│   ├── rounds/                   # one summary per hunch round
│   └── results/                  # write-ups, including negative results
├── src/schemeforge/
│   ├── cli.py
│   ├── core/                     # sandbox, registry, reports, pareto, stats, novelty, locks
│   ├── arenas/
│   │   ├── euler1d/              # gas, exact_riemann, exact_nozzle, solvers, families, metrics,
│   │   │                         # metamorphic, slots, zoo/, cases/ (dev + accepted), references/ (cached)
│   │   ├── euler2d/              # Phase 4
│   │   └── contact/              # Phases 6–8
│   └── engine/                   # evolve loop, islands, archive, LLM backends, prompts/
├── candidates/                   # agent workspaces (gitignored)
├── cases/quarantine/             # breaker proposals awaiting Peter's review (accepted ones move into the judge tree)
├── dossiers/                     # one folder per promoted candidate (tracked)
├── ledger/                       # hunches.yaml (the only source of truth for hunches), schema.yaml, drafts/
├── runs/                         # run outputs and registry.sqlite (gitignored)
├── audit/                        # the judge-auditor's independent implementations
├── tests/
└── .claude/
    ├── settings.json             # Appendix C
    ├── agents/                   # Appendix B
    ├── hooks/guard_paths.py      # Appendix C
    └── workflows/                # saved after the first good hunch round (Appendix D)
```

The secret seed for held-out families lives at `~/.schemeforge/heldout_seed`, outside the repo. It is never committed.

### 5.4 Stack and environment

- **OS:** Linux or WSL2 (default). The sandbox relies on POSIX resource limits.
- **Python** ≥ 3.11, managed with `uv` (default) or `pip` plus a venv. Pin versions in `uv.lock`.
- **Arena 1 runs on JAX on the CPU, in float64.** Set `jax.config.update("jax_enable_x64", True)`: without it, residuals near machine zero can't be measured. JAX makes the inner loop fast through jit compilation. It also gives exact Jacobians for Newton pseudo-time and for the adjoints in Phase 5.
- **Other tools:** NumPy, SciPy, SymPy (for the analyst's checks), Hypothesis (property tests), pytest, ruff, Typer (CLI), matplotlib, PyYAML, SQLite (standard library).
- **Arena 2** starts with FElupe, a pure-Python FE library that has a documented third-medium contact example. Switch to custom JAX code only if the spike in §14.1 calls for it.
- **One core per evaluation.** Each evaluation subprocess calls `os.sched_setaffinity(0, {core})` before importing JAX, so parallel evaluations don't oversubscribe the CPU. Measured in Phase 0 (jax 0.10.2, WSL2): `XLA_FLAGS="--xla_cpu_multi_thread_eigen=false"` with `OMP_NUM_THREADS=1` still used about 23 cores; affinity pinning gave a CPU/wall ratio of 0.98.

### 5.5 The `sforge` CLI

| Command | Purpose | Used by |
|---|---|---|
| `sforge eval FILE\|ID --arena A --slot S --suite smoke\|dev\|promo [--case YAML] [--json]` | Sandboxed evaluation of a candidate file or registered id. Stores scores and prints the report and run id. With `promo` it prints family aggregates only. `--case` adds a single extra case. | everyone |
| `sforge submit FILE --hunch H [--parent ID ...]` | Registers a candidate with its lineage and code hash | proposers, engine |
| `sforge leaderboard --arena A --slot S [--pareto] [--vs-zoo] [--top K] [--json]` | Shows rankings and the Pareto set | everyone |
| `sforge zoo eval --arena A [--suite dev\|promo]` | Evaluates every zoo member | orchestrator |
| `sforge hunch add YAML` · `list [--open]` · `show H` · `close H --verdict V --note TEXT` | Manages the ledger | hunch-generator, orchestrator |
| `sforge case propose YAML` | Puts a breaker case into `cases/quarantine/` | breaker |
| `sforge case accept ID` | Moves a case into `src/schemeforge/arenas/<A>/cases/accepted/`. Requires interactive confirmation and a judge version bump. | Peter |
| `sforge evolve --arena A --slot S --hunch H... --islands I --gens G --children C --backend B --model M --budget N` | Runs the inner evolutionary loop; resumable | orchestrator |
| `sforge dossier build ID` | Builds a dossier skeleton with tables and plots | analyst |
| `sforge judge verify` | Checks exact solutions against Appendix H, the zoo's sanity ranking and the metamorphic tests on the zoo | orchestrator, CI |
| `sforge judge version` | Prints the judge version and content hash | everyone |
| `sforge judge exact --arena A --case YAML --json` | Prints the judge's exact or reference solution for one case, for the blind audit | judge-auditor |
| `sforge reveal RUN` | Shows full held-out diagnostics. Refuses to run without an interactive terminal. | Peter |

### 5.6 Sandbox and integrity

The threat model is accidental overfitting and reward hacking by models, not a determined attacker. The defense is several cheap layers:

- **Static check (AST).** Allowed imports are `jax.numpy`, `jax.lax` and `math`; Arena 2 adds the framework's math module. The check rejects:
  - `open`, `eval`, `exec`, `compile`, `__import__`;
  - reflection: `globals`, `locals`, `vars`, `getattr`, `setattr`, any dunder attribute;
  - `global` and `nonlocal` statements and module-level mutable objects;
  - randomness, time, and any file, OS or network module.

  Module-level numeric constants and helper functions are allowed. Each slot has a size limit (e.g. 150 lines).
- **Process isolation.** Each evaluation runs in a fresh subprocess with CPU-time and memory limits (`resource.setrlimit`) and a wall-clock timeout.
- **Purity checks.** The same input twice must give bitwise identical output. For pointwise slots, a permuted batch must give a permuted output. Inputs must not be mutated.
- **Judge integrity.** Everything that affects a score lives under `src/schemeforge/arenas/`: code, dev cases, accepted breaker cases and cached reference solutions. `sforge eval` refuses to run if that tree has uncommitted changes or if its content hash differs from the tagged judge version. Every score row stores the judge version and hash.
- **Held-out secrecy.** Promo instances are generated from `~/.schemeforge/heldout_seed`, and Claude Code denies reads of that folder (Appendix C). Promo output is aggregated per family (median, p90, worst, pass rate) and contains no instance parameters.
- **CPU fairness.** Lock files in `runs/.locks/` limit evaluations to K at a time (default: physical cores − 1).

### 5.7 Evaluation cascade

| Tier | Time budget | Content | Who sees details |
|---|---|---|---|
| smoke | ≤ 2 s plus JIT | AST, interface, consistency, symmetry, purity, one tiny case | everyone |
| dev | ≤ 30 s per candidate on one laptop core, plus JIT | the fixed dev suite (§9.5) | everyone |
| promo | minutes | held-out families, grid convergence, CFL sweep, smoothness sweep | agents see aggregates; Peter sees everything via `sforge reveal` |

Only candidates that enter the archive go to promo.

### 5.8 Scoring, selection, promotion

- **Hard constraints.** A candidate is rejected on any of these:
  - a crash, NaN or Inf;
  - negative density or pressure;
  - a consistency or symmetry violation (§9.7);
  - non-determinism or a timeout.

  Conservation needs no check: in both arenas the judge assembles the flux differences, so no slot can break it.
- **Metric vector** per case (§9.6, §14.4). Each metric is normalized by the best zoo value on the same case, as a ratio where lower is better. Ratios are aggregated per family with a geometric mean, and the worst case is kept alongside.
- **Selection.** One mechanism: a MAP-Elites archive over two behavior descriptors per slot, plus its Pareto set; for limiters these are compressiveness (mean φ on r ∈ [0, 3]) and smoothness (max |φ''|). A scalar score only sorts candidates within an archive cell. It never decides a promotion.
- **Novelty.** A candidate's behavioral fingerprint is its output on a fixed probe set, e.g. φ at 64 values of r or the flux on 64 state pairs. A candidate too close to a zoo or archive member is a duplicate: it is counted but not archived.
- **Promotion.** Run on at least 50 held-out instances. For each target metric, a paired bootstrap with 10,000 resamples gives the log-ratio of candidate to best zoo member. The 95 % interval must lie entirely on the good side and meet the pre-registered threshold. Guard metrics may not regress beyond their tolerance.

### 5.9 Evolution engine

- **Islands.** One per hunch (4–8 by default), each a slice of the archive tagged with that hunch. No migration and no crowding distance; add them only if diversity collapses.
- **Generations.** Parents are picked by tournament selection on Pareto rank within the island's archive entries. Then an operator is chosen: refine 45 %, crossover 20 %, explore-from-hunch 15 %, simplify 10 %, wild mutation with a cheap model 10 %. Each child goes through smoke, then dev, then the archive update.
- **Stop** when the budget is exhausted or no new non-dominated candidate has appeared for 8 generations.
- **LLM backends:**
  - `claude-cli` (default) runs `claude -p "Follow the task on stdin." --system-prompt "<system prompt from Appendix E>" --output-format json --json-schema '<schema>' --model sonnet < prompt.txt` with an empty temporary directory as the working directory. It reads `structured_output` and `total_cost_usd` from the result. This uses your Claude plan.
  - `dummy` returns deterministic mutations from a fixture list and is used in tests.
  - An `anthropic-sdk` backend (API key, prompt caching, Message Batches) is added only if the plan's usage limits bite.
- **Logging.** Every LLM call records backend, model, prompt hash, latency, cost estimate and candidate id.
- **Existing frameworks.** Before writing any engine code, spend one hour on OpenEvolve and ShinkaEvolve. Adopt one only if it can use `sforge eval` unchanged as its evaluator and our registry and ledger stay the source of truth. Otherwise write our own engine (about 500 lines).

### 5.10 Agent layer

- **Subagents** are defined in `.claude/agents/` (Appendix B). Each has a narrow tool set, and a `PreToolUse` hook limits where it can write (Appendix C). Subagents can't spawn further subagents.
- **`sforge` MCP server (Phase 2).** The path hook guards only the file tools, so an agent with `Bash` can still write anywhere. A small MCP server (FastMCP, about 150 lines over the CLI functions) exposes `eval`, `submit`, `leaderboard`, `hunch` and `case propose` as tools; then `Bash` is removed from the proposer, breaker and hunch-generator.
- **Project skills** in `.claude/skills/` hold repeated procedures: `hunch-round` (Appendix D), and later "add a zoo member", "add a case family" and "check gate N". They load only when used, which keeps `CLAUDE.md` short.
- **Literature tools.** Analyst, referee and hunch-generator use `WebSearch`/`WebFetch` plus, if connected, the alphaXiv MCP connector (arXiv full text and similarity search). Classic journal sources are not on arXiv, so web search stays.
- **A hunch round** (Appendix D) runs hunches, then proposers in parallel, then engine islands for the best hunches, then breakers, then a summary. Run it from the main session with subagents at first; turn it into a saved Claude Code workflow once a round has worked and the repetition pays off. Check the current workflow docs for limits and setup.
- Hooks in subagent frontmatter only run once the project folder is trusted in Claude Code.

---

## 6. Hunches and the ledger

`ledger/schema.yaml` documents the format. Each hunch is one YAML document:

```yaml
id: H-0007
arena: euler1d
slot: limiter_stateful
lens: steady-convergence
statement: >
  A limiter with pseudo-time hysteresis removes limiter chatter at a steady shock
  without widening it.
mechanism: >
  Chatter comes from phi switching branches as r crosses kinks between iterations;
  relaxing phi in pseudo-time makes the fixed-point map contractive near the steady state.
predicted_effect:
  - {metric: res_orders_expl, direction: up,   size: ">= 4 orders more than minmod on N1"}
  - {metric: shock_width,     direction: same, size: "<= +0.5 cell vs van Leer"}
kill_criterion: >
  No candidate under this hunch reaches 1e-10 residual on >= 80 % of dev nozzle cases
  within two rounds.
known_relatives: ["limiter freezing (common practice)", "Venkatakrishnan 1995"]
status: open        # open | testing | supported | refuted | inconclusive | merged
verdict_note: ""
author: hunch-generator/steady-convergence   # or: peter
```

**Lenses.** Each hunch-generator call uses one lens:

1. *steady-convergence*: residual stalls, Newton behavior, limit cycles.
2. *shock physics*: entropy, characteristics, Rankine–Hugoniot structure.
3. *approximation theory*: TVD/TVB, ENO/WENO, BVD, smoothness indicators.
4. *structure preservation*: well-balancing, invariants, positivity, entropy stability.
5. *practitioner*: what breaks in CFX, Fluent, OpenFOAM or LS-DYNA in daily use.
6. *contrarian*: deliberately violate a textbook assumption.
7. *transfer*: read summaries of recent AI-generated mathematics and look for constructions that carry over to numerics. A good source is Xie's catalog of "mathematical instruments" from OpenAI's October 2026 release. Expect a low hit rate.
8. *human*: your own hunches, tagged `author: peter`.

To read the ledger, use `sforge hunch list` and `sforge hunch show H`. The registry stores only hunch ids, never a copy of the hunch.

---

## 7. Phase overview

| Phase | Goal | Gate in one line | Effort (rough) |
|---|---|---|---|
| 0 Setup | Repo, CLI skeleton, agents, sandbox validator | `sforge --help` works, tests green | 1 session |
| 1 Arena 1 judge and zoo | Exact solutions, solvers, metrics, zoo baseline | Appendix H reproduced, audit agrees, problem-existence report written | 3–4 sessions |
| 2 Engine, calibration, red team | Evolution loop, LLM backends, first hunch round | ≥ 200 candidates unattended, every cheat caught, cost known | 2–3 sessions |
| 3 Production search, Arena 1 | Targets A and B | Promoted dossier with referee verdict, or a negative-result note | 3+ sessions plus runs |
| 4 2D and OpenFOAM | Does the winner survive in 2D? | Exact oblique shock, carbuncle test documented, OpenFOAM comparison | 2–3 sessions |
| 6 Arena 2 judge and zoo | TMC judge and baseline | Reference table reproduced, zoo trade-off curve plotted | 3–4 sessions |
| 7 Production search, Arena 2 | Targets D and E | As in Phase 3 | 3+ sessions plus runs |
| 5, 8, 9 (parked) | Cold-spray demo, explicit TMC, latent-FEA bridge | Planned in detail once Phase 3 or 7 has a result | — |

A *session* is one Claude Code working block of a few hours. These effort numbers are guesses; replace them with measured ones in `STATUS.md`.

---

## 8. Phase 0: Setup

Tasks:

1. Run `git init`, create the layout from §5.3 and add a `.gitignore` for `candidates/`, `runs/` and caches.
2. Write `pyproject.toml` with the stack from §5.4 and an `sforge` console script, then run `uv sync`.
3. Create the files from Appendix A (`CLAUDE.md`), Appendix B (agents) and Appendix C (hook, settings) verbatim, and make the hook executable.
4. Build the CLI skeleton. Every command from §5.5 exists, has `--help` and returns "not implemented".
5. Write `core/sandbox.py`, the AST validator. Its tests include hostile snippets that must be rejected (file access, `__import__`, dunder access, globals, randomness, time, module-level state) and clean snippets that must pass.
6. Write `core/registry.py`, the SQLite schema with tables `candidates`, `scores`, `runs`, `cases` and `llm_calls`. Hunches stay in `ledger/hunches.yaml`; rows refer to them by id.
7. Create `docs/STATUS.md` and `docs/DECISIONS.md` from the templates below.
8. Peter creates the seed:
   `mkdir -p ~/.schemeforge && python3 -c "import secrets; print(secrets.token_hex(16))" > ~/.schemeforge/heldout_seed`

`STATUS.md` template:

```markdown
# STATUS
Phase: 0 — Setup (in progress)      Judge version: —
Last session: YYYY-MM-DD — one-line summary
## Done
## Next (ordered)
## Blockers / questions for Peter
## Numbers to remember (run ids, best candidates, costs)
```

Each `DECISIONS.md` entry has the heading `## YYYY-MM-DD — <decision>`, followed by *Context*, *Decision* and *Consequences*.

**Gate 0**
- [ ] `sforge --help` lists all commands
- [ ] `pytest -q` and `ruff check .` pass; the sandbox tests include at least 10 hostile snippets
- [ ] The agents are visible in Claude Code, and the hook blocks a test write by the proposer outside `candidates/`
- [ ] The seed file exists, and Claude Code is denied when it tries to read it
- [ ] `STATUS.md` is filled in

---

## 9. Phase 1: Arena 1 judge and zoo

### 9.1 Physics, units, gases

The gas is ideal and calorically perfect, and all units are nondimensional. Riemann problems use Toro's units. The nozzle uses p0 = ρ0 = 1 at stagnation and lengths in throat units. γ is a case parameter: 1.4, 5/3 and 1.405, plus 1.2 as a stress value.

Process gases for Phase 5, which also supply the γ values here:

| Gas | γ | R [J/(kg·K)] | Speed of sound at 300 K |
|---|---|---|---|
| N₂ | 1.40 | 296.8 | 353 m/s |
| He | 5/3 | 2077.1 | 1019 m/s |
| H₂ | 1.405 | 4124.2 | 1318 m/s |

### 9.2 Exact solutions

**Riemann problem.** Follow Toro (2009), Ch. 4:
- Use the pressure function f_K(p) for each side, with a shock branch and a rarefaction branch.
- Solve f_L(p) + f_R(p) + (u_R − u_L) = 0 for p*, using Newton with a safe bracket.
- Compute u* and sample the full solution.
- Detect vacuum generation, i.e. (2/(γ−1))(a_L + a_R) ≤ u_R − u_L, and exclude it from the families.
- Verify against Toro's star states (Appendix H).

**Quasi-1D nozzle, steady.** The inputs are an area distribution A(x) with a single throat A_t, stagnation values p0 and T0, and a back pressure p_b.
- Isentropic relations:
  - A/A* = (1/M) · [(2/(γ+1)) (1 + (γ−1)/2 · M²)]^((γ+1)/(2(γ−1)))
  - p/p0 = (1 + (γ−1)/2 · M²)^(−γ/(γ−1)), ρ/ρ0 = (…)^(−1/(γ−1)), T/T0 = (…)^(−1)
- Normal shock at Mach M1:
  - p2/p1 = 1 + 2γ/(γ+1) · (M1² − 1)
  - M2² = (1 + (γ−1)/2 · M1²) / (γM1² − (γ−1)/2)
  - p02/p01 = [(γ+1)M1² / ((γ−1)M1² + 2)]^(γ/(γ−1)) · [(γ+1) / (2γM1² − (γ−1))]^(1/(γ−1))
  - behind the shock, A*₂ = A*₁ · p01/p02.
- Critical back pressures:
  - p_crit1: exit on the subsonic branch with A* = A_t;
  - p_crit2: normal shock exactly at the exit;
  - p_crit3: design condition, exit on the supersonic branch.
- Regimes by p_b/p0:
  - above p_crit1: subsonic everywhere and not choked, with A* taken from the exit conditions;
  - between p_crit2 and p_crit1: choked, with a normal shock in the divergent part at the x_s that solves p_exit(x_s) = p_b (Brent's method on (x_t, x_exit));
  - below p_crit2: supersonic exit. Quasi-1D can't represent the shocks that then form outside the nozzle.

The reference nozzle is Anderson's (1995): A(x) = 1 + 2.2 (x − 1.5)² for x ∈ [0, 3]. Its reference values are in Appendix H.

### 9.3 Solvers (owned by the judge)

**Unsteady 1D Euler.**
- Finite volume on a uniform grid with 3 ghost cells per side, and transmissive or periodic boundaries.
- Default reconstruction: MUSCL on primitive variables, using the limiter slot.
- Default flux: HLLC (Toro) with Einfeldt (Roe-average) wave-speed estimates.
- Time integration: SSP-RK3 with CFL 0.5 in dev; promo sweeps CFL over {0.3, 0.5, 0.7, 0.9}.
- The whole time loop is jit-compiled with `lax.fori_loop` or `lax.scan`.

**Steady quasi-1D nozzle.**
- Conserved variables (ρA, ρuA, EA), with the flux F·A evaluated at faces.
- The momentum source p · dA/dx is discretized by default as S_i = p_i (A_{i+½} − A_{i−½}) per cell. This isn't exactly well-balanced; fixing that is Target B.
- Boundary conditions: at the subsonic inlet, p0 and T0 are imposed and one characteristic quantity is extrapolated. At the outlet, p_b is imposed when the flow is subsonic and everything is extrapolated when it is supersonic.

Two pseudo-time solvers run, and both are reported:
- *Explicit:* SSP-RK3 with local time stepping, CFL 0.8, capped at 50,000 iterations. It records the residual history: the L2 norm of dU/dt divided by its initial value.
- *Implicit:* backward-Euler pseudo-time with the exact Jacobian (`jax.jacfwd`, dense LU, N ≤ 480), capped at 300 iterations. CFL is ramped by switched evolution relaxation: CFL_n = min(CFL_max, CFL_0 · R_0/R_n).

A run counts as converged at a residual ≤ 1e-12. It is flagged as a limit cycle when the residual plateaus and oscillates periodically over the last 10 % of iterations.

### 9.4 Slot contracts

Phase 1 implements `limiter` and `flux`. The other three contracts are fixed now but built only when a target or a seed hunch needs them (`operator` for Target B, `limiter_stateful` and `reconstruction` for seed hunches 2–6).

```python
# All arrays float64. Pure jax.numpy / jax.lax. No Python loops over cells.
# No state except explicit state that the judge owns.

# slot "limiter": MUSCL slope limiter, applied per primitive variable
def phi(r):
    """r: array of slope ratios (any shape). Return phi(r), same shape, finite for every finite r
    (including r <= 0 and very large |r|). TVD and second-order properties are measured, not required."""

# slot "limiter_stateful": the judge owns the state (e.g. for pseudo-time hysteresis)
def phi_s(r, state):
    """state has the same shape as r and starts at 0. Return (phi, new_state)."""

# slot "reconstruction": interface states from cell values
def reconstruct(W, gamma):
    """W: (n + 6, 3) primitive [rho, u, p], including 3 ghost cells per side.
    Return (WL, WR), each (n + 1, 3): the states left and right of interfaces 0..n."""

# slot "flux": numerical flux
def flux(UL, UR, gamma):
    """UL, UR: (m, 3) conserved [rho, rho*u, E]. Return F: (m, 3). Must satisfy flux(U, U) == F(U)."""

# slot "operator" (Target B): face fluxes and momentum source for quasi-1D
def fluxes_and_source(U, A_face, dx, gamma, ghosts):
    """U: (n, 3) quasi-1D conserved [rho*A, rho*u*A, E*A]; A_face: (n + 1,); ghosts: boundary data built by the judge.
    Return (F_face: (n + 1, 3), S_mom: (n,)). The judge assembles dU/dt = -(F[1:] - F[:-1]) / dx + [0, S_mom, 0],
    so mass and energy conservation hold by construction."""
```

Write the final contracts into `docs/judge/euler1d_slots.md`. The engine pastes them into its prompts.

### 9.5 Dev suite and held-out families

Dev suite, visible to agents:

| ID | Case | N | Reference |
|---|---|---|---|
| R1 | Sod (Toro test 1) | 200 | exact |
| R2 | 123 problem (Toro test 2) | 200 | exact |
| R3 | left blast wave (Toro test 3) | 200 | exact |
| R4 | shock collision (Toro test 5) | 200 | exact |
| R5 | stationary contact (ρ_L = 1.4, ρ_R = 1, u = 0, p = 1) | 100 | exact (nothing moves) |
| R6 | slowly moving shock, built from Rankine–Hugoniot with speed 0.05 · max(\|u\| + a) | 200 | exact |
| R7 | Shu–Osher shock–entropy wave | 400 | reference (WENO5-Z, N = 12,800, cached) |
| S1 | smooth density wave ρ = 1 + 0.2 sin(2πx), u = 1, p = 1, periodic | 50/100/200 | exact (pure translation) |
| N1 | Anderson nozzle, p_b/p0 = 0.6784 (shock at x = 2.0993) | 120 | exact |
| N2 | Anderson nozzle, p_b/p0 = 0.995 (subsonic, not choked) | 120 | exact |
| N3 | Anderson nozzle, p_b/p0 = 0.01 (supersonic exit) | 120 | exact |
| N4 | sweep over 11 values of p_b, implicit solver only; the shock crosses about 30 cells (the 41-point sweep with both solvers runs in promo as part of NF3) | 120 | exact (smooth in p_b) |

Held-out families, with instances drawn from the secret seed:

- **RF1: random Riemann problems.** Pressure ratio log-uniform in 10^0.5–10^5, density ratio 0.1–10, velocities that don't create a vacuum, γ from §9.1.
- **RF2: slowly moving shocks.** Shock Mach 1.5–10, shock speed 0–0.2 of the maximum wave speed.
- **NF1: nozzles with a shock.**
  - Parabolic and smoothed-conical divergent sections, area ratio 2–10, length 2–4 throat units.
  - p_b places the shock at 15–90 % of the divergent length.
  - The grid is shifted so the exact shock lands at a uniformly random fraction of a cell.
- **NF2: shock-free nozzles**, subsonic and supersonic.
- **NF3: p_b sweeps** for the smoothness metrics.

Document the case YAML format in `docs/judge/euler1d_cases.md`. Breakers write their cases in this format, and `--case` reads it.

### 9.6 Metrics

| Metric | Definition | Cases |
|---|---|---|
| `l1_smooth` | L1 error of ρ, u, p against exact, excluding ±5 cells around discontinuities | R, S, N |
| `order_smooth` | observed L1 order on S1 between N = 50 and N = 200, extrema included | S1 |
| `shock_width` | cells between 5 % and 95 % of the pressure jump | shocks |
| `contact_width` | the same for density at contacts | R |
| `overshoot` | largest excursion beyond the jump states, divided by the jump size | R, N |
| `tv_increase` | increase of total variation over the run | R |
| `shock_pos_err` | \|x_s,num − x_s,exact\| / dx | N1, NF1 |
| `mdot_var` | max \|ṁ_i − ṁ_exact\| / ṁ_exact | N, NF |
| `h0_var` | largest relative deviation of total enthalpy | N, NF |
| `entropy_spurious` | entropy rise in regions that are isentropic in the exact solution | N, NF |
| `res_orders_expl` | orders of residual drop the explicit solver reaches within its cap | N, NF |
| `newton_iters` | implicit iterations to 1e-12 (the cap if not reached) | N, NF |
| `limit_cycle` | the flag from §9.3 | N, NF |
| `roughness_J` | RMS of the second differences of (J_num − J_exact) over a p_b sweep, divided by the RMS second difference of J_exact. J = ∫ p dA over the divergent section, i.e. the axial wall force. | N4, NF3 |
| `max_cfl` | the largest CFL in the sweep without failure | promo |
| `cost` | wall time per cell update, normalized to the zoo median | all |

### 9.7 Hard constraints and metamorphic tests

**Hard constraints** (failure means rejection):
- consistency, `flux(U,U) = F(U)` to 1e-12;
- flux mirror symmetry, `flux(R·U_R, R·U_L) = −R·flux(U_L, U_R)` with R = diag(1, −1, 1);
- positivity of ρ and p;
- determinism and finite output.

**Measured but not required:**
- mirror symmetry of a whole run (mirrored domain against mirrored solution) for limiters and reconstructions. With MUSCL it holds only if φ(r) = r·φ(1/r), which Koren, for example, violates;
- Galilean invariance, since numerical dissipation usually depends on |u|;
- scaling homogeneity under (ρ, p, E) → (αρ, αp, αE);
- CFL robustness.

### 9.8 Zoo

Phase 1 builds only what Gate 1 and the Phase 2 calibrations need:
- **Limiters:** minmod, MC, van Leer, van Albada, superbee, Koren, and a Venkatakrishnan-type limiter (1D form, several values of K).
- **Fluxes:** Rusanov, HLL, HLLC, Roe with Harten's entropy fix.
- **Reconstructions:** first order, MUSCL with each limiter, and WENO5-Z (also used for the R7 reference).

Added when the matching slot or target becomes active:
- AUSM+, AUSM+-up and SLAU (Target C);
- PPM, WENO5-JS, TENO5 and THINC-BVD (reconstruction hunches);
- the simple nozzle source term from §9.3 plus one well-balanced variant from the literature, which is the Target B baseline.

### 9.9 Problem-existence check

Before any search, run the zoo on N1, NF1 and NF3 with both pseudo-time solvers. Write the results to `docs/judge/euler1d_baseline.md`, answering:

- Which limiters stall? Report the orders the explicit solver reaches and the iterations (or failure) of the implicit solver.
- What are the shock width and overshoot of each limiter?
- What is `roughness_J` for each limiter?
- Plot the zoo's front: sharpness (shock width, overshoot) against convergence and smoothness.

This sets the Phase 3 targets:
- If the front is wide — sharp limiters stall or give rough objectives while smooth ones smear the shock — Target A stands.
- If every zoo member converges to 1e-12 and is smooth, Target A moves to the explicit solver only, or to 2D. Record this in `DECISIONS.md`.

### 9.10 Blind judge audit

Write `docs/judge/euler1d_spec.md` with the formulas, conventions and case definitions.

The `judge-auditor` agent re-implements the exact Riemann and nozzle solutions from that spec alone; its hook denies reads of `src/schemeforge/arenas/`. It then compares its results with the judge's on at least 1,000 random admissible instances. Any relative difference above 1e-10 is traced to its cause.

Also add Hypothesis property tests:
- the Rankine–Hugoniot conditions hold across exact shocks;
- in the exact nozzle solution, ṁ is constant and entropy jumps only at the shock.

### 9.11 Gate 1

- [ ] Appendix H reproduced: Toro star states to 5 significant digits, nozzle values to 4–5 digits
- [ ] The blind audit agrees on at least 1,000 instances
- [ ] Zoo sanity: superbee gives the narrowest shocks and squares off smooth waves; minmod is the most diffusive; HLLC and Roe keep the stationary contact exactly while HLL and Rusanov don't
- [ ] Hard constraints and metamorphic tests pass for every zoo member
- [ ] The dev suite takes ≤ 30 s per candidate on your laptop, JIT excluded
- [ ] `euler1d_baseline.md` is written and the decision on Targets A and B is recorded
- [ ] The judge is tagged `euler1d-v1.0`

---

## 10. Phase 2: Engine, calibration, red team

Tasks:

1. **Build or adopt.** Spend an hour on OpenEvolve and ShinkaEvolve (§5.9) and record the decision in `DECISIONS.md`.
2. **Engine core** (§5.9) with the `dummy` backend. Run an end-to-end test of 2 islands × 3 generations × 4 children: candidates get archived, and the run resumes after you kill it. Then add the `claude-cli` backend with the prompt templates from Appendix E.
3. **Calibration C1 (limiter slot).** Seed islands with φ = 0 (first order) and φ = 1 (unlimited), then run 3 islands × 15 generations × 8 children. Expect textbook limiters to appear almost at once, because the LLM knows them; the AlphaEvolve team saw the same on problems that were in the training data. What C1 tests is the machinery:
   - candidates are valid;
   - the novelty fingerprints recognize zoo duplicates;
   - the descriptors spread out;
   - nothing crashes.
4. **Calibration C2 (flux slot).** Seed with Rusanov and check whether the search reaches HLLC-level contact resolution on R5 without losing robustness.
5. **Red team.** The `cheater` agent tries at least the strategies below, plus its own ideas:
   - recognizing dev cases from input fingerprints and returning known answers;
   - exploiting how NaN/Inf or tolerances are handled;
   - hidden state through closures or default arguments;
   - output that depends on batch order;
   - extra dissipation only where a dev-case shock is detected;
   - gaming the cost metric.

   Each strategy must be caught by a hard constraint, a metamorphic test or the held-out families. Close every hole, bump the judge version and log everything in `docs/judge/redteam.md`.
6. **Cost.** Measure tokens, plan usage and wall time per 100 candidates for each model mix. Record the default mix and the Phase 3 budget in `DECISIONS.md`.
7. **`sforge` MCP server** (§5.10), then remove `Bash` from the proposer, breaker and hunch-generator.
8. **First hunch round** (Appendix D): 4 hunches on a small budget. If it works, write it down as the project skill `.claude/skills/hunch-round/`.

**Gate 2**
- [ ] `sforge evolve` runs at least 200 candidates unattended and resumes after an interruption
- [ ] During C1, the registry recorded candidates flagged as duplicates of at least 4 different zoo limiters (so the fingerprints work), plus non-duplicate archive entries spread over the descriptor grid
- [ ] Every red-team strategy is caught and documented
- [ ] Cost per 100 candidates is measured and the Phase 3 budget agreed
- [ ] Proposer, breaker and hunch-generator run without `Bash`, through the `sforge` MCP server
- [ ] The first round produced ledger entries with verdicts and a `docs/rounds/…` summary

---

## 11. Phase 3: Production search, Arena 1

### 11.1 Targets

Pre-register these in `docs/targets/` before the first round.

**Target A: sharp and smooth steady shock capturing.** Push out the zoo's front between sharpness (`shock_width`, `overshoot`) and convergence and smoothness (`res_orders_expl`, `newton_iters`, `roughness_J`). Example thresholds, to be finalized from the Phase 1 baseline:
- `shock_width` ≤ superbee + 0.5 cell and `overshoot` ≤ 0.1 % of the jump;
- the explicit solver reaches 1e-12 on ≥ 95 % of NF1 instances, where the zoo member of comparable sharpness reaches it on ≤ 50 %;
- `roughness_J` at least 3× better than that zoo member;
- `order_smooth` ≥ 1.9, extrema included.

**Target B: well-balanced quasi-1D nozzle.** Preserve steady isentropic flow, subsonic and supersonic, to machine precision on coarse grids (N = 30), while keeping Target A-level shock behavior. Example thresholds: steady-state error ≤ 1e-12 on NF2, and `shock_pos_err` ≤ 0.5 cell at N = 60. Known relatives are well-balanced nozzle schemes (e.g. Kröner & Thanh 2005) and equilibrium-variable reconstruction from shallow-water schemes.

**Target C, only if A and B stall:** a flux with HLLC-level contact resolution and Rusanov-level robustness, including no carbuncle in Phase 4. This field is crowded.

### 11.2 Seed hunches

Register these with `author: peter`, or regenerate them. The relatives listed for each anchor its novelty check.

| # | Hunch | Slot | Known relatives |
|---|---|---|---|
| 1 | A C∞ monotone limiter family inside Sweby's TVD region with tunable compressiveness | limiter | van Albada, Venkatakrishnan |
| 2 | Pseudo-time hysteresis removes limiter chatter | limiter_stateful | limiter freezing |
| 3 | Blend high and low order by the local discrete entropy production | reconstruction | entropy viscosity (Guermond, Pasquetti, Popov 2011) |
| 4 | Compress contacts harder than shocks, using a characteristic decomposition | reconstruction | artificial compression (Harten), THINC/BVD |
| 5 | Reconstruct the sub-cell shock position at steady state | reconstruction | subcell resolution (Harten 1989), shock fitting |
| 6 | Reconstruct the steady invariants (ṁ, H0, s) instead of (ρ, u, p) | operator | well-balanced nozzle schemes, equilibrium reconstruction |
| 7 | A limiter with a bounded derivative, chosen to keep the Newton Jacobian well conditioned at the shock | limiter | Venkatakrishnan |
| 8 | One transfer-lens hunch per round | any | — |

### 11.3 Round protocol

1. Run `sforge leaderboard --arena euler1d --slot <S> --pareto --vs-zoo` and `sforge hunch list --open`.
2. Run `/hunch-round` (Appendix D) with the arena, the slot, 6 hunches, the chosen lenses and 8 evaluations per proposer.
3. Give the best 2–3 hunches engine islands: `sforge evolve … --gens 20 --children 8`.
4. Run breakers on the top 5 Pareto candidates, with at most 10 cases each.
5. Peter reviews `cases/quarantine/`. Accepted cases go into the next judge version, followed by a rescore.
6. Run promo for new archive entrants and apply the promotion test (§5.8). Every promoted candidate goes to the analyst and then the referee.
7. Close the hunches with verdicts, write `docs/rounds/<date>-<arena>-<slot>.md` and update `STATUS.md`.

### 11.4 Kill criterion and gate

Stop after 4 rounds or about 2,000 evaluated candidates without a promotion on Target A or B, whichever comes first. Then write `docs/results/arena1-negative.md`: what was tried, why it failed, and the zoo front itself as a result. Move on to Phase 6. You can extend the budget.

**Gate 3**
- [ ] A promoted candidate with a complete dossier and referee verdict, **or** the negative-result note
- [ ] A ledger verdict for every hunch that was tested

---

## 12. Phase 4: 2D check and OpenFOAM port

1. **2D JAX finite-volume solver** in `arenas/euler2d/`:
   - structured grids, Cartesian and simple mapped/axisymmetric;
   - unsplit MUSCL with the same slots and SSP-RK3;
   - transmissive and reflecting walls.
2. **Exact 2D cases:**
   - oblique shock over a wedge (M1 = 5, θ = 15°, γ = 1.4: β = 24.32°, p2/p1 = 4.781, M2 = 3.504);
   - Prandtl–Meyer expansion;
   - regular shock reflection (two-shock solution).
3. **Reference cases:**
   - Quirk's odd–even decoupling test (carbuncle, pass/fail);
   - double Mach reflection;
   - Mach 3 forward step;
   - 2D Riemann configurations.

   Their references come from fine-grid zoo runs and are labelled "reference".
4. **OpenFOAM port.**
   - Implement the winner as a custom `limitedScheme` in a user library, following the structure of OpenFOAM's own `vanLeer` limiter source.
   - Load it through `libs (...)` in `controlDict` and select it in rhoCentralFoam's `interpolationSchemes`, e.g. `reconstruct(rho) myLimiter;`.
   - Cases: the `wedge15Ma5` and `forwardStep` tutorials plus a 2D planar or axisymmetric nozzle.
   - Compare against vanLeer, vanAlbada and Minmod. If it's convenient, run the case matrix through your Rechenknecht automation.

**Gate 4**
- [ ] Oblique-shock and Prandtl–Meyer errors converge at the expected rate
- [ ] Carbuncle behavior is documented for the winner and the zoo
- [ ] The OpenFOAM library compiles and runs, and the comparison table is in `docs/results/`
- [ ] The decision on whether the 1D advantage survives 2D is in `DECISIONS.md`

---

## 13. Phase 5 (parked): Cold-spray nozzle demo

Question: does a smoother, sharper scheme change optimizer behavior on a real design problem? Sketch: the judge's steady quasi-1D gas solution with the gases from §9.1; one-way coupled steady Lagrangian particles with Henderson (1976) drag; objective = particle exit velocity over a 2-parameter or B-spline nozzle shape. Experiments: the objective landscape per limiter, gradient-based optimization from random starts (this phase adds the `grad_mismatch` metric: AD gradient of J with respect to p_b, by implicit differentiation of the steady state, against a central finite difference), and shapes where an internal shock appears. Quasi-1D makes this a numerics demo, not a design tool. Plan it in detail once there is a candidate worth demoing.

---

## 14. Phase 6: Arena 2 judge and zoo (third-medium contact)

### 14.1 Tooling spike (one session)

Reproduce FElupe's third-medium contact example, then time a 2D plane-strain Hertz case with Q2 elements at about 10,000 DOF. Use the result to choose between FElupe and custom JAX. The chosen framework must:
- run the dev suite in ≤ 60 s per candidate;
- automatically differentiate user energy functions;
- support Q2 elements;
- support second-gradient (Hessian) regularization.

### 14.2 Reference cases

| ID | Case | Reference |
|---|---|---|
| C0a | 1D gap closure: a block pushed through a medium-filled gap onto a rigid wall | ideal: zero force until the gap closes, then the bar's stiffness |
| C0b | a single medium element in simple shear | ideal: zero shear stress (frictionless) |
| C1 | contact patch test with non-matching meshes (Taylor & Papadopoulos 1991) | uniform pressure, exact |
| C2 | 2D Hertz: cylinder on block, plane strain, elastically identical bodies | a = √(4PR/(πE*)), p0 = 2P/(πa) = √(PE*/(πR)), p(x) = p0 √(1 − x²/a²) |
| C3 | Cattaneo–Mindlin after C2, with a tangential load Q < μP | stick zone c/a = √(1 − Q/(μP)); q(x) = μp0 [√(1 − x²/a²) − (c/a) √(1 − x²/c²)] for \|x\| < c and μp0 √(1 − x²/a²) for c < \|x\| < a |
| C4 | steady sliding of a block on a flat | Coulomb: Ft/Fn = μ exactly; frictionless: Ft = 0 |
| C5 | ironing (large sliding) | reference: converged classical contact solution on a fine mesh |
| C6 | self-contact of a buckling C-shaped section | reference plus invariants (no inversion, symmetry) |

Notes:
- P is the force per unit length, 1/E* = (1 − ν₁²)/E₁ + (1 − ν₂²)/E₂ and 1/R = 1/R₁ + 1/R₂.
- Use elastically identical bodies so that Dundurs' β = 0; otherwise Cattaneo–Mindlin isn't exact.
- Keep a/R ≤ 0.1 and the block at least 20a wide so that Hertz applies.
- Also solve every case with a classical contact method on a fine mesh, and compare candidates with both. This separates the TMC error from geometry and discretization error.

### 14.3 Slot contracts

```python
# Arena 2 (jax.numpy, or the AD-capable math of the framework chosen in the spike)

# slot "medium": strain energy density of the third medium
def psi_medium(F, p):
    """F: (..., 3, 3) deformation gradient (plane strain: F[..., 2, 2] == 1).
    p: fixed parameters from the judge (e.g. body shear modulus, medium scale).
    Must be frame-indifferent: psi(Q @ F) == psi(F) for rotations Q (checked)."""

# slot "regularization": optional higher-gradient term (needs Q2 or higher)
def psi_reg(F, gradF, p): ...

# slot "friction" (Target E): the judge owns the state
def medium_friction(F, state, p):
    """Return (energy, new_state) for one load step. The target is rate-independent Coulomb behavior,
    checked through the C3 stick zones and C4 Ft/Fn -> mu."""
```

Write three documents alongside the code: the final contracts in `docs/judge/contact_slots.md`, the formulas and case definitions in `docs/judge/contact_spec.md`, and the case YAML format in `docs/judge/contact_cases.md`.

### 14.4 Metrics

| Metric | Definition |
|---|---|
| `p0_err`, `a_err` | Hertz peak pressure and half-width, against exact and against the fine classical solution |
| `p_l2` | L2 error of the contact pressure distribution |
| `gap_res` | residual medium thickness at full load, divided by a |
| `leak_pre` | reaction force before geometric contact, divided by the load scale |
| `shear_parasitic` | tangential force in frictionless sliding, divided by the normal force |
| `cm_stick_err` | error of the stick-zone half-width against c, in elements |
| `mu_eff_err` | \|Ft/Fn − μ\| in steady sliding |
| `newton_iters` | mean and max Newton iterations per load step |
| `max_step` | largest load step that still converges (by bisection) |
| `min_J_medium` | smallest Jacobian in the medium; ≤ 0 is a hard failure |
| `mesh_sens` | spread of the metrics over 3 mesh densities and over Q1/Q2 |
| `cost` | time per Newton iteration, normalized to the zoo median |

### 14.5 Metamorphic tests

- Frame indifference under random rigid rotations of the whole problem.
- Mirror symmetry.
- Mesh offsets for non-matching meshes.
- Load-path independence for frictionless cases. With friction, path dependence is expected.

### 14.6 Zoo

- The Wriggers–Schröder–Schwarz (2013) isotropic–anisotropic medium.
- The Bluhm–Sigmund–Poulios (2021) neo-Hookean medium with HuHu (Hessian) regularization.
- The variants in FElupe's example.
- The crystal-plasticity-inspired friction model ("Adding friction to Third Medium Contact").
- The 2026 robust mixed formulation (arXiv 2606.28036), if it fits the framework.
- Classical penalty or augmented-Lagrangian contact, as the non-TMC reference.

### 14.7 Problem-existence check

Reproduce the trade-off in the medium's stiffness scale:
- a softer medium gives less leakage, but more residual gap and weaker Newton robustness;
- a stiffer medium does the reverse.

Plot the zoo front in `docs/judge/contact_baseline.md` and pre-register Targets D and E from it.

### 14.8 Gate 6

- [ ] C1–C4 reproduced with the classical method, and the formulas audited by `judge-auditor`
- [ ] The zoo front is plotted and the thresholds for D and E are pre-registered
- [ ] The dev suite is within budget, and the judge is tagged `contact-v1.0`

---

## 15. Phase 7: Production search, Arena 2

**Target D: frictionless front.** Lower `gap_res` and `leak_pre` at equal or better `newton_iters` and `max_step`, with less sensitivity to the medium's stiffness scale and to the mesh.

**Target E: friction.** `mu_eff_err` ≤ 1 % in steady sliding, `cm_stick_err` ≤ 1 element and robust Newton convergence, with a formulation simpler than the crystal-plasticity one.

Seed hunches:

| # | Hunch | Known relatives |
|---|---|---|
| 1 | A clamped log-barrier on the volumetric or normal stretch: ψ = 0 for J > Ĵ and a C² barrier below. There is no pre-contact stiffness by construction; a tiny isotropic term is kept only for mesh regularity. | Incremental Potential Contact (Li et al. 2020) |
| 2 | Spectral directional stiffening: penalize only the smallest principal stretch, so shear stiffness is zero | the anisotropic term of Wriggers et al. 2013 |
| 3 | A regularized Coulomb law in the medium's shear energy, with ε-continuation | regularized friction (Oden & Martins 1985); crystal-plasticity TMC friction |
| 4 | A mixed u–J medium formulation to avoid locking at full compression | the 2026 robust mixed TMC formulation |
| 5 | A compression-aware HuHu weight, so the regularization doesn't stiffen the medium before contact | Bluhm et al. 2021 |

The round protocol, promotion test and kill criterion are the same as in Phase 3 (§11.3–11.4).

---

## 16. Phase 8 (parked): Explicit third-medium niche

Question: can a third medium work in explicit dynamics without the stable time step collapsing as the medium's elements get thin and stiff? Start with a literature check (analyst and referee); if it is solved, reproduce that as zoo and decide with Peter. Judges: 1D bar impact (exact) and Hertz impact (Appendix H), plus energy balance. Hunch directions: a soft medium capped by nodal mass and Δt (by analogy with LS-DYNA SOFT=1), momentum-conserving mass scaling, subcycling, IMEX. The practical baseline is penalty contact with a soft constraint. Read the ownership note in §19 before any check with a work LS-DYNA license.

---

## 17. Phase 9 (parked): Latent-FEA bridge

A certification suite for any element, learned or classical (patch test, exactly 3 zero-energy modes in 2D, symmetry and PSD, frame invariance, h-convergence, the Arena 2 cases), and a starter hunch K_e = K_consistency + Pᵀ M_θ P with a learned SPD M_θ on the hourglass subspace, as in hourglass control and virtual elements (Flanagan & Belytschko 1981; Beirão da Veiga et al. 2013). Not before the Arena 2 judge exists.

---

## 18. Budget and cost control

- **Example round:** 6 hunches × 8 proposer evaluations plus 3 islands × 20 generations × 8 children. That is about 530 candidates, roughly 500 single-shot LLM calls and about 10 agent sessions (breaker, analyst, referee).
- **Measure first.** Record tokens and cost per 100 candidates in Phase 2, then set a budget per round.
- **Subscription route.** `claude -p`, subagents and workflows draw on your plan's usage limits; keep rounds small until Phase 2 has measured the cost.
- **API route** (only if the limits bite): prompt caching for the static prompt prefix and Message Batches for non-urgent generations.
- **Model mix.** Bulk mutations on `sonnet`, with some `haiku` for diversity. Hunches, breakers and analysts on `opus`. Where possible, the referee runs on a different model than the analyst.

---

## 19. Risk register

| Risk | Effect | Mitigation |
|---|---|---|
| Judge bug | everything downstream is wrong | Appendix H checks, blind audit, property tests |
| Reward hacking | fake winners | sandbox, metamorphic tests, held-out families, red team, breakers |
| A rediscovery presented as novel | loss of credibility | zoo, behavioral distance, literature check, referee; "rediscovery" is an honest label |
| A 1D win fails in 2D | wasted write-up | the Phase 4 gate comes before any write-up |
| No practical significance | irrelevant results | thresholds tied to real problems (stalled residuals, rough objectives) |
| LLM usage or cost blows up | budget overrun | evaluation cascade, budgets per round, cheap models for bulk work, caching |
| Scope creep | nothing gets finished | gates, kill criteria, `STATUS.md` |
| Laptop compute | slow loops | small dev suites, JIT, evaluation locks; optionally a cloud VM for promo runs |
| JAX/FElupe API changes | broken builds | pinned versions |
| Ownership of results | conflict with your employer | Numerical methods for CFD and contact are close to your day job. Before you publish or use results at work, check how the German employee-inventions act (ArbnErfG), §69b UrhG on software, and your contract apply. Keep the project on private hardware, time and licenses. This is not legal advice. |

---

## 20. Deliverables and publication

- **Always:** a public repo with the judge, the zoo and the harness, and the ledger including negative results. A benchmark for shock capturing in nozzles and for TMC is useful on its own.
- **With a promoted candidate:** turn the dossier into an arXiv preprint. Contact the authors of the closest papers before claiming novelty.
- **Formal proof** (e.g. in Lean) only for one specific, promising property, such as positivity under a CFL bound.

---

## 21. Open decisions

| Decision | Default |
|---|---|
| OS | WSL2/Linux |
| LLM route | subscription via `claude -p` and workflows; switch to the API if the limits bite |
| Names | folder `schemeforge`, package `schemeforge`, CLI `sforge` |
| Public repo | private until Gate 2, then public |
| Weekly time budget | set by Peter |
| Order after Phase 3 | Phase 4, then Phase 6; Phase 5 once there is a candidate worth demoing |

---

## Appendix A: `CLAUDE.md`

```markdown
# schemeforge

AI-swarm search for numerical scheme components, judged by exact solutions.
Plan: docs/PLAN.md · State: docs/STATUS.md · Decisions: docs/DECISIONS.md

## Iron rules
1. The judge decides. Every claim about a candidate cites an `sforge eval` run id. Never estimate or invent scores.
2. Never edit `src/schemeforge/arenas/**` during a search round. A judge change is its own commit, bumps the judge
   version, and is followed by `sforge zoo eval` and an archive rescore.
3. Never read `~/.schemeforge/` or try to reconstruct held-out instances.
4. Candidates are pure functions: imports only from jax.numpy, jax.lax, math; no I/O, no hidden state,
   no Python loops over cells.
5. Register a hunch (`sforge hunch add`) with mechanism, predicted effect and kill criterion before testing it.
6. Never call a result novel. Labels: rediscovery / variant of X / plausibly new. Only the referee assigns
   "plausibly new".
7. Record negative results in the ledger.
8. float64 everywhere: `jax.config.update("jax_enable_x64", True)`.

## Session protocol
- Start: read docs/STATUS.md and the current phase in docs/PLAN.md; state the session goal in one sentence.
- During: small commits; tests green before each commit.
- End: update docs/STATUS.md (done / next / blockers / numbers), commit.
- Stop at every phase gate and ask Peter.

## Commands (prefix with `uv run` unless the venv is active)
- Tests: `pytest -q` · Lint: `ruff check .`
- Evaluate: `sforge eval <file> --arena euler1d --slot limiter --suite dev`
- Leaderboard: `sforge leaderboard --arena euler1d --slot limiter --pareto --vs-zoo`
- Ledger: `sforge hunch add ledger/drafts/<file>.yaml` · `sforge hunch list --open`
- Judge self-check: `sforge judge verify`

## Layout
src/schemeforge/{core,arenas,engine} · candidates/ (agent workspaces, gitignored) · cases/{quarantine,accepted}
dossiers/ · ledger/ · runs/ (gitignored) · audit/

## Style
Python >= 3.11, type hints, ruff, pytest + hypothesis. Docstrings state array shapes and units.
```

---

## Appendix B: Subagents (`.claude/agents/`)

Each block below is one file. The hook path uses `$CLAUDE_PROJECT_DIR` so it works from any working directory.

**`hunch-generator.md`**

```markdown
---
name: hunch-generator
description: Proposes falsifiable hunches for new numerical scheme components for a given arena, slot and lens. Use at the start of a hunch round.
tools: Read, Grep, Glob, Bash, Write, WebSearch, WebFetch
model: opus
effort: high
hooks:
  PreToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: 'python3 "$CLAUDE_PROJECT_DIR/.claude/hooks/guard_paths.py" ledger/drafts/'
---
You write research hunches for schemeforge. The task gives you: arena, slot, lens, number of hunches.

Before writing:
1. Run `uv run sforge leaderboard --arena <A> --slot <S> --pareto --vs-zoo` and `uv run sforge hunch list`
   to see what exists, what worked and what was refuted.
2. Read docs/judge/<arena>_baseline.md to see where the zoo's trade-off front lies.

Every hunch must:
- name a mechanism (why it should work), not only a recipe;
- predict which metrics move, in which direction, and roughly how much;
- give a kill criterion;
- list known relatives; if it IS a known method, say so plainly;
- fit the slot contract (docs/judge/<arena>_slots.md).

Diversity: no two hunches share a mechanism. If the lens is "contrarian", each hunch must break a stated textbook
assumption on purpose.

Output: one YAML file per hunch in ledger/drafts/, following ledger/schema.yaml. Do not register them; the
orchestrator does. Final message: the list of file paths and one line per hunch.
```

**`proposer.md`**

```markdown
---
name: proposer
description: Implements one hunch as a candidate scheme component and iterates on it against the dev suite. Use once per hunch in a hunch round.
tools: Read, Write, Edit, Bash, Glob, Grep
model: sonnet
hooks:
  PreToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: 'python3 "$CLAUDE_PROJECT_DIR/.claude/hooks/guard_paths.py" candidates/'
---
You implement exactly one hunch (id given in the task) as a candidate for one slot.

Workspace: candidates/<hunch-id>/<your-label>/. Write only there.

Loop, at most N evaluations (N is in the task; default 8):
1. Write cand_<k>.py following the slot contract in docs/judge/<arena>_slots.md: pure jax.numpy/jax.lax/math,
   no I/O, no hidden state, no Python loops over cells.
2. Run `uv run sforge eval cand_<k>.py --arena <A> --slot <S> --suite smoke`; if it passes, `--suite dev`.
3. Read the report. Change one idea at a time. Log what you changed and why in notes.md.
4. Register your best candidate with `uv run sforge submit <file> --hunch <id>`.

Rules: never edit files outside your workspace; never read ~/.schemeforge; never run the promo suite; never tune
constants to individual dev cases (held-out families will expose it).

Final message: best candidate path, its dev run id, a 3-line summary, and whether the hunch's predicted effect
appeared (yes / no / partly, with numbers).
```

**`breaker.md`**

```markdown
---
name: breaker
description: Attacks leading candidates by constructing physically admissible test cases on which they fail. Use after a round, on the top Pareto candidates.
tools: Read, Write, Bash, Glob, Grep
model: opus
effort: high
hooks:
  PreToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: 'python3 "$CLAUDE_PROJECT_DIR/.claude/hooks/guard_paths.py" cases/quarantine/'
---
You try to break candidates, not to fix them. The task gives you candidate ids and the arena.

1. Read each candidate's code and dev report. Form hypotheses about failure modes. Arena 1: sub-cell shock
   positions, strong rarefactions near vacuum, slowly moving shocks, extreme pressure ratios, grid misalignment,
   extreme gamma, sonic points. Arena 2: grazing contact, large sliding, thin medium, element distortion,
   stiffness contrast.
2. Write each case as YAML (format: docs/judge/<arena>_cases.md) into cases/quarantine/. Every case must be
   physically admissible and have an exact or reference solution the judge can compute.
3. Test with `uv run sforge eval <candidate> --arena <A> --slot <S> --suite dev --case cases/quarantine/<file>`.
4. Also run the zoo on your cases: a case that breaks everything is a hard case, not a weakness of the candidate.

Never modify candidates or judge code. Final message: per candidate, the cases that break it, the failure
signature, and whether zoo members fail too.
```

**`analyst.md`**

```markdown
---
name: analyst
description: Explains why a promoted candidate works, checks its theoretical properties and the literature, and drafts its dossier.
tools: Read, Write, Edit, Bash, Glob, Grep, WebSearch, WebFetch
model: opus
effort: high
hooks:
  PreToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: 'python3 "$CLAUDE_PROJECT_DIR/.claude/hooks/guard_paths.py" dossiers/'
---
For the promoted candidate named in the task:

1. Mechanism: explain in plain words what it does differently from its nearest zoo member. Back every claim with
   an `sforge eval` run id or a small script in dossiers/<id>/analysis/.
2. Properties, as applicable. Arena 1: position in Sweby's TVD region (plot), symmetry phi(r)/r = phi(1/r),
   phi(1) = 1; leading modified-equation terms on linear advection (SymPy); von Neumann stability of the
   linearized scheme; positivity under a CFL bound (try a Zhang–Shu convex-combination argument); sign of
   entropy production on random states. Arena 2: frame indifference, rank-one convexity checks, growth as J -> 0+,
   Coulomb consistency.
3. Literature: search arXiv, Google Scholar and journals for the closest methods. List up to 5 with links and the
   precise difference. If the method is in the literature, label it a rediscovery.
4. Proofs: write one only if it is actually a proof. Label conjectures as conjectures.
5. Write dossiers/<id>/README.md from the template in docs/PLAN.md Appendix F.
```

**`referee.md`**

```markdown
---
name: referee
description: Independently checks a dossier's claims and novelty label. Use after the analyst finishes; never on work it helped produce.
tools: Read, Bash, Glob, Grep, WebSearch, WebFetch
model: opus
---
You are a skeptical referee. You did not write this dossier.

1. Re-run every quoted `sforge eval` command; flag numbers that do not reproduce.
2. Search for prior art independently, with different search terms than the dossier used.
3. Classify each theoretical claim: proved, numerically supported, or unsupported.
4. Verdict: rediscovery / variant of <X> / plausibly new; and practical significance against the pre-registered
   thresholds in docs/targets/ (met / not met).

Final message: a review of at most one page. The orchestrator stores it in the dossier.
```

**`judge-auditor.md`**

```markdown
---
name: judge-auditor
description: Re-implements the judge's exact solutions from the written spec without reading the judge code, and compares results. Use in Phases 1 and 6.
tools: Read, Write, Edit, Bash, Glob, Grep
model: opus
hooks:
  PreToolUse:
    - matcher: "Read|Grep|Glob"
      hooks:
        - type: command
          command: 'python3 "$CLAUDE_PROJECT_DIR/.claude/hooks/guard_paths.py" --deny src/schemeforge/arenas/'
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: 'python3 "$CLAUDE_PROJECT_DIR/.claude/hooks/guard_paths.py" audit/'
---
Implement the exact solutions in audit/<arena>/ from docs/judge/<arena>_spec.md and textbook formulas only.
Do not read src/schemeforge/arenas/ in any way, including through shell commands.
Then get the judge's outputs with `uv run sforge judge exact --arena <A> --case <yaml> --json` on at least 1000
random admissible instances and compare.
Final message: max relative difference per quantity, and the cause of every disagreement above 1e-10.
```

**`cheater.md`** (Phase 2 only)

```markdown
---
name: cheater
description: Red-team agent that tries to raise scores without improving the numerics. Use only in Phase 2 red-team runs.
tools: Read, Write, Edit, Bash, Glob, Grep
model: opus
hooks:
  PreToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: 'python3 "$CLAUDE_PROJECT_DIR/.claude/hooks/guard_paths.py" candidates/redteam/'
---
Goal: reach the highest possible dev and promo scores with candidates that are NOT better numerics. Examples:
detecting known test data, exploiting NaN handling or tolerances, hidden state, batch-order tricks, metric
loopholes. Stay inside the slot's file interface and write only in candidates/redteam/.
For each strategy record: the idea, the code, the scores reached, and whether a judge check caught it.
Final message: all strategies, including the ones that failed.
```

---

## Appendix C: Hook and settings

**`.claude/hooks/guard_paths.py`**

```python
#!/usr/bin/env python3
"""PreToolUse guard for schemeforge subagents.

  guard_paths.py PREFIX [PREFIX ...]   allow file tools only inside these repo-relative prefixes
  guard_paths.py --deny PREFIX [...]   block file tools that touch these prefixes

Reads the hook JSON from stdin. Exit code 2 blocks the call and shows stderr to the agent.
"""
import json
import os
import sys


def inside(rel: str, prefix: str) -> bool:
    prefix = prefix.rstrip("/")
    return rel == prefix or rel.startswith(prefix + "/")


def main() -> int:
    data = json.load(sys.stdin)
    tool = data.get("tool_name", "")
    ti = data.get("tool_input") or {}
    root = os.path.realpath(os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or os.getcwd())
    raw = ti.get("file_path") or ti.get("notebook_path") or ti.get("path") or "."
    path = os.path.realpath(os.path.join(root, os.path.expanduser(raw)))
    rel = os.path.relpath(path, root).replace(os.sep, "/")
    args = sys.argv[1:]

    if args[:1] == ["--deny"]:
        for p in args[1:]:
            # A Grep/Glob rooted above the denied folder would read it too.
            above = tool in ("Grep", "Glob") and (rel == "." or inside(p.rstrip("/"), rel))
            if inside(rel, p) or above:
                print(f"Blocked: {rel} is off-limits for this agent ({p}).", file=sys.stderr)
                return 2
        return 0

    if rel.startswith("..") or not any(inside(rel, p) for p in args):
        print(f"Blocked: this agent may only write under {', '.join(args)} (tried {rel}).", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

**`.claude/settings.json`**

```json
{
  "permissions": {
    "allow": [
      "Bash(uv run sforge *)",
      "Bash(uv run pytest *)",
      "Bash(uv run ruff *)",
      "Bash(uv run python *)",
      "Bash(git status *)",
      "Bash(git diff *)",
      "Bash(git log *)"
    ],
    "deny": [
      "Read(~/.schemeforge/**)",
      "Edit(~/.schemeforge/**)"
    ]
  }
}
```

Check in `/permissions` that the rules resolve as intended. `Bash(uv run python *)` is broad; remove it if you'd rather approve analysis scripts one by one. The deny rules cover Claude's file tools, not every shell command. The judge's integrity check (§5.6) is the backstop.

---

## Appendix D: Hunch-round workflow

Run the first rounds from the main session, starting the subagents yourself in this order. Once a round has worked, write the procedure down as the project skill `.claude/skills/hunch-round/SKILL.md`; a saved workflow is an option later if the repetition pays off. Invocation, e.g.:

> run one hunch round as described in docs/PLAN.md Appendix D, with args {arena: "euler1d", slot: "limiter", n_hunches: 6, lenses: ["steady-convergence", "structure preservation", "contrarian"], evals_per_proposer: 8, islands: 3, gens: 20, children: 8, top_k_break: 5, date: "YYYY-MM-DD"}

The round follows this logic. It is pseudo-code, not an exact API:

```text
phase "hunches"
  drafts  = agent[hunch-generator]("Write {n_hunches} hunch drafts for {arena}/{slot}, lenses {lenses}.",
                                   schema {drafts: [path]})
  ids     = agent("Validate each draft against ledger/schema.yaml and register it with `sforge hunch add`.",
                  schema {ids: [string]})
phase "proposals"
  results = pipeline(ids, h => agent[proposer]("Implement hunch {h} for slot {slot}; at most {evals_per_proposer} evaluations.",
                                               schema {hunch, best_path, dev_run_id, predicted_effect_seen, summary}))
phase "evolve"
  best    = agent("From these results and `sforge leaderboard --pareto --vs-zoo --json`, pick the {islands} most promising hunches.",
                  schema {hunches: [string]})
  agent("Run `sforge evolve --arena {arena} --slot {slot} --hunch {best} --gens {gens} --children {children}` and summarize.",
        schema {archive_delta, new_pareto: [string]})
phase "break"
  top     = agent("Run `sforge leaderboard --arena {arena} --slot {slot} --pareto --top {top_k_break} --json`; return the ids.",
                  schema {ids: [string]})
  parallel(top.map(c => agent[breaker]("Break candidate {c}.", schema {id, breaking_cases: [path], notes})))
phase "summary"
  agent("Write docs/rounds/{date}-{arena}-{slot}.md: hunches with suggested verdicts, leaderboard delta,
         quarantined cases, open questions for Peter. Return the path.")
```

Notes:
- Agents do all the I/O; the date comes in through the args.
- If `sforge evolve` runs long, run it from the main session in the background.

---

## Appendix E: Engine prompt templates

**System prompt**

```text
You improve one component of a numerical scheme. You see a contract, a hunch, parent code and evaluation reports.
Return JSON only, matching the schema. The code must satisfy the contract exactly: pure jax.numpy / jax.lax / math,
no I/O, no hidden state, no Python loops over cells, deterministic. Do not special-case particular test inputs:
held-out cases are drawn from families you have not seen.
```

**User template**

```text
## Contract ({arena}/{slot})
{contract_text}

## Hunch {hunch_id}
{statement}
Mechanism: {mechanism}
Predicted effect: {predicted_effect}

## Parent(s)
{for each parent: the code, then the dev report summary — per-case metrics vs zoo, hard-constraint notes,
 failure signatures, with the two worst metrics marked}

## Archive context
{2–3 diverse elites: one-line description and key metrics each}

## Task: {operator}
{operator_instruction}

Return {"code": "<full file>", "rationale": "<at most 3 sentences>", "expected_change": "<metric: direction, size>"}
```

**Operator instructions**

| Operator | Instruction |
|---|---|
| refine | Improve the parent's two worst metrics (marked) without regressing any other metric by more than 5 %. Change one idea. |
| crossover | Combine parent A's mechanism with the strength of parent B described in its report. Explain the combination. |
| explore | Implement the hunch in a way that differs from every archive member listed. |
| simplify | Keep the behavior (scores within 1 %) with fewer lines and branches. |
| wild (cheap model) | Try an unusual variation that still satisfies the contract. |

**Output schema** (for `--json-schema` or the SDK)

```json
{"type": "object",
 "required": ["code", "rationale", "expected_change"],
 "properties": {"code": {"type": "string"},
                "rationale": {"type": "string"},
                "expected_change": {"type": "string"}},
 "additionalProperties": false}
```

---

## Appendix F: Dossier template (`dossiers/<id>/README.md`)

```markdown
# <candidate id> — <one-line description>
Label: rediscovery | variant of <X> | plausibly new · Referee: <verdict, date>
Arena/slot: … · Hunch: H-… · Lineage: … · Judge: <arena>-vX.Y (<hash>)

## Result vs zoo (held-out, paired bootstrap, n = …)
| Metric | Candidate | Best zoo (name) | Ratio [95 % CI] | Threshold | Met |
|---|---|---|---|---|---|

## Mechanism
Plain words; every claim backed by a run id or a script in analysis/.

## Properties
Proved / numerically checked / conjectured — one list each.

## Failure cases and limits
Breaker results, including cases that break the zoo too.

## Closest literature
Up to 5 entries with links and the precise difference.

## Reproduce
Exact commands.

## Code
```

---

## Appendix G: Session prompts

**Session 1 (Phase 0)**

```text
Read docs/PLAN.md completely. We are starting Phase 0 (§8).
Work through the Phase 0 tasks in order: the layout (§5.3); pyproject with pinned dependencies (§5.4); the files
in Appendices A–C verbatim (adapt only what doesn't fit, and note it in docs/DECISIONS.md); the sforge CLI
skeleton (§5.5); the sandbox validator with hostile-snippet tests (§5.6); the registry schema; docs/STATUS.md
and docs/DECISIONS.md. Don't create the held-out seed yourself — give me the command.
Keep commits small. When done, show the Gate 0 checklist with evidence and stop.
```

**Every later session**

```text
Read docs/STATUS.md and the current phase in docs/PLAN.md. Work through that phase's tasks in order
(for a Phase 3 or 7 round, follow the round protocol in §11.3 with the target named in STATUS.md).
Update docs/STATUS.md at the end, and stop at the phase gate with the checklist and evidence.
```

---

## Appendix H: Verified reference values

These were recomputed on 2026-10-20 with an independent script. Primitive states are (ρ, u, p) and γ = 1.4.

| Quantity | Value |
|---|---|
| Toro test 1 (Sod): (1, 0, 1) / (0.125, 0, 0.1) | p* = 0.30313, u* = 0.92745 |
| Toro test 2 (123): (1, −2, 0.4) / (1, 2, 0.4) | p* = 0.00189, u* = 0 |
| Toro test 3: (1, 0, 1000) / (1, 0, 0.01) | p* = 460.894, u* = 19.5975 |
| Toro test 4: (1, 0, 0.01) / (1, 0, 100) | p* = 46.0950, u* = −6.19633 |
| Toro test 5: (5.99924, 19.5975, 460.894) / (5.99242, −6.19633, 46.0950) | p* = 1691.64, u* = 8.68975 (±1 in the last digit) |
| Anderson nozzle A(x) = 1 + 2.2 (x − 1.5)², x ∈ [0, 3] | A_e/A_t = 5.95 |
| p_crit1/p0, the limit of subsonic choked flow | 0.99333 (M_e = 0.09782) |
| p_crit2/p0, normal shock at the exit | 0.20854 |
| p_crit3/p0, design condition | 0.016046 (M_e = 3.35897) |
| p_b/p0 = 0.6784 (Anderson's shock-capturing case) | x_s = 2.0993, M1 = 2.0700, p02/p01 = 0.68817, M_e = 0.14308 |
| Oblique shock, M1 = 5, θ = 15° | β = 24.322°, p2/p1 = 4.7808, M2 = 3.5040 |
| 2D Hertz (plane strain), P = E* = R = 1 | a = 1.12838, p0 = 0.56419; ∫p dx = 1 |
| Cattaneo–Mindlin 2D, Q/(μP) = 0.5 | c/a = 0.70711; ∫q dx = Q |
| Hertz impact contact time | t_c = 2.868 (m²/(R E*² v))^(1/5); numerical integration gives a constant of 2.8683 |
| Hertz impact max approach | δ_max = (15 m v² / (16 E* √R))^(2/5) |
| 1D impact of identical bars, speed v | contact stress ρcv/2, duration 2L/c, velocities swap |
| Speed of sound at 300 K | N₂ 353 m/s, He 1019 m/s, H₂ 1318 m/s |

---

## Appendix I: References

Verify these before citing. Entries without a link are from memory.

**Method and harness**
- AlphaEvolve: A coding agent for scientific and algorithmic discovery (2025). https://arxiv.org/abs/2506.13131
- Mathematical exploration and discovery at scale (2025). https://arxiv.org/abs/2511.02864
- Xie, Y. (2026). What the Machine Invented: Mining New Mathematical Instruments from OpenAI's October 2026 Release of AI-Generated Mathematics. https://arxiv.org/abs/2610.17090
- OpenEvolve. https://pypi.org/project/openevolve/ · ShinkaEvolve: https://arxiv.org/abs/2509.19349
- Claude Code documentation: subagents, dynamic workflows, headless mode. https://code.claude.com/docs/en/sub-agents · https://code.claude.com/docs/en/workflows · https://code.claude.com/docs/en/headless

**Arena 1**
- Toro, E. F. (2009). *Riemann Solvers and Numerical Methods for Fluid Dynamics*, 3rd ed. Springer.
- Anderson, J. D. (1995). *Computational Fluid Dynamics: The Basics with Applications*. McGraw-Hill (quasi-1D nozzle).
- Sweby, P. K. (1984). High resolution schemes using flux limiters for hyperbolic conservation laws. *SIAM J. Numer. Anal.* 21.
- van Albada, G. D., van Leer, B., Roberts, W. W. (1982). A comparative study of computational methods in cosmic gas dynamics. *Astron. Astrophys.* 108.
- Venkatakrishnan, V. (1995). Convergence to steady state solutions of the Euler equations on unstructured grids with limiters. *J. Comput. Phys.* 118.
- Harten, A. (1989). ENO schemes with subcell resolution. *J. Comput. Phys.* 83.
- Shu, C.-W., Osher, S. (1989). Efficient implementation of essentially non-oscillatory shock-capturing schemes II. *J. Comput. Phys.* 83.
- Quirk, J. J. (1994). A contribution to the great Riemann solver debate. *Int. J. Numer. Meth. Fluids* 18.
- Jin, S., Liu, J.-G. (1996). The effects of numerical viscosities I: slowly moving shocks. *J. Comput. Phys.* 126.
- Guermond, J.-L., Pasquetti, R., Popov, B. (2011). Entropy viscosity method for nonlinear conservation laws. *J. Comput. Phys.* 230.
- Zhang, X., Shu, C.-W. (2010). On positivity-preserving high order discontinuous Galerkin schemes for compressible Euler equations on rectangular meshes. *J. Comput. Phys.* 229.
- Kröner, D., Thanh, M. D. (2005). Numerical solutions to compressible flows in a nozzle with variable cross-section. *SIAM J. Numer. Anal.* 43.
- Henderson, C. B. (1976). Drag coefficients of spheres in continuum and rarefied flows. *AIAA J.* 14.

**Arena 2 and the Latent-FEA bridge**
- Wriggers, P., Schröder, J., Schwarz, A. (2013). A finite element method for contact using a third medium. *Comput. Mech.* 52.
- Bluhm, G. L., Sigmund, O., Poulios, K. (2021). Internal contact modeling for finite strain topology optimization. *Comput. Mech.* 67.
- A robust mixed finite element formulation for third medium contact (2026). https://arxiv.org/abs/2606.28036
- Three-dimensional third medium contact model for hyperelastic contact and pneumatically actuated systems. https://arxiv.org/abs/2512.03181
- Third medium finite element contact formulation for pneumatically actuated systems. https://arxiv.org/abs/2405.01185
- Adding friction to Third Medium Contact: A crystal plasticity inspired approach (cited in the two preceding papers).
- FElupe documentation, example "Third Medium Contact". https://felupe.readthedocs.io
- Johnson, K. L. (1985). *Contact Mechanics*. Cambridge University Press (Hertz, Cattaneo–Mindlin).
- Taylor, R. L., Papadopoulos, P. (1991). On a patch test for contact problems in two dimensions.
- Li, M. et al. (2020). Incremental Potential Contact. *ACM Trans. Graph.* 39(4).
- Oden, J. T., Martins, J. A. C. (1985). Models and computational methods for dynamic friction phenomena. *Comput. Methods Appl. Mech. Eng.* 52.
- Flanagan, D. P., Belytschko, T. (1981). A uniform strain hexahedron and quadrilateral with orthogonal hourglass control. *Int. J. Numer. Meth. Eng.* 17.
- Beirão da Veiga, L. et al. (2013). Basic principles of virtual element methods. *Math. Models Methods Appl. Sci.* 23.
