# Sorting Algorithms Analysis

Comparative analysis of three sorting algorithms: **Insertion Sort**, **Merge Sort**, and **Timsort**.

## Empirical Results

Test results are located in the `results/` folder:

- `results.json` — numerical measurement data

## Key Conclusions

### 1. Timsort — Most Efficient for Practical Use

- Combines advantages of Merge Sort (stability, O(n log n)) and Insertion Sort (efficiency on small arrays)
- Uses "runs" — finds natural sorted sequences in data
- Adaptive: O(n) on sorted data, O(n log n) on random data

### 2. Merge Sort — Reliable, But Not Optimal

- Guaranteed O(n log n) in all cases
- Requires additional O(n) memory
- Does not utilize characteristics of input data structure

### 3. Insertion Sort — Only for Small Arrays

- O(n²) makes it unsuitable for large data
- O(n) on nearly sorted data

## 🚀 Usage

```bash
python sort_analysis.py
```

Results will be saved in the `results/` folder.
