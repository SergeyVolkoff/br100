import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], '..'))
sys.path.insert(1, os.path.join(sys.path[0], '../..'))

import pexpect

ssh = pexpect.spawn('ssh storage@storage@git-ci-storage.opk-bulat.ru')
print(ssh.expect("storage@git-ci-storage.opk-bulat.ru's password:"))
print(ssh.sendline("storage"))
ssh.expect('git-ci-storage')
print(ssh.before)
ssh.close()