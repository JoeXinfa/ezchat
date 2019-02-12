# -*- coding: utf-8 -*-
"""
A chat system
"""

import argparse
import socket
import threading

BUFFER_SIZE = 2048 # what's the best size?


class myThread(threading.Thread):
   def __init__(self, chatter, job):
      threading.Thread.__init__(self)
      self.chatter = chatter
      self.job = job
   def run(self):
       if self.job == "send":
           while True:
               msg = self.chatter.get_input()
               self.chatter.send_to_all(msg)
       if self.job == "receive":
           while True:
               data, address = self.chatter.udp_socket.recv(BUFFER_SIZE)
               #data, address = chatter.udp_socket.recvfrom(BUFFER_SIZE)
               if data:
                   self.chatter.parse_income_msg(data)


class Chatter:

    def __init__(self, screen_name, host_name, tcp_port):
        self.screen_name = screen_name
        self.host_name = host_name
        self.tcp_port = tcp_port
        self.set_tcp_socket()
        self.set_udp_socket()
        self.peers = {}
        self.make_msg_helo()
        self.send_msg_helo()

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
        #ip_address = socket.gethostbyname(self.host_name)
        ip_address = socket.gethostbyname(socket.gethostname())
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
            self.parse_server_acpt(msg[5:])
        elif msg.startswith("RJCT"):
            screen_name = msg[5:].replace('\n', '')
            print("Screen Name already exists: {}".format(screen_name))
            exit()
        else:
            raise Exception("Unknown response: {}".format(msg))

    def parse_server_acpt(self, msg):
        msg.replace('\n', '') # trim newline
        records = msg.split(':')
        for record in records:
            name, ip, port = record.split(' ')
            self.peers[name] = (ip, int(port))
            if name != self.screen_name:
                print("{} is in the chatroom".format(name))
        print("{} accepted to the chatroom".format(self.screen_name))

    def get_input(self):
        msg = input(self.screen_name + ": ")
        return "MESG " + self.screen_name + ": " + msg + "\n"

    def send_to_all(self, msg):
        # Create a UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        data = msg.encode()
        for name in self.peers:
            server_address = self.peers[name]
            sock.sendto(data, server_address)

    @staticmethod
    def parse_income_msg(msg):
        print(msg[5:])


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

    # Create new threads
    thread1 = myThread(chatter, "send")
    thread2 = myThread(chatter, "receive")

    # Start new Threads
    thread1.start()
    thread2.start()

    while True:
        pass

    # one thread listen for message the user inputs
#    while True:
#        msg = chatter.get_input()
#        chatter.send_to_all(msg)

    # another thread listen for peers' messages on the UDP port
#    while True:
#        try:
#            data, address = chatter.udp_socket.recv(BUFFER_SIZE)
#            #data, address = chatter.udp_socket.recvfrom(BUFFER_SIZE)
#        except Exception as e:
#            print(e)
#        finally:
#            chatter.udp_socket.close()
#        if data:
#            chatter.parse_income_msg(data)


if __name__ == '__main__':
    main()
