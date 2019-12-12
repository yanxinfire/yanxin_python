import socket
import os
import pickle
import hashlib
import time
import re


def ftp_server(ip="localhost", port=6699):
    server = socket.socket()
    server.bind((ip, port))
    server.listen()

    try:
        while True:
            print("Waiting for new connection...")
            conn, addr = server.accept()
            while True:
                print("Waiting for %s send the command!", addr)
                data = conn.recv(4096).decode(encoding="utf-8")
                if not data:
                    print("Client (%s,%s) has lost the connection!" % (addr[0], addr[1]))
                    break
                print(data)
                if re.search(" |^ls|^pwd|^dir", data):
                    result = os.popen(data).read()
                    if not result:
                        conn.send(b'FAIL')
                        continue
                    response = pickle.dumps(result)
                    conn.sendall(response)
                    time.sleep(0.5)
                    conn.send(b'EOF')
                elif os.path.isfile(data):
                    m = hashlib.md5()
                    with open(data, "rb") as f1:
                        while True:
                            file_data = f1.read(8192)
                            if not file_data:
                                time.sleep(0.5)
                                conn.send(b'EOF')
                                break
                            m.update(file_data)
                            conn.send(file_data)
                    conn.send(m.hexdigest().encode(encoding="utf-8"))
                else:
                    conn.send(b'FILE_FAIL')
    except KeyboardInterrupt as e:
        print("\033[0;31mByeBye!\033[0m")
    finally:
        server.close()


if __name__ == '__main__':
    ftp_server()
