"""An sqllite backend for foghorn"""

import sqlite3
import logging
import dateutil.parser

from foghornd.plugins.listhandler import ListHandlerBase
from foghornd.greylistentry import GreylistEntry


class Sqllite(ListHandlerBase):
    """An sqllite3 backend for foghorn"""

    db_file = 'foghorn.sqlite3'
    select_query = 'SELECT host, first_seen, last_seen FROM %s WHERE host=?'
    queries = {}

    def __init__(self, settings):
        super(Sqllite, self).__init__(settings)
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
        insert_query = 'INSERT OR IGNORE INTO greylist values(?, ?, ?)'
        update_query = 'UPDATE GREYLIST SET first_seen=?, last_seen=? WHERE host=?'
        cursor = self.sql_conn.cursor()
        # sqllite3 does not support "insert or update"
        cursor.execute(insert_query, (entry.dns_field, entry.first_seen, entry.last_seen))
        cursor.execute(update_query, (entry.first_seen, entry.last_seen, entry.dns_field))
        self.sql_conn.commit()

    def initdb(self):
        """Create the databases and configure the queries"""
        definition = """(host TEXT NOT NULL ,
                        first_seen DATETIME NOT NULL,
                        last_seen DATETIME NOT NULL,
                        PRIMARY KEY (host))"""

        for table in ['whitelist', 'blacklist', 'greylist']:
            query = 'CREATE TABLE IF NOT EXISTS %s %s' % (table, definition)
            self.cursor.execute(query)

        for table in ['whitelist', 'blacklist', 'greylist']:
            self.queries[table] = {}

        for table in ['whitelist', 'blacklist', 'greylist']:
            self.queries[table]["select"] = self.select_query % (table)

        self.sql_conn.commit()
