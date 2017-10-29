#!py

import logging
import subprocess
from slacker import Slacker

slack = Slacker('xoxp-226792929462-225250171360-260800059796-84e42e6ad4ccd7376fda3aa95b3c3fb3')
log = logging.getLogger(__name__)

def run():
  cmd = "salt mongo-mongos mongobackup.backup"
  log.info("running cmd ")
  mssg_out = subprocess.check_output(cmd, shell=True)
  log.info(mssg_out)
  slack.chat.post_message('#devops',mssg_out,'saltstackbot' )
  return {}
