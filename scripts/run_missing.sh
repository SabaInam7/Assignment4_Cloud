#!/bin/bash
set -e
mkdir -p results

for replicas in 1 2 3; do
  kubectl scale deployment emi-web --replicas="$replicas"
  kubectl rollout status deployment/emi-web --timeout=180s

  for rate in 10 25 50 100 200; do
    prefix="results/fixed_r${replicas}_q${rate}"

    if [ -s "${prefix}.csv" ]; then
      echo "Skipping existing: ${prefix}.csv"
      continue
    fi

    echo "Running: replicas=$replicas rate=$rate"

    python3 scripts/profile.py --duration 60 --prefix "$prefix" &
    PROF=$!

    python3 scripts/loadgen.py --rate "$rate" --duration 60 --out "${prefix}.csv"

    wait "$PROF"
  done
done

kubectl scale deployment emi-web --replicas=3
kubectl rollout status deployment/emi-web
echo "ALL 15 EXPERIMENTS FINISHED"
