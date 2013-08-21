#!/usr/bin/python
import os

class Service:
  def __init__(self, name, state):
    self.name = name
    self.status = "Unknown"
    self.desiredState = state
  
  def getStatus(self):
    if self.status == "Unknown":
      self.update()
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
    if self.getStatus() != "Running":
      return os.system("/sbin/service "+self.name+" start") == 0
    return True

  def stop(self):
    if self.getStatus() != "Stopped":
      return os.system("/sbin/service "+self.name+" stop") == 0
    return True

  def update(self):
    if os.system("/sbin/service "+self.name+" status | grep running") == 0:
      self.status = "Running"
      return
    self.status = "Stopped"
    
class InitdService(Service):
  def start(self):
    if self.getStatus() != "Running":
      return os.system("/etc/init.d/"+self.name+" start") == 0
    return True

  def stop(self):
    if self.getStatus() != "Stopped":
      return os.system("/etc/init.d/"+self.name+" stop") == 0
    return True

  def update(self):
    if os.system("/etc/init.d/"+self.name+" status | grep running") == 0:
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
