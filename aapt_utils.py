#!/usr/bin/env python
# -*- coding: UTF-8 -*-


def parse_map(info):
    sub_values = info[info.find(":") + 1:]
    _map = {}
    for value in sub_values.split(" "):
        kv = parse_key_value(value.strip())
        if len(kv[0]) == 0:
            continue
        _map[kv[0]] = kv[1]
    return _map

def parse_key_value(kv):
    f = kv.find("=")
    key = kv[0:f]
    # value = kv[f + 1:]
    value = parse_value(kv[f + 1:])
    return (key, value)

def parse_value(v):    
    return v[v.find("'") + 1 :-1]