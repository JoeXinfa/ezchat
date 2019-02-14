# -*- coding: utf-8 -*-
"""
A chat system
"""

import argparse
import socket
import threading

BUFFER_SIZE = 2048 # what's the best size?


class SendThread(threading.Thread):
   def __init__(self, chatter):
      threading.Thread.__init__(self)
      self.chatter = chatter
   def run(self):
       while True:
           msg = self.chatter.get_input()
           self.chatter.send_to_all(msg)


class ReceiveThread(threading.Thread):
   def __init__(self, chatter):
      threading.Thread.__init__(self)
      self.chatter = chatter
   def run(self):
       while True:
           msg, address = self.chatter.udp_socket.recvfrom(BUFFER_SIZE)
           msg = msg.decode("utf-8")
           if msg.startswith("MESG"):
               self.chatter.parse_income_msg(msg)
           elif msg.startswith("JOIN"):
               self.chatter.parse_server_join(msg)
           elif msg.startswith("EXIT"):
               self.chatter.parse_server_exit(msg)
           else:
               raise Exception("Unknown message: {}".format(msg))


class Chatter:

    def __init__(self, screen_name, host_name, tcp_port):
        self.screen_name = screen_name
        self.host_name = host_name
        self.tcp_port = tcp_port
        self.set_tcp_socket()
        self.set_udp_socket()
        self.peers = {}
#        self.make_msg_helo()
#        self.send_msg_helo()

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

    def make_msg_helo(self):
        ip_address = socket.gethostbyname(self.host_name)
        #ip_address = socket.gethostbyname(socket.gethostname()) # not work?
        self.msg_helo = "HELO " + self.screen_name + " " +\
            ip_address + " " + str(self.udp_port) + "\n"

    def send_msg_helo(self):
        self.tcp_socket.send(self.msg_helo.encode())
        # To fix getting partial response from the server
        msg_expected = ' '
        while msg_expected[-1] != '\n':
            msg_received = self.tcp_socket.recv(BUFFER_SIZE)
            msg_received = msg_received.decode("utf-8")
            msg_expected += msg_received
        msg_expected = msg_expected[1:]
        #print("msg_from_server =", msg_expected)
        self.deal_server_response_to_helo(msg_expected)

    def deal_server_response_to_helo(self, msg):
        if msg.startswith("ACPT"):
            self.parse_server_acpt(msg)
        elif msg.startswith("RJCT"):
            self.parse_server_rjct(msg)
        else:
            raise Exception("Unknown response: {}".format(msg))

    def parse_server_rjct(self, msg):
        name = msg[5:].replace('\n', '')
        print("Screen Name already exists: {}".format(name))
        exit()
        # TODO how to let user keep using the terminal after this?

    def parse_server_acpt(self, msg):
        msg = msg[5:].replace('\n', '')
        records = msg.split(':')
        for record in records:
            name, ip, port = record.split(' ')
            self.peers[name] = (ip, int(port))
            if name != self.screen_name:
                print("{} is in the chatroom".format(name))

    def parse_server_join(self, msg):
        msg = msg[5:].replace('\n', '')
        name, ip, port = msg.split(' ')
        if name == self.screen_name:
            print("{} accepted to the chatroom".format(name))
        if name not in self.peers:
            self.peers[name] = (ip, int(port))

    def parse_server_exit(self, msg):
        name = msg[5:].replace('\n', '')
        print("{} has left the chatroom".format(name))
        self.peers.pop(name, None)

    @staticmethod
    def parse_income_msg(msg):
        print(msg[5:])

    def get_input(self):
        msg = input(self.screen_name + ": ")
        return "MESG " + self.screen_name + ": " + msg + "\n"
        # TODO how to let user Ctrl+C to exit the chat?
        # handle emit EXIT message and can keep use that terminal?

    def send_to_all(self, msg):
        data = msg.encode()
        for name in self.peers:
            server_address = self.peers[name]
            self.udp_socket.sendto(data, server_address)


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
    recv = ReceiveThread(chatter)
    send = SendThread(chatter)

    recv.start()
    chatter.make_msg_helo()
    chatter.send_msg_helo()
    send.start()


if __name__ == '__main__':
    main()
