#!/usr/bin/python
import os

class Service:
  def __init__(self, name, state):
    self.name = name
    self.status = "Unknown"
    self.desiredState = state
  
  def getStatus(self):
    if self.status == "Unknown":
      self.running()
    return self.status

  def check(self):
    return self.getStatus() == self.desiredState

  def correctState(self):
    if not(self.check()):
      if self.desiredState == "Running":
        self.start()
      else:
        self.stop()
    return self.check()

class SysvService(Service):
  def start(self):
    if not(self.running()):
      os.system("/sbin/service "+self.name+" start")
    return self.running()

  def stop(self):
    if self.running():
      os.system("/sbin/service "+self.name+" stop")
    return not(self.running())

  def running(self):
    if not(os.system("/sbin/service "+self.name+" status | grep running")):
      self.status = "Running"
      return True
    self.status = "Stopped"
    return False
    

services = {"cfengine3":SysvService,
            "mdmonitor":SysvService,
            "xinetd":SysvService,
            "httpd":SysvService,
            "tomcat6":SysvService,
            "abrtd":SysvService,
            "avahi-daemon":SysvService,
            "avahi-dnsconfd":SysvService,
            "cachefilesd":SysvService,
            "iscsi":SysvService,
            "iscsid":SysvService,
            "lldpad":SysvService,
            "ifdhandler":SysvService,
            "pcscd":SysvService,
            "pppoe-server":SysvService,
            "qpidd":SysvService,
            "rhsmcertd":SysvService,
            "sanlock":SysvService,
            "slpd":SysvService,
            "spiceusbsrvd":SysvService,
            "spice-vdagentd":SysvService,
            "virt-who":SysvService,
            "wdmd":SysvService,}

def makeService(name, desiredState):
  if name in services.keys():
    return services[name](name, desiredState)
  return SysvService(name, desiredState)
