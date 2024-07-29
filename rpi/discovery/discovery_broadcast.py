#! /usr/local/rpi_home/python3/bin/python3

import socket
import time

def send_broadcast_and_listen():
    # Set up the broadcast socket
    broadcast_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    broadcast_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Set up the listening socket
    listen_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_sock.bind(('', 3100))

    # Send a broadcast message
    broadcast_message = b"Hello, is anyone there?"
    broadcast_sock.sendto(broadcast_message, ('<broadcast>', 3100))
    print("Broadcast message sent.")

    # Wait for a response
    broadcast_sock.settimeout(5)
    try:
        while True:
            response, address = listen_sock.recvfrom(1024)
            print(f"Received response: {response} from {address}")
            break
    except socket.timeout:
        print("No response received within the timeout period.")

if __name__ == "__main__":
    send_broadcast_and_listen()
