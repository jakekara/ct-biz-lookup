# CLI tool for CT Biz Registration lookup
#
# usage: python ctbiz.py SEARCH_TERM OUTPUT_FILENAME
# Searches for SEARCH_TERM and saves to OUTPUT_FILENAME as a csv

import sys
from BizSearch import BizSearch

if len(sys.argv) < 3:
    print "Invalid usage"
    exit(1)

term = sys.argv[1]
outfile = sys.argv[2]
s = BizSearch()
s.search(term)
s.write(outfile)
