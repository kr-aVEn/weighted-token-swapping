"""
Token Swapping on a Single Broom Graph
========================================
Project: Weighted Token Swapping on Graphs
Authors: Tharun Babu, Abhijith V, Sachin S, Shreeram V Rakesh
Guide:   Dr. Indulekha T S
Amrita Vishwa Vidyapeetham, Amritapuri Campus (2024-2025)

Description:
    A single broom is a tree formed by joining the center of a star graph
    to one end of a path graph.

    Vertices:
        Star vertices: v1, v2, ..., vk
        Path vertices: vk+1, ..., vn
        (Note: vk+1 is both the star center and a path node)

    Tokens are partitioned into:
        Star markers — tokens whose home is a star vertex
        Path markers — tokens whose home is a path vertex

    Algorithm Aᵦ — Three Phase Sorting:
        Phase 1 (Smin): Home the star marker closest to its home on the path
        Phase 2 (Pmax): Home the largest unhomed path marker
        Phase 3 (Star Swap): Resolve remaining misplaced star markers

    Properties of Algorithm Aᵦ:
        1. Star markers on the path always move leftward (toward their home)
           in order of increasing distance from home.
        2. Path markers move rightward to their home, shifting smaller
           path markers toward the center.
        3. Swaps between two star markers never occur on a path edge.

    Time Complexity: O(n²)
    Worst-case total swaps:
        Wᵦ = P(P+1)/2 + (S-P) + P(P-1)/2 + ⌈3S/2⌉
        where S = star vertices, P = path vertices
"""


class SingleBroom:
    def __init__(self, k, pi):
        """
        Initialize the broom with star size k and permutation pi.

        Args:
            k  : Number of star vertices (indices 0..k-1 are star region)
            pi : List representing the token permutation (1-indexed tokens)
        """
        self.k = k
        self.original = pi
        self.pi = pi.copy()
        self.n = len(pi)
        self.swaps = []

    def is_sorted(self):
        """Check if every token is in its home position."""
        return all(self.pi[i] == i + 1 for i in range(self.n))

    # -------------------------------------------------------------------------
    # Phase 3: Star Swap — Resolve misplaced markers within the star region
    # -------------------------------------------------------------------------
    def star_swap(self):
        """
        Home any remaining misplaced star markers.
        Uses the center (index k-1) as a relay to cycle through and place
        all remaining star markers at their correct positions.
        """
        n = self.k
        while self.pi[:n] != sorted(self.pi[:n]):
            i = self.pi[n - 1]
            if i != n:
                tgt = i - 1
                if tgt < n - 1:
                    self.pi[n - 1], self.pi[tgt] = self.pi[tgt], self.pi[n - 1]
                    self.swaps.append((self.pi[n - 1], self.pi[tgt]))
            else:
                for j in range(n - 1):
                    if self.pi[j] != j + 1:
                        i = self.pi[j]
                        tgt = i - 1
                        self.pi[n - 1], self.pi[tgt] = self.pi[tgt], self.pi[n - 1]
                        self.swaps.append((self.pi[n - 1], self.pi[tgt]))
                        break

    # -------------------------------------------------------------------------
    # Phase 1: Smin — Home the star marker nearest to its home on the path
    # -------------------------------------------------------------------------
    def s_min(self):
        """
        Identify and home all star markers that are currently on the path.
        Star markers (value < k) on the path are moved leftward to the
        star-path boundary, then swapped into their star home position.

        Processes markers in order of increasing distance from their home.
        """
        k, n = self.k, self.n
        star = self.pi[: k - 1]
        path = self.pi[k - 1: n]

        p = 0
        while p < len(path):
            smin = path[p]
            # A star marker is one whose home index is within the star region
            if 0 < smin < k and smin <= len(star):
                # Bubble this marker leftward to the boundary (index 0 of path)
                while p:
                    path[p], path[p - 1] = path[p - 1], path[p]
                    self.swaps.append((path[p], path[p - 1]))
                    p -= 1
                # Swap it into its star home
                self.swaps.append((star[smin - 1], path[0]))
                star[smin - 1], path[0] = path[0], star[smin - 1]
                p = 0
            else:
                p += 1

        self.pi = star + path

    # -------------------------------------------------------------------------
    # Phase 2: Pmax — Home the largest unhomed path marker
    # -------------------------------------------------------------------------
    def p_max(self):
        """
        Home path markers in decreasing order of value.
        The largest unhomed path marker is moved directly to its correct
        position, shuffling smaller markers toward the star-path boundary.
        """
        k = self.k
        path = self.pi[k - 1:]

        while path:
            pmax = max(path)
            if pmax == k:
                # The center marker (value k) is already at the boundary
                path.remove(pmax)
                continue
            cur = self.pi.index(pmax)
            tgt = pmax - 1
            while cur != tgt:
                nxt = cur + 1 if cur < tgt else cur - 1
                self.swaps.append((self.pi[cur], self.pi[nxt]))
                self.pi[cur], self.pi[nxt] = self.pi[nxt], self.pi[cur]
                cur = nxt
            path.remove(pmax)

    # -------------------------------------------------------------------------
    # Main sort driver
    # -------------------------------------------------------------------------
    def sort(self):
        """
        Execute Algorithm Aᵦ in three phases and print the results.
        """
        print(f"\nInitial permutation: {self.pi}")
        print(f"Star size (k): {self.k}, Total vertices (n): {self.n}\n")

        if self.is_sorted():
            print("Permutation is already sorted.")
            return

        # --- Phase 1: Smin ---
        self.s_min()
        print(f"After Phase 1 (Smin): {self.pi}")
        print(f"  Swaps so far: {self.swaps}\n")

        if self.is_sorted():
            self._print_result()
            return

        # --- Phase 2: Pmax ---
        self.p_max()
        print(f"After Phase 2 (Pmax): {self.pi}")
        print(f"  Swaps so far: {self.swaps}\n")

        if self.is_sorted():
            self._print_result()
            return

        # --- Phase 3: Star Swap ---
        self.star_swap()
        print(f"After Phase 3 (Star Swap): {self.pi}")
        print(f"  Swaps so far: {self.swaps}\n")

        self._print_result()

    def _print_result(self):
        print("=" * 50)
        print(f"Initial permutation : {self.original}")
        print(f"Final permutation   : {self.pi}")
        print(f"Total swaps         : {len(self.swaps)}")
        print(f"Swap sequence       : {self.swaps}")
        print("=" * 50)


def main():
    try:
        n = int(input("Number of vertices: "))
        if n < 4:
            print("Need at least 4 vertices (broom requires star + path).")
            return
        k = int(input("Size of star (k): "))
        if k < 2 or k > n - 2:
            print(f"k must satisfy 2 <= k <= {n - 2} for a valid broom.")
            return
        pi = list(map(int, input("Enter permutation separated by spaces: ").split()))
        if len(pi) != n:
            print(f"Permutation must have exactly {n} values.")
            return
        swapper = SingleBroom(k, pi)
        swapper.sort()
    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    main()
