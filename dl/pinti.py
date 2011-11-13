#!/usr/bin/env python
# encoding: utf-8

from putio import Api, PutioError
import os
import logging
log = logging.getLogger('pinti')
logging.basicConfig(filename='log/pinti.log',level=logging.INFO, format='%(asctime)-15s - %(levelname)-8s- %(message)s')

#define CLI options
from optparse import OptionParser
parser = OptionParser()
parser.add_option("-u", "--username", 
                  action="store", type="string", dest="username",
                  help="put.io USERNAME/API_KEY")
parser.add_option("-p", "--password", 
                  action="store", type="string", dest="password",
                  help="put.io PASSWORD")
parser.add_option("-k", "--key", 
                  action="store", type="string", dest="apikey",
                  help="put.io API KEY")
parser.add_option("-s", "--secret", 
                  action="store", type="string", dest="apisecret",
                  help="put.io API SECRET")
parser.add_option("-f", "--folder", 
                  action="store", type="string", dest="folder",
                  help="download folder on put.io")
parser.add_option("-c", "--cont", "--continue",
                  action="store_true", dest="continu",
                  help="continue downloading until all files are downloaded.")
parser.add_option("--keep",
                  action="store_true", dest="keep",
                  help="keeps the file on the server after successful download")

(options, args) = parser.parse_args()

#init variables to use
username = options.username
password = options.password
apikey = options.apikey
apisecret = options.apisecret
folder = options.folder
continu = options.continu
keep = options.keep
if not apikey:
    apikey = username
if not folder:
    folder = 'download'
    
# connecting your put.io with your api key and api secret
api = Api(apikey, apisecret)

# getting your items
items = api.get_items()
for it in items:
    if it.name == folder:
        dir = it
        break
        
if not dir:
    log.warning('download directory not found, creating')
    dir = api.create_folder(name=folder)

try:
    items = api.get_items(parent_id=dir.id)
except PutioError:
    items = ()

log.info('%s items to download, starting...' % len(items))
for it in items:
    if not it.is_dir:
        dl_url = it.get_download_url()
        filename = it.name
        log.info('.. downloading %s from %s ...' % (filename, dl_url))
        
        #execute wget
        cmd = 'wget --no-check-certificate --auth-no-challenge --user=%s --password=%s %s -O "%s" >> log/wget.log' % (username, password, dl_url, filename)
        #log.info("executing '%s'" % cmd)        
        success = not os.system(cmd)
        
        if success:
            log.info('.. download successfull.')
        else:
            log.info('.. download failed!')
            
        if keep:
            log.info('.. keeping file on server')
            
        #remove file from server
        if not keep and success:
            log.info('.. deleting file from server...')
            try:
                it.delete_item()
            except PutioError:
                log.error('.. cannot delete file %s' % it.name)
                break
            
        #continue downloading?
        if not continu:
            log.info('.. continue downloading with the next file')
            break
