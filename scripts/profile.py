import argparse, subprocess, csv, time, psutil, os
from datetime import datetime, timezone

p = argparse.ArgumentParser()
p.add_argument("--duration", type=int, default=60)
p.add_argument("--prefix", required=True)
a = p.parse_args()

os.makedirs("results", exist_ok=True)

host_file = a.prefix + "_host.csv"
pod_file = a.prefix + "_pods.csv"

start = time.monotonic()
next_pod = start

with open(host_file, "w", newline="") as hf, open(pod_file, "w", newline="") as pf:
    hw = csv.writer(hf)
    pw = csv.writer(pf)
    hw.writerow(["timestamp", "host_cpu_percent"])
    pw.writerow(["timestamp", "pod", "cpu", "memory"])

    while time.monotonic() - start < a.duration:
        timestamp = datetime.now(timezone.utc).isoformat()
        cpu = psutil.cpu_percent(interval=1)
        hw.writerow([timestamp, cpu])
        hf.flush()

        if time.monotonic() >= next_pod:
            try:
                result = subprocess.run(
                    ["kubectl", "top", "pods"],
                    capture_output=True, text=True, timeout=3
                )
                for line in result.stdout.strip().splitlines()[1:]:
                    fields = line.split()
                    if len(fields) >= 3:
                        pw.writerow([timestamp, fields[0], fields[1], fields[2]])
                pf.flush()
            except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
                print("Pod metrics unavailable; continuing host profiling")
            next_pod += 15

print("Profiling complete:", host_file, pod_file)
