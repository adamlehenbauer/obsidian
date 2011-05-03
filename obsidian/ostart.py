#!/usr/bin/python

import sys
import argparse
import ConfigParser

parser = argparse.ArgumentParser(description='Starts the process named by \'appid\'')
parser.add_argument('appid', metavar='appid', type=str)
parser.add_argument('--dry-run', '-d', action='store_true')

args = parser.parse_args()
appid = args.appid

if appid:
    print "starting [%s]" % sys.argv[1]
else:
    print "appid required"
    exit(1)

config = ConfigParser.ConfigParser()
config.read('cnf')

# get the config file defaults out first, and recreate
# the config, providing those
defaults = dict(config.items('default'))
config = ConfigParser.ConfigParser(defaults)
config.read('cnf')

java_cmd = config.get(appid, 'java_home')
classpath = config.get(appid, 'classpath')
class_ = config.get(appid, 'class')
java_opts = config.get(appid, 'java_opts')
# TODO
app_args = config.get(appid, 'conf')

print " ".join([java_cmd, "-classpath", classpath, java_opts, class_, app_args])
