"""BLACKLIST these hosts in this hostsfile"""

import sys
import sqlite3
import requests
from foghornd.plugins.listhandler.Sqlite_subscription import Sqlite_subscription


class Sqlite_subscription_hosts(Sqlite_subscription):
    """An sqllite3 backend for foghorn"""

    db_file = 'foghorn_subscription.sqlite3'
    select_query = 'SELECT host, first_seen, last_seen FROM %s WHERE host=?'
    queries = {}
    addips = ["0.0.0.0"]

    # def __init__(self, settings):
    #     super(Sqlite_subscription_hosts, self).__init__(settings)

    def load_lists(self, signal_recvd=None, frame=None):
        """
        This function will be called to reload the lists.
        In our case this  does nothing
        """
        # pylint: disable=W0613
        for url in self.settings.loader_settings["subscriptions"]:
            response = requests.get(url)

            try:
                items = response.text
                cursor = self.sql_conn.cursor()
                for list_type in ["blacklist"]:
                    query = "DELETE FROM %s WHERE subscription=?" % list_type
                    cursor.execute(query, (url,))

                    query = "INSERT OR IGNORE INTO %s (host) VALUES (?)" % list_type
                    for item in items.split("\n"):
                        row = item.split()
                        if len(row) < 2:
                            continue
                        if row[1] in self.addips:
                            cursor.execute(query, (row[2],))

                    self.sql_conn.commit()
            except sqlite3.Error as e:
                print "An error occurred:", e.args[0]
                exit(1)
            except:
                print "Unable to load subscription: ", response
                print sys.exc_info()[0]
