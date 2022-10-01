"""
Initiating connection to database and pulling base dependencies
"""



from mongoengine import *


#Importing Configuration File
import BudgetEngine.config as config

#Importing Data Models
from BudgetEngine.projection import *
from BudgetEngine.user import *


#getting environment variables
evars = config.Vars()

#Connect to database
register_connection(alias='default',name=evars.DBName, host=evars.MongoDBIP, port=evars.MongoDBPort)