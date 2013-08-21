#!/usr/bin/python

import os
import sys
import time
import daemon
import signal
import lockfile
import ConfigParser

CONFIG_FILE = "/usr/csee/etc/serviced.conf"
LOCK_FILE = "/var/lock/serviced.pid"

def getConfig(configfile):
  config = ConfigParser.ConfigParser()
  config.readfp(open(configfile))
  return dict((key, value) for (key, value) in config.items("main"))

config = getConfig(CONFIG_FILE)

def reloadConfig(config):
  config = getConfig(CONFIG_FILE)
  services = [serviceInfo.makeService(x.strip(), "Running") for x in config['start'].split(",")]
  services.extend([serviceInfo.makeService(x.strip(), "Stopped") for x in config['stop'].split(",")]

def checkState(config):
  services = []
  processes.extend([process(x, True) for x in config['start'].split(" ")])
  processes.extend([process(x, False) for x in config['stop'].split(" ")])
  for i in processes:
    if i.desiredState:
      i.start()
    else:
      i.stop()

def main():
  context = daemon.DaemonContext()
  context.signal_map = {
    signal.SIGUSR1: reloadConfig(config),
    }
  context.pidfile = lockfile.FileLock(LOCK_FILE)
  sys.exit(0)
  if not("-f" in sys.argv):
    with context:
      while True:
        checkState(config)
        time.sleep(float(config['sleep_time']))
  else:
    while True:
      checkState(config)
      time.sleep(float(config['sleep_time']))

main()
