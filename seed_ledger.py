"""
seed_ledger.py – generates or replays experiment seeds
Usage:
    python seed_ledger.py         # writes seeds.json
"""
import json, time, random, os, sys

RNG = random.Random(42)           # deterministic seed for reproducibility
N   = 30                          # how many experiment runs

seeds = {f"run_{i}": RNG.randrange(2**32) for i in range(N)}
with open("seeds.json", "w") as f:
    json.dump(seeds, f, indent=2)
print("✓  wrote seeds.json with", N, "seeds")
