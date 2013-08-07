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
  processes.extend([process(x, True) for x in config['start'].split(" ")])
  processes.extend([process(x, False) for x in config['stop'].split(" ")])
  for i in processes:
    if i.checkMethod(i.name) != i.desiredState:
      i.setMethod(i.name, i.desiredState)

def main():
  context = daemon.DaemonContext()
  context.signal_map = {
    signal.SIGUSR1: reloadConfig(config),
    }
  context.pidfile = lockfile.FileLock(LOCK_FILE)
  for i in config['stop'].split(" "):
    os.system("/sbin/service "+i+" status")
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

    
def serviceStatus(name):
  return os.system("/sbin/service "+name+" status | grep stopped")

def serviceSet(name, state):
  if state:
    stateText = "start"
  else:
    stateText = "stop"
  os.system("/sbin/service "+name+" "+stateText)

class process:
  def __init__(self, name, state):
    self.name = name
    self.status = "Unknown"
    self.desiredState = state
    methods = {
      "cfengine3": (serviceStatus, serviceSet),
      "mdmonitor": (serviceStatus, serviceSet),
      "xinetd": (serviceStatus, serviceSet),
      "httpd": (serviceStatus, serviceSet),
      "tomcat6": (serviceStatus, serviceSet),
      "abrtd": (serviceStatus, serviceSet),
      "avahi-daemon": (serviceStatus, serviceSet),
      "avahi-dnsconfd": (serviceStatus, serviceSet),
      "cachefilesd": (serviceStatus, serviceSet),
      "iscsi": (serviceStatus, serviceSet),
      "iscsid": (serviceStatus, serviceSet),
      "lldpad": (serviceStatus, serviceSet),
      "ifdhandler": (serviceStatus, serviceSet),
      "pcscd": (serviceStatus, serviceSet),
      "pppoe-server": (serviceStatus, serviceSet),
      "qpidd": (serviceStatus, serviceSet),
      "rhsmcertd": (serviceStatus, serviceSet),
      "sanlock": (serviceStatus, serviceSet),
      "slpd": (serviceStatus, serviceSet),
      "spiceusbsrvd": (serviceStatus, serviceSet),
      "spice-vdagentd": (serviceStatus, serviceSet),
      "virt-who": (serviceStatus, serviceSet),
      "wdmd": (serviceStatus, serviceSet),

      }
    if self.name in methods.keys():
      self.checkMethod, self.setMethod = methods[self.name]
    else:
      self.checkMethod, self.setMethod = (serviceStatus, serviceSet)

main()
