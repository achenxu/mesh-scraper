import socket

def check_pid_collection(pid_collection):
    """Scan a range of PIDs for a site starting at initial_num.

    Arguments
    site(string) -- The site who's PIDs will be scanned
    pid_collection(list) -- PIDs to be scanned

    Return a list of valid PIDs from pid_collection.
    """
    # Create socket & connect to image provider
    scanner_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    scanner_socket.settimeout(2.5)
    scanner_socket.connect(('res-3.cloudinary.com', 80))

    # Send a request for each pid through the socket
    for pid in pid_collection:
        http_data = (f'HEAD /ssenseweb/image/upload/{pid}_1.jpg HTTP/1.1\r\n'
                     'Host: res-1.cloudinary.com\r\n'
                     'Accept: */*\r\n'
                     'Connection: keep-alive\r\n\r\n')

        # Send the HTTP request data to the server
        scanner_socket.sendall(http_data.encode())

    # Create a buffer with socket response data
    buffer = b''
    while True:
        try:
            resp_data = scanner_socket.recv(4096)
        except socket.timeout:
            # print('Socket timed out!')
            break
        buffer += resp_data

    # Split the buffer into separate HTTP responses
    responses = str(buffer).split('HTTP/1.1')[1:]

    # Create list of valid PIDs
    valid_pids = []
    for i, resp in enumerate(responses):
        if '200 OK' in resp:
            valid_pids.append(pid_collection[i])

    return valid_pids

if __name__ == '__main__':

    prefix = '182011M23' # 182011 for Nike, M23 for shoes
    test_pids = [f'{prefix}{x}' for x in range(6000, 8000)]
    collection_size = 50

    for i in range(0, len(test_pids), collection_size):
        valid_pids = check_pid_collection(test_pids[i:i+collection_size])
        print(valid_pids)
