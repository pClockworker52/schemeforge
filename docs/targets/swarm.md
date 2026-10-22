# Swarm criterion: does the agent layer add value? (pre-registered)

Pre-registered 2026-10-22, before round 3 and before any hunch-generator, proposer or breaker run (PLAN §11.5,
step 3b). Rounds 1 and 2 were run by the orchestrator alone (docs/rounds/2026-10-21-euler1d-limiter.md), so the
thesis of PLAN §1, that an agent swarm searches better than one session doing the same work by hand, has not been
tested. This file fixes how round 3 tests it. It is judged at the step 3e gate, separately from Target A: a
negative answer here is a result about the method, not about the numerics.

## What counts as agent work

- **Agent hunch:** a ledger entry whose `author` starts with `hunch-generator/`, registered before any of its
  candidates is evaluated.
- **Agent candidate:** a registry candidate with `origin` = `proposer` or `engine`, under an agent hunch.
- The orchestrator may register, run and summarize, but must not edit agent hunches or candidates. If it has to
  (a broken draft), the entry counts as orchestrator work.

## Criterion

The swarm **adds value** in round 3 if both hold:

- **S1, new ideas.** At least one agent hunch is not a parameter sweep of an earlier hunch. A hunch is a sweep
  when its mechanism is one already registered (H-0001…H-0011) and only constants or the base limiter change. Peter
  decides at the gate from the ledger text. The round summary lists each agent hunch with its nearest earlier
  hunch and a one-line difference.
- **S2, the engine improves on its seeds.** At least one engine island ends with an elite that (a) is
  non-dominated against its island seed on the dev objectives of its slot (`engine/objectives.py`) and better on
  at least one, and (b) is not worse than the seed on promo: for each of A1–A5 and A7 (docs/targets/A.md), the
  elite's family statistic is within 2 % of the seed's or better.

**Fails** if S1 or S2 does not hold. Record the outcome in the round summary, and as a ledger hunch closed with
the evidence (author `orchestrator/method`), like any other negative result.

## Numbers to report either way

So the next round can be compared with rounds 1 and 2:

| Quantity | Round 1 (orchestrator) | Round 3 (agents) |
|---|---|---|
| hunches registered / refuted / inconclusive / supported | 4 / 3 / 1 / 0 | |
| engine children / duplicates | 48 / 6 | |
| islands whose elite meets S2 | not measured (the H-0003 wild child c-44f8015f87 was sharper than its seed but rougher on N4) | |
| list price per 100 candidates | $5.6 | |
| cases quarantined by breakers | 0 (breaker not run) | |

## Not part of the criterion

Promotion on Target A, novelty labels, and wall-clock time. A swarm that adds value can still fail Target A.
