#!/usr/bin/python

import os
import sys
import time
import daemon
import signal
import ConfigParser

CONFIG_FILE = "/usr/csee/etc/serviced.conf"

def getConfig(configfile):

def reloadConfig(config):
  config = getConfig(configFile)

def checkState(config):

def main():
  config = getConfig(CONFIG_FILE)
  context = daemon.DaemonContext()
  context.signal_map = {
    signal.SIGUSR1: reloadConfig(config),
    }
  with context:
    while True:
      checkState(config)
      time.sleep(config['sleepTime'])
    
main()
