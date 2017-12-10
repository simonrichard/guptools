guptools
========

guptools is a Python toolkit to develop polarized unification grammars (in French:
Grammaires d'Unification Polarisées)<sup>1</sup>. It was developed
as part of my master's thesis in linguistics at Université de Montréal. I worked with
[François Lareau](http://www.francoislareau.info/) at the [Observatoire
de linguistique Sens-Texte](http://olst.ling.umontreal.ca/).

[1] Kahane, S. (2004). Grammaires d'unification polarisées.
Proceedings of TALN 2004 (pp. 233-242). Fez, Morocco.

Installation
------------

guptools is not on PyPI so it must be downloaded and installed manually.
Dependencies are listed in setup.py and requirements.txt and are installed
automatically when you install the module with pip.

```shell
git clone https://github.com/simonrichard/guptools.git
cd guptools/
pip install .
```

Quickstart
----------

```python
>>> from guptools import import_grammar, SAMPLE_GRAMMAR
>>> G = import_grammar(SAMPLE_GRAMMAR)
>>> S1 = G.structs["S1"]
>>> S2 = G.structs["S2"]

>>> print(S1)
[      [ label    = '1'     ] ]
[      [ polarity = 'black' ] ]
[ E1 = [ source   = 'N1'    ] ]
[      [ target   = 'N2'    ] ]
[      [ type     = 'edge'  ] ]
[                             ]
[      [ label    = 'sleep' ] ]
[ N1 = [ polarity = 'black' ] ]
[      [ type     = 'node'  ] ]
[                             ]
[      [ label    = 'dog'   ] ]
[ N2 = [ polarity = 'black' ] ]
[      [ type     = 'node'  ] ]
  
>>> results = S1 + S2
>>> print(len(results))
2
>>> print(results[1])
[         [ label    = 'sleep' ] ]
[ OBJ_1 = [ polarity = 'black' ] ]
[         [ type     = 'node'  ] ]
[                                ]
[         [ label    = 'dog'   ] ]
[ OBJ_2 = [ polarity = 'black' ] ]
[         [ type     = 'node'  ] ]
[                                ]
[         [ label    = 'small' ] ]
[ OBJ_3 = [ polarity = 'black' ] ]
[         [ type     = 'node'  ] ]
[                                ]
[         [ label    = '1'     ] ]
[         [ polarity = 'black' ] ]
[ OBJ_4 = [ source   = 'OBJ_1' ] ]
[         [ target   = 'OBJ_2' ] ]
[         [ type     = 'edge'  ] ]
[                                ]
[         [ label    = '1'     ] ]
[         [ polarity = 'black' ] ]
[ OBJ_5 = [ source   = 'OBJ_3' ] ]
[         [ target   = 'OBJ_2' ] ]
[         [ type     = 'edge'  ] ]
  
>>> results[1].is_neutral
True
```

Questions or problems
---------------------

Feel free to create a new issue on [GitHub](https://github.com/simonrichard/guptools) if you have any questions or problems.
