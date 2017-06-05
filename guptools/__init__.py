from os.path import dirname, join

from .core import Grammar

import_grammar = Grammar._import

SAMPLE_GRAMMAR = join(dirname(__file__), "data/sample.gup")
