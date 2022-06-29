"""Declaring variables"""

#Declaring Variables - fill in any variables as neccessary

def envVars(var):
    """Function to pull in variables for application configuration"""
    if var=='MongoDBIP': varOut='localhost'
    if var=='HostExternalIP': varOut='127.0.0.1'
    if var=='PlaidClientID': varOut=''
    if var=='PlaidSecret': varOut=''
    return varOut
