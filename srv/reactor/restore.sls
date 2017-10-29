#!py

import logging
import subprocess
from  slacker import Slacker

slack = Slacker('xoxp-226792929462-225250171360-259658264771-e6ce9af604e97e3f6348de3ed037d08c')
log = logging.getLogger(__name__)

def run():
    
    cmd = "salt mongo-mongos mongobackup.restore " + data['post']['key']
    mssg_out = subprocess.check_output(cmd, shell=True)

    slack.chat.post_message('#devops',mssg_out,'saltstackbot' )
    
    return {}
