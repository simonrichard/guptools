import networkx as nx

from collections import defaultdict
from itertools import chain, combinations
from itertools import product as cartesian

__all__ = ["generate"]

THRESHOLD = 25


def filter_non_viable(pairs, grammar):
    """Return a list of pairs that seem to be compatible."""
    viable_dict = dict()
    pairs = list(pairs)
    unsure = defaultdict(int)

    while pairs:
        for i, pair in reversed(list(enumerate(pairs))):
            if is_viable(pair, viable_dict, grammar) is None:
                unsure[pair] += 1
                if unsure[pair] < THRESHOLD:
                    continue
                viable_dict[pair] = True
            del pairs[i]
    return [pair for pair in viable_dict if viable_dict[pair]]


def is_viable(pair, viable_dict, grammar):
    """Return False if the pair has incompatible function-value pairs."""
    a, b = pair
    viable = unsure = None

    funcs = grammar.funcs
    product_table = grammar.polarity_system.table

    non_viable_criteria = [
        lambda f, v: f in funcs.labeling and v[0] != v[1],
        lambda f, v: f in funcs.structuring and viable_dict.get(v) is False,
        lambda f, v: f in funcs.polarizing and not product_table[v[0]].get(v[1])
    ]

    for func in set(a) & set(b):
        x = a[func], b[func]
        if any(test(func, x) for test in non_viable_criteria):
            viable = False
            break
        elif func in grammar.funcs.structuring and viable_dict.get(x) is None:
            unsure = True
    else:
        if not unsure:
            viable = True

    viable_dict[pair] = viable
    return viable


def implications(pair, grammar):
    a, b = pair
    for func in set(a) & set(b) & set(grammar.funcs.structuring):
        linked_pair = a[func], b[func]
        yield tuple(map(frozenset, (pair, linked_pair)))


def indirect(stack):
    """Return all the pairs that are unified indirectly in a stack."""
    g = nx.Graph(stack)
    for group in nx.connected_components(g):
        yield from map(frozenset, combinations(group, 2))


def generate(a, b):
    grammar = a.grammar
    a, b = [x.node.values() for x in [a, b]]

    pairs = filter_non_viable(cartesian(a, b), grammar)
    intra = map(lambda s: cartesian(s, repeat=2), (a, b))
    intra = filter_non_viable(chain(*intra), grammar)
    viable_pairs = set(map(frozenset, pairs + intra))

    stacks = chain.from_iterable(
        combinations(pairs, n) for n in range(1, len(pairs)+1))
    implic = tuple(chain(*(implications(p, grammar) for p in pairs)))

    for stack in map(list, stacks):
        stack_ = set(map(frozenset, stack))

        if any(stack_ & {x, i} == {x} for x, i in implic):
            continue
        if any(not viable_pairs & {s} for s in indirect(stack)):
            continue

        yield stack
