"""Trying to use sockets with https."""
import socket
import ssl

host = 'httpbin.org'
port = 443

test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
test_socket_ssl = ssl.wrap_socket(test_socket, ssl_version=ssl.PROTOCOL_TLSv1)
test_socket_ssl.settimeout(5)
test_socket_ssl.connect((host, port))

http_data = (f'GET /ip HTTP/1.1\r\n'
             'Host: httpbin.org\r\n'
             'Accept: */*\r\n'
             'Connection: keep-alive\r\n\r\n')

test_socket_ssl.sendall(http_data.encode('utf-8'))

buffer = b''
while True:
    try:
        resp_data = test_socket_ssl.recv(4096)
    except Exception as err:
        print(err)
        break
    else:
        buffer += resp_data

print(str(buffer))
