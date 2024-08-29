from lib763.SSHOperator import SSHOperator
from CONST import *

ssh = SSHOperator(
    SSH_USERNAME, SSH_HOST, SSH_PASSWORD, SSH_KEY, SSH_PORT
)
print(ssh.connect_ssh())

print(ssh.get_file('/home/naru3/out.txt','./'))