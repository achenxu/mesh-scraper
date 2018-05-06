import socket

# TODO: Better name for this module

def scrape_pid_collection(site, pid_collection, proxy=None):
    """Scrape a range of PIDs for a site starting at initial_num.

    Args:
        site: The site who's PIDs will be scraped.
        pid_collection: List of PIDs to be scraped.
        proxy: An ip:port formatted proxy.

    Returns:
        A list of scraped PIDs from pid_collection.
    """
    if proxy:
        # Create socket & connect to proxy server
        # TODO: Support for ip:port:user:pass proxies
        host, port = proxy.split(':')
        port = int(port)
        scraper_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        scraper_socket.settimeout(10)
        scraper_socket.connect((host, port)) # Connect to the proxy server
        url_prefix = 'http://i1.adis.ws/i/jpl'
    else:
        # Create socket & connect to image provider directly
        scraper_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        scraper_socket.settimeout(10)
        scraper_socket.connect(('i1.adis.ws', 80))
        url_prefix = '/i/jpl'

    # Send a request for each pid through the socket
    for pid in pid_collection:
        http_data = (f'HEAD {url_prefix}/{site}_{pid}_a HTTP/1.1\r\n'
                     'Host: i1.adis.ws\r\n'
                     'Accept: */*\r\n'
                     'Connection: keep-alive\r\n\r\n')

        # Send the HTTP request data to the server
        scraper_socket.sendall(http_data.encode('utf-8'))

    # Create a buffer with socket response data
    buffer = b''
    while True:
        try:
            resp_data = scraper_socket.recv(4096)
        except socket.timeout:
            # print('Socket timed out!')
            break
        else:
            buffer += resp_data

    # Split the buffer into separate HTTP responses
    responses = str(buffer).split('HTTP/1.1')[1:]

    # Create list of scraped PIDs
    scraped_pids = []
    for i, resp in enumerate(responses):
        if '200 OK' in resp:
            scraped_pids.append(pid_collection[i])

    return scraped_pids
