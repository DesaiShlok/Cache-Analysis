# Cache Hierarchy Instrumentation & Analysis Tool

## Overview
A high-performance cache simulator and profiling suite built on the **Intel PIN** dynamic binary instrumentation framework. This tool captures runtime memory access traces (Loads/Stores) from arbitrary x86 executables and feeds them into a configurable cache model to characterize memory system behavior.

The project focuses on analyzing the "Three C's" of cache misses (Cold, Capacity, Conflict) and the impact of architectural parameters (Associativity, Block Size, Capacity) on application performance.

## Key Features
- **Dynamic Binary Instrumentation (DBI):** Uses Intel PIN to inject analysis routines into running binaries without recompilation, capturing accurate instruction-level memory traces.
- **Configurable Cache Model:**
  - **Associativity:** Fully configurable from Direct-Mapped (1-way) to Fully Associative.
  - **Block Size:** Supports variable cache line sizes (8B - 128B) to analyze spatial locality trade-offs.
  - **Replacement Policies:** Implements Least Recently Used (LRU) and Optimal (Belady's MIN) policies for comparative analysis.
- **Miss Classification:** Precisely categorizes misses into Cold, Capacity, Conflict, and Replacement types to identify performance bottlenecks.
- **Automated Visualization:** Python-based pipeline to generate sensitivity curves and miss distribution histograms.

## Technical Architecture
* **Instrumentation Engine:** Intel PIN (C++)
* **Simulation Logic:** C++ (LRU/Optimal algorithms)
* **Analysis & Visualization:** Python (Matplotlib, Pandas)
* **Workloads:** Matrix Multiplication (spatial/temporal locality tests), Linked List (pointer chasing), HashMap (scattered access).

## Repo Structure
├── src/
│   ├── cache.cpp           # Intel PIN tool & cache simulation logic
│   ├── workloads/          # Test binaries (MatrixMult, LinkedList, HashMap)
│   └── utils/              # Helper macros for address manipulation
├── scripts/
│   ├── run_sensitivity.sh  # Automation script for parameter sweeps
│   └── plot_results.py     # Visualization generation
├── results/                # Generated miss rate data and graphs
├── Makefile                # Build configuration
└── README.md               # Documentation

## Performance Insights
### 1. The "Working Set" Inflection Point
Analysis of a 48KB matrix multiplication working set revealed a sharp "Capacity Wall."
* **< 48KB Cache:** 98% Miss Rate (Capacity Thrashing).
* **> 64KB Cache:** < 1% Miss Rate (Working set fits entirely in cache).
* **Takeaway:** Demonstrates the critical importance of sizing cache to fit the application's hot working set.

### 2. Associativity & Conflict Misses
* **Direct-Mapped (1-way):** High conflict miss rate (14%) due to aliasing of matrix rows to the same cache sets.
* **2-Way Associative:** Conflict misses drop to near zero (< 0.5%).
* **Takeaway:** Even minimal associativity (2-way) eliminates the majority of conflict misses in strided access patterns.

### 3. Block Size & Cache Pollution
* **Small Blocks (8B):** High cold misses due to poor spatial prefetching.
* **Large Blocks (128B):** Increased conflict misses due to "Cache Pollution" — loading unused neighbors evicts useful data in column-major traversals.
* **Optimal:** 32B-64B block size balanced spatial locality with pollution risks.

## Usage
### 1. Build the Pin Tool
```bash
make
```
*This Project Summary is AI generated, for deeper insights on the projects technical details reach out to me at sbd2150@columbia.edu*


