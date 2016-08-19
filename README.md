# README

This README is for the foghorn project.

## What is this repository for?

* foghorn is a configurable DNS proxy to allow for black-, white-, and greylisting of DNS resources.
* Version 0.1

## How do I get set up?

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
[in FoghornSettings.py](https://github.com/hasameli/foghorn/blob/master/foghornd/FoghornSettings.py)


### Dependencies
foghorn is dependent on python and twisted

### Installation
Foghorn can be installed via PIP directly from this GitHub repository. To install first, then edit the configuration settings later, run:

```
python -m pip install git+git://github.com/hasameli/foghorn.git --user
```

Otherwise, you can clone the repository and install it manually:
```
git clone https://github.com/hasameli/foghorn.git
cd foghorn
python setup.py install --user
```


### Deployment instructions
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

## Contribution guidelines

* We would like contributions to be in line with the PEP8 standards.
* We would like if you run pylint before sending contributions. It makes things a little tidier.
* If adding a new feature, please check if it's listed in the issues and reference it in your PR

## License

[MIT](https://github.com/hasameli/foghorn/blob/master/docs/LICENSING)

## Who do I talk to?

* foghorn@hasameli.com
* On Twitter, talk to @munin
