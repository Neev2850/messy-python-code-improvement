"""
Benchmark Module: Comparing Messy vs Refactored Code Performance
Demonstrates the massive runtime improvements between O(n^2) and O(n) deduplication.
"""

import time
import random
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from case_studies.etl.messy_etl import cln as messy_cleaner
from case_studies.etl.refactored_etl import clean_user_records


def generate_mock_data(n: int = 5000):
    first_names = ["Aarav", "Priya", "Rahul", "Ananya", "Rohan", "Sneha", "Neev", "Vikram", "Neha", "Aditya"]
    last_names = ["Sharma", "Verma", "Rupareliya", "Gupta", "Patel", "Mehta", "Singh", "Kumar"]
    domains = ["gmail.com", "yahoo.com", "outlook.com", "jecrc.ac.in"]

    data = []
    for i in range(n):
        fn = random.choice(first_names)
        ln = random.choice(last_names)
        # Induce duplicates every ~5th record
        email_prefix = f"{fn.lower()}.{ln.lower()}{i % 400}"
        data.append({
            "name": f"  {fn} {ln}  ",
            "email": f"  {email_prefix}@{random.choice(domains)}  ",
            "age": random.randint(15, 80)
        })
    return data


def run_benchmark():
    print("=" * 60)
    print("       BENCHMARK: MESSY O(n^2) VS REFACTORED O(n) ETL")
    print("=" * 60)
    test_size = 4000
    print(f"Generating {test_size} records with deliberate duplicates and whitespace...")
    dataset = generate_mock_data(test_size)

    # 1. Messy Cleaner
    start = time.perf_counter()
    messy_results = messy_cleaner(dataset)
    messy_time = time.perf_counter() - start
    print(f"\n[Messy O(n^2)] Output Records: {len(messy_results)}")
    print(f"[Messy O(n^2)] Elapsed Time:   {messy_time:.4f} seconds")

    # 2. Refactored Cleaner
    start = time.perf_counter()
    refactored_results, dropped = clean_user_records(dataset)
    refactored_time = time.perf_counter() - start
    print(f"\n[Refactored O(n)] Output Records: {len(refactored_results)} (Dropped: {dropped})")
    print(f"[Refactored O(n)] Elapsed Time:   {refactored_time:.4f} seconds")

    speedup = messy_time / refactored_time if refactored_time > 0 else 1.0
    print("-" * 60)
    print(f"🚀 Speedup Factor: {speedup:.2f}x faster execution!")
    print("=" * 60)


if __name__ == "__main__":
    run_benchmark()
