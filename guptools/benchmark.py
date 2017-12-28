import argparse
import re
import time

from itertools import product
from statistics import mean
from tabulate import tabulate

from . import import_grammar, stacks, SAMPLE_GRAMMAR


DEFAULT_NUM_ITERATIONS = 25


def get_stack_benchmarks(grammar, num_iterations=None, pattern=None):
    grammar = import_grammar(grammar or SAMPLE_GRAMMAR)
    pattern = re.compile(pattern or '')
    num_iterations = num_iterations or DEFAULT_NUM_ITERATIONS
    structs = {n: struct for n, struct in grammar.structs.items() if pattern.search(n)}

    for n_a, n_b in product(structs, repeat=2):
        times = []
        for _ in range(num_iterations):
            start = time.time()
            for _ in stacks.generate(structs[n_a], structs[n_b]):
                pass
            times.append(time.time() - start)
        yield (n_a, n_b, mean(times))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--grammar', type=str)
    parser.add_argument('--num-iterations', type=int)
    parser.add_argument('--pattern', type=str)
    args = parser.parse_args()

    benchmarks = get_stack_benchmarks(args.grammar, args.num_iterations, args.pattern)
    print(tabulate(
        benchmarks,
        headers=('Struct #1', 'Struct #2', 'Average'),
        tablefmt='psql',
        floatfmt='.8f'
    ))


if __name__ == '__main__':
    main()
