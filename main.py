from meshscraper import Scraper

def main():

    proxies = [
        '127.0.0.1:6001',
        '127.0.0.1:6002'
    ]

    fp_scraper = Scraper('fp', 0, 1000, collection_size=100, num_threads=16, proxies=proxies)
    fp_scraper.start()

    sz_scraper = Scraper('sz', 0, 300000, collection_size=100, num_threads=16, proxies=proxies)
    sz_scraper.start()

    jd_scraper = Scraper('jd', 0, 300000, collection_size=100, num_threads=16, proxies=proxies)
    jd_scraper.start()

    hp_scraper = Scraper('hp', 0, 300000, collection_size=100, num_threads=16, proxies=proxies)
    hp_scraper.start()

if __name__ == '__main__':
    main()
