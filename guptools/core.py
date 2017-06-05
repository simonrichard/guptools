import networkx as nx
import networkx.algorithms.isomorphism as iso

from collections import defaultdict, ChainMap
from itertools import chain, filterfalse, repeat

from . import stacks
from .gupparser import import_grammar
from .polarities import PolaritySystem
from .utils import Forward


class Grammar:

    def __init__(self, funcs, polarity_system, structs):
        self.funcs = funcs
        self.polarity_system = PolaritySystem(*polarity_system)
        self.structs = {}
        for n, objects in structs.items():
            self.structs[n] = Structure(objects, self)

    @classmethod
    def _import(cls, path):
        return Grammar(*import_grammar(path))


class Structure(nx.DiGraph):

    def __init__(self, objects, grammar):
        self.grammar = grammar

        # A few shortcuts.
        self.funcs = self.grammar.funcs
        self.product = self.grammar.polarity_system.product

        super().__init__()
        for n, obj in objects.items():
            self.add_node(n, Object(obj))
        for n, obj in self.nodes(True):
            for func in set(obj) & set(self.funcs.structuring):
                self.add_edge(n, obj[func], func=func)
                obj[func] = self.node[obj[func]]

    def __eq__(self, other):
        """Return True if the two structures are isomorphic."""
        func_vals = iso.categorical_node_match(self.funcs.polarizing + self.funcs.labeling, repeat(None))
        func_name = iso.categorical_edge_match("func", None)
        return nx.is_isomorphic(self, other, func_vals, func_name)

    def assemble(self, other, fwtab, compl):
        """Return a new structure after a successful combination."""
        all_objects = chain(self.node.values(), other.node.values())
        # An object is copied if it wasn't forwarded to another object.
        objects_to_copy = filterfalse(fwtab.get, all_objects)

        # Objects are copied and updated. This dictionary maps objects to their copy.
        mapping = {obj: Object(ChainMap(compl[obj], obj)) for obj in objects_to_copy}
        new_objects = {"OBJ_%d" % (i + 1): obj for i, obj in enumerate(mapping.values())}
        key_by_object = {obj: n for n, obj in new_objects.items()}

        for obj in new_objects.values():
            for func in obj:
                if func in self.funcs.structuring:
                    copy = mapping[fwtab[obj[func]]]
                    obj[func] = key_by_object[copy]

        return Structure(new_objects, self.grammar)

    def combine(self, other):
        structures = []
        forward = Forward()
        compl = defaultdict(dict)

        for stack in stacks.generate(self, other):
            while stack:
                a, b = [forward[x] for x in stack.pop()]
                if a is b:
                    continue
                forward[b] = a

                for func, a_, b_ in Object.intersection(a, b, compl):
                    if func in self.funcs.structuring:
                        stack.append([a_, b_])
                    elif func in self.funcs.polarizing:
                        compl[a][func] = self.product(a_, b_)

                for func, b_ in Object.difference(b, a, compl):
                    compl[a][func] = forward[b_]

            structure = Structure.assemble(self, other, forward, compl)
            if structure not in structures:
                structures.append(structure)

            forward.clear()
            compl.clear()

        return structures

    def __add__(self, other):
        return self.combine(other)


class Object(dict):

    def __hash__(self):
        return id(self)

    def __bool__(self):
        return True

    def _compare(self, other, compl, intersection):
        self, other = [ChainMap(compl[x], x) for x in [self, other]]
        if intersection:
            for func in set(self) & set(other):
                yield func, self[func], other[func]
        else:
            for func in set(self) - set(other):
                yield func, self[func]

    def intersection(self, other, compl):
        return Object._compare(self, other, compl, True)

    def difference(self, other, compl):
        return Object._compare(self, other, compl, False)
