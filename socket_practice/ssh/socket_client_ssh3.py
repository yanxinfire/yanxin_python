"""
Server sends "User-Defined Finish Signal"--> "EOF",
and client receives data in a loop until receive the "EOF"
"""

import socket
import pickle


def create_client(ip="localhost", port=6699):
    client = socket.socket()
    client.connect((ip, port))
    while True:
        msg = input(">>").strip()
        if not msg:
            print("Message can not be empty!")
            continue
        if msg == 'quit()':
            break
        client.send(msg.encode(encoding="utf-8"))
        data = b''
        while True:
            recv_data = client.recv(8)
            print(recv_data)
            if recv_data == b'EOF':
                break
            data += recv_data
        print(pickle.loads(data))
    client.close()


if __name__ == '__main__':
    create_client()
