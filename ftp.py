from ftplib import FTP
import os

class MyFTP(object):
    
    connection = None
    host = None
    port = 21
    username = None
    password = None
    target_folder = None
    files = []
    
    def __init__(self, host, port, username, password, target_folder, local_folder):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.target_folder = target_folder
        self.local_folder = local_folder
        self.connection = FTP()
    
    def login(self):
        
        self.connection.connect(host=self.host, port=self.port)
        self.connection.login(user=self.username, passwd=self.password)
    
    def get_file_list(self):
        
        self.connection.cwd(self.target_folder)
        self.files = self.connection.nlst()
    
    def download(self, filename):
        temp_filename = filename + '.downloading'
        self.connection.retrbinary('RETR {}'.format(filename), open('{}/{}'.format(self.local_folder, temp_filename), 'wb').write)
        os.rename("{}/{}".format(self.local_folder, temp_filename), 
                  "{}/{}".format(self.local_folder, filename))
    
    def quit(self):
        self.connection.quit()


if '__main__' == __name__:
    
    F = MyFTP('ftp.lax.8B79.edgecastcdn.net', 21, 'info@verican.com', 'tvc_med1a', 'TVC/test', 'videos')
    F.login()
    F.get_file_list()
    for filename in F.files:
        print("> {}".format(filename))
    
    F.download(F.files[0])
    
    F.quit()
