#! /usr/local/rpi_home/python3/bin/python3

import socket

def listen_and_respond():
    # Set up the socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.bind(('', 3100))

    while True:
        # Receive the broadcast message
        message, address = sock.recvfrom(1024)
        print(f"Received message: {message} from {address}")

        # Respond to the sender
        response = b"Message received"
        sock.sendto(response, address)
        print(f"Sent response to {address}")

if __name__ == "__main__":
    listen_and_respond()
