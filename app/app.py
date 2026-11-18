"""Sample batch application used in the Jobs/CronJobs lab.

It simulates a small "daily sales report" task: it generates 1000 random
orders, prints summary statistics and exits.  Setting the environment
variable FAIL=true makes it exit with status 1 so that the retry
behaviour of a Kubernetes Job can be observed.
"""
import os
import random
import socket
import sys
import time
from datetime import datetime

print(f"[{datetime.now()}] Batch app started on pod {socket.gethostname()}")

if os.getenv("FAIL") == "true":
    print("ERROR: simulated failure")
    sys.exit(1)

orders = [random.randint(100, 5000) for _ in range(1000)]
print(f"Processing {len(orders)} orders...")
time.sleep(5)
print(f"Total sales   : {sum(orders)}")
print(f"Average order : {sum(orders) / len(orders):.2f}")
print(f"Largest order : {max(orders)}")
print("Report generated successfully")
