import socket
import pickle
import hashlib
import os
import re


def ftp_client(ip="localhost", port=6699):
    try:
        client = socket.socket()
        client.connect((ip, port))
        while True:
            msg = input(">>").strip()
            if not msg:
                print("Message can not be empty!")
                continue
            if msg == 'quit()':
                break

            # if msg is a path,then change its path form into "xx/xx/xx"
            msg = msg.replace("\\", "/")
            client.send(msg.encode(encoding="utf-8"))
            download_filename = ""
            if re.search(" |^ls|^pwd|^dir", msg):
                data = b''
                while True:
                    recv_data = client.recv(8192)
                    if recv_data == b'FAIL':
                        print("The file dosen't exist!")
                        break
                    if recv_data == b'EOF':
                        break
                    data += recv_data
                print(pickle.loads(data))
            else:
                download_filename = os.path.split(msg)[1] + "_dw"
                m = hashlib.md5()
                flag = ""
                with open(download_filename, "wb") as f1:
                    while True:
                        recv_data = client.recv(8192)
                        if recv_data == b'FILE_FAIL':
                            print("The file dosen't exist!")
                            flag = "FILE_FAIL"
                            break
                        if recv_data == b'EOF':
                            break
                        m.update(recv_data)
                        f1.write(recv_data)
                if flag == "FILE_FAIL":
                    os.remove(download_filename)
                    continue
                recv_md5 = client.recv(4096).decode(encoding="utf-8")
                if recv_md5 != m.hexdigest():
                    os.remove(download_filename)
                    download_filename = "File receiving has finished!"
    except Exception as e:
        print("haha")
        if os.path.isfile(download_filename):
            os.remove(download_filename)
    finally:
        client.close()


if __name__ == '__main__':
    ftp_client()
