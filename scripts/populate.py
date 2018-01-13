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

def change_attribute(obj, attribute, value): 
	obj.__dict__[attribute] = value

### MAIN ###
def __main__():
	# DEBUG
	#print(DBGEN.ARGS)
	#print(PSQL.DATABASE)
	#for i in PSQL.DATABASE_TABLES:
	#	print (i)
	print(args)
	# DEBUG

	# execute DBGEN with the scale
	#runDbgen(args.scale)

	# execute TBL2CSV 
	runTbl2Csv(DBGEN.PATH,args.data_path)

	
### MAIN ###

### DBGEN ###
# desc: function to execute the DBGEN program with the args passed
# return: output of the STDOUT from the proess
def runDbgen(scale):
	print('runDbgen(): START')

	# create a new object instance of the DBGEN class
	dbgen1 = DBGEN()
	# set the dbgen.ARGS to the value provided
	dbgen1.ARGS += scale
	# set the command 
	command = dbgen1.PATH+"/"+dbgen1.BIN

	# Set up the echo command and direct the output to a pipe
	# subprocess.Popen(args, bufsize=-1, executable=None, stdin=None, stdout=None, stderr=None, preexec_fn=None, close_fds=True, shell=False, cwd=None, env=None, universal_newlines=False, startupinfo=None, creationflags=0, restore_signals=True, start_new_session=False, pass_fds=(), *, encoding=None, errors=None)
	p1 = subprocess.Popen([command, "-vf", dbgen1.ARGS], stdout=subprocess.PIPE, cwd=dbgen1.PATH)
	# Run the command
	output = p1.communicate()[0]

	# subprocess.run(args, *, stdin=None, input=None, stdout=None, stderr=None, shell=False, cwd=None, timeout=None, check=False, encoding=None, errors=None)
	#output = subprocess.run([dbgen1.LOCATION, dbgen1.ARGS], stdout=subprocess.PIPE, cwd="/srv/repo/DW-Tech-Challenge-1/TPCH/2.17.3/dbgen/")

	print (output)
	print('runDbgen(): END')
	
### DBGEN ###

### TBL2CSV ###
# desc: function to transform TBL files to CSV file to be ready to load them into POSTGRES DB
# return: list of files
def runTbl2Csv(src,dst):
	print('runTbl2Csv(): START')
	# create a new object instance of the TBL2CSV class
	tbl2csv1 = TBL2CSV()
	# set the command 
	command = tbl2csv1.PATH+"/"+tbl2csv1.BIN

	# Set up the echo command and direct the output to a pipe
	# subprocess.Popen(args, bufsize=-1, executable=None, stdin=None, stdout=None, stderr=None, preexec_fn=None, close_fds=True, shell=False, cwd=None, env=None, universal_newlines=False, startupinfo=None, creationflags=0, restore_signals=True, start_new_session=False, pass_fds=(), *, encoding=None, errors=None)
	p1 = subprocess.Popen([command, src, dst], stdout=subprocess.PIPE, cwd=tbl2csv1.PATH)
	# Run the command
	output = p1.communicate()[0]
	
	print (output)
	print('runTbl2Csv(): END')
	
### TBL2CSV ###

### runRemoveConstraint(database) ###
# desc: function to remove constraints
# return: none
def runRemoveConstraint(database):
	print('runRemoveConstraint(): START')
	print('runRemoveConstraint(): END')
### runRemoveConstraint(database) ###

### runTruncate(database) ###
# desc: function to remove constraints
# return: none
def runTruncate(database):
	print('runTruncate(): START')
	print('runTruncate(): END')
### runTruncate(database) ###

### runLoad(database) ###
# desc: function to remove constraints
# return: none
def runLoad(database):
	print('runLoad(): START')
	print('runLoad(): END')
### runLoad(database) ###

### runAddConstraint(database) ###
# desc: function to remove constraints
# return: none
def runAddConstraint(database):
	print('runAddConstraint(): START')
	print('runAddConstraint(): END')
### runAddConstraint(database) ###

#### ADVANCED  / EXTRA FUNCTIONS ####

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
