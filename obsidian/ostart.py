#!/usr/bin/python

import sys
import argparse

parser = argparse.ArgumentParser(description='Starts the process named by \'appid\'')
parser.add_argument('appid', metavar='appid', type=str)
parser.add_argument('--dry-run', '-d', action='store_true')

args = parser.parse_args()

if args.appid:
    print "starting [%s]" % sys.argv[1]
else:
    print "appid required"
