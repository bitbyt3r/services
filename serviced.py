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

def checkState(config):
  processes = []
  processes.extend([process(x, "start") for x in config['start'].split(" ")])
  processes.extend([process(x, "stop") for x in config['stop'].split(" ")])
  
  

def main():
  context = daemon.DaemonContext()
  context.signal_map = {
    signal.SIGUSR1: reloadConfig(config),
    }
  context.pidfile = lockfile.FileLock(LOCK_FILE)
  with context:
    while True:
      checkState(config)
      time.sleep(config['sleepTime'])
    
main()

class process:
  def __init__(self, name, state):
    self.name = name
    self.status = "Unknown"
    self.desiredState = state
    methods = {
      "mrepo": (serviceStatus, serviceSet),
      }
    if self.name in methods.keys():
      self.checkMethod, self.setMethod = methods[self.name]
    else:
      self.checkMethod, self.setMethod = (serviceStatus, serviceSet)
