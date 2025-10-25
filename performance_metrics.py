"""
Performance Metrics Module for Hackathon
=========================================

A simple module to measure execution time and memory usage of your code.
Use this to track and compare the performance of different solutions.

Basic Usage:
-----------
    from performance_metrics import start_metrics, finish_metrics

    start_metrics()
    # Your code here
    result = finish_metrics("metrics.csv")

Features:
---------
- Accurate execution time measurement using time.perf_counter()
- Python memory allocation tracking via tracemalloc
- Automatic CSV logging for easy comparison
- UTC timestamps for consistent tracking
"""

import csv
import os
import time

try:
    import tracemalloc
except Exception:
    # tracemalloc might not be available in very old Python versions
    tracemalloc = None

# Internal state to track metrics between start and finish calls
_STATE = {
    "active": False,  # Whether metrics are currently being collected
    "started_iso": None,  # ISO timestamp when metrics started
    "t0": 0.0,  # Starting time in seconds (from perf_counter)
    "tm_started": False,  # Whether we started tracemalloc (to stop it later)
}


def start_metrics():
    """
    Start timing and memory tracking for your code.

    This function should be called immediately before the code you want to measure.
    It starts a high-resolution timer and begins tracking Python memory allocations.

    Raises:
        RuntimeError: If metrics are already running (you must call finish_metrics() first)

    Example:
        >>> start_metrics()
        >>> # Your algorithm here
        >>> result = finish_metrics()

    Note:
        - Uses time.perf_counter() for accurate elapsed time measurement
        - Automatically starts tracemalloc if available
        - Records UTC timestamp for consistent logging
    """
    if _STATE["active"]:
        raise RuntimeError("Metrics already running. Call finish_metrics() first.")

    # Mark metrics as active and record start time
    _STATE["active"] = True
    _STATE["started_iso"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    _STATE["t0"] = time.perf_counter()

    # Start memory tracking if tracemalloc is available
    if tracemalloc is not None:
        if not tracemalloc.is_tracing():
            tracemalloc.start()
            _STATE["tm_started"] = True
        else:
            # tracemalloc was already running (started elsewhere)
            _STATE["tm_started"] = False

        # Reset peak memory to track only this execution window (Python 3.9+)
        if hasattr(tracemalloc, "reset_peak"):
            tracemalloc.reset_peak()


def finish_metrics(output_path=None):
    """
    Stop measuring and collect performance metrics.

    This function calculates elapsed time, collects memory statistics, prints a summary
    to the console, and optionally appends results to a CSV file for tracking.

    Args:
        output_path (str, optional): Path to CSV file for logging results.
            If the file doesn't exist, it will be created with headers.
            If None, results are only printed to console.

    Returns:
        dict: A dictionary containing:
            - timestamp_utc (str): ISO formatted UTC timestamp when metrics started
            - elapsed_seconds (float): Total execution time in seconds
            - memory_source (str): "tracemalloc" if available, "none" otherwise
            - py_alloc_current_bytes (int or None): Current memory allocated by Python
            - py_alloc_peak_bytes (int or None): Peak memory allocated during execution

    Raises:
        RuntimeError: If start_metrics() was not called first

    Example:
        >>> start_metrics()
        >>> data = [i**2 for i in range(1000000)]
        >>> metrics = finish_metrics("my_results.csv")
        >>> print(f"Took {metrics['elapsed_seconds']} seconds")

    Example Output:
        === Performance Metrics ===
        started_utc: 2025-10-22T14:30:45Z
        elapsed_seconds: 2.456789
        memory_source: tracemalloc
        py_alloc_current_bytes: 8000000
        py_alloc_peak_bytes: 8500000
    """
    if not _STATE["active"]:
        raise RuntimeError("start_metrics() must be called before finish_metrics().")

    # Calculate elapsed time
    elapsed = time.perf_counter() - _STATE["t0"]

    # Collect memory statistics if available
    mem_source = "none"
    tm_current = None
    tm_peak = None
    if tracemalloc is not None:
        tm_current, tm_peak = tracemalloc.get_traced_memory()
        mem_source = "tracemalloc"
        # Only stop tracemalloc if we started it
        if _STATE["tm_started"]:
            tracemalloc.stop()

    # Build result dictionary
    result = {
        "timestamp_utc": _STATE["started_iso"],
        "elapsed_seconds": round(elapsed, 6),
        "memory_source": mem_source,
        "py_alloc_current_bytes": tm_current,
        "py_alloc_peak_bytes": tm_peak,
    }

    # Print summary to console
    print("=== Performance Metrics ===")
    print(f"started_utc: {result['timestamp_utc']}")
    print(f"elapsed_seconds: {result['elapsed_seconds']}")
    print(f"memory_source: {result['memory_source']}")
    if mem_source == "tracemalloc":
        print(f"py_alloc_current_bytes: {tm_current}")
        print(f"py_alloc_peak_bytes: {tm_peak}")

    # Optionally append results to CSV file
    if output_path:
        header = [
            "timestamp_utc",
            "elapsed_seconds",
            "memory_source",
            "py_alloc_current_bytes",
            "py_alloc_peak_bytes",
        ]
        file_exists = os.path.exists(output_path)
        with open(output_path, "a+", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=header)
            if not file_exists:
                writer.writeheader()
            writer.writerow({k: result.get(k) for k in header})

    # Reset state for next measurement
    _STATE.update(
        {
            "active": False,
            "started_iso": None,
            "t0": 0.0,
            "tm_started": False,
        }
    )

    return result


# ====================
# Usage Examples
# ====================

def example_basic_usage():
    """
    Example 1: Basic usage with console output only
    """
    print("\n--- Example 1: Basic Usage ---")
    start_metrics()

    # Simulate some work
    total = sum(i ** 2 for i in range(1000000))

    metrics = finish_metrics()
    print(f"\nResult calculated: {total}")
    print(f"Execution took: {metrics['elapsed_seconds']} seconds\n")


def example_with_csv_logging():
    """
    Example 2: Log results to CSV for comparison
    """
    print("\n--- Example 2: CSV Logging ---")
    start_metrics()

    # Different algorithm for comparison
    data = []
    for i in range(1000000):
        data.append(i ** 2)

    metrics = finish_metrics("hackathon_metrics.csv")
    print(f"\nResults logged to: hackathon_metrics.csv")
    print(f"Peak memory used: {metrics['py_alloc_peak_bytes']} bytes\n")


def example_multiple_runs():
    """
    Example 3: Measure multiple algorithm variations
    """
    print("\n--- Example 3: Multiple Runs ---")

    # First approach: list comprehension
    start_metrics()
    result1 = [i ** 2 for i in range(500000)]
    metrics1 = finish_metrics("comparison.csv")

    # Second approach: map function
    start_metrics()
    result2 = list(map(lambda x: x ** 2, range(500000)))
    metrics2 = finish_metrics("comparison.csv")

    print(f"\nList comprehension: {metrics1['elapsed_seconds']}s")
    print(f"Map function: {metrics2['elapsed_seconds']}s")
    print(f"Results saved to comparison.csv for analysis\n")


def example_error_handling():
    """
    Example 4: Proper error handling
    """
    print("\n--- Example 4: Error Handling ---")
    try:
        start_metrics()
        # Your code here
        result = [i for i in range(100000)]
        metrics = finish_metrics()
        print("Success! Metrics collected.")
    except Exception as e:
        print(f"Error occurred: {e}")
        # Note: If an exception occurs, you may need to handle cleanup
        if _STATE["active"]:
            print("Warning: Metrics were not properly finished due to error")


# Uncomment below to run examples:
if __name__ == "__main__":
    print("=" * 60)
    print("PERFORMANCE METRICS MODULE - USAGE EXAMPLES")
    print("=" * 60)

    example_basic_usage()
    example_with_csv_logging()
    example_multiple_runs()
    example_error_handling()

    print("\n" + "=" * 60)
    print("TIP: Import this module in your task submission:")
    print("     from performance_metrics import start_metrics, finish_metrics")
    print("=" * 60)

