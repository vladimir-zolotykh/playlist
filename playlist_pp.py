#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
"""
>>> parse_file("blondie_pp.pls")
{'File1': 'Blondie/Atomic/01-Atomic.ogg', 'Title1': 'Blondie - Atomic', \
'Length1': '230', 'File18': "Blondie/Atomic/18-I'm Gonna Love You Too.ogg", \
'Title18': "Blondie - I'm Gonna Love You Too", 'Length18': '-1', \
'NumberOfEntries': '18', 'Version': '2'}
>>> parse_string("[playlist]\\n\
File1=Blondie/Atomic/01-Atomic.ogg\\n\
Title1=Blondie - Atomic\\n\
Length1=230\\n\
# A comment\\n\
\\n\
File18=Blondie/Atomic/18-I'm Gonna Love You Too.ogg\\n\
Title18=Blondie - I'm Gonna Love You Too\\n\
Length18=-1\\n\
NumberOfEntries=18\\n\
Version=2\\n\
")
{'File1': 'Blondie/Atomic/01-Atomic.ogg', 'Title1': 'Blondie - Atomic', \
'Length1': '230', 'File18': "Blondie/Atomic/18-I'm Gonna Love You Too.ogg", \
'Title18': "Blondie - I'm Gonna Love You Too", 'Length18': '-1', \
'NumberOfEntries': '18', 'Version': '2'}
"""
from typing import Any
import io
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
    line = ini_header | key_value | pp.pythonStyleComment | pp.Empty()
    return line


def parse_string(str_literal) -> PLS_PAIRS:
    so = io.StringIO(str_literal)
    return parse_file_obj(so)


def parse_file_obj(fo) -> PLS_PAIRS:
    pairs: PLS_PAIRS = {}
    for line in fo:
        res = bnf().parse_string(line[:-1])
        if "key" in res:
            pairs[res["key"]] = res["value"]
    return pairs


def parse_file(filename="blondie_pp.pls") -> PLS_PAIRS:

    with open(filename, "r") as f:
        return parse_file_obj(f)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
