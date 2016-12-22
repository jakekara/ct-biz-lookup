#!/usr/local/bin/python

from BizSearch import BizSearch
import sys

if len(sys.argv) < 3:
    exit(-1)

term = sys.argv[1]
outfile = sys.argv[2]

bs = BizSearch(outfile)
bs.search(term)
