from datetime import timedelta

class FoghornSettings(object):
  #"""TODO: change from hardcoded values to config file"""
  logfile = "foghornd.log"
  DNSServerIP = "192.168.1.1" #"""Sever providing DNS resolution"""
  GreyIP = "192.168.5.1" #"""Local IP to listen on"""
  DNSPort = 10053 #"""Local port number to listen on"""
  Sinkhole = "127.0.0.1" #"""Sinkhole IP for black/greylisting"""

  GreyOut = timedelta(hours=24) #"""Time from firstseen to first allowed"""
  BlackOut = timedelta(hours=180) #"""Time from lastseen after which it is no longer allowed"""
  RefreshPeriod = timedelta(minutes=5)

  WhitelistFile = "greydns/whitelist"
  BlacklistFile = "greydns/blacklist"
  GreylistFile = "greydns/greylist"

