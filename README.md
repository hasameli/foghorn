# README #

This README is for the foghorn project.

### What is this repository for? ###

* foghorn is a configurable DNS proxy to allow for black-, white-, and greylisting of DNS resources.
* Version 0.1

### How do I get set up? ###

* Summary of set up
* Configuration
* Dependencies
foghorn is dependent on python and twisted

* Deployment instructions
See the diagram in the bsideslv-2016 presentation in the docs folder for 
an overview.

foghorn MUST be positioned within a network with egress filtering 
enabled for DNS - only the local resolver can be allowed to make 
outbound requests for DNS.

Also, squid or some similar proxy should be in place to filter naked IP 
requests, in order to mitigate the possibility of certain workarounds 
that would otherwise be available to attackers.

After baselining, the workstations that you desire to protect should be 
configured to use the foghorn server as their DNS resolver, and any ACLs 
adjusted accordingly. 


### Contribution guidelines ###

* Writing tests
* Code review
* Other guidelines

### Who do I talk to? ###

* foghorn@hasameli.com
* On Twitter, talk to @munin
