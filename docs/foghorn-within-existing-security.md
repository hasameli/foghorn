## Using foghorn Within Your Existing Security Plan

Foghorn is intended to act in conjunction with, rather than as a replacement for, your existing security infrastructure. 

### Infrastructure Auditing

The prerequisites to set up foghorn provide the network administrator with several inherent benefits for controlling the network. If, during this setup process, certain systems begin malfunctioning, it's a clue that they are either set up incorrectly or being used in an out of scope fashion.

### Training

Use foghorn to backstop your existing counter-phishing training and operations. The sinkhole directive in the configuration allows you to direct suspicious requests to a specific address - like a place to file a ticket with your existing IT department to report suspected phishing emails. Providing a means for the effective reporting of phishing emails allows you to reward users who act correctly; having foghorn available to backstop users who are fooled by such emails allows for understanding who may require more training and also allows for an opportunity to educate them.

### Reconnaissance

Use foghorn to watch for indicators of phishing or malware. Used in conjunction with your existing log aggregation and analysis tools, foghorn can generate intelligence that will highlight potential problems.

For example, if a given domain appears as greylisted from a variety of assets, this may indicate that a phishing campaign has sent the same or similar links to several persons in your organization.

Likewise, if a single asset is shown as attempting to access a large number of greylisted domains, this could be an indication of a system compromised by malware, and attempting to connect to a C&C server designated by a domain generation algorithm.

Further, seeing any greylisted entries at all from assets that are not normally used for interactive user activities - fileservers, for instance - can indicate that they are being used out of their intended scope or that some person or malware is attempting to exfiltrate information from them.

### DFIR

Look at foghorn's logs retrospectively to help determine the means by which an incident occurred. Use this information to determine IOCs to detect other affected systems, and to fingerprint the infrastructure than an attacker is using to carry out a campaign.

Set up alerts for the kinds of events called out under 'reconnaissance' in your SIEM platform, so that it can notify you when an incident is in progress.

Make use of the delay that foghorn imposes on attackers to take countermeasures against any attacks that may be occurring. 

### Threat Intelligence

Dovetailing into the last point, foghorn allows for the collection of threat intelligence information. If you're an MSSP, you can use the information collected from any foghorn installations you have access to in order to determine where attacks are coming from - and you can update blacklists accordingly. 
