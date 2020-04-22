#!/usr/bin/env python3

import sys
import re
import binascii


file = sys.argv[1:]

if not file:
    file = ["/dev/stdin"]

with open(file[0], 'r') as f:
    pwds = f.read().splitlines()

for line in pwds:
    if line.strip() == "":
        continue

    uid, pwd = line.split(":", 1)

    part1 = ""
    part2 = ""

    if pwd.startswith("$HEX"):
        r = re.search(r'^\$HEX\[([0-9A-Za-z]+)\](.*)$', pwd)
        part1 = binascii.unhexlify(r.group(1)).decode('utf-8')
        if r.group(2):
            part2 = r.group(2)
    elif "$HEX" in pwd:
        r = re.search(r'^(.*)\$HEX\[([0-9A-Za-z]+)\]$', pwd)
        part2 = binascii.unhexlify(r.group(2)).decode('utf-8')

        if r.group(1):
            part1 = r.group(1)
    else:
        part1 = pwd

    print(uid + ":" + part1 + part2)




