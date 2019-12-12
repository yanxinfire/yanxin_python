"""
This version uses length of data stream to control the
moments that when recv() should be finished
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
        recv_data_size = client.recv(1024).decode()
        client.send(b'ACK')
        if int(recv_data_size) == 0:
            recv_data = client.recv(8192)
            if recv_data.decode() == "FAIL":
                print("Command Not Found!")
                continue
        print("result size should be : %s" % recv_data_size)
        data_size = 0
        data = b''
        while int(recv_data_size) != data_size:
            recv_data = client.recv(8192)
            data += recv_data
            data_size += len(recv_data)
        else:
            print("result size: %s" % data_size)
            print(pickle.loads(data))
    client.close()


if __name__ == '__main__':
    create_client()
