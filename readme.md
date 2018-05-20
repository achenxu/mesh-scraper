# mesh-scraper
Image scraper for mesh sites.
Supports Footpatrol, size?, JD Sports, and The Hip Store.

## Running the script
Make sure you're in the mesh-scraper directory.
```
python3 main.py
```

## Setup/Configuration
Make sure to use proxies or run the scraper with a throwaway IP. The IP address used to scrape will be flagged and will receive soft bans on a bunch of different websites.

### Scraper
You can configure the scraper by editing these keyword argument values for the four Scraper instances in main.py:
**range_start** - The first PID you want the scraper to check.
**range_end** - The last PID you want the scraper to check.
**collection_size** - The amount of PIDs each scraper thread will check at a time.
**num_threads** - The amount of internal scraper threads to create. Adjust this based on the capabilities of your machine.

### Proxies
You can use proxies with the scraper by adding them to the proxies list in main.py.
Only ip:port proxies are supported. Support for ip:port:user:pass proxies will be added soon.
Each request will be assigned a random proxy from the proxies list.

### Discord
The scraper can post PIDs to discord as soon as it finds them.
Just set the discord_webhook variable in main.py to your full webhook URL.

![new pid found](https://i.imgur.com/hEuDpPk.png)

## todo
- User friendly installation/configuration
- ip:port:user:pass proxy support
- Flask app to view and manage PIDs stored in database
