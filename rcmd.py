"""Remote executing same commands on different hosts in multi threads by using ssh

Reading the hostsfile like following form:
ip,port,username,password(this line shall not be in hostsfile!)
192.168.12.76,22,root,oracle
192.168.12.10,22,mysql,oracle
192.168.12.20,22,oracle,oracle
...
then executing the commands on these hosts.
Attention:
The "multi threads" in title is for the multi "ssh" in the sametime.
But when beginning to execute commands on each host,the processing is serializable.
"""
import sys
import paramiko
import threading
import os


def rcmd(host, user, passwd, port=22, *cmds):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    ssh.connect(hostname=host, username=user, password=passwd, port=port)
    for cmd in cmds:
        stdin, stdout, stderr = ssh.exec_command(cmd)
        print("STDOUT: ", stdout.read().decode())
        print("STDERR: ", stderr.read().decode())
    ssh.close()


def cope_with_recvs(hostfile, *cmds):
    with open(hostfile, "r", encoding="utf-8") as f1:
        for line in f1:
            # 一定要用strip去除尾部的回车！
            host_info = line.strip().split(",")
            host = host_info[0]
            port = host_info[1]
            user = host_info[2]
            passwd = host_info[3]

            t = threading.Thread(
                target=rcmd,
                args=(host, user, passwd, port, *cmds)
            )
            t.start()


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage:%s hostfiles "command1" "command2" ...' % sys.argv[0])
        exit(3)
    if not os.path.exists(sys.argv[1]):
        print("Hostfile:%s dosen't exist!")
        exit(4)
    cope_with_recvs(sys.argv[1], *sys.argv[2:])
