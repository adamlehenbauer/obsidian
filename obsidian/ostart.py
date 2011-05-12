#!/usr/bin/python

"""
Starts a Java program defined by file 'cnf'.
"""
def ostart():
    import sys
    import argparse
    import ConfigParser
    import os

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

    args = jvm_opts
    args.append("-classpath")
    args.append(classpath)
    args.extend(system_opts)
    args.append(class_)
    args.extend(app_args)

    #print " ".join(args)

    os.execv(java_cmd, args)

if __name__ == "__main__":
    ostart()

