#!/usr/bin/python3

import socket


def send_knock(ip: str, port: int):
    """send_knock sends a udp packet to the specified ip and port

    This function is used to send a "knock" that our server will be scanning
    or listening for. The sequence is decided in the client function
    """
    UDP_IP = ip
    UDP_PORT = port
    MESSAGE = ""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))
    return sock
