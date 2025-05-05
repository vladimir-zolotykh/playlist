#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Any
from numbers import Number
import pyparsing as pp

PLS_PAIRS = dict[str, Any]


def bnf() -> pp.core.ParserElement:
    ini_header = pp.Combine(pp.Literal("[") + pp.Regex(r"[^]]+") + pp.Literal("]"))
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
    print(main())
