#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
"""
>>> main("blondie_pp.pls")
{'File1': 'Blondie/Atomic/01-Atomic.ogg', 'Title1': 'Blondie - Atomic', \
'Length1': '230', 'File18': "Blondie/Atomic/18-I'm Gonna Love You Too.ogg", \
'Title18': "Blondie - I'm Gonna Love You Too", 'Length18': '-1', \
'NumberOfEntries': '18', 'Version': '2'}
"""
from typing import Any
import pyparsing as pp

PLS_PAIRS = dict[str, Any]


def bnf() -> pp.core.ParserElement:
    # fmt: off
    ini_header = (pp.Suppress("[") + pp.CharsNotIn("]")("header") +
                  pp.Suppress("]"))
    # fmt: on
    key = pp.Word(pp.alphas + pp.alphanums + "_").set_results_name("key")
    value = pp.restOfLine.set_results_name("value")
    key_value = key + pp.Suppress("=") + value
    blank = pp.Regex(r"^$")
    comment = pp.Regex(r"#.*")
    line = ini_header | key_value | comment | blank
    return line


def main(filename="blondie_pp.pls") -> PLS_PAIRS:
    pairs: PLS_PAIRS = {}
    with open(filename, "r") as f:
        for line in f:
            res = bnf().parse_string(line[:-1])
            if "key" in res:
                pairs[res["key"]] = res["value"]
    return pairs


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(main())
