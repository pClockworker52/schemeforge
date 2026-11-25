#!/usr/bin/env bash
# Query the judge for every batch in audit/contact/cases/; answers in audit/contact/judge/, stderr in *.err.
set -u
cd /home/user/schemeforge
mkdir -p audit/contact/judge
for f in audit/contact/cases/batch_*.yaml; do
  b=$(basename "$f" .yaml)
  if [ -s "audit/contact/judge/$b.json" ]; then continue; fi
  start=$(date +%s)
  uv run --extra contact sforge judge exact --arena contact --case "$f" --json \
    > "audit/contact/judge/$b.json" 2> "audit/contact/judge/$b.err"
  echo "$b exit=$? $(( $(date +%s) - start ))s"
done
