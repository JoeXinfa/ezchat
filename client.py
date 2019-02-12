# -*- coding: utf-8 -*-
"""
A chat system
"""

import argparse
import socket
import sys


class Chatter:

    def __init__(self, screen_name, host_name, tcp_port):
        self.screen_name = screen_name
        self.host_name = host_name
        self.tcp_port = tcp_port
        self.set_tcp_socket()
        self.set_udp_socket()

    def set_tcp_socket(self):
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the socket to the port
        server_address = (self.host_name, self.tcp_port)
        #print('connecting to {} port {}'.format(*server_address))
        sock.connect(server_address)
        self.tcp_socket = sock

    def set_udp_socket(self, port=0):
        # port=0 tells the OS to pick a port
        # Create a UDP/IP socket -> DGRAM
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Bind the socket to a port of OS's choosing
        server_address = (self.host_name, port)
        sock.bind(server_address)
        # To find what port the OS picked, call getsockname()
        self.udp_socket = sock
        self.udp_port = sock.getsockname()[1]
        print('My UDP port is: {}'.format(self.udp_port))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("screen_name", help="Your screen/user name")
    parser.add_argument("host_name", help="The server hostname")
    parser.add_argument("tcp_port", help="The server welcome tcp port", type=int)

    # parse the arguments
    args = parser.parse_args()
    screen_name = args.screen_name
    host_name = args.host_name
    tcp_port = args.tcp_port
    
    chatter = Chatter(screen_name, host_name, tcp_port)
    #print("chatter name: {}".format(chatter.screen_name))


if __name__ == '__main__':
    main()
