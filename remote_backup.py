## Usage
#event-handler config_archive
#   trigger on-startup-config
#   action bash python /mnt/flash/remote_backup.py 172.16.1.1 user password ns-MGMT
#   delay 1

#dc1-leaf1(config)#more flash:remote_backup.log 
#2025-08-13 07:28:14 DEBUG    Connected to 172.16.1.1.
#2025-08-13 07:28:14 DEBUG    Uploading startup-config to /dc1-leaf1_20250813072813.cfg

## import modules
import sys
import os
import pexpect
import datetime
import socket
import logging

## Logging
logger = logging.getLogger()
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', filename='/mnt/flash/remote_backup.log', encoding='utf-8', level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S')

##  set time and folder
now = datetime.datetime.now()
os.chdir('/mnt/flash')

## get vars
try:
    get_addr = sys.argv[1]
    get_user = sys.argv[2]
    get_pass = sys.argv[3]
    get_nspc = sys.argv[4]
    get_time = (now.strftime("%Y%m%d%H%M%S"))
    get_host = socket.gethostname()
    connect_command = "ip netns exec "+get_nspc+" sftp " + get_user+'@'+get_addr
    copy_command = "put startup-config " + get_host + '_' + get_time + '.cfg'
except Exception as e:
    logger.debug(e)

## run backup
try:
    result = []
    child = pexpect.spawn(connect_command)
    child.expect('(?i)password:')
    child.sendline(get_pass)
    child.expect('(?i)>')
    logger.debug(child.before.decode("utf-8").split("\n")[1])
    child.sendline(copy_command)
    child.expect('(?i)>')
    logger.debug(child.before.decode("utf-8").split("\n")[1])
    child.sendline('quit')
    child.expect(pexpect.EOF, timeout=3)
    print ("remote backup finished")
except Exception as e:
    logger.debug(e)
