# Sample Inputs and Expected Outputs

## Path (Line Graph)

### Example 1 — Reverse permutation (worst case)
**Input:**
```
Number of vertices: 4
Tokens: 4, 3, 2, 1
Weights: 1, 1, 1, 1
```
**Expected Output:**
```
Swap: 4 <-> 3,  Cost: 2
Swap: 4 <-> 2,  Cost: 2
Swap: 4 <-> 1,  Cost: 2
Swap: 3 <-> 2,  Cost: 2
Swap: 3 <-> 1,  Cost: 2
Swap: 2 <-> 1,  Cost: 2
Total cost: 12
Total swaps: 6
```

### Example 2 — Zero-weight token (cost saving)
**Input:**
```
Number of vertices: 4
Tokens: 4, 3, 2, 1
Weights: 1, 1, 0, 1   ← token 2 has weight 0
```
**Expected Output:**
```
Total cost: 8    (reduced from 12 due to zero-weight token 2)
```

---

## Star Graph

### Example 1 — Two disjoint cycles
**Input:**
```
Number of vertices: 5
Tokens at v1..v5: 1, 3, 2, 5, 4
Weights:          1, 1, 1, 1, 1
```
*Cycle structure: (2,3) and (4,5) — two locked cycles*

**Expected Output:**
```
Chosen strategy S1
Swap sequence: 6 swaps
Total cost: 6
```

### Example 2 — One large cycle through center
**Input:**
```
Number of vertices: 5
Tokens at v1..v5: 2, 3, 1, 5, 4
Weights:          1, 1, 1, 1, 1
```

---

## Broom (Single)

### Example 1 — From the paper
**Input:**
```
Number of vertices: 4
Size of star (k): 2
Permutation: 3 2 4 1
```
**Expected Output:**
```
After Phase 1 (Smin): [1, 2, 4, 3]
  Swaps: [(4, 3), (2, 4)]

After Phase 2 (Pmax): [1, 2, 3, 4]
  Swaps: [(4, 3), (2, 4), (4, 3)]

Initial permutation : [3, 2, 4, 1]
Final permutation   : [1, 2, 3, 4]
Total swaps         : 3
```

### Example 2 — Already sorted
**Input:**
```
Number of vertices: 4
Size of star (k): 2
Permutation: 1 2 3 4
```
**Expected Output:**
```
Permutation is already sorted.
```

### Example 3 — Star markers on path (larger broom)
**Input:**
```
Number of vertices: 8
Size of star (k): 5
Permutation: 1 6 8 7 3 2 4 5
```
*(Star markers 3 and 2 are on the path at positions v7 and v8)*

**Expected Output:**
```
Phase 1: Homes star markers 3 and 2 (5 swaps)
Phase 2: Homes path marker 8 (1 swap)
Phase 3: Homes star markers 5 and 4 (3 swaps)
Total: 9 swaps
```

---

## Weight Configuration Impact (Broom — Key Observation)

| Case | Zero-weight token location | Strategy | Cost reduction |
|---|---|---|---|
| 1.1 | One path token (weight 0) | Use as cycle-unlocker before homing | High |
| 1.2 | One star token (weight 0) | Bring to center, unlock all locked cycles | High |
| 2.1 | Star token K on path (weight 0) | Delay K's homing; use for cycle unlocking | Medium |
| 2.2 | Star token K on path (weight 1) | Find lightest helper; then home K | Low–Medium |

**Key insight:** A zero-weight token incurs no swap cost. Delaying its placement and routing it through locked cycles effectively "unlocks" them for free, drastically reducing total swap cost.
