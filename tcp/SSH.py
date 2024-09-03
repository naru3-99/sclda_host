from lib763.SSHOperator import SSHOperator
from CONST import *

def main():
    ssh = SSHOperator(
        SSH_USERNAME, SSH_HOST, SSH_PASSWORD, SSH_KEY, SSH_PORT
    )
    print(ssh.connect_ssh())
    print(ssh.execute_sudo("dmesg > out.txt"))
    print(ssh.get_file('/home/naru3/out.txt','./'))

if __name__ == '__main__':
    main()