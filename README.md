# Messy Python Code Improvement (AI-Assisted)

A practical case study project showcasing how messy, tightly-coupled legacy Python scripts can be systematically refactored using **AI assistance** into modular, readable, type-safe, and high-performance software.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![AI Assisted](https://img.shields.io/badge/AI-Assisted%20Refactoring-purple.svg)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

---

## 🎯 Motivation & Objectives

In production codebases, technical debt accumulates rapidly due to:
- Lack of type hints and input validation
- Global state mutations and magic numbers
- Sub-optimal complexity (e.g., $O(n^2)$ deduplication)
- Silent exception swallowing (`except: pass`)

This project provides side-by-side **Before vs After** comparisons refactored with AI prompting, highlighting the transformation of code smells into clean Pythonic architectures.

---

## 🔍 Case Studies

### 1. E-Commerce Billing Engine
- **Messy (`case_studies/ecommerce/messy_orders.py`)**:
  - Global variable mutations (`TOTAL`, `ITEMS`).
  - Cryptic variable names (`pr`, `p`, `q`, `d`).
  - Duplicated floating-point math leading to rounding inaccuracies.
- **Refactored (`case_studies/ecommerce/refactored_orders.py`)**:
  - Encapsulated immutable `@dataclass(frozen=True)` representations.
  - Strict input validation raising domain-specific exceptions.
  - Strategy Pattern with `Protocol` for discount calculations (`Save10`, `Save20`, `VIP`).
  - Precise monetary arithmetic using Python's `Decimal`.

### 2. Data Cleaning & ETL Pipeline
- **Messy (`case_studies/etl/messy_etl.py`)**:
  - Nested loops checking duplicates resulting in $O(n^2)$ time complexity.
  - Swallows all exceptions silently without logging.
- **Refactored (`case_studies/etl/refactored_etl.py`)**:
  - $O(n)$ hash-set deduplication.
  - Regex-based email verification and boundary validation.
  - Structured logging with `logging` module.

---

## 📊 Performance Benchmark Results

Run the benchmark comparing $O(n^2)$ nested iterations vs $O(n)$ set hashing on 4,000 records:

```bash
python benchmark.py
```

| Implementation | Time Complexity | 4,000 Records Runtime | Memory Profile |
| :--- | :--- | :--- | :--- |
| **Messy ETL** | $O(n^2)$ | ~0.428s | High allocations |
| **Refactored ETL** | $O(n)$ | ~0.012s | Constant overhead |
| **Speedup** | - | **~35x Faster** | Clean & Typed |

---

## 📂 Directory Structure

```text
messy-python-code-improvement/
├── case_studies/
│   ├── ecommerce/
│   │   ├── messy_orders.py
│   │   └── refactored_orders.py
│   └── etl/
│       ├── messy_etl.py
│       └── refactored_etl.py
├── benchmark.py
├── tests/
│   └── test_refactoring.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🧪 Running Tests

```bash
python -m unittest discover -s tests
```

---

## 👤 Author
**Neev Rupareliya**  
- B.Tech CSE Student, JECRC University  
- GitHub: [@Neev2850](https://github.com/Neev2850)  
- Portfolio: [personal-portfolio-mu-eosin-58.vercel.app](https://personal-portfolio-mu-eosin-58.vercel.app)
