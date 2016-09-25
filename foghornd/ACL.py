"""ACL - Access control lists for foghorn"""

from ipaddress import ip_address, ip_network
import collections


class ACL(object):
    acls = {}

    def __init__(self, settings={}):
        """Acceptance: (allow_TYPE or 0.0.0.0/0) - deny_TYPE"""
        acl_settings = settings.acl
        for acl in ["a"]:
            # Default Accept
            rule = ip_network(u"0.0.0.0/0")

            acl_list = acl_settings.get("allow_%s" % acl, None)
            acl_black = acl_settings.get("deny_%s" % acl, None)

            if acl_list:
                try:  # Network
                    rule = ip_network(unicode(acl_list))
                except ValueError:  # Host
                    rule = ip_address(unicode(acl_list))

            if acl_black:
                try:  # Network
                    rule = rule.address_exclude(ip_network(unicode(acl_black)))
                except ValueError:  # Host
                    rule = rule.address_exclude(ip_address(unicode(acl_black)))

            if isinstance(rule, collections.Iterable):
                self.acls["allow_%s" % acl] = [rule]
            else:
                self.acls["allow_%s" % acl] = rule

    def check_acl(self, acl, host):
        host = ip_address(unicode(host))
        if not self.acls[acl]:
            return True

        for acl_list in self.acls[acl]:
            print acl_list
            if host in acl_list:
                return True
        return False
