"""ACL - Access control lists for foghorn"""

from ipaddress import ip_address, ip_network


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
                rule = ip_network(unicode(acl_list))

            if acl_black:
                rule = rule.address_exclude(ip_network(unicode(acl_black)))
                self.acls["allow_%s" % acl] = rule
            else:
                self.acls["allow_%s" % acl] = [rule]

    def check_acl(self, acl, host):
        host = ip_address(unicode(host))
        rule = self.acls[acl]
        if not rule:
            return True

        for r in rule:
            if host in r:
                return True

        return False
