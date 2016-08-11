# DNS Greylisting with foghorn

DNS is an essential utility for the functioning of internet-connected resources, and one which a careful administrator can control. The foghorn utility provides a means to add greylisting capability to one's local DNS infrastructure with minimal impact to legitimate business traffic, while at the same time insulating users of the network from phishing, malware C2, and other similar attacks.

## What is greylisting?

Greylisting is the practice of introducing purposeful delays into certain selected networked protocols in order to obstruct or mitigate attacks.

Greylisting originated in SMTP as a means of obstructing spam. [RFC 6647](https://tools.ietf.org/html/rfc6647) describes how this works, and gives guidelines for when it is applicable; in summary, by summarily rejecting the first attempt by an unknown sender to send email, many purpose-built spam senders will fail to complete their transactions and the recipient will avoid receiving spam from those senders.

In the case of foghorn, we have taken the same basic concept and applied it to DNS. When a workstation attempts to fetch a DNS record not previously seen on the network, the greylister will initially resolve that domain to some locally-controlled asset rather than allowing the request to complete; after some timeout period, the request will then resolve as normal.

## Why do I want to greylist DNS?

Greylisting DNS provides a mitigative strategy for many kinds of attacks.

Phishing, for instance, entices the user into clicking on some link which will bring them to a landing page purporting to belong to some resource for which access credentials are required; generally, the page is structured to appear to the user as though it is legitimately part of the site it purports to represent. Care is taken to clone the livery of the legitimate site as closely as possible in order to take advantage of most users' tendency to recognize the site's appearance rather than pay close attention to the URL. 

In the case where greylisting capability is being used, the legitimate site is likely to be within the greylister's passthrough period, while a site purporting to belong to that org will be novel to the requesting network and thus resolve to a locally controlled asset

Most phishing domains persist (as of 2014) for 24 hours or less; delaying resolution of novel domains for that period of time means that the user who has been phished is far less likely to receive access to the malicious resource.

This neutralizes the attack, and providing the network administrator with both notification that such an attack is taking place and an opportunity to engage with the user about the attempt to retrieve their credentials. If the administrator sees significant numbers of logs that a given domain has been denied by greylist for many assets on their network, that is likely to indicate a (spear)phishing attack.

Likewise, many modern botnets and similar malicious software implants use DGA - domain generation algorithms - to build a set of pseudo-random domains for the malware to use to contact the 'bot herder' for instructions or to upload information. These domains are constantly under attack - both by being blacklisted in widely-distributed lists, and in being shut down by law enforcement and other agencies with an interest in attacking criminal infrastructure. Given this hostile environment, the algorithmically-generated domains persist for only a short time - minutes to hours.

Greylisting, by denying proper resolution to these bots, will not only neuter their ability to access C2 resources but also make their existence on the network incredibly obvious to the administrators; logging significant numbers of different denied domains from a single local asset may indicate an issue of this type.

Other types of malicious activity may be affected by this as well - things like data exfiltration via DNS requests, mail clients being scripted to automatically download malware, ransomware C2, etc.

## Theory of Operations 

The resolver determines whether the requested domain exists on the whitelist, then the blacklist, then the greylist. If it does not exist on any of these lists, then the domain is added to the greylist and the initial greyout time period begins - by default, 24 hours.

If the domain has not been requested within the last (by default) 7 days, then the greyout time begins again as per an initial fetch.

(List trimming will be implemented in the future to manage list size and purge blacked-out domains at intervals)

If the domain is on the whitelist, or is beyond the greyout period and the blackout has not yet elapsed, then the domain will be resolved properly.

If the domain is on the blacklist, is not yet out of the greyout period, or is beyond the blackout period since last reference, then it will be resolved to a locally-controlled asset. 

The default tuning of 24 hours for the greyout period is specifically in reference to the current average persistence of phishing collection sites being slightly under 24 hours.

The use of a blackout to clip out domains that are not recently referenced is to account for situations in which a benign domain is, after a period of inactivity, acquired by a malicious actor and used to compromise former users of that domain.

## Why Shouldn't I Just Use....

### Training?

Training is expensive and largely ineffective. The best successes derive from repeated, in-depth training, which raises the expense significantly - but even in those cases, a significant number of users still fail to properly respond to phishing incidents in tests.

This is not to say that training is not needed, but using greylisting in adjunct to training will be significantly more effective than training alone.

### Blacklists?

Blacklists are reactive, expensive, and generalized. Blacklists can only be populated when the hostile domains are already known - thus, they cannot be effective against novel domains that have not exhibited hostile behavior in the past. They are often expensive - ranging from hundreds to thousands of dollars per year for the professional ones - which is often out of reach for small and medium businesses. They are generalized - there's not usually any provision to determine whether the threats enumerated on the blacklists are pertinent to your specific situation, and they won't be likely to know which threat actors might target your business specifically. 

Blacklists are useful, but they are often not agile enough to compete with today's threats, many of which specifically try to avoid blacklisting.

### Whitelists?

Whitelists are restrictive and difficult to manage - they require a lot of hands-on work to keep them up to date, which results in signficant support expense. 

### Domain Reputation services?

Domain reputation services are often expensive, and do not address situations where an existing benign domain has been coopted into a malicious network. 


## Prerequisites for Use

In order to use foghorn, you must have certain prerequisites configured into your network.

First and foremost, you must filter DNS - port 53 UDP and TCP - outbound from every system except for your designated local resolver.

For Windows networks, that will usually be your ActiveDirectory server; other networks will generally have that as part of their network hardware, an LDAP server, or some other system designated for use.

Second, in order to mitigate naked IP requests bypassing DNS resolution, your network will require a local proxy set to filter such requests.

Third, once the baselining period is over, the workstations that require protection must be configured to acquire their DNS from the greylisting server and cannot have access to the designated DNS resolver - only the greylisting server should mediate connections between the workstations and the DNS resolver.

Fourth, the greylister's whitelist should be populated with the local domain (to facilitate proper lookups) and any known-good domains for which immediate resolution is required; likewise, the blacklist should be populated with any known-bad domains that you wish to block. 

Fifth, some baselining of your existing DNS traffic will be needed in order to populate the greylist. At this time, there is no provision within the application to do so (though this functionality is being planned); accordingly, copying existing DNS traffic from your network to the inbound network connection of the greylister for at least 24 hours will be required. This can be accomplished via a SPAN or mirror port, or by a temporary iptables or similar rule in the case of a UNIX-type resolver tee-ing the appropriate traffic to the greylister.

## Limitations

At this point in time, foghorn only intercepts "A" records. Other types of DNS records are not intercepted at this time. This is likely to change fairly quickly during development.

If some set of users routinely engages in research activities across a broad range of domains, they may require a higher than usual requirement for expediting greyout expiry; these users may need to bypass the normal controls.

## Installation

At this point in time, the foghorn POC runs as a python script and may require elevated privileges. Clone the repository to your local system and run it; for long-duration use you may wish to build a startup script or use something like supervisord in order to keep it running correctly.

(This should change in the near future as this migrates from a POC to a proper utility)

By default, foghorn is configured to divert entries within the 'greyout' period (the initial period where lookups are rejected) to localhost. If you have a local 'honeytrap' server that you wish to use in order to engage with your users - perhaps to file tickets or something of that sort - then you can change this entry to point to that server's IP; you will need to configure the HTTP responder on this system to answer on any domain request.

Further, you will want to ensure your local HTTP/s proxy is configured to reject requests for naked IPs. This is to avoid the obvious method of circumventing DNS greylisting by not using DNS.

Network topology should be structured as mentioned in the "Prerequisites" section above.

You may wish to take advantage of the logging provisions built into the foghorn system to gain awareness of how your users are being attacked. Use rsyslog or a similar utility to export the logs from foghorn's logfiles to your existing SIEM or other log-analysis infrastructure, or use fail2ban or a similar utility to script some action to notify you upon certain thresholds being reached.

The logs describe several conditions, in the form of:

` "[Allowed|Rejected[/condition]] by [white|black|grey]list [domain] ref-by [requestor]" `

Allowed by whitelist: This domain has been resolved properly because it is on the whitelist. 

Rejected by blacklist: This domain has been resolved to a locally controlled asset because it is on the blacklist

Allowed by greylist: This domain has been resolved properly because it is within the 'permitted' greylisting window

Rejected/timeout by greylist: This domain has been resolved to a locally controlled asset because the time to blackout has been exceeded.

Rejected/greyout by greylist: This domain has been resolved to a locally controlled asset because the greyout time has not yet elapsed

Rejected/notseen by greylist: As per Rejected/greyout, but indicating the first instance of seeing this domain.

## Configuration

The `settings.json` file holds the configuration information for 
foghorn. 

The settings are as follows:

`blackout` - This is the time after which greylisted entries are no 
longer valid, expressed in hours - 180 hours = 7 days.

`dns_port` - This is the port on which foghorn listens. Change this to 
53 when you decide to put it inline.

`dns_server_ip` - This is the resolver that you are using to manage DNS 
for your network. If you're running AD, then this will generally point 
to your AD server. Make sure that this, and only this, server has the 
capability to request DNS outside the network. 

NOTE: At this time, foghorn only supports single DNS resolvers.

`file` - This is the file that foghorn logs to. Make sure that the 
foghorn process has the ability to write to that location.

`grey_ip` - This is the IP that foghorn listens on.

`greyout` - This value indicates the initial greyout period (the period 
before a previously unseen domain becomes valid). It's expressed in 
hours, and defaults to 24 hours.

`refresh` - This value governs how often the greylist is written to 
disk. It is expressed in minutes; the default is every 5 minutes.

`sinkhole` - This value indicates what address a blacked-out or 
greyed-out domain will be resolved to. It defaults to 127.0.0.1 
(localhost); if you want to resolve it to a server that will provide 
useful information to the user, replace this value with the IP of that 
server and ensure that the webserver instance is configured to accept 
any domain requested.
