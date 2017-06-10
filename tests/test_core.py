import networkx as nx

from guptools import SAMPLE_GRAMMAR
from guptools.core import Grammar, Structure, Object
from guptools.utils import Complement

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

    def test__is_neutral(self):
        assert S1.is_neutral is True
        assert S2.is_neutral is False

    def test__to_dict(self):
        objects = {
            "N1": {"type": "node", "label": "eat", "polarity": "black"},
            "N2": {"type": "node", "polarity": "white"},
            "N3": {"type": "node", "polarity": "white"},
            "E1": {"type": "edge", "label": "1", "source": "N1", "target": "N2", "polarity": "black"},
            "E2": {"type": "edge", "label": "2", "source": "N1", "target": "N3", "polarity": "black"}
        }
        S3 = Structure(objects, G1)
        assert S3.to_dict() == objects


class TestObject:

    def test_intersection(self):
        O1 = S1.node["N1"]
        O2 = S2.node["E1"]
        inter = Object.intersection(O1, O2, Complement())
        expected = [
            ("type", "node", "edge"),
            ("label", "sleep", "1"),
            ("polarity", "black", "black")
        ]
        assert set(inter) == set(expected)

        # The function-value pairs in compl should have priority
        # over the contents of an object.
        compl = Complement()
        compl[O2]["label"] = "2"
        inter = Object.intersection(O1, O2, compl)
        expected[1] = ("label", "sleep", "2")
        assert set(inter) == set(expected)

    def test_difference(self):
        O1 = S1.node["N1"]
        O2 = S2.node["N2"]
        diff = Object.difference(O1, O2, Complement())
        expected = [
            ("label", "sleep")
        ]
        assert set(diff) == set(expected)

        # The function-value pairs in compl should have priority
        # over the contents of an object.
        compl = Complement()
        compl[O2]["label"] = "dog"
        assert set(Object.difference(O1, O2, compl)) == set()
