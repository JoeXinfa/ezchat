# -*- coding: utf-8 -*-
"""
A chat system - server
"""

import argparse
import socket
import threading
import sys


class Server:
    def __init__(self, welcome_tcp_port):
        self.welcome_tcp_port = welcome_tcp_port
        self.ip_address = self.get_ip_address()
        self.set_welcome_tcp_socket()

    def get_ip_address(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip_address = s.getsockname()[0]
            s.close()
        except:
            ip_address = socket.gethostbyname('localhost')
        ip_address = socket.gethostbyname('localhost')
        print("ip_address:", ip_address)
        return ip_address

    def set_welcome_tcp_socket(self):
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the socket to the port
        server_address = (self.ip_address, self.welcome_tcp_port)
        sock.bind(server_address)
        # Call listen() puts the socket into server mode
        sock.listen()
        while True:
            # Wait for a connection
            print("waiting for a connection")
            connection, client_address = sock.accept()
            print("connection:", connection)
            print("client_address:", client_address)
        self.welcome_tcp_socket = sock


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("welcome_tcp_port", help="The server welcome tcp port", type=int)

    # parse the arguments
    args = parser.parse_args()
    welcome_tcp_port = args.welcome_tcp_port
    
    server = Server(welcome_tcp_port)


if __name__ == '__main__':
    main()
