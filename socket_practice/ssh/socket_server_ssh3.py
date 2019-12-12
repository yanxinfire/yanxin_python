import socket
import os
import pickle
import time


def create_server(ip="localhost", port=6699):
    server = socket.socket()
    server.bind((ip, port))
    server.listen()

    try:
        while True:
            print("Waiting for new connection...")
            conn, addr = server.accept()

            while True:
                print("New connection is conneted in!", addr)
                data = conn.recv(4096)
                if not data:
                    print("Client (%s,%s) has lost the connection!" % (addr[0], addr[1]))
                    break
                print("Recv: %s" % data.decode(encoding="utf-8"))
                response = pickle.dumps(os.popen(data.decode()).read())
                conn.sendall(response)
                #防止粘包
                time.sleep(0.5)
                conn.send(b'EOF')
    except KeyboardInterrupt as e:
        print("\033[0;31mByeBye!\033[0m")
    finally:
        server.close()


if __name__ == '__main__':
    create_server()
