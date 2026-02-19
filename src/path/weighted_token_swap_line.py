"""
Weighted Token Swapping on a Line/Path Graph
============================================
Project: Weighted Token Swapping on Graphs
Authors: Tharun Babu, Abhijith V, Sachin S, Shreeram V Rakesh
Guide:   Dr. Indulekha T S
Amrita Vishwa Vidyapeetham, Amritapuri Campus (2024-2025)

Description:
    In unweighted token swapping on a path, the minimum number of swaps
    equals the number of inversions. In the weighted case, the minimum cost
    is: sum over all inversions (t, t') of [w(t) + w(t')].

    This implementation uses a greedy approach — moving the largest token
    to its correct position first, then the second largest, and so on.

Algorithm:
    - Process tokens from largest value to smallest
    - For each token, move it rightward to its target position via adjacent swaps
    - Cost of each swap = sum of weights of the two involved tokens

Time Complexity: O(n^2)
Upper Bound on swaps: n(n-1)/2  (when permutation is in reverse order)
"""


class Graph:
    def graph_input(self):
        """Read graph input: number of vertices, token values, and token weights."""
        n = int(input("Enter the number of vertices: "))
        graph = [[0, 0] for _ in range(n)]
        token_set = set()

        for i in range(n):
            token = int(input(f"Enter token at vertex {i + 1}: "))

            if token > n:
                print(
                    f"Error: Token value {token} exceeds the number of vertices ({n}). "
                    f"Please enter a value <= {n}."
                )
                return []

            if token in token_set:
                print(
                    f"Error: Token value {token} is repeated. Tokens must be unique."
                )
                return []

            token_set.add(token)

            weight = int(input(f"Enter weight of token {i + 1}: "))
            graph[i][0] = token
            graph[i][1] = weight

        return graph


def weighted_token_sort(graph):
    """
    Sort tokens on a path using weighted adjacent swaps.

    Strategy: Process tokens from largest to smallest.
    Each token is moved rightward to its correct position (1-indexed).
    Cost per swap = w(token_a) + w(token_b).
    """
    if not graph:
        return

    n = len(graph)
    swap_log = []
    total_cost = 0

    # Build token-to-weight mapping
    weight_map = {token: weight for token, weight in graph}
    tokens = [token for token, _ in graph]

    print("\nInitial configuration:")
    for i, (token, weight) in enumerate(graph):
        print(f"  Vertex {i+1}: Token {token}, Weight {weight}")

    # Process tokens from largest to smallest
    for target_token in sorted(tokens, reverse=True):
        current_pos = tokens.index(target_token)
        correct_pos = target_token - 1  # 0-indexed target

        # Skip if already in correct position
        if current_pos == correct_pos:
            continue

        # Move token rightward to its correct position
        while current_pos < correct_pos:
            token_a = tokens[current_pos]
            token_b = tokens[current_pos + 1]
            cost = weight_map[token_a] + weight_map[token_b]
            swap_log.append((token_a, token_b, cost))
            total_cost += cost

            # Perform the swap
            tokens[current_pos], tokens[current_pos + 1] = (
                tokens[current_pos + 1],
                tokens[current_pos],
            )
            current_pos += 1

    # Print results
    print("\nSwap sequence:")
    for token_a, token_b, cost in swap_log:
        print(f"  Swap: {token_a} <-> {token_b},  Cost: {cost}")

    print(f"\nFinal arrangement: {tokens}")
    print(f"Total cost: {total_cost}")
    print(f"Total swaps: {len(swap_log)}")


# Driver Code
if __name__ == "__main__":
    my_graph = Graph()
    graph_data = my_graph.graph_input()
    weighted_token_sort(graph_data)
