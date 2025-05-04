#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Union
import re

INI_HEADER = re.compile(r"^\[[^]]+\]$")
KEY_VALUE_RE = re.compile(r"^(?P<key>\w+)\s*=\s*(?P<value>.*)$")
VOC_TYPE = dict[str, Union[str, int]]  # vocabulary


def parse(file, vocabulary: VOC_TYPE, lowercase_keys=False) -> VOC_TYPE:
    for lino, line in enumerate(file, start=1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        key_value = KEY_VALUE_RE.match(line)
        if key_value:
            key = key_value.group("key")
            if lowercase_keys:
                key = key.lower()
            vocabulary[key] = key_value.group("value")
        else:
            ini_header = INI_HEADER.match(line)
            if not ini_header:
                print("Failed to parse line {0}: {1}".format(lino, line))
    return vocabulary


blondie_voc: VOC_TYPE = {}
if __name__ == "__main__":
    with open("blondie.pls") as f:
        parse(f, blondie_voc)
    print(blondie_voc)
