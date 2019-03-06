# -*- coding: utf-8 -*-
"""
A chat system - server
"""

import argparse
import socket
import threading
import sys

BUFFER_SIZE = 2048 # what's the best size?


class ServantThread(threading.Thread):
    
    def __init__(self, server, connection_socket, client_address):
        super(ServantThread, self).__init__()
        self.server = server # the server parent
        self.connection_socket = connection_socket
        self.client_address = client_address
        self.client_ip = client_address[0]
        self.client_port = client_address[1]
        
    def run(self):
        self.running = True
        while self.running:
            print("servant thread running", self.client_ip, self.client_port)
            self.running = False


class Server:
    def __init__(self, welcome_tcp_port):
        self.welcome_tcp_port = welcome_tcp_port
        self.ip_address = self.get_ip_address()
        self.set_welcome_tcp_socket()
        self.servant_threads = []

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

    def start(self):
        sock = self.welcome_tcp_socket
        while True:
            # Wait for a connection
            print("waiting for a connection")
            connection, client_address = sock.accept()
            servant_thread = ServantThread(self, connection, client_address)
            self.servant_threads.append(servant_thread)
            servant_thread.start()
        
    def set_welcome_tcp_socket(self):
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the socket to the port
        server_address = (self.ip_address, self.welcome_tcp_port)
        sock.bind(server_address)
        # Call listen() puts the socket into server mode
        sock.listen()
        self.welcome_tcp_socket = sock


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("welcome_tcp_port", help="The server welcome tcp port", type=int)

    # parse the arguments
    args = parser.parse_args()
    welcome_tcp_port = args.welcome_tcp_port
    
    server = Server(welcome_tcp_port)
    server.start()


if __name__ == '__main__':
    main()
