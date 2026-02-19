# Weighted Token Swapping on Graphs

> Undergraduate Research Project — Bachelor of Computer Applications  
> Amrita Vishwa Vidyapeetham, Amritapuri Campus (2024–2025)

---

## 👥 Authors

| Name | Registration Number |
|---|---|
| Abhijith V | AM.EN.U3BCA22001 |
| Sachin S | AM.EN.U3BCA22049 |
| Shreeram V Rakesh | AM.EN.U3BCA22053 |
| Tharun Babu | AM.EN.U3BCA22057 |

**Project Guide:** Dr. Indulekha T S  
**Department:** Computer Science and Applications, Amrita School of Computing

---

## 📌 Overview

Token swapping is a combinatorial optimization problem where tokens placed on a graph must be rearranged to their target positions using a sequence of **adjacent swaps**. In the **weighted variant**, each token carries a weight and the cost of any swap equals the sum of the weights of the two tokens involved.

This project implements and evaluates algorithms for weighted token swapping on three graph topologies:

- **Path (Line Graph)** — tokens arranged linearly
- **Star Graph** — one central node connected to all leaves
- **Broom Graph** — a hybrid structure combining a path and a star

The broom topology is the primary focus, as it introduces unique algorithmic challenges not present in simpler structures.

---

## 🧠 Problem Statement

Given a graph `G = (V, E)` with `n` vertices, tokens `T = [t₁, t₂, ..., tₙ]` each with weight `w(tᵢ) ∈ ℤ⁺`, find a sequence of adjacent swaps that:

1. Moves every token to its correct (target) position
2. Minimizes total cost = Σ (w(tᵢ) + w(tⱼ)) over all swaps

This problem is **NP-hard** on general graphs and remains complex even on trees in the weighted setting.

---

## 📐 Graph Structures

### Path / Line
- Vertices connected in a sequence: `v1 — v2 — v3 — ... — vn`
- Optimal swaps = number of inversions
- Upper bound: `n(n-1)/2`

### Star
- Central node `v1` connected to all leaf nodes `v2, ..., vn`
- Optimal swaps = `m + c` where `m` = unhomed leaves, `c` = non-trivial locked cycles (excluding center)
- Upper bound: `⌈3(n-1)/2⌉`

### Broom (Single)
- Star center joined to one end of a path via an edge
- Vertices partitioned into **star vertices** `v1, ..., vk` and **path vertices** `vk+1, ..., vn`
- Tokens partitioned into **star markers** and **path markers**

---

## ⚙️ Algorithms

### Path — Weighted Token Swapping
Minimum cost of sorting = sum over all inversions `(t, t')` of `[w(t) + w(t')]`

Tokens are moved using a greedy approach: largest token to correct position first, moving only rightward.

### Star — Weighted Token Swapping
Uses a strategy-selection mechanism based on three token types:
- **x** — lightest token in the unlocked cycle
- **a** — lightest misplaced token in a locked cycle
- **h** — lightest homed leaf token

Three strategies are evaluated to minimize cost when resolving locked cycles.

### Broom — Algorithm Aᵦ (Three-Phase)

| Phase | Description |
|---|---|
| **Step 1 — Smin** | Home the star marker closest to its home that resides on the path |
| **Step 2 — Pmax** | Home the largest unhomed path marker |
| **Step 3 — Star Swap** | Resolve remaining misplaced star markers within the star |

**Time Complexity:** O(n²)

**Worst-case swap count:**

```
Wᵦ = P(P+1)/2 + (S-P) + P(P-1)/2 + ⌈3S/2⌉
```

where `S` = number of star vertices, `P` = number of path vertices.

---

## 🔬 Key Observations (Weighted Cases on Broom)

| Case | Description | Strategy |
|---|---|---|
| 1.1 | Path + Star tokens misplaced in own regions; one zero-weight path token | Use zero-weight token to unlock cycles; home farthest path token last |
| 1.2 | One zero-weight star token | Bring to star center to unlock cycles; then resolve path |
| 2.1 | Star token K (weight 0) on path | Delay homing K; use it to unlock star cycles first |
| 2.2 | Star token K (weight 1) on path | Find lightest available token to unlock; home K after |
| 3.1 | Two star tokens on path (heavy first) | Home heavy first, use light to unlock star |
| 3.2 | Two star tokens on path (light first) | Use light to unlock star, then home heavy |
| 4.1 | All star tokens on path (weight 0), path tokens on star (weight 1) | Home heavy path tokens first using light star tokens |
| 4.2 | All star tokens on path (random), path tokens weight 0 | Home zero-weight path tokens first; resolve star cycles after |
| 5 | Some star tokens (weight 0) on path, some path tokens on star | Home heaviest misplaced path token first; zero-weight star tokens last |
| 6.1 | One star token misplaced, all others homed | Resolve path first; home last star token from center at end |
| 6.2 | One path token misplaced, all others homed | Resolve star first; home the remaining path token at end |

**Key Insight:** Zero-weight tokens are powerful utilities — delaying their placement and using them to unlock locked cycles significantly reduces total swap cost.

---

## 🗂️ Project Structure

```
weighted-token-swapping/
│
├── README.md
├── src/
│   ├── path/
│   │   └── weighted_token_swap_line.py      # Weighted token swapping on a line/path
│   ├── star/
│   │   └── weighted_token_swap_star.py      # Weighted token swapping on a star
│   └── broom/
│       └── token_swap_single_broom.py       # Token swapping on a single broom
│
├── docs/
│   └── Final_Project_Report.pdf            # Full undergraduate project report
│
└── examples/
    └── sample_inputs.md                     # Sample inputs and expected outputs
```

---

## 🚀 Getting Started

### Requirements
- Python 3.8+
- No external libraries required

### Running the Path Algorithm

```bash
cd src/path
python weighted_token_swap_line.py
```
**Sample Input:**
```
Enter the number of vertices: 4
Enter token at vertex 1: 4
Enter weight of token 1: 1
Enter token at vertex 2: 3
Enter weight of token 2: 1
Enter token at vertex 3: 2
Enter weight of token 3: 0
Enter token at vertex 4: 1
Enter weight of token 4: 1
```

### Running the Star Algorithm

```bash
cd src/star
python weighted_token_swap_star.py
```

### Running the Broom Algorithm

```bash
cd src/broom
python token_swap_single_broom.py
```
**Sample Input:**
```
Number of vertices: 4
Size of star (k): 2
Enter permutation separated by spaces: 3 2 4 1
```
**Expected Output:**
```
After s_min: [(4, 3), (2, 4)]
After p_max: [(4, 3), (2, 4), (4, 3)]
Sorted!
Initial: [3, 2, 4, 1]
Final: [1, 2, 3, 4]
```

---

## 📚 References

1. Ajila, L., and T. S. Indulekha. "Colored Token Swapping Using Broom." *IEEE GCAT 2024*.
2. Chitturi, B., and T. S. Indulekha. "Sorting permutations with a transposition tree." *IEEE ICMSAO 2019*.
3. Sadanandan, I. T., and B. Chitturi. "Optimal algorithms for sorting permutations with brooms." *Algorithms 15.7* (2022): 220.
4. Yamanaka et al. "Swapping labeled tokens on graphs." *Theoretical Computer Science 586* (2015): 81–94.
5. Biniaz et al. "Token swapping on trees." *Discrete Mathematics & Theoretical Computer Science 24* (2023).

---

## 📄 License

This project is submitted as an undergraduate academic project. The source code is shared for educational reference.
