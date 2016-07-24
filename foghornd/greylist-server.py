#!/usr/bin/env python

from GreylistEntry import GreylistEntry
from scapy.all import *
import sys, os, logging, time
from datetime import datetime,timedelta

#"""TODO: change from hardcoded values to config file"""
DNSServerIP = "192.168.1.1" #"""Sever providing DNS resolution"""
GreyIP = "192.168.5.1" #"""Local IP to listen on"""
DNSPort = 53 #"""Local port number to listen on"""
Sinkhole = "127.0.0.1" #"""Sinkhole IP for black/greylisting"""

GreyOut = timedelta(hours=24) #"""Time from firstseen to first allowed"""
BlackOut = timedelta(hours=180) #"""Time from lastseen after which it is no longer allowed"""

WhitelistFile = "/etc/greydns/whitelist"
BlacklistFile = "/etc/greydns/blacklist"
GreylistFile = "/etc/greydns/greylist"

blacklist = set()
whitelist = set()
greylist = {}

logging.basicConfig(format = '%(asctime)s %(levelname)8s %(message)s', filename = '/var/log/greylist.log', filemode='a')

#""" Stolen cavalierly from thepacketgeek's scapy/dns script """
filter = "udp port 53 and ip dst " + GreyIP + " and not ip src " + GreyIP

def loadGreyList(file):
    f = open(file, mode='r', bufsize=-1)
    for line in f:
        createListEntry(line.split(','))
    f.close()
    return True
def loadList(file, list):
    f = open(file, mode='r', bufsize=-1)
    for line in f:
        listd(line)
    f.close()
    return True    
def writeGreyList(file, greylist):
    f = open(file, mode='w', bufsize=-1)
    items = greylist.values()
    for line in items:
        f.write(",".join(line.getDnsField, line.getFirstSeen, line.getLastSeen) + "\n")
    f.close()
    return True
def DNS_Responder(GreyIP):
    def forwardDNS(orig_pkt):
        response = sr1(IP(dst=DNSServerIP)/UDP(sport=orig_pkt[UDP].sport)/\
            DNS(rd=1,id=orig_pkt[DNS].id,qd=DNSQR(qname=orig_pkt[DNSQR].qname)),verbose=0)
        respPkt = IP(dst=orig_pkt[IP].src)/UDP(dport=orig_pkt[UDP].sport)/DNS()
        respPkt[DNS] = response[DNS]
        send(respPkt,verbose=0)
        return respPkt.summary()
    def spoof(pkt, key):
        spfResp = IP(dst=pkt[IP].src)\
        /UDP(dport=pkt[UDP].sport, sport=53)\
        /DNS(id=pkt[DNS].id,ancount=1,an=DNSRR(rrname=pkt[DNSQR].qname,rdata=localIP)\
        /DNSRR(rrname=key,rdata=Sinkhole))
        return send(spfResp,verbost=0)
    def getResponse(pkt):
        if (DNS in pkt and pkt[DNS].opcode == 0L and pkt[DNS].ancount == 0 and pkt[IP].src != GreyIP):
            key = pkt['DNS Question Record'].qname
            if whitelist.has_key(key):
#                """Key is in whitelist"""
                logging.debug('Allowed by whitelist %s req-by %s' % key, orig_pkt[IP].src)
                return forwardDNS(pkt)
            if blacklist.has_key(key):
#                """Key is in blacklist"""
                logging.debug('Rejected by blacklist %s req-by %s' % key, orig_pkg[IP].src)
                return spoof(pkt, key)
            if greylist.has_key(key):
#                """Key exists in greylist"""
                curtime = datetime.now()
                entry = greyList[key]
                if ((curtime - GreyOut) >= entry.getFirstSeen):
#                """Is the entry in the greyout period?"""
                    if (curtime - BlackOut <= entry.getLastSeen):
#                        """Is the entry in the blackout period?"""
                        logging.debug('Allowed by greylist %s req-by %s' % key, orig_pkt[IP].src)
                        return forwardDNS(packet)
                    else:
                        logging.debug('Rejected/timeout by greylist %s req-by %s' % key, orig_pkt[IP].src)
                        entry.setFirstSeen()
                        entry.setLastSeen()
                        return spoof(pkt, key)
                else:
                    logging.debug('Rejected/greyout by greylist %s req-by %s' % key, orig_pkt[IP].src)
                    return spoof(pkt, key)
            else:
#                """Entry not found in any list, so add it"""    
                logging.debug('Rejected/notseen by greylist %s req-by %s' % key, orig_pkt[IP].src)
                createListEntry(key)                
                return spoof(pkt, key)
        else:
            return False

def main():
    loadList(WhitelistFile, whitelist)
    loadList(BlacklistFile, blacklist)
    loadGreyList(GreylistFile)
    refresh = datetime.now()
    while 1:
        sniff(filter=filter,prn=DNS_Responder(GreyIP))
        if (refresh < (datetime.now() - timedelta(minutes=5))):
            refresh = datetime.now()
            writeGreyList(GreylistFile, greylist)
