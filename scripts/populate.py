# argparse
import argparse

# subprocess
import subprocess

# import config.py
from config import *

### ARGS ###
# parser of arguments on command line
parser = argparse.ArgumentParser()
#ordered arguments
parser.add_argument('scale', help="integer value to be used when invoking dbgen")
parser.add_argument('data_path', help="filesystem directory that will contain the files that qgen will generate.")
parser.add_argument('db_name', help="name of database that contains the empty TPC-H tables.")

# parse the args
args = parser.parse_args()
### ARGS ###


### MAIN ###
def __main__():
	# DEBUG
	print(DBGEN.ARGS)
	print(PSQL.DATABASE)
	for i in PSQL.DATABASE_TABLES:
		print (i)
	print(args)
	# DEBUG
### MAIN ###

### DBGEN ###
# desc: function to execute the DBGEN program with the args passed
# return: output of the STDOUT from the proess
def runDbgen():
	print('runDbgen')
### DBGEN ###

### LIST FILES ###
# desc: function to list the generated TBL files
# return: array/list of files
def getDbgenFiles():
	print('getDbgenFiles')
### LIST FILES ###

### TRUNCATE  TABLE ###
def truncateTable(database,table):
	print('getDbgenFiles')
### LIST FILES ###
### TRUNCATE  TABLE ###

# EXAMPLE OF SUBPROCESS
# Ask the user for input
#host = raw_input("Enter a host to ping: ")    
#host = 'localhost'

# Set up the echo command and direct the output to a pipe
#p1 = subprocess.Popen(['ping', '-c 2', host], stdout=subprocess.PIPE)

# Run the command
#output = p1.communicate()[0]

#print (output)
# EXAMPLE OF SUBPROCESS

__main__()
