The foghorn daemon is intended to act as a listener on port 53 and MITM 
DNS traffic for the purpose of black-, white-, and greylisting entries.

This daemon is written in Python and depends on scapy

There are four configuration files: 

/usr/greydns/blacklist - a UTF-8 encoded list of blacklisted domains, one per 
line.
/usr/greydns/whitelist - a UTF-8 encoded list of whitelisted domains, one per 
line.
/usr/greydns/greylist - a UTF-8 encoded file for greylisted entities, one per 
line, listed as a comma-separated list of DNS, firstseen, and lastseen 
times.
/usr/greydns/foghorn.config - a configuration file specifying the behavior of 
foghornd.


