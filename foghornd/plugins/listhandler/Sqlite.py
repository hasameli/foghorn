"""An sqlite backend for foghorn"""

import sqlite3
import logging
import dateutil.parser

from foghornd.plugins.listhandler import ListHandlerBase
from foghornd.greylistentry import GreylistEntry


class Sqlite(ListHandlerBase):
    """An sqlite3 backend for foghorn"""

    db_file = 'foghorn.sqlite3'
    select_query = 'SELECT host, first_seen, last_seen FROM %s WHERE host=?'
    insert_query = 'INSERT OR IGNORE INTO %s (host, tag, first_seen, last_seen) VALUES (?,?, datetime("now"), datetime("now"))'
    delete_query = 'DELETE FROM %s where host=?'
    delete_tag_query = 'DELETE FROM %s where tag=?'
    queries = {}

    def __init__(self, settings):
        super(Sqlite, self).__init__(settings)
        self.settings = settings
        self.logging = logging.getLogger('foghornd')
        self.sql_conn = sqlite3.connect(self.db_file)
        self.cursor = self.sql_conn.cursor()
        self.initdb()

    def load_lists(self, signal_recvd=None, frame=None):
        """
        This function will be called to reload the lists.
        In our case this  does nothing
        """
        # pylint: disable=W0613

    def save_state(self):
        """noop - we have no state to save"""

    def check_whitelist(self, query):
        """Check the whitelist for this query"""
        cursor = self.sql_conn.cursor()
        host = query.name.name
        cursor.execute(self.queries["whitelist"]["select"], (host,))
        row = cursor.fetchone()
        if row:
            return True
        return False

    def check_blacklist(self, query):
        """Check the blacklist for this query"""
        cursor = self.sql_conn.cursor()
        host = query.name.name
        cursor.execute(self.queries["blacklist"]["select"], (host,))
        row = cursor.fetchone()
        if row:
            return True
        return False

    def check_greylist(self, query, baseline, peer_address):
        """Check the greylist for this query"""
        cursor = self.sql_conn.cursor()
        host = query.name.name
        cursor.execute(self.queries["greylist"]["select"], (host,))
        elements = cursor.fetchone()
        if elements:
            entry = GreylistEntry(
                elements[0],
                dateutil.parser.parse(elements[1]),
                dateutil.parser.parse(elements[2])
            )
            return entry

    def update_greylist(self, entry):
        insert_query = 'INSERT OR IGNORE INTO greylist values(?, ?, ?, ?)'
        update_query = 'UPDATE GREYLIST SET first_seen=?, last_seen=? WHERE host=?'
        cursor = self.sql_conn.cursor()
        # sqlite3 does not support "insert or update"
        cursor.execute(insert_query, (entry.dns_field, entry.first_seen, entry.last_seen, "foghorn"))
        cursor.execute(update_query, (entry.first_seen, entry.last_seen, entry.dns_field))
        self.sql_conn.commit()

    def add_to_list(self, target, host, tag=None):
        query = self.queries[target]["insert"]
        cursor = self.sql_conn.cursor()
        cursor.execute(query, (host, tag))
        self.sql_conn.commit()

    def delete_from_list(self, target, host):
        query = self.queries[target]["delete"]
        cursor = self.sql_conn.cursor()
        cursor.execute(query, (host,))
        self.sql_conn.commit()

    def delete_tag_from_list(self, target, tag):
        query = self.queries[target]["delete_tag"]
        cursor = self.sql_conn.cursor()
        cursor.execute(query, (tag,))
        self.sql_conn.commit()

    def add_to_whitelist(self, host, tag=None):
        self.add_to_list("whitelist", host, tag)

    def add_to_blacklist(self, host, tag=None):
        self.add_to_list("blacklist", host, tag)

    def add_to_greylist(self, host, tag=None):
        self.add_to_list("greylist", host, tag)

    def delete_from_whitelist(self, host):
        self.delete_from_list("whitelist", host)

    def delete_from_blacklist(self, host):
        self.delete_from_list("blacklist", host)

    def delete_from_greylist(self, host):
        self.delete_from_list("greylist", host)

    def delete_tag_from_whitelist(self, tag):
        self.delete_tag_from_list("whitelist", tag)

    def delete_tag_from_blacklist(self, tag):
        self.delete_tag_from_list("blacklist", tag)

    def delete_tag_from_greylist(self, tag):
        self.delete_tag_from_list("greylist", tag)

    def query_greylist(self):
        query = "SELECT HOST, FIRST_SEEN, LAST_SEEN, TAG FROM greylist"
        cursor = self.sql_conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()

    def query_whitelist(self):
        query = "SELECT HOST, FIRST_SEEN, LAST_SEEN, TAG FROM whitelist"
        cursor = self.sql_conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()

    def query_blacklist(self):
        query = "SELECT HOST, FIRST_SEEN, LAST_SEEN, TAG FROM blacklist"
        cursor = self.sql_conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()

    def initdb(self):
        """Create the databases and configure the queries"""
        definition = """(host TEXT NOT NULL ,
                        first_seen DATETIME NOT NULL,
                        last_seen DATETIME NOT NULL,
                        tag TEXT,
                        PRIMARY KEY (host))"""

        for table in ['whitelist', 'blacklist', 'greylist']:
            query = 'CREATE TABLE IF NOT EXISTS %s %s' % (table, definition)
            self.cursor.execute(query)
            self.sql_conn.commit()

        for table in ['whitelist', 'blacklist', 'greylist']:
            self.queries[table] = {}
            self.queries[table]["select"] = self.select_query % (table)

        for table in ['whitelist', 'blacklist', 'greylist']:
            self.queries[table]["insert"] = self.insert_query % (table)

        for table in ['whitelist', 'blacklist', 'greylist']:
            self.queries[table]["delete"] = self.delete_query % (table)

        for table in ['whitelist', 'blacklist', 'greylist']:
            self.queries[table]["delete_tag"] = self.delete_tag_query % (table)
