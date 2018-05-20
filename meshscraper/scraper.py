from queue import Queue
import threading
import time

from meshscraper.util import convert_to_pid, create_logger
from meshscraper.scrapehandler import ScrapeHandler
from meshscraper.poster import Poster
from meshscraper.saver import Saver

class Scraper(threading.Thread):
    """Create and control collection checker(scrape handler) threads."""

    def __init__(self, site, range_start, range_end, collection_size=50,
                 num_threads=4, proxies=[], discord_webhook=None):
        threading.Thread.__init__(self)
        self.site = site # fp, sz, jd, or hp
        self.range_start = range_start
        self.range_end = range_end
        self.collection_size = collection_size
        self.num_threads = num_threads
        self.proxies = proxies
        self.discord_webhook = discord_webhook

        self.logger = create_logger(f'{self.site} scraper', logger_level=20)

    def run(self):
        """Start and control the scraping process."""
        start_time = time.time()

        # Create the save queue
        # This is where newly scraped PIDs will be put & saved
        save_queue = Queue()

        # Create & start the saver thread - save PIDs to database on separate thread
        saver_thread = Saver(self.site, save_queue)
        # Start the saver thread
        saver_thread.daemon = True
        saver_thread.start()

        # Create a poster thread & poster queue if there's a webhook
        post_queue = None
        if self.discord_webhook:
            post_queue = Queue()
            poster_thread = Poster(self.site, self.discord_webhook, post_queue)
            poster_thread.daemon = True
            poster_thread.start()

        # Get a set of PIDs that are already stored in the database
        stored_pids = saver_thread.get_stored_pids()

        # Create a list of product IDs to check for
        # pids list will not include product ids that have already been scraped
        pids = []
        for i in range(self.range_start, self.range_end + 1):
            product_id = convert_to_pid(i)
            if product_id not in stored_pids:
                pids.append(product_id)

        # Create pid collections & add them to collection_queue
        # A pid collection is just a list of x amount of pids
        collection_queue = Queue()
        for i in range(0, len(pids), self.collection_size):
            collection_queue.put(pids[i:i + self.collection_size])

        # Create ScrapeHandler threads
        for _ in range(self.num_threads):
            scrape_handler = ScrapeHandler(self.site,
                                           collection_queue,
                                           save_queue,
                                           post_queue,
                                           proxies=self.proxies)
            scrape_handler.daemon = True
            scrape_handler.start()

        self.logger.info(f'Checking for new PIDs!')

        # Wait for queues to empty before exiting
        collection_queue.join()
        save_queue.join()
        if post_queue:
            post_queue.join()

        self.logger.info(f'Checked range {self.range_start} to {self.range_end} '
                         f'in {time.time() - start_time} seconds!')
