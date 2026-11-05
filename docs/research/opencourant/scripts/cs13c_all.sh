#!/bin/bash
# CS-13c campaign driver (coldspray-hunch-cs13c.md): pass 1 (24 runs + 3 noheat runs, reported only), then pass 2
# (the 24 runs again to t_c, for P2 and P3). R/48 first; budget stop: any R/48 run over 1 h of engine time stops
# the campaign before the rest (exit code 3). Run detached: setsid nohup bash cs13c_all.sh <work> > log 2>&1 &
set -u
W=${1:-$HOME/oc_runs/cs13c/runs}
HERE=$(cd "$(dirname "$0")" && pwd)
PY=/mnt/c/Users/peter/schemeforge/.venv/bin/python
P1=$W/pass1.csv
P2=$W/pass2.csv
mkdir -p "$W"
export THREADS=${THREADS:-8}

done1() { [ -f "$P1" ] && grep -q "^C$1$(printf %02d "$2")v$(printf %04d "$3")," "$P1"; }
done2() { [ -f "$P2" ] && grep -q "^C$1$(printf %02d "$2")v$(printf %04d "$3")tc," "$P2"; }

budget() {  # engine seconds of the last R/48 row
  $PY - "$P1" <<'EOF'
import csv, sys
rows = [r for r in csv.DictReader(open(sys.argv[1])) if r["n_r"] == "48"]
sys.exit(3 if rows and float(rows[-1].get("engine_s") or 0) > 3600 else 0)
EOF
}

for V in 800 500 1100; do
  for T in k237 k0; do
    done1 $T 48 $V && continue
    echo "pass1 $T R/48 $V $(date)"
    $PY "$HERE/cs13c.py" run "$W" "$P1" $T 48 $V
    budget || { echo "BUDGET STOP: an R/48 run took more than 1 h $(date)"; exit 3; }
  done
done
for N in 32 24 16; do
  for V in 500 800 1100; do
    for T in k237 k0; do
      done1 $T $N $V && continue
      echo "pass1 $T R/$N $V $(date)"
      $PY "$HERE/cs13c.py" run "$W" "$P1" $T $N $V
    done
  done
done
for V in 500 800 1100; do
  done1 noheat 16 $V || { echo "pass1 noheat R/16 $V $(date)"; $PY "$HERE/cs13c.py" run "$W" "$P1" noheat 16 $V; }
done
echo "PASS1 DONE $(date)"
for N in 16 24 32 48; do
  for V in 500 800 1100; do
    for T in k237 k0; do
      done2 $T $N $V && continue
      echo "pass2 $T R/$N $V $(date)"
      $PY "$HERE/cs13c.py" tc "$W" "$P1" "$P2" $T $N $V
    done
  done
done
echo "ALL DONE $(date)"
