# FAQ

* Why do I need to do all that complicated network stuff? Can't I just set my workstations to point to foghorn and be happy?

You could, sure - but that means anyone who does manage to compromise your workstations (or users who think this is inconvenient) can set the DNS resolver to 8.8.8.8 and circumvent the controls. It's much better to make sure that only the correct path is open.

* Won't this block new domains from propagating into the network?

Yes, for 24 hours. After that point, if they're visited consistently, then the greylist will keep them current.

* Why not just use OpenDNS or summat like? It's simpler than this setup, and they do domain reputation.

Domain reputation is a great tool, but it's not very useful if someone compromises a good-reputation domain and uses it to phish you. Greylisting is more likely to catch that situation, especially if it's targeted at your company specifically.

* I'm an Enterprise-class user and...

Sorry, but this is really more focused at small and medium size businesses who don't have the options you do. Though if you want to try deploying this in certain departments, you too might find some benefit!

* Why are 24 hours and 7 days the default times?

As of 2014, the average persistence of phishing domains dropped below 24 hours; phishing is the original problem this was intended to solve, so it was scaled accordingly.

Seven days for the blackout limit was based on the assumption most business users would visit sites they needed to get to at least weekly.

* Why do you need a blackout at all?

Two reasons - first, there have been instances where a company has gone out of business and some other party has purchased that company's domain names and used them to exploit pre-existing reputations. Second, we don't want to maintain greylisted domains forever - that would become unmanageable. If you're not visiting the site regularly, there's no reason to keep it in the list. 

* What if I want to go surfing reddit? This greylisting thing gets in the way of all the cool stuff!

Bribe your admin to whitelist imgur and other domains, or browse reddit on a non-work machine. 

Most business users only visit a relatively small number of domains to do their work; once foghorn is baselined correctly, it isn't likely to impact those significantly.

* Why didn't you use a bayesian algorithm to recognize obvious phishing domains?

Because that doesn't account for the cases where the attacker has taken over someone's inactive website and used it for a phishing endpoint.

* Won't this mess up fast-flux DNS like Amazon and other people use?

No - we're greylisting by the domain name, not the IP that the domain 
resolves to. Fast-flux DNS, provided that the domain name associated 
with it is in the whitelist or in the allowed window of the greylist, 
will work as per usual.

* I want some help setting this up. Do you have any consultants or something?

Email < foghorn at hasameli.com > and we'll make arrangements.

* Why don't you have $FEATURE?

We haven't written it yet - this is a very rough POC as yet. If you want 
to contribute, we'd be happy to take suggestions or pull requests!
