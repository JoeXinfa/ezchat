# -*- coding: utf-8 -*-
"""
A chat system - server
"""

import argparse
import socket
import threading
import sys

BUFFER_SIZE = 2048 # what's the best size?


class ChatterMember:
    def __init__(self, name, ip, udp_port):
        self.name = name
        self.ip = ip
        self.udp_port = udp_port


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
        tcp_socket = self.connection_socket
        while self.running:
            try:
                msg_expected = ' '
                while msg_expected[-1] != '\n':
                    msg_received = tcp_socket.recv(BUFFER_SIZE)
                    msg_received = msg_received.decode("utf-8")
                    msg_expected += msg_received
                msg_expected = msg_expected.strip()
            except:
                self.running = False # force stop
            self.parse_client_message(msg_expected)

    def parse_client_message(self, msg):
        msg_command = msg[:4]
        if msg_command == 'HELO':
            self.parse_msg_helo(msg)
        elif msg_command == 'EXIT':
            self.parse_msg_exit(msg)
        else:
            raise Exception("Unknown message: {}".format(msg))

    def parse_msg_helo(self, msg):
        msg = msg.split()
        name, ip, port = msg[1:4]
        member = ChatterMember(name, ip, port)
        members = self.server.get_members()
        if member.name in members.keys():
            self.send_msg_rjct(member)
        else:
            self.server.add_member(member)
            self.send_msg_acpt()
            
    def send_msg_rjct(self, member):
        print("reject", member.name)

    def send_msg_acpt(self):
        members = self.server.get_members()
        print("accept", members)

    def parse_msg_exit(self, msg):
        pass

class Server:
    def __init__(self, welcome_tcp_port):
        self.welcome_tcp_port = welcome_tcp_port
        self.ip_address = self.get_ip_address()
        self.set_welcome_tcp_socket()
        self.servant_threads = []
        self.members = {}
        self.members_lock = threading.Lock()

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

    def get_members(self):
        self.members_lock.acquire()
        members = self.members
        self.members_lock.release()
        return members

    def add_member(self, member):
        self.members_lock.acquire()
        key = member.name
        self.members[key] = member
        self.members_lock.release()
        self.send_msg_join(member)
        print("members", self.members)
        
    def send_msg_join(self, member):
        pass


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