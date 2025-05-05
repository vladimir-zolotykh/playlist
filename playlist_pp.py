#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import pyparsing as pp


def bnf() -> pp.core.ParserElement:
    ini_header = pp.Combine(pp.Literal("[") + pp.Regex(r"[^]]+") + pp.Literal("]"))
    value = pp.Regex(r".+")
    key = pp.Word(pp.alphas + pp.alphanums)
    key_value = key + pp.Literal("=") + value
    blank = pp.Regex(r"^$")
    comment = pp.Regex(r"#.*")
    line = ini_header | key_value | comment | blank
    return line


if __name__ == "__main__":
    with open("blondie_pp.pls", "r") as f:
        for line in f:
            res = bnf().parse_string(line[:-1])
            print(res)
