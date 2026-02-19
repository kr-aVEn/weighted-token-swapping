"""
Weighted Token Swapping on a Star Graph
========================================
Project: Weighted Token Swapping on Graphs
Authors: Tharun Babu, Abhijith V, Sachin S, Shreeram V Rakesh
Guide:   Dr. Indulekha T S
Amrita Vishwa Vidyapeetham, Amritapuri Campus (2024-2025)

Description:
    In a star graph, vertex v1 is the center and v2..vn are leaves.
    All swaps happen between the center and a leaf.

    Unweighted optimal = m + c
        where m = unhomed leaves, c = non-trivial locked cycles (leaf-only)

    Weighted case: at least (m + c) swaps needed; the globally lightest
    token is used to resolve locked cycles, potentially needing up to 2
    extra swaps per locked cycle.

Strategy Selection:
    - x: lightest token in the unlocked cycle (cycle containing center)
    - a: lightest misplaced token in any locked cycle
    - h: lightest homed leaf token
    Strategy 1 (use x only), 2 (bring a, unlock, return a), 3 (use h)

Time Complexity: O(n^2)
Upper Bound on swaps: ceil(3(n-1)/2)
"""


class StarTokenSwapper:
    def __init__(self, n):
        self.n = n
        self.tokens = [0] * n
        self.weights = {}
        self.read_input()

    def read_input(self):
        """Read token placement and weights for all n vertices."""
        seen = set()
        for i in range(self.n):
            token = int(input(f"Enter token at vertex {i+1}: "))
            if token < 1 or token > self.n:
                raise ValueError(f"Token must be between 1 and {self.n}")
            if token in seen:
                raise ValueError(f"Duplicate token {token} found")
            seen.add(token)

            weight = int(input(f"Enter weight of token {token}: "))
            self.tokens[i] = token
            self.weights[token] = weight

        print("\nInitial state:")
        for i in range(self.n):
            t = self.tokens[i]
            print(f"  Vertex {i+1}: Token {t}, Weight {self.weights[t]}")

    def is_sorted(self):
        """Check if all tokens are at their home vertices."""
        return all(self.tokens[i] == i + 1 for i in range(self.n))

    def find_cycles(self):
        """Find all cycles of length >= 2 in the permutation."""
        visited = [False] * self.n
        cycles = []
        for i in range(self.n):
            if not visited[i]:
                cycle = []
                cur = i
                while not visited[cur]:
                    visited[cur] = True
                    cycle.append(cur)
                    cur = self.tokens[cur] - 1
                if len(cycle) > 1:
                    cycles.append(cycle)
        return cycles

    def unlocked_cycle(self):
        """Return the cycle containing vertex 0 (the center node)."""
        visited, cycle, cur = [False] * self.n, [], 0
        while not visited[cur]:
            visited[cur] = True
            cycle.append(cur)
            cur = self.tokens[cur] - 1
        return cycle

    def locked_cycles(self):
        """Return all cycles that do NOT include the center (vertex 0)."""
        unlocked = set(self.unlocked_cycle())
        return [c for c in self.find_cycles() if not set(c).issubset(unlocked)]

    def find_x(self):
        """Find the lightest token in the unlocked (center) cycle."""
        cycle = self.unlocked_cycle()
        x = min(cycle, key=lambda v: self.weights[self.tokens[v]])
        return self.tokens[x], self.weights[self.tokens[x]]

    def find_a(self):
        """Find the lightest misplaced token in any locked cycle."""
        min_token, min_w = None, float("inf")
        for cyc in self.locked_cycles():
            for v in cyc:
                t = self.tokens[v]
                if v != t - 1 and self.weights[t] < min_w:
                    min_token, min_w = t, self.weights[t]
        return (min_token, min_w) if min_token else (None, None)

    def find_h(self):
        """Find the lightest token that is correctly homed on a leaf."""
        min_token, min_w = None, float("inf")
        for i in range(1, self.n):
            if self.tokens[i] == i + 1:
                t, w = self.tokens[i], self.weights[self.tokens[i]]
                if w < min_w:
                    min_token, min_w = t, w
        return (min_token, min_w) if min_token else (None, None)

    def choose_strategy(self):
        """
        Select which strategy to use for resolving locked cycles.
        Strategy 1: Use x directly (cheapest overall)
        Strategy 2: Bring a into unlocked cycle, unlock, restore a
        Strategy 3: Use homed token h as helper
        """
        x, wx = self.find_x()
        a, wa = self.find_a()
        h, wh = self.find_h()

        if a is None:
            return 1, (x, wx, a, wa, h, wh)
        if wx <= wa and (wh is None or wx < wh):
            return 1, (x, wx, a, wa, h, wh)
        if wa < (wh if wh else float("inf")):
            return 2, (x, wx, a, wa, h, wh)
        return 3, (x, wx, a, wa, h, wh)

    def swap(self, v):
        """Swap the token at center (vertex 0) with token at leaf vertex v."""
        t0, tv = self.tokens[0], self.tokens[v]
        cost = self.weights[t0] + self.weights[tv]
        self.tokens[0], self.tokens[v] = tv, t0
        print(
            f"  Swap center (Token {t0}, W={self.weights[t0]}) "
            f"<-> Vertex {v+1} (Token {tv}, W={self.weights[tv]}),  Cost={cost}"
        )
        return cost

    def perform_strategy(self):
        """Execute the chosen strategy to sort all tokens."""
        total = 0
        strat, (x, wx, a, wa, h, wh) = self.choose_strategy()

        print(f"\nChosen strategy S{strat}: x={x} w={wx}, a={a} w={wa}, h={h} w={wh}\n")
        print("Swap sequence:")

        def bring(token):
            nonlocal total
            if token and self.tokens[0] != token:
                total += self.swap(self.tokens.index(token))

        def resolve_lockeds():
            nonlocal total
            for cyc in self.locked_cycles():
                for v in cyc:
                    if v and self.tokens[v] != v + 1:
                        total += self.swap(v)
                        break

        if strat == 1:
            bring(x)
            resolve_lockeds()
        elif strat == 2:
            bring(x)
            bring(a)
            resolve_lockeds()
            bring(a)
        else:  # strat 3
            bring(x)
            bring(h)
            resolve_lockeds()
            bring(h)

        # Final sweeps on the unlocked cycle
        while not self.is_sorted():
            for v in self.unlocked_cycle():
                if v and self.tokens[v] != v + 1:
                    total += self.swap(v)
                    break
            else:
                break

        print("\nFinal state:")
        for i in range(self.n):
            print(f"  Vertex {i+1}: Token {self.tokens[i]}")
        print(f"\nTotal cost: {total}")


def main():
    try:
        n = int(input("Enter number of vertices: "))
        if n < 4:
            print("Star must have at least 4 vertices (1 center + 3 leaves).")
            return
        StarTokenSwapper(n).perform_strategy()
    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    main()
