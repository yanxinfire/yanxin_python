"""
This version used set recv()'s timeout to control the
moments that when recv() should be terminated,and catch
the exception named "socket.timeout" to continue the program!
"""
import socket
import pickle


def create_client(ip="localhost", port=6699):
    client = socket.socket()
    client.connect((ip, port))
    # set timeout
    client.settimeout(2)
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
            # try and catch the socket.timeout to end up receiving data
            try:
                recv_data = client.recv(8192)
            except socket.timeout as e:
                break
            data += recv_data
        print(pickle.loads(data))
    client.close()


if __name__ == '__main__':
    create_client()
