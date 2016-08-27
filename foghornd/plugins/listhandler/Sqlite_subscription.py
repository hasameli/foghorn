"""An sqllite backend for foghorn"""

import sys
import requests
import sqlite3
from foghornd.plugins.listhandler.Sqlite import Sqlite


class Sqlite_subscription(Sqlite):
    """An sqllite3 backend for foghorn"""

    db_file = 'foghorn_subscription.sqlite3'
    select_query = 'SELECT host, first_seen, last_seen FROM %s WHERE host=?'
    queries = {}

    def load_lists(self, signal_recvd=None, frame=None):
        """
        This function will be called to reload the lists.
        In our case this  does nothing
        """
        # pylint: disable=W0613
        for url in self.settings.loader_settings["subscriptions"]:
            response = requests.get(url)

            try:
                items = response.json()
                cursor = self.sql_conn.cursor()
                for list_type in ["whitelist", "blacklist"]:
                    query = "DELETE FROM %s WHERE subscription=?" % list_type
                    cursor.execute(query, (url,))

                    query = "INSERT OR IGNORE INTO %s (host) VALUES (?)" % list_type
                    for item in items[list_type]:
                        cursor.execute(query, (item,))

                    self.sql_conn.commit()
            except sqlite3.Error as e:
                print "An error occurred:", e.args[0]
                exit(1)
            except:
                print "Unable to load subscription: ", response
                print sys.exc_info()[0]
                print response.content

    def initdb(self):
        """Create the databases and configure the queries"""
        definition = """(host TEXT NOT NULL,
                        first_seen DATETIME,
                        last_seen DATETIME,
                        subscription TEXT,
                        PRIMARY KEY (host,subscription))"""

        for table in ['whitelist', 'blacklist', 'greylist']:
            query = 'CREATE TABLE IF NOT EXISTS %s %s' % (table, definition)
            self.cursor.execute(query)
            query = 'CREATE INDEX IF NOT EXISTS subscription_idx ON %s (subscription)' % table
            self.cursor.execute(query)

        for table in ['whitelist', 'blacklist', 'greylist']:
            self.queries[table] = {}

        for table in ['whitelist', 'blacklist', 'greylist']:
            self.queries[table]["select"] = self.select_query % (table)

        self.sql_conn.commit()
