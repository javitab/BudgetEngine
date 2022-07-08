"""Declaring variables"""

#Declaring Variables - fill in any variables as neccessary

def config_read():
    filename = 'config.json'
    contents = open(filename).read()
    config = eval(contents)
    MongoDBIP = config['MongoDBIP']
    MongoDBPort = config['MongoDBPort']
    HostExternalIP = config['HostExternalIP']

if __name__ == "__main__":
    config_read()