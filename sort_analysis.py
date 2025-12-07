"""
Аналіз алгоритмів сортування: Insertion Sort, Merge Sort та Timsort.
Порівняння часу виконання.
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
        raise ValueError(f"Невідомий тип даних: {data_type}")


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
        
        # Insertion Sort (пропускаємо для великих масивів)
        insertion_time = measure_time(insertion_sort, data, repeats)
        results["insertion_sort"].append(insertion_time)
        
        # Merge Sort
        merge_time = measure_time(merge_sort, data, repeats)
        results["merge_sort"].append(merge_time)
        
        # Timsort (вбудований sorted)
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

    conclusions = """

 ТЕОРЕТИЧНА СКЛАДНІСТЬ:
   - Insertion Sort: O(n²) — найгірший і середній випадок
   - Merge Sort: O(n log n) — у всіх випадках
   - Timsort: O(n log n) — найгірший, O(n) — найкращий (для майже відсортованих)

 Результати:
"""
    
    # Аналіз результатів для random даних
    if "random" in all_results:
        random_results = all_results["random"]
        sizes = random_results["sizes"]
        
        # Порівняння на найбільшому розмірі де є всі три алгоритми
        valid_idx = -1
        for i in range(len(sizes) - 1, -1, -1):
            if random_results["insertion_sort"][i] is not None:
                valid_idx = i
                break
        
        if valid_idx >= 0:
            size = sizes[valid_idx]
            ins_time = random_results["insertion_sort"][valid_idx]
            merge_time = random_results["merge_sort"][valid_idx]
            tim_time = random_results["timsort"][valid_idx]
            
            speedup_ins_vs_tim = ins_time / tim_time if tim_time > 0 else 0
            speedup_merge_vs_tim = merge_time / tim_time if tim_time > 0 else 0
            
            conclusions += f"""
   На масиві розміром {size} (випадкові дані):
   - Insertion Sort: {ins_time:.6f} сек
   - Merge Sort:     {merge_time:.6f} сек
   - Timsort:        {tim_time:.6f} сек

    Timsort швидший за Insertion Sort у {speedup_ins_vs_tim:.1f}x разів
    Timsort швидший за Merge Sort у {speedup_merge_vs_tim:.1f}x разів
"""

    # Аналіз для відсортованих даних
    if "sorted" in all_results:
        sorted_results = all_results["sorted"]
        sizes = sorted_results["sizes"]
        
        # Знаходимо індекс з максимальним розміром
        max_idx = len(sizes) - 1
        merge_time = sorted_results["merge_sort"][max_idx]
        tim_time = sorted_results["timsort"][max_idx]
        
        conclusions += f"""
   На вже відсортованому масиві (розмір {sizes[max_idx]}):
   - Merge Sort: {merge_time:.6f} сек
   - Timsort:    {tim_time:.6f} сек
"""

    conclusions += """
🔑 КЛЮЧОВІ ВИСНОВКИ:

1. TIMSORT — НАЙЕФЕКТИВНІШИЙ для практичного використання:
   • Поєднує переваги Merge Sort (стабільність, O(n log n)) та 
     Insertion Sort (ефективність на малих масивах і майже відсортованих)
   • Використовує "runs" — знаходить природні послідовності в даних
   • Адаптивний: O(n) на відсортованих, O(n log n) на випадкових даних

2. MERGE SORT — надійний, але не оптимальний:
   • Гарантований O(n log n), але потребує додаткової пам'яті O(n)
   • Не використовує структуру вхідних даних

3. INSERTION SORT — ефективний лише для малих масивів:
   • O(n²) робить його непридатним для великих даних
   • Але O(n) на майже відсортованих — тому Timsort його використовує!

💡 ПРАКТИЧНА РЕКОМЕНДАЦІЯ:
   Завжди використовуйте вбудовані sorted() або list.sort() в Python.
   Вони оптимізовані на рівні C і використовують Timsort.
   Власні реалізації сортування варто писати лише в навчальних цілях.

══════════════════════════════════════════════════════════════════════════════
"""
    return conclusions

def main():    
    sizes = [100, 500, 1000, 2000, 5000, 10000]
    
    all_results = run_full_analysis(sizes, repeats=3)
    
    save_results(all_results, "results/results.json")
    
    return all_results


if __name__ == "__main__":
    results = main()
