import csv
import os

class MetricsEngine:
    def __init__(self):
        os.makedirs('results/csv', exist_ok=True)
        self.file = 'results/csv/metrics.csv'

        with open(self.file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['step','throughput','failure_rate','recovery'])

    def log(self, step, throughput, failure_rate, recovery):
        with open(self.file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([step, throughput, failure_rate, recovery])
