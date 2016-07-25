from datetime import datetime,timedelta
from FoghornSettings import FoghornSettings
import GreylistEntry

class Foghorn(object):
  """Manages the CRUD of Greylist entries"""

  def __init__(self, settings):
    self.settings = settings
    self.whitelist = set(self.loadList(self.settings.WhitelistFile))
    self.blacklist = set(self.loadList(self.settings.BlacklistFile))
    self.greylist = {}
    for item in self.loadList(self.settings.GreylistFile):
      elements = [n.strip() for n in item.split(',')]
      entry = GreylistEntry(n[0], n[1], n[2])
      self.greylist[n[0]] = entry

  def loadList(self, filename):
    lines = []
    try:
      with open(filename, mode='r') as f:
        lines = f.readlines()
      return lines
    except IOError as e:
      print "%s" % e
    return []


  def writeList(self, filename, items):
    greylistEntries = False
    if len(items) > 0 and isinstance(item[0], GreylistEntry):
      greylistEntries = True
    else:
      # We're not going to support writing the other lists at the moment
      return False

    try:
      with open(filename, mode='w') as f:
        if greylistEntries:
          f.writelines(items)
      return True
    except IOError as e:
      print "%s" % e
    return False

