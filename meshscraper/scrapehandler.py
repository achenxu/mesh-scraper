import threading
import random

from meshscraper.wrapper import scrape_pid_collection

class ScrapeHandler(threading.Thread):
    """Handle the scraping process on a separate thread."""

    def __init__(self, site, collection_queue, save_queue, post_queue=None, proxies=[]):
        threading.Thread.__init__(self)
        self.site = site
        self.collection_queue = collection_queue
        self.save_queue = save_queue
        self.post_queue = post_queue
        self.proxies = proxies

    def _get_random_proxy(self):
        try:
            return random.choice(self.proxies)
        except IndexError:
            return None

    def run(self):
        """Scrape PIDs from collection queue and add them to save queue."""
        while True:
            pid_collection = self.collection_queue.get()

            try:
                scraped_pids = scrape_pid_collection(self.site, pid_collection,
                                                     proxy=self._get_random_proxy())
            except Exception as err:
                print('Error checking PID collection!')
                print(err)
                pass
            else:
                # Add scraped pids to save_queue
                for pid in scraped_pids:
                    self.save_queue.put(pid)
                    if self.post_queue:
                        self.post_queue.put(pid)

            self.collection_queue.task_done()
