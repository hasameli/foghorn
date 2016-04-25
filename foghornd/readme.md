The foghorn daemon is intended to act as a listener on port 53 and MITM 
DNS traffic for the purpose of black-, white-, and greylisting entries.

This daemon is written in [Pony](http://www.ponylang.org/)

There are four configuration files: 

blacklist.txt - a UTF-8 encoded list of blacklisted domains, one per 
line.
whitelist.txt - a UTF-8 encoded list of whitelisted domains, one per 
line.
greylist.json - a UTF-8 encoded file for greylisted entities in JSON 
format, documented below.
foghorn.config - a configuration file specifying the behavior of 
foghornd.


