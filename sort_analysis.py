"""
Sorting algorithms analysis: Insertion Sort, Merge Sort, and Timsort.
Execution time comparison.
"""
import timeit
import json
import copy
from pathlib import Path
from typing import Callable

from insertion_sort import insertion_sort
from merge_sort import merge_sort

def measure_time(sort_func: Callable, data: list, repeats: int = 5) -> float:
    times = []
    for _ in range(repeats):
        data_copy = copy.deepcopy(data)
        
        start = timeit.default_timer()
        sort_func(data_copy)
        end = timeit.default_timer()
        
        times.append(end - start)
    
    return sum(times) / len(times)


def measure_timsort(data: list, repeats: int = 5) -> float:
    times = []
    for _ in range(repeats):
        data_copy = copy.deepcopy(data)
        
        start = timeit.default_timer()
        sorted(data_copy)
        end = timeit.default_timer()
        
        times.append(end - start)
    
    return sum(times) / len(times)

def generate_test_data(size: int, data_type: str = "random") -> list[int]:
    import random
    
    if data_type == "random":
        return [random.randint(0, 100000) for _ in range(size)]
    elif data_type == "sorted":
        return list(range(size))
    elif data_type == "reversed":
        return list(range(size, 0, -1))
    elif data_type == "partial":
        data = list(range(size))
        for _ in range(int(size * 0.3)):
            i, j = random.randint(0, size-1), random.randint(0, size-1)
            data[i], data[j] = data[j], data[i]
        return data
    else:
        raise ValueError(f"Unknown data type: {data_type}")


def run_analysis(
    sizes: list[int] = None,
    data_type: str = "random",
    repeats: int = 5,
) -> dict:
    if sizes is None:
        sizes = [100, 500, 1000, 2000, 5000, 10000]
    
    results = {
        "sizes": sizes,
        "data_type": data_type,
        "insertion_sort": [],
        "merge_sort": [],
        "timsort": [],
    }
    
    for size in sizes:
        data = generate_test_data(size, data_type)
        
        # Insertion Sort (skip for large arrays)
        insertion_time = measure_time(insertion_sort, data, repeats)
        results["insertion_sort"].append(insertion_time)
        
        # Merge Sort
        merge_time = measure_time(merge_sort, data, repeats)
        results["merge_sort"].append(merge_time)
        
        # Timsort (built-in sorted)
        timsort_time = measure_timsort(data, repeats)
        results["timsort"].append(timsort_time)
    
    return results


def run_full_analysis(sizes: list[int] = None, repeats: int = 5) -> dict:
    if sizes is None:
        sizes = [100, 500, 1000, 2000, 5000, 10000]
    
    data_types = ["random", "sorted", "reversed", "partial"]
    all_results = {}
    
    for data_type in data_types:
        all_results[data_type] = run_analysis(sizes, data_type, repeats)
    
    return all_results

def save_results(all_results: dict, save_path: str = "results/results.json"):
    Path(save_path).parent.mkdir(parents=True, exist_ok=True)
    
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)

def main():    
    sizes = [100, 500, 1000, 2000, 5000, 10000]
    
    all_results = run_full_analysis(sizes, repeats=3)
    
    save_results(all_results, "results/results.json")
    
    return all_results


if __name__ == "__main__":
    results = main()
