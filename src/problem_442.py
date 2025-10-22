# Problem: https://projecteuler.net/problem=442
from collections import deque, defaultdict

class Node:
    def __init__(self):
        self.children = [None] * 10
        self.fail = None
        self.output = False

def main():
    """
    Purpose
    -------
    Solves Project Euler problem 442 by finding the 10^18-th eleven-free integer, where an eleven-free
    integer does not contain any substring that is a power of 11 except 1 in its decimal representation.

    Method / Math Rationale
    -----------------------
    Constructs an Aho-Corasick automaton for the forbidden substrings (decimal representations of
    11^k for k >= 1). Identifies good states (no match). Uses dynamic programming to precompute the
    number of valid ways to extend from each good state with a given number of digits. Determines the
    digit length d for the result, then constructs the number digit by digit by greedily choosing the
    smallest digit that covers the remaining count.

    Complexity
    ----------
    O(sum of pattern lengths * 10 + max_d * num_states * 10), which is small (around 10^5 operations)
    given max_d=50 and num_states ~5000.

    References
    ----------
    https://projecteuler.net/problem=442
    """
    patterns = []
    power = 11
    for _ in range(100):
        pat = [int(c) for c in str(power)]
        patterns.append(pat)
        power *= 11

    root = Node()
    for pat in patterns:
        node = root
        for digit in pat:
            if node.children[digit] is None:
                node.children[digit] = Node()
            node = node.children[digit]
        node.output = True

    root.fail = root
    queue = deque()
    for i in range(10):
        if root.children[i]:
            root.children[i].fail = root
            queue.append(root.children[i])
        # No else: implicit to root in get_next

    while queue:
        current = queue.popleft()
        for i in range(10):
            if current.children[i]:
                child = current.children[i]
                queue.append(child)
                f = current.fail
                while f != root and f.children[i] is None:
                    f = f.fail
                child.fail = f.children[i] if f.children[i] else root
                child.output = child.output or child.fail.output

    all_nodes = []
    def collect(node):
        if node:
            all_nodes.append(node)
            for child in node.children:
                collect(child)
    collect(root)

    good_nodes = [node for node in all_nodes if not node.output]
    id_map = {node: i for i, node in enumerate(good_nodes)}

    def get_next(current, digit):
        while current != root and current.children[digit] is None:
            current = current.fail
        if current.children[digit]:
            return current.children[digit]
        return root

    adj = [defaultdict(int) for _ in good_nodes]
    for s_idx, s_node in enumerate(good_nodes):
        for d in range(10):
            next_node = get_next(s_node, d)
            if not next_node.output:
                t_idx = id_map[next_node]
                adj[s_idx][t_idx] += 1

    max_d = 50
    counts = [[0] * len(good_nodes) for _ in range(max_d + 1)]
    for s in range(len(good_nodes)):
        counts[0][s] = 1
    for l in range(1, max_d + 1):
        for s in range(len(good_nodes)):
            for t, mult in adj[s].items():
                counts[l][s] += mult * counts[l - 1][t]

    def get_exact(d):
        if d == 0:
            return 0
        res = 0
        for dig in range(1, 10):
            next_node = get_next(root, dig)
            if not next_node.output:
                res += counts[d - 1][id_map[next_node]]
        return res

    n = 10**18
    cum = 0
    d = 0
    while True:
        d += 1
        exact = get_exact(d)
        if cum + exact >= n:
            break
        cum += exact

    remaining = n - cum
    res = []
    current_node = root
    for pos in range(d):
        dig_range = range(1, 10) if pos == 0 else range(10)
        for dig in dig_range:
            next_node = get_next(current_node, dig)
            if next_node.output:
                continue
            cnt = counts[d - pos - 1][id_map[next_node]]
            if remaining <= cnt:
                res.append(str(dig))
                current_node = next_node
                break
            else:
                remaining -= cnt

    print(''.join(res))

if __name__ == "__main__":
    main()