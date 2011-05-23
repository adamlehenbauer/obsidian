#!/usr/bin/python

import os

# ./.obs.cnf and ~/.obs.cnf
project_conf_name = '.obs.cnf'
# /etc/obs.cnf
system_conf_name = '/etc/obsidian.cnf'

"""
Starts a Java program defined by file 'cnf'.
"""
def ostart():
    import sys
    import argparse
    import ConfigParser

    parser = argparse.ArgumentParser(description='Starts the process named by \'appid\'')
    parser.add_argument('appid', metavar='appid', type=str)
    parser.add_argument('--dry-run', '-d', action='store_true')
    parser.add_argument('--file', '-f', dest='conf_file', type=str)

    args = parser.parse_args()
    appid = args.appid
    conf_file = args.conf_file

    if conf_file:
        conf_file = open(conf_file, 'r')
    else:
        conf_file = find_conf_file()

    if not conf_file:
        raise ConfigError('could not find config file')
        
    if appid:
        print "starting [%s]" % appid
    else:
        print "appid required"
        exit(1)

    config = ConfigParser.ConfigParser()
    #config.readfp(conf_file)
    config.read(conf_file.name)

    # get the config file defaults out first, and recreate
    # the config, providing those
    defaults = dict(config.items('default'))
    config = ConfigParser.ConfigParser(defaults)
    #config.readfp(conf_file)
    config.read(conf_file.name)

    java_cmd = config.get(appid, 'java_home') + "/bin/java"
    classpath = config.get(appid, 'classpath')
    class_ = config.get(appid, 'class')

    jvm_opts = config.get(appid, 'java_opts')
    jvm_opts = jvm_opts.split(' ')

    if config.has_option(appid, 'system_opts'):
        system_opts = config.get(appid, 'system_opts')
        system_opts = system_opts.split(' ')
    else:
        system_opts = []

    if config.has_option(appid, 'conf'):
        app_args = config.get(appid, 'conf')
        app_args = app_args.split(' ')
    else:
        app_args = []

    c_args = [java_cmd]
    c_args.extend(jvm_opts)
    c_args.append("-classpath")
    c_args.append(classpath)
    c_args.extend(system_opts)
    c_args.append(class_)
    c_args.extend(app_args)

    #print " ".join(args)
    if args.dry_run:
       print " ".join(c_args)
       return

    os.execv(java_cmd, c_args)

def find_conf_file():
    conf_file = find_in_parent_dir(project_conf_name)
    if(conf_file):
        return conf_file

    conf_file = os.path.expanduser(os.path.join('~', project_conf_name))
    if os.path.exists(conf_file):
        return open(conf_file, 'r')

    if os.path.exists(system_conf_name):
        return open(system_conf_name, 'r')
        
    return None

def find_in_parent_dir(fname):
    p = os.path.abspath(os.path.curdir)
    
    while not os.path.exists(os.path.join(p, project_conf_name)):
        oldp, p = p, os.path.dirname(p)
        if p == oldp:
            return None
    
    return open(os.path.join(p, project_conf_name), 'r') 

class ConfigError(Exception):
    def __init__(self, msg):
        self.msg = msg

if __name__ == "__main__":
    try:
        ostart()
    except ConfigError as e:
        print e.msg

