# Breaker report: c-140c60abbe (H-0013 island, g014_004_simplify.py), euler1d / reconstruction_stateful, judge euler1d-v1.4

Breaker agent report, saved by the orchestrator. Claims are the agent's; run ids are from its own evals (dev suite
with the case). Three cases proposed (B-0034 … B-0036); none accepted; no code changed. Drafts B-16NN.

Baselines (dev): candidate r-20261023-223159-2b82, muscl_van_leer r-20261023-223331-05f8. Already on dev the candidate
is worse on implicit convergence: B-0011 implicit not converged, 300 Newton steps (van Leer converged, 123); N5
implicit 2/3, 155 steps (van Leer 3/3, 65).

## Proposed cases

| Quarantine | Draft | Candidate | van Leer | frozen vL | Other zoo |
|---|---|---|---|---|---|
| B-0034 | B-1626_cold_collision_p1e-5 | rejected, non-finite (r-20261023-234329-4940) | ok, l1 1.39e-3, tv 0.45, shock 0.97 (r-20261023-234500-cc56) | ok (r-20261023-234603-04a5) | — |
| B-0035 | B-1614_anderson_gamma12_dense | implicit 3/9 converged, mean 227 Newton; explicit 8/9 (r-20261023-231024-ad59) | implicit 9/9, 78.6; explicit 8/9 (r-20261023-231354-8461) | implicit 9/9, 78.4; explicit 7/9 (r-20261023-231501-3021) | — |
| B-0036 | B-1601_leblanc | contact 45 (never completes), overshoot 0.0198 (r-20261023-223623-1488) | 18.9, 0.0132 (r-20261023-224234-813e) | 18.9 (r-20261023-224439-42a8) | thinc_bvd 11.3 (r-20261023-224543-0871) |

## Details
- **B-0034**, planar Noh-type cold collision (1, 2, 1e-5)/(1, −2, 1e-5), γ 1.4, N 200, t 0.5 (stream Mach ≈ 535):
  NaN almost at once. Likely mechanism (code reading): projection with the cold centre cell's sound speed turns the
  velocity jump into acoustic amplitudes of ≈ ±900; separately limited, they no longer cancel in p + a²(a1 + a3), and
  the face pressure goes negative. p 1e-6 also crashes (B-1616, r-20261023-231658-ab59; not proposed, same mechanism);
  p 1e-3 and 1e-2 survive (r-20261023-232403-4f60, -232527-241f); single slow Mach 100 / 1000 shocks survive
  (r-20261023-234037-4b7b, -233916-3e18). thinc_bvd crashes at p 1e-6 (r-20261023-232033-c764) and already at 1e-3
  (r-20261023-232653-7987); weno5z survives 1e-6 (r-20261023-234215-7bbd).
- **B-0035**, Anderson nozzle γ 1.2, N 120, nine back pressures 0.95 … 0.55: Newton stalls at 300 for 6 of 9. Narrow:
  γ 1.1 / 1.25 / 1.3 / 1.4 / 5/3 converge (r-20261023-225826-f0af, -233719-e161, -230839-aa7c, -233033-4751,
  -233208-c961); γ 1.2 at N 240 converges with 147 steps (r-20261023-233519-14fa); parabolic and conical at γ 1.2
  converge (r-20261023-230540-bc40, -230710-5a2d). Same signature as dev B-0011 over a range of shock positions.
  Subset B-1607 also failed, 3/4 / 3/4 (r-20261023-225309-7569; vL 4/4 r-20261023-225450-a9b3, frozen
  r-20261023-225547-6226); not proposed, contained in B-0035.
- **B-0036**, LeBlanc: resolution-dependent — at N 800 (B-1609) candidate 19.6 vs van Leer 18.3
  (r-20261023-230005-d2ac, -230311-2aac). The agent says a stronger case should replace it.

## Tried without a failure (not proposed)
Near-vacuum 123 (r-20261023-223753-8baf); blast 1e7 (r-20261023-223923-fabb); slow Mach 20 shock, tv 0.27 vs 0.60,
overshoot 0.0081 vs 0.0151 (r-20261023-224055-5ca4 / -224331-937a); heavy/light tube, candidate better
(r-20261023-230135-38af / -230411-cc69); slow contact ~2000 steps, width 2.84 (r-20261023-233342-50c6); N5-geometry
parabolic sweeps, explicit 3/4 vs vL 1/4 (r-20261023-224934-ab37 / -225700-7b11) and all converged
(r-20261023-231211-6e35); Anderson N 240 all converged (r-20261023-225109-cff9).

Drafts: cases/quarantine/drafts/B-1601_*.yaml … B-1626_*.yaml.
