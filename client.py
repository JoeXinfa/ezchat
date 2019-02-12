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
    print("chatter name: {}".format(chatter.screen_name))


if __name__ == '__main__':
    main()
