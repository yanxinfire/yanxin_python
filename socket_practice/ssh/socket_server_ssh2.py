import socket
import os
import pickle



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
                result = os.popen(data.decode()).read()
                if not result:
                    conn.send("0".encode())
                    # 防止粘包
                    conn.recv(1024)
                    conn.send("FAIL".encode())
                    continue
                response = pickle.dumps(result)
                # Here should send the length of bytes stream,not the len of String
                # because len("汉字") == 2,but,for example:len("汉字".encode("utf-8") == 6)
                conn.send(str(len(response)).encode())
                conn.sendall(response)
    except KeyboardInterrupt as e:
        print("\033[0;31mByeBye!\033[0m")
    finally:
        server.close()


if __name__ == '__main__':
    create_server()
