import constraint
import networkx as nx

from itertools import product as cartesian
from math import ceil, log
from operator import add


class PolaritySystem:

    def __init__(self, polarities, neutral, product_table):
        self.P = polarities
        self.N = neutral
        self.table = product_table

        self.is_monotone = True
        self.is_final = True
        self.is_declarative = True
        self.is_dynamic = bool(set(self.P) > set(self.N) and self.N)

        g = nx.DiGraph()
        for a in self.table:
            for prod in self.table[a].values():
                if a != prod:
                    g.add_edge(a, prod)

        try:
            order = nx.topological_sort(g)
            if set(self.N) != set(order[-len(self.N):]):
                self.is_final = False
        except nx.NetworkXUnfeasible:
            self.is_monotone = False
            self.is_final = False

        for a, b, c in cartesian(self.table, repeat=3):
            try:
                x = self.table[self.table[a][b]][c]
                y = self.table[self.table[b][c]][a]
                if x != y:
                    self.is_declarative = False
                    break
            except KeyError:
                continue

    def product(self, x, y):
        return self.table[x][y]

    def decompose(self):
        def sum_eq(a, b, c):
            return tuple(map(add, a, b)) == c

        length = ceil(log(len(self.P), 2))
        configs = cartesian([0, 1], repeat=length)

        prob = constraint.Problem()
        prob.addVariables(self.P, list(configs))
        prob.addConstraint(constraint.AllDifferentConstraint())

        for p1 in self.table:
            for p2 in self.table[p1]:
                prob.addConstraint(sum_eq, (p1, p2, self.table[p1][p2]))

        return prob.getSolution()
