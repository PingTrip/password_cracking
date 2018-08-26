#!/usr/bin/env python

import sys
from collections import defaultdict
import string
import texttable as tt
import argparse
from math import sqrt


def calc_stndrd_dvtn(sample):
    mean = float(sum(sample)) / len(sample)
    sd = sqrt(sum((x - mean)**2 for x in sample) / (len(sample) - 1))
    return {'mean': mean, 'ssd': sd}


def calc_z(observation, stats):
    return (observation - stats['mean']) / stats['ssd']


def sort_gen(char_set):
    if args.sort_seen:
        for char, cnt in sorted(char_set['chr_cnts'].iteritems(), key=lambda (k, v): (v, k), reverse=True):
            yield (char, cnt)
    else:
        for char, cnt in sorted(char_set['chr_cnts'].iteritems()):
            yield(char, cnt)


parser = argparse.ArgumentParser(description='Character frequency analysis to aid in password cracking.')
parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin, help='password file to analyze')
parser.add_argument('--show-missing', action='store_true', help='Output includes characters with a count of zero')
parser.add_argument('--show-z', action='store_true', help='Calculates the Z-Score (sample standard deviation) for each character')
parser.add_argument('--sort-seen', action='store_true', help='Sort by counts each character occured')
args = parser.parse_args()

# Define the dicts tp hold character info
lower_d = {'chr_cnts': defaultdict(int)}
upper_d = {'chr_cnts': defaultdict(int)}
digits_d = {'chr_cnts': defaultdict(int)}
special_d = {'chr_cnts': defaultdict(int)}

format_str = " {0} = {1} "

# Read text from file
for line in args.infile:
    for c in line:
        if c == "\n":
            continue
        if c in string.ascii_lowercase:
            lower_d['chr_cnts'][c] += 1
        elif c in string.ascii_uppercase:
            upper_d['chr_cnts'][c] += 1
        elif c in string.digits:
            digits_d['chr_cnts'][c] += 1
        elif c in string.punctuation:
            special_d['chr_cnts'][c] += 1


if args.show_missing:
    for c in string.ascii_uppercase:
        if c not in upper_d['chr_cnts']:
            upper_d['chr_cnts'][c] = 0
    for c in string.ascii_lowercase:
        if c not in lower_d['chr_cnts']:
            lower_d['chr_cnts'][c] = 0
    for c in string.digits:
        if c not in digits_d['chr_cnts']:
            digits_d['chr_cnts'][c] = 0
    for c in string.punctuation:
        if c not in special_d['chr_cnts']:
            special_d['chr_cnts'][c] = 0

# Calculate sample standard deviation
if args.show_z:
    format_str = " {0} = {1} ({2:.2f})"

    upper_d['stats'] = calc_stndrd_dvtn(upper_d['chr_cnts'].values())
    lower_d['stats'] = calc_stndrd_dvtn(lower_d['chr_cnts'].values())
    digits_d['stats'] = calc_stndrd_dvtn(digits_d['chr_cnts'].values())
    special_d['stats'] = calc_stndrd_dvtn(special_d['chr_cnts'].values())
else:
    upper_d['stats'] = None
    upper_d['stats'] = None
    upper_d['stats'] = None
    upper_d['stats'] = None


# Build list of formated counts
if args.show_z:
    upper = [format_str.format(char, cnt, calc_z(cnt, upper_d['stats'])) for char, cnt in sort_gen(upper_d)]
    lower = [format_str.format(char, cnt, calc_z(cnt, lower_d['stats'])) for char, cnt in sort_gen(lower_d)]
    digits = [format_str.format(char, cnt, calc_z(cnt, digits_d['stats'])) for char, cnt in sort_gen(digits_d)]
    special = [format_str.format(char, cnt, calc_z(cnt, special_d['stats'])) for char, cnt in sort_gen(special_d)]
else:
    upper = [format_str.format(char, cnt) for char, cnt in sort_gen(upper_d)]
    lower = [format_str.format(char, cnt) for char, cnt in sort_gen(lower_d)]
    digits = [format_str.format(char, cnt) for char, cnt in sort_gen(digits_d)]
    special = [format_str.format(char, cnt) for char, cnt in sort_gen(special_d)]

max_row = max(len(upper), len(lower), len(digits), len(special))

# Pad columns to equal lengths
upper += [''] * (max_row - len(upper))
lower += [''] * (max_row - len(lower))
digits += [''] * (max_row - len(digits))
special += [''] * (max_row - len(special))

# Generate table for printing
tab = tt.Texttable()
headings = ['Upper', 'Lower', 'Digits', 'Special']
tab.header(headings)

for i in range(0, max_row):
    tab.add_row([upper[i], lower[i], digits[i], special[i]])

print tab.draw()
