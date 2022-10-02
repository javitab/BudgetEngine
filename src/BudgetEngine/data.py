"""
Initiating connection to database and pulling base dependencies
"""

from mongoengine import *


#Importing Configuration File
from . import config


#Importing Data Models
from . import projection
from . import user


#getting environment variables
evars = config.Vars()

#Connect to database
register_connection(alias='default',name=evars.DBName, host=evars.MongoDBIP, port=evars.MongoDBPort)