from meshscraper import Scraper

def main():

    # Add discord webhook here
    discord_webhook = ''

    """
    Example:
    discord_webhook = 'https://discordapp.com/api/webhooks/sdljflksdjflkdfs'
    """

    # Add proxies here
    proxies = []

    """
    Example:
    proxies = [
        '127.0.0.1:6001',
        '127.0.0.1:6002',
        '127.0.0.1:6003',
        '127.0.0.1:6004',
        '127.0.0.1:6005'
    ]
    """

    # Create & start Footpatrol scraper
    fp_scraper = Scraper('fp',
                         range_start=0,
                         range_end=300000,
                         collection_size=100,
                         num_threads=8,
                         proxies=proxies,
                         discord_webhook=discord_webhook)
    fp_scraper.start()

    # Create & start size? scraper
    sz_scraper = Scraper('sz',
                         range_start=0,
                         range_end=300000,
                         collection_size=100,
                         num_threads=8,
                         proxies=proxies,
                         discord_webhook=discord_webhook)
    sz_scraper.start()

    # Create & start JD Sports scraper
    jd_scraper = Scraper('jd',
                         range_start=0,
                         range_end=3000000,
                         collection_size=100,
                         num_threads=8,
                         proxies=proxies,
                         discord_webhook=discord_webhook)
    jd_scraper.start()

    # Create & start The Hip Store scraper
    hp_scraper = Scraper('hp',
                         range_start=0,
                         range_end=3000000,
                         collection_size=100,
                         num_threads=8,
                         proxies=proxies,
                         discord_webhook=discord_webhook)
    hp_scraper.start()

if __name__ == '__main__':
    main()
