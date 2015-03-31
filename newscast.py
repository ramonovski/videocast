import json
from ftp import MyFTP
from glob import glob
import os
import sys
import time


def read_config(config_file):
    return json.load(open(config_file, 'r'))


def sync_files(config):
    
    F = MyFTP(config['server'], config['port'], 
              config['username'], config['password'], 
              config['server_folder'], config['local_folder'])
    F.login()
    F.get_file_list()
    
    local_files = []
    local_list = glob("{}/*".format(config['local_folder']))
    
    prefix_length = len(config['local_folder']) + 1
    
    for local_file in local_list:
        filename = local_file[prefix_length:]
        local_files.append(filename)
    
    remote_files = F.files
    
    #for filename in F.files:
    #    print("> {}".format(filename))
    
    delete_list = []
    download_list = []
    
    for filename in set(local_files) ^ set(remote_files):
        if filename in local_files and filename not in remote_files:
            delete_list.append(filename)
        elif filename in remote_files  and filename not in local_files:
            download_list.append(filename)
        
    #print(delete_list)
    #print(download_list)
    
    if len(delete_list) > 0 or len(download_list) > 0:
        os.system("touch /tmp/reload_videocast")
        
    for filename in delete_list:
        os.unlink("{}/{}".format(config['local_folder'], filename))
        print("Deleted local file: {}".format(filename))
    
    for filename in download_list:
        print("Downloading remote file: {}".format(filename))
        F.download(filename)
        
    #F.download(F.files[0])
    
    F.quit()

if '__main__' == __name__:
    
    config = read_config('config.json')
    #print(config)
    
    while True:
        try:
            sync_files(config)
            #time.sleep(20)
            time.sleep(720*60)   # 12 hours
            #time.sleep(30*60)   # 30 mintues
        except (KeyboardInterrupt, SystemExit) as exp:
            print("Good bye!")
            sys.exit()
        except Exception as exp:
            print("Error: " + str(exp))
