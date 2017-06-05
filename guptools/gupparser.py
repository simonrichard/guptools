from collections import defaultdict, namedtuple
from pyparsing import *

__all__ = ["import_grammar"]

Functions = namedtuple("Functions", ["polarizing", "structuring", "labeling"])


def bracketed(expr, brackets="{}"):
    l_b, r_b = [Literal(b).suppress() for b in brackets]
    return l_b + expr + r_b


def section(head, body):
    return Literal(head).suppress() + bracketed(body)


def get_parser():
    identifier = Word(alphanums + alphas8bit + "_")
    multiword = identifier | QuotedString('"')

    funcs = Group(Each(
        Group(section(t, ZeroOrMore(identifier))).setResultsName(t)
        for t in Functions._fields)
    )

    polarities = section("polarities", ZeroOrMore(identifier))
    neutral = section("neutral", ZeroOrMore(identifier))
    product = bracketed(Group(identifier * 3), "()")
    product_table = section("product_table", ZeroOrMore(product))

    pair = Group(identifier + Literal("=").suppress() + multiword)
    object = Group(identifier + bracketed(Group(delimitedList(pair))))
    struct = Group(identifier + bracketed(Group(ZeroOrMore(object))))
    structs = Group(ZeroOrMore(struct))

    grammar_def = (
        funcs.setResultsName("functions") +
        polarities.setResultsName("polarities") +
        neutral.setResultsName("neutral") +
        product_table.setResultsName("product") +
        structs.setResultsName("structures")
    )

    # Allow Python-style block and inline comments.
    grammar_def = grammar_def.ignore("#" + restOfLine)

    return grammar_def


def import_grammar(path):
    with open(path) as gup:
        g = gup.read()
        g = get_parser().parseString(g)

    product_table = defaultdict(dict)
    for p1, p2, product in g["product"]:
        product_table[p1][p2] = product
        product_table[p2][p1] = product
    polarities = g["polarities"].asList()
    neutral = g["neutral"].asList()
    polarity_system = polarities, neutral, product_table

    functions = Functions(**{t: funcs.asList() for t, funcs in g["functions"].items()})
    structures = {}
    for n, objects in g["structures"]:
        structures[n] = {obj: pairs.asList() for obj, pairs in objects}

    return functions, polarity_system, structures
