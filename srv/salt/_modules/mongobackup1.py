import logging
import uuid
import subprocess
import os, math
import re
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from  slacker import Slacker



log = logging.getLogger(__name__)


class RunCmd(object):
    def run_cmd(self, cmd):
        self.cmd = cmd
        subprocess.call(self.cmd, shell=True)

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


    slack = Slacker('xoxp-226792929462-225250171360-259658264771-e6ce9af604e97e3f6348de3ed037d08c')

    slack.chat.post_message('#devops', key)


    return "Backup done S3 key ==> " + str(key)






