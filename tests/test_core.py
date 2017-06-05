import networkx as nx

from guptools import SAMPLE_GRAMMAR
from guptools.core import Grammar, Object

G1 = Grammar._import(SAMPLE_GRAMMAR)
S1 = G1.structs["S1"]
S2 = G1.structs["S2"]


class TestStructure:

    def test___init__(self):
        assert len(S1) == 3
        assert S1.node["E1"]["source"] is S1.node["N1"]
        assert S1.node["E1"]["target"] is S1.node["N2"]

        # Objects should not be converted to dicts when they
        # are inserted.
        assert type(S1.node["E1"]) is Object
        assert S1.grammar is G1

    def test___eq__(self):
        S3 = nx.DiGraph.copy(S1)
        # Structure equality should not depend on object identifiers
        # because they are arbitrary.
        nx.relabel_nodes(S3, {"N2": "N3"}, copy=False)
        assert S1 == S3
        # Two structures should not be equal if at least one function
        # value pair is different.
        S3.node["N3"]["label"] = "cat"
        assert S1 != S3
