import logging
import uuid
import subprocess
import os, math
import re
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from  slacker import Slacker
import pymongo


log = logging.getLogger(__name__)


class RunCmd(object):
    def run_cmd(self, cmd):
        self.cmd = cmd
        subprocess.call(self.cmd, shell=True)

def slackNotification():

    slack = Slacker('xoxp-226792929462-225250171360-260800059796-84e42e6ad4ccd7376fda3aa95b3c3fb3')
    return slack

def _getMeHost():
    return __grains__['ip_interfaces']['eth0'][0]

def _filename():
    for f in os.listdir('/data'):
        if re.match('dumpfile', f):
            return f

def _dump():
    """
    function takes a dump of the entire mongo db instance
    """
    host = _getMeHost()
    mongo_dump = 'mongodump --host ' + host +' -o /data/backup'
    tar_cmd = 'tar -czf ' + '/data/dumpfile_' + str(uuid.uuid4()) + '.tar.gz'  + ' /data/backup'
    log.info("This is the tar command :" + tar_cmd )    
    a = RunCmd()
    a.run_cmd("rm -rf /data/dumpfile*")    
    a.run_cmd(mongo_dump)   
    a.run_cmd(tar_cmd)
    log.info("done with dump")


def _upload():
    conn = S3Connection('AKIAJIRGIYOS2LGEDX6A','7C2dGs6rCqOqrAFGv/kBwR/YyqNY0ZXPJuky8wUl')
    bucket = conn.get_bucket('mongocluster')
    log.info("connected to bucket")
    k = Key(bucket)
    source_path = '/data/' + _filename()
    k.set_contents_from_filename(source_path)
    return k.key

def backup():
    _dump()
    key= _upload()
    a = RunCmd()
    remove_file = 'rm -rf ' +  '/data/' + _filename()
    a.run_cmd(remove_file)
    #r = requests.post('http://52.37.172.89:27179/hook/stagingdbRestore', data = {'key': key})
    log.info("backup done sending notice to slack")

    s = slackNotification()

    s.chat.post_message('#devops', key)


    return "Backup done S3 key ==> " + str(key)


# def _getMeRestoreCmd():  
#   host = _getMeHost()
#   cmd = 'mongorestore --host ' + host + ' -d /data/backup/harpreet'


def fetchDump(key_value):
  host = _getMeHost()
  tar_cmd = 'tar -xvf ' + '/data/'+ key_value  + ' -C /data'
  a = RunCmd()
  conn = S3Connection('AKIAJIRGIYOS2LGEDX6A','7C2dGs6rCqOqrAFGv/kBwR/YyqNY0ZXPJuky8wUl')    
  log.info("sandeep")
  log.info(key_value)
  log.info(type(key_value))
  bucket = conn.get_bucket('mongocluster')
  key = bucket.get_key(key_value)
  log.info(type(key))
  log.info(key)
  #key.get_contents_to_filename('/data/' + key_value)
  #a.run_cmd(tar_cmd)
  
  return key

def operateOnUserCall():
  host = _getMeHost()
  global harpreet
  client = pymongo.MongoClient(host, 27017)
  db = client.harpreet 

  return db


#def _importUserData(key):
#    """
#    function imports  user data collections
#    """
#    count = 0
#    host = _getMeHost()
    
    # stop_balancer = 'mongo --host ' + host + ' /opt/stopbalancer.js'
    # start_balancer = 'mongo --host ' + host + ' /opt/startbalancer.js


#    a = RunCmd()
    #a.run_cmd(stop_balancer)

#    for c in harpreetcollections:
#        if c not in configCollections:
#            log.info('importing collection : ' + c)
#            log.info('mongorestore -d harpreet -c ' + c + ' -h ' +  host + ' /data/backup/harpreet/' + c + '.bson')
#            a.run_cmd('mongorestore -d harpreet -c ' + c + ' -h ' +  host + ' /data/backup/harpreet/' + c + '.bson')

    # a.run_cmd(start_balancer)

#    a.run_cmd("rm -rf /data/backup")
#    a.run_cmd("rm -rf /data/" + key) 





def restore(key):
  _fetchDump(key)
  operateOnUserColl('drop')
#    _importUserData(key)
#    return 'restored'










