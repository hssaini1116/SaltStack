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
  
users = []

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
    log.info("backup done sending notice to slack")

    s = slackNotification()

    s.chat.post_message('#devops', key)


    return "Backup done S3 key ==> " + str(key)


# def _getMeRestoreCmd():  
#   host = _getMeHost()
#   cmd = 'mongorestore --host ' + host + ' -d /data/backup/harpreet'


def _fetchDump(key_value):
  host = _getMeHost()
  tar_cmd = 'tar -xvf ' + '/data/'+ key_value  + ' -C /data'
  a = RunCmd()
  conn = S3Connection('AKIAJIRGIYOS2LGEDX6A','7C2dGs6rCqOqrAFGv/kBwR/YyqNY0ZXPJuky8wUl')    
  #log.info("sandeep")
  log.info(key_value)
  log.info(type(key_value))
  bucket = conn.get_bucket('mongocluster')
  key = bucket.get_key(key_value)
  #log.info("Harpreet") 
  log.info(type(key))
  log.info(key)
  key.get_contents_to_filename('/data/' + key_value)
  a.run_cmd(tar_cmd)
  

def operateOnUserCall(action):
  host = _getMeHost()
  global users
  client = pymongo.MongoClient(host, 27017)
  db = client.harpreet 
  
  #showcollections = db.users.count()
  
  users.extend( db.collection_names() )
  
  if action == 'drop':
      log.info('droping collection users')
      db.drop_collection('users')

  elif action == 'create':
      log.info('creating collection users ')
      db.create_collection('users') 
       
  #return showcollections


def _importUserData(key):
    """
    function imports  user data collections
    """
    count = 0
    host = _getMeHost()
    

    a = RunCmd()

    log.info('importing collection') 
    log.info('mongorestore -d harpreet -c users -h ' +  host + '/data/data/backup/harpreet/users.bson')
    a.run_cmd('mongorestore -d harpreet -c users -h ' +  host + ' /data/data/backup/harpreet/users.bson')


#    a.run_cmd("rm -rf /data/backup")
#    a.run_cmd("rm -rf /data/" + key) 





def restore(key):
  _fetchDump(key)
  operateOnUserCall('drop')
  _importUserData(key)
  s = slackNotification()
  s.chat.post_message('#devops', "restored", key ) 
  return "restore"










