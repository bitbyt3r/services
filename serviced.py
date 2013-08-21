#!/usr/bin/python

import os
import sys
import time
import daemon
import signal
import lockfile
import traceback
import ConfigParser
import serviceInfo

CONFIG_FILE = "/extra/projects/services/serviced.conf"
LOCK_FILE = "/var/lock/serviced.pid"

def getConfig(configfile):
  config = ConfigParser.ConfigParser()
  config.readfp(open(configfile))
  return dict((key, value) for (key, value) in config.items("main"))

def reloadConfig():
  config = getConfig(CONFIG_FILE)
  services = [serviceInfo.makeService(x.strip(), "Running") for x in config['start'].split(",")]
  services.extend([serviceInfo.makeService(x.strip(), "Stopped") for x in config['stop'].split(",")])
  return config, services

def checkState(services):
  for i in services:
    i.correctState()

def main():
  context = daemon.DaemonContext()
  context.stderr = open("/extra/projects/services/stderr.log", "w+")
  context.stdout = open("/extra/projects/services/stdout.log", "w+")
  context.pidfile = lockfile.FileLock(LOCK_FILE)
  if not("-f" in sys.argv):
    print "Entering Daemon Mode"
    config, services = reloadConfig()
#    with context:
    if True:
      print "Going"
      while True:
        config, services = reloadConfig()
        print config, services
        checkState(services)
        time.sleep(float(config['sleep_time']))
  else:
    print "Running outside of Daemon"
    while True:
      config, services = reloadConfig()
      checkState(services)
      time.sleep(float(config['sleep_time']))

main()
