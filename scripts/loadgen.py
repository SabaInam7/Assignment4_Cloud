import argparse, urllib.request, urllib.error
import json, random, time, csv
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor

URL = "http://emi.local/api/emi"

def send_request():
    payload = {
        "P": random.randint(100000, 5000000),
        "rate": random.randint(1, 20),
        "n": random.randint(12, 360)
    }
    body = json.dumps(payload).encode()
    start = time.perf_counter()
    stamp = datetime.now(timezone.utc).isoformat()
    try:
        req = urllib.request.Request(
            URL, data=body,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=15) as response:
            result = json.loads(response.read().decode())
            status = response.status
            served = result.get("servedBy", "")
            error = ""
    except Exception as e:
        status, served, error = 0, "", str(e)

    latency = (time.perf_counter() - start) * 1000
    return stamp, status, latency, served, error

def run_phase(pool, rate, duration, futures):
    interval = 1.0 / rate
    end = time.monotonic() + duration
    next_request = time.monotonic()

    while time.monotonic() < end:
        futures.append(pool.submit(send_request))
        next_request += interval
        delay = next_request - time.monotonic()
        if delay > 0:
            time.sleep(delay)

parser = argparse.ArgumentParser()
parser.add_argument("--rate", type=int)
parser.add_argument("--duration", type=int, default=60)
parser.add_argument("--out", required=True)
parser.add_argument("--phases")
args = parser.parse_args()

futures = []
with ThreadPoolExecutor(max_workers=200) as pool:
    if args.phases:
        for phase in args.phases.split(","):
            rate, duration = map(int, phase.split(":"))
            run_phase(pool, rate, duration, futures)
    else:
        run_phase(pool, args.rate, args.duration, futures)

    rows = [f.result() for f in futures]

with open(args.out, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["timestamp", "status", "latency_ms", "servedBy", "error"])
    writer.writerows(rows)

success = sum(1 for r in rows if 200 <= r[1] < 300)
print("Total requests:", len(rows))
print("Successful:", success)
print("Failed:", len(rows)-success)
print("Average response time (ms):",
      round(sum(r[2] for r in rows)/len(rows), 2) if rows else 0)
print("Saved:", args.out)
