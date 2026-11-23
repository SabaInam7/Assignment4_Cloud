import csv
import os
import matplotlib.pyplot as plt

rates = [10, 25, 50, 100, 200]
replicas = [1, 2, 3]

success_rates = {r: [] for r in replicas}
avg_latencies = {r: [] for r in replicas}

for r in replicas:
    for q in rates:
        filename = f"results/fixed_r{r}_q{q}.csv"

        with open(filename) as f:
            rows = list(csv.DictReader(f))

        total = len(rows)
        successful = [x for x in rows if x["status"] == "200"]

        success_rate = (len(successful) / total * 100) if total else 0
        latencies = [
            float(x["latency_ms"])
            for x in successful
            if x["latency_ms"]
        ]
        avg_latency = sum(latencies) / len(latencies) if latencies else 0

        success_rates[r].append(success_rate)
        avg_latencies[r].append(avg_latency)

os.makedirs("graphs", exist_ok=True)

for r in replicas:
    plt.plot(rates, success_rates[r], marker="o", label=f"{r} replicas")

plt.xlabel("Request Rate")
plt.ylabel("Successful Requests (%)")
plt.title("Success Rate vs Request Rate")
plt.legend()
plt.grid(True)
plt.savefig("graphs/success_rate.png", dpi=300)
plt.close()

for r in replicas:
    plt.plot(rates, avg_latencies[r], marker="o", label=f"{r} replicas")

plt.xlabel("Request Rate")
plt.ylabel("Average Latency (ms)")
plt.title("Average Latency vs Request Rate")
plt.legend()
plt.grid(True)
plt.savefig("graphs/average_latency.png", dpi=300)
plt.close()

print("Graphs generated successfully!")
print("graphs/success_rate.png")
print("graphs/average_latency.png")
