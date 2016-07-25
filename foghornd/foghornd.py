#!/usr/bin/env python

import sys, os, logging, time
from datetime import datetime
from twisted.internet import reactor
from twisted.names import client, dns, server

from FoghornSettings import FoghornSettings
from Foghorn import Foghorn


class Main(object):
  foghorn = None
  settings = None

  def __init__(self):
    self.settings = FoghornSettings()
    self.foghorn = Foghorn(self.settings)
    logger = logging.getLogger('foghornd')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s %(levelname)8s %(message)s")
    cl = logging.StreamHandler()
    cl.setLevel(logging.DEBUG)
    cl.setFormatter(formatter)
    logger.addHandler(cl)
    fh = logging.FileHandler(self.settings.logfile)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

  def run(self):
    #kick off the server
    factory = server.DNSServerFactory(
        clients=[self.foghorn, client.Resolver(resolv='/etc/resolv.conf')]
    )
    protocol = dns.DNSDatagramProtocol(controller=factory)

    reactor.listenUDP(self.settings.DNSPort, protocol)
    reactor.listenTCP(self.settings.DNSPort, factory)

    reactor.run()
#    # TODO: make this able to stop gracefully
#    while True:
#      sniff(filter=self.filterString,prn=DNS_Responder(self.settings.GreyIP))
#      if (refresh < (datetime.now() - self.settings.RefreshPeriod)):
#        refresh = datetime.now()
#        writeGreyList(GreylistFile, greylist)
#
#  def DNS_Responder(localIP):
#    def forwardDNS(orig_pkt):
#      response = sr1(IP(dst=self.settings.DNSServerIP)/UDP(sport=orig_pkt[UDP].sport)/\
#        DNS(rd=1,id=orig_pkt[DNS].id,qd=DNSQR(qname=orig_pkt[DNSQR].qname)),verbose=0)
#      respPkt = IP(dst=orig_pkt[IP].src)/UDP(dport=orig_pkt[UDP].sport)/DNS()
#        respPkt[DNS] = response[DNS]
#        send(respPkt,verbose=0)
#      return respPkt.summary()
#
#    def spoof(pkt, key):
#      spfResp = IP(dst=pkt[IP].src)\
#        /UDP(dport=pkt[UDP].sport, sport=53)\
#        /DNS(id=pkt[DNS].id,ancount=1,an=DNSRR(rrname=pkt[DNSQR].qname,rdata=localIP)\
#        /DNSRR(rrname=key,rdata=self.settings.Sinkhole))
#      return send(spfResp,verbost=0)
#
#    def getResponse(pkt):
#      if (DNS in pkt and pkt[DNS].opcode == 0L and pkt[DNS].ancount == 0 and pkt[IP].src != localIP):
#        key = pkt['DNS Question Record'].qname
#        if whitelist.has_key(key):
#          # Key is in whitelist
#          logging.debug('Allowed by whitelist %s req-by %s' % key, orig_pkt[IP].src)
#          return forwardDNS(pkt)
#        if blacklist.has_key(key):
#          # Key is in blacklist
#          logging.debug('Rejected by blacklist %s req-by %s' % key, orig_pkg[IP].src)
#          return spoof(pkt, key)
#        if greylist.has_key(key):
#          # Key exists in greylist
#          curtime = datetime.now()
#          entry = greyList[key]
#          if ((curtime - self.settings.GreyOut) >= entry.getFirstSeen):
#            # Is the entry in the greyout period?
#            if (curtime - self.settings.BlackOut <= entry.getLastSeen):
#              # Is the entry in the blackout period?
#              logging.debug('Allowed by greylist %s req-by %s' % key, orig_pkt[IP].src)
#              return forwardDNS(packet)
#            else:
#              logging.debug('Rejected/timeout by greylist %s req-by %s' % key, orig_pkt[IP].src)
#              entry.setFirstSeen()
#              entry.setLastSeen()
#              return spoof(pkt, key)
#          else:
#            logging.debug('Rejected/greyout by greylist %s req-by %s' % key, orig_pkt[IP].src)
#            return spoof(pkt, key)
#        else:
#          # Entry not found in any list, so add it
#          logging.debug('Rejected/notseen by greylist %s req-by %s' % key, orig_pkt[IP].src)
#          createListEntry(key)
#          return spoof(pkt, key)
#      else:
#        return False

if __name__=='__main__':
  foghornd = Main()
  foghornd.run()
