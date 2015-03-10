import json
from glob import glob
import os
import sys
import time

def read_config(config_file):
    return json.load(open(config_file, 'r'))


def get_playlist(config):

    local_files = []
    files = glob("{}/*".format(config['local_folder']))
    for filename in files:
        if not filename.endswith('.downloading'):
            local_files.append(filename)
    
    return local_files

def play_video(filename):
    
    cmd = 'omxplayer -b -r "{}"'.format(filename)
    os.system(cmd)


if '__main__' == __name__:
    
    config = read_config('config.json')
    local_files = get_playlist(config)
    
    while True:
        try:
            while 0 == len(local_files):
                time.sleep(10)
                local_files = get_playlist(config)
            
            for local_file in local_files:
                print("Playing " + local_file)
                play_video(local_file)
                time.sleep(1)
                if os.path.exists('/tmp/reload_videocast'):
                    local_files = get_playlist(config)
                    os.unlink('/tmp/reload_videocast')
                    break
            
        except (KeyboardInterrupt, SystemExit) as exp:
            print("Good bye!")
            sys.exit()
        except:
            print("Error: " + str(exp))
