#!/usr/bin/env python

import sys
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

    if "$HEX" in pwd:
        pwd = binascii.unhexlify(pwd[pwd.find("[") + 1:pwd.find("]")]).decode('utf-8')

    print uid + ":" + pwd
    
