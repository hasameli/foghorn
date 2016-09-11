# README

This README is for the foghorn project.

**Table of Contents**

- [Description](#description)
- [Setup](#setup)
  - [Configuration](#configuration)
  - [Dependencies](#dependencies)
  - [Installation](#installation)
  - [Deployment Instructions](#deployment-instructions)
- [FAQ](#faq)
- [Contributor Guidelines](#contributor-guidelines)
- [License](#license)
- [Contact](#contact)

## Description

* foghorn is a configurable DNS proxy to allow for black-, white-, and greylisting of DNS resources.
* Version 0.1

## Setup

### Configuration
Configuration details can be found in [docs/foghorn-whitepaper.md](https://github.com/hasameli/foghorn/blob/master/docs/foghorn-whitepaper.md) -
you will need to configure your networks to be compatible with certain
prerequisites before foghorn will be effective

There are four configuration files:
  * `greydns/blacklist` - a UTF-8 encoded list of blacklisted domains, one per line.
  * `greydns/whitelist` - a UTF-8 encoded list of whitelisted domains, one per line.
  * `greydns/greylist` - a UTF-8 encoded file for greylisted entities, one per line,
listed as a comma-separated list of DNS, firstseen, and lastseen times.
  * `settings.json` - a json dictionary of configuration variables, lightly documented
[in settings.py](https://github.com/hasameli/foghorn/blob/master/foghornd/settings.py)


### Dependencies
foghorn is dependent on python, twisted, python-dateutil, and requests

Your OS may have specific packages required to install some of these - for example, CentOS 7 demands python-devel

### Installation
Foghorn requires that `twisted`, `python-dateutil`, and `requests` be installed prior to use. Run:

```
pip install twisted python-dateutil requests
```

Foghorn can then be installed via PIP directly from this GitHub repository. To install first, then edit the configuration settings later, run:

```
python -m pip install git+git://github.com/hasameli/foghorn.git --user
```

Otherwise, you can clone the repository and install it manually:
```
git clone https://github.com/hasameli/foghorn.git
cd foghorn
python setup.py install --user

```
After you have configured the settings in `foghornd/settings.json` appropriately for your network (see the docs folder for an explanation of the settings) you can run foghorn with
```
make run
```
and test it out. 


### Deployment Instructions
See the diagram in the
[bsideslv-2016 presentation](https://github.com/hasameli/foghorn/raw/master/docs/bsides-preso.pdf)
in the docs folder for an overview; see also the
[foghorn-whitepaper.md](https://github.com/hasameli/foghorn/blob/master/docs/foghorn-whitepaper.md)
for rationale, etc.

foghorn MUST be positioned within a network with egress filtering
enabled for DNS - only the local resolver can be allowed to make
outbound requests for DNS.

Also, squid or some similar proxy should be in place to filter naked IP
requests, in order to mitigate the possibility of certain workarounds
that would otherwise be available to attackers.

After baselining, the workstations that you desire to protect should be
configured to use the foghorn server as their DNS resolver, and any ACLs
adjusted accordingly.

## FAQ

[Available here](https://github.com/hasameli/foghorn/blob/master/docs/FAQ.md)

## Gotchas

Installing this within Virtualbox or KVM may require [forwarding ports](http://wiki.libvirt.org/page/Networking#Forwarding_Incoming_Connections) in order to ensure access to the VM.

Some OSs may require development tools be installed before twisted will install correctly.

If you desire foghorn to run on the standard DNS port 53, you MUST run with root privileges. Use this with caution! The default port is set to 10053 specifically to avoid this.

If you change the settings in `settings.json` you will need to rerun `setup.py` as per the instructions above before the new settings will be enabled.

## Contributor Guidelines

* We would like contributions to be in line with the PEP8 standards.
* We would like if you run pylint before sending contributions. It makes things a little tidier.
* If adding a new feature, please check if it's listed in the issues and reference it in your PR

## License

[MIT](https://github.com/hasameli/foghorn/blob/master/docs/LICENSING)

## Contact

* foghorn@hasameli.com
* On Twitter, talk to @munin
