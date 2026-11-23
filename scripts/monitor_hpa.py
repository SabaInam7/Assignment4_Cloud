import subprocess, json, csv, time
from datetime import datetime, timezone

with open("results/autoscaling_hpa.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["timestamp", "elapsed_seconds", "request_rate",
                "cpu_percent", "current_replicas", "desired_replicas"])

    start = time.monotonic()
    while time.monotonic() - start < 600:
        elapsed = int(time.monotonic() - start)

        if elapsed < 120:
            rate = 10
        elif elapsed < 420:
            rate = 100
        else:
            rate = 10

        try:
            raw = subprocess.check_output(
                ["kubectl", "get", "hpa", "emi-web", "-o", "json"],
                text=True
            )
            data = json.loads(raw)
            current = data.get("status", {}).get("currentReplicas", 0)
            desired = data.get("status", {}).get("desiredReplicas", 0)

            cpu = ""
            for metric in data.get("status", {}).get("currentMetrics", []):
                if metric.get("resource", {}).get("name") == "cpu":
                    cpu = metric["resource"]["current"].get(
                        "averageUtilization", ""
                    )

            w.writerow([
                datetime.now(timezone.utc).isoformat(),
                elapsed, rate, cpu, current, desired
            ])
            f.flush()
            print(elapsed, rate, cpu, current, desired)
        except Exception as e:
            print("Monitoring error:", e)

        time.sleep(15)
