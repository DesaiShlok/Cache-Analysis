# Cache Simulation Analyzer
# this script runs the cacheSim with multiple configurations and collects the results to store it into a CSV file
import subprocess
import csv
import os
import re
import itertools
import time
from datetime import datetime
import shutil
import sys
import platform
import psutil
import multiprocessing
import statistics
import argparse
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict
from tabulate import tabulate

# Function to run the cache simulator with given parameters
def run_cache_simulator(cache_size, block_size, associativity, replacement_policy, prefetcher):
    pin_root = "/users/sbd2150/HW2/pin-external-3.31-98869-gfa6f126a8-gcc-linux"
    pin_tool = "/users/sbd2150/HW2/gitConn/CompArch_HW2/cacheSim/obj-intel64/cache.so"
    command = [
        f"{pin_root}/pin",
        "-t", pin_tool,
        "-dl1_c", str(cache_size),      # Cache size in KB
        "-b", str(block_size),          # Block size in bytes
        "-dl1_a", str(associativity),   # Associativity
        # Note: replacement_policy and prefetcher may need different parameter names
        # For now, we'll include them as comments since they're not clear from the help
        "--", "./matrixMultSimple"  # The target program to analyze
    ]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        # The cache statistics are printed to stderr, not stdout
        output = result.stderr + result.stdout
        return output
    except subprocess.CalledProcessError as e:
        print(f"Error running cacheSim with parameters {command}: {e}")
        print(f"stderr: {e.stderr}")  # Debug: show error output
        return None     
# Function to parse the output of the cache simulator
# the format of the output is assumed to be:
# L1 Data (config)         Size: 32(KB)    Line size: 64(B)        Associativity: 8        Num sets: 64
# Matrix multiplication complete
# L1 Data (hit/miss)       Instructions: 53572514  References: 15264597    Miss rate: 0.0044       MPKI: 1.2592
#       Total         Cold     Capacity      Mapping  Replacement
#       67456         3170        16022         2057        46207
# create a CSV file after parsing the output with the first row as the info on L1 Data (config)
# the second row as the info on L1 Data (hit/miss)
# the third row as the info on Total, Cold, Capacity, Mapping, Replacement
def parse_cache_simulator_output(output):
    lines = output.strip().split('\n')
# Removed debug output
    
    if len(lines) < 6:  # Need at least 6 lines based on the actual format
        print("Unexpected output format from cacheSim")
        return None

    try:
        # Find the config line (line 0)
        config_line = lines[0]
        # Find the hit/miss line (line 3)
        hit_miss_line = lines[3] 
        # Find the stats line (line 5)
        stats_line = lines[5]
        
        # Parse config line: L1 Data (config)    Size: 32(KB)    Line size: 64(B)    Associativity: 8    Num sets: 64
        cache_size = re.search(r'Size:\s*(\d+)', config_line).group(1)
        block_size = re.search(r'Line size:\s*(\d+)', config_line).group(1)
        associativity = re.search(r'Associativity:\s*(\d+)', config_line).group(1)
        num_sets = re.search(r'Num sets:\s*(\d+)', config_line).group(1)
        
        # Parse hit/miss line: L1 Data (hit/miss)    Instructions: 53571727    References: 15264104    Miss rate: 0.0044    MPKI: 1.2594
        instructions = re.search(r'Instructions:\s*([\d.]+)', hit_miss_line).group(1)
        references = re.search(r'References:\s*([\d.]+)', hit_miss_line).group(1)
        miss_rate = re.search(r'Miss rate:\s*([\d.]+)', hit_miss_line).group(1)
        mpki = re.search(r'MPKI:\s*([\d.]+)', hit_miss_line).group(1)
        
        # Parse stats line: 67466         3176        16023         2063        46204
        stats_numbers = stats_line.strip().split()
        total, cold, capacity, mapping, replacement = stats_numbers
        
        # Combine all values into a single list
        all_values = [cache_size, block_size, associativity, num_sets, 
                     instructions, references, miss_rate, mpki,
                     total, cold, capacity, mapping, replacement]
        return all_values
    except Exception as e:
        print(f"Error parsing output: {e}")
        return None   
# Function to write results to a CSV file (append mode)
def write_results_to_csv(results, filename):
    headers = [
        "Cache Size (KB)", "Block Size (B)", "Associativity", "Num Sets",
        "Instructions", "References", "Miss Rate", "MPKI",
        "Total", "Cold", "Capacity", "Mapping", "Replacement"
    ]
    
    # Check if file exists and has content
    file_exists = os.path.exists(filename)
    write_header = True
    
    if file_exists:
        # Check if file has content (more than just header)
        with open(filename, 'r', newline='') as file:
            reader = csv.reader(file)
            rows = list(reader)
            if len(rows) > 0:
                # File exists and has at least a header, don't write header again
                write_header = False
    
    # Append to file (or create if doesn't exist)
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        if write_header:
            writer.writerow(headers)
        for result in results:
            writer.writerow(result)
# Main function to run the analysis
def main():     
        # Define the configurations to test
        cache_sizes = [256]  # in KB
        block_sizes = [64]       # in Bytes
        associativities = [1]   # 1 for direct-mapped, n for n-way set associative
        
        results = []
        
        # Iterate over all combinations of configurations
        for cache_size, block_size, associativity in itertools.product(
                cache_sizes, block_sizes, associativities):
                
                print(f"Running cacheSim with Cache Size: {cache_size}KB, Block Size: {block_size}B, "
                      f"Associativity: {associativity}")
                output = run_cache_simulator(cache_size, block_size, associativity, None, None)
                if output:
                    parsed_result = parse_cache_simulator_output(output)
                    if parsed_result:
                        results.append(parsed_result)
        # Write all results to a CSV file
        write_results_to_csv(results, "cache_simulation_results.csv")
        print("Results written to cache_simulation_results.csv")

if __name__ == "__main__":
    main()
