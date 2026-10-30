#!/bin/bash
# After a judge bump (PLAN §2 rule 2): tests, judge self-check, zoo dev + promo, then re-evaluate every non-zoo
# candidate of the given slot on dev under the new judge, P at a time.
#   bash scripts/rescore.sh <slot> [P]
# SKIP_ZOO=1 skips the tests, judge check and zoo evaluation (when rescoring a second slot after the first).
set -u
slot="$1"; P="${2:-6}"
cd "$(dirname "$0")/.."
S=.venv/bin/sforge
if [ "${SKIP_ZOO:-0}" != 1 ]; then
    .venv/bin/pytest -q 2>&1 | tail -1
    $S judge verify --arena euler1d 2>&1 | tail -1
    $S zoo eval --arena euler1d --suite dev 2>&1 | grep -v -e CUDA -e bogus | tail -20
    $S zoo eval --arena euler1d --suite promo 2>&1 | grep -v -e CUDA -e bogus | tail -3
fi
.venv/bin/python - "$slot" <<'PY' > runs/rescore_ids.txt
import sqlite3, sys
c = sqlite3.connect("runs/registry.sqlite")
for (cid,) in c.execute("SELECT id FROM candidates WHERE slot = ? AND origin != 'zoo'", (sys.argv[1],)):
    print(cid)
PY
echo "rescoring $(wc -l < runs/rescore_ids.txt) candidates"
xargs -P "$P" -I{} sh -c "$S eval {} --arena euler1d --slot $slot --suite dev > /dev/null 2>&1; echo {} \$?" \
    < runs/rescore_ids.txt | awk '{n[$2]++} END {for (k in n) print "exit " k ": " n[k]}'
