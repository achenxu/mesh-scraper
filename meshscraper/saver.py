from datetime import datetime
import threading
import sqlite3

from meshscraper.util import create_logger

class Saver(threading.Thread):

    def __init__(self, site, save_queue):
        threading.Thread.__init__(self)
        self.site = site
        self.save_queue = save_queue
        self.logger = create_logger(f'{self.site} saver', logger_level=20)
        self.conn = None
        self.cursor = None
        self.__setup_db()

    def __setup_db(self):
        # Connect to the database
        self.conn = sqlite3.connect('product_ids.db', check_same_thread=False)
        self.cursor = self.conn.cursor()

    def get_stored_pids(self):
        """Return a set of stored PIDs in the database."""
        with self.conn:
            self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS {self.site}_ids
                                (product_id TEXT PRIMARY KEY,
                                image_url TEXT,
                                time_scraped TIMESTAMP)""")

            # Create a list of already stored product ids
            self.cursor.execute(f"SELECT * FROM {self.site}_ids")
            rows = self.cursor.fetchall()
            stored_pids = set([x[0] for x in rows])

        return stored_pids

    def run(self):
        """Save pids to an sqlite database from save_queue."""
        while True:
            product_id = self.save_queue.get()
            product_url = f'http://i1.adis.ws/i/jpl/{self.site}_{product_id}_a'
            timestamp = datetime.now()

            self.logger.debug(f'Saving {product_id} for {self.site}')

            # Save the PID to the database
            with self.conn:
                try:
                    self.cursor.execute(f"INSERT INTO {self.site}_ids VALUES (?,?,?)",
                                        (product_id,
                                         product_url,
                                         timestamp))
                except sqlite3.IntegrityError as err:
                    self.logger.error(err)
                else:
                    self.logger.info(f'Added {product_id} to database!')

            self.save_queue.task_done()
