# Problem: https://projecteuler.net/problem=122
import itertools

def main():
    limit = 200
    min_operations = [0, 0] + [None] * (limit - 1)
    num_unknown = [limit - 1]

    def explore_chains(chain, max_ops):
        if len(chain) > max_ops or num_unknown[0] == 0:
            return

        max_val = chain[-1]
        for i in reversed(range(len(chain))):
            for j in reversed(range(i + 1)):
                sum_val = chain[i] + chain[j]
                if sum_val <= max_val:
                    break
                if sum_val <= limit:
                    chain.append(sum_val)
                    if min_operations[sum_val] is None:
                        min_operations[sum_val] = len(chain) - 1
                        num_unknown[0] -= 1
                    explore_chains(chain, max_ops)
                    chain.pop()

    for ops in itertools.count(1):
        if num_unknown[0] == 0:
            return str(sum(min_operations))
        explore_chains([1], ops)

if __name__ == "__main__":
    print(main())