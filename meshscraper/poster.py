import threading
import time

import requests

from meshscraper.util import create_logger

class Poster(threading.Thread):

    def __init__(self, site, discord_webhook, post_queue):
        threading.Thread.__init__(self)
        self.site = site
        self.discord_webhook = discord_webhook
        self.post_queue = post_queue
        self.logger = create_logger(f'{self.site} poster', logger_level=20)

    def _post_to_discord(self, product_id):
        """Post a product ID to discord."""

        image_link = f'http://i1.adis.ws/i/jpl/{self.site}_{product_id}_a'

        formatted_data = {
            "as_user": True,
            "attachments": [
                {
                    "fallback": f'New {self.site.upper()} PID found! {product_id}',
                    "author_name": f'New {self.site.upper()} PID found!',
                    "title": product_id,
                    "title_link": image_link,
                    "thumb_url": image_link,
                    "footer": "github.com/idontcop/mesh-scraper"
                }
            ]
        }

        resp = requests.post(self.discord_webhook + '/slack', json=formatted_data)
        resp.raise_for_status()

    def run(self):
        while True:
            product_id = self.post_queue.get()
            self.logger.debug(f'Posting {product_id} to discord!')

            # Post the product ID to discord
            try:
                self._post_to_discord(product_id)
            except requests.exceptions.RequestException:
                self.logger.error(f'Error posting {product_id} to discord!')
            else:
                self.logger.info(f'Posted {product_id} to discord!')

            self.post_queue.task_done()

            # Sleep to avoid discord rate limit
            time.sleep(1)
