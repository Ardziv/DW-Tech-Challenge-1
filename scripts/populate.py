# argparse
import argparse

# subprocess
import subprocess

# import config.py
from config import *

# parser of arguments on command line
parser = argparse.ArgumentParser()
#ordered arguments
parser.add_argument('scale', help="integer value to be used when invoking dbgen")
parser.add_argument('data_path', help="filesystem directory that will contain the files that qgen will generate.")
parser.add_argument('db_name', help="name of database that contains the empty TPC-H tables.")

# parse the args
args = parser.parse_args()

print(DBGEN.ARGS)
print(PSQL.DATABASE)
for i in PSQL.DATABASE_TABLES:
	print (i)
print(args)

# Ask the user for input
host = raw_input("Enter a host to ping: ")    

# Set up the echo command and direct the output to a pipe
p1 = subprocess.Popen(['ping', '-c 2', host], stdout=subprocess.PIPE)

# Run the command
output = p1.communicate()[0]

print (output)

