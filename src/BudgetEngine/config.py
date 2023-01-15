import os

while os.path.exists('config.json') == False:
    path_parent = os.path.dirname(os.getcwd())
    os.chdir(path_parent)


class Vars:
    
    def __init__(self):
        filename = 'config.json'
        contents = open(filename).read()
        config = eval(contents)
        self.MongoDBIP = config['MongoDBIP']
        self.MongoDBPort = config['MongoDBPort']
        self.HostExternalIP = config['HostExternalIP']
        self.DBName = config['DBName']
        self.demo_mode = config['demo_mode']
