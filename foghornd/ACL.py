"""ACL - Access control lists for foghorn"""

from ipaddress import ip_address, ip_network


class ACL(object):
    acls = {}
    default = False

    def __init__(self, settings={}):
        """Acceptance: (allow_TYPE or 0.0.0.0/0) - deny_TYPE"""
        acl_settings = settings.acl
        # By default deny unless we have a whitelist
        self.default = acl_settings.get("default", False)
        for acl in ["a", "aaaa", "mx", "srv"]:
            acl_name = "allow_%s" % acl
            self.acls[acl_name] = {}

            acl_list = acl_settings.get("allow_%s" % acl, None)
            acl_black = acl_settings.get("deny_%s" % acl, None)

            if acl_list:
                rule = ip_network(unicode(acl_list))
                self.acls[acl_name]["allow"] = self.compile_rule(rule)

            if acl_black:
                rule = ip_network(unicode(acl_black))
                self.acls[acl_name]["deny"] = self.compile_rule(rule)

    def compile_rule(self, rule):
        compiled = {}
        for host in rule:
            compiled[host] = 1
        return compiled

    def check_acl(self, acl, host):
        host = ip_address(unicode(host))
        rule = self.acls[acl]

        try:
            rule["deny"][host]
            return False
        except KeyError:
            pass

        try:
            rule["allow"][host]
            return True
        except KeyError:
            pass

        try:
            rule["allow"]
            return False
        except KeyError:
            pass

        return self.default
