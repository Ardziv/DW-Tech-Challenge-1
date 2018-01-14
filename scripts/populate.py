# os, stat , errno
import os, stat, errno
# argparse
import argparse
# subprocess
import subprocess
import shlex

# import config.py
from config import *

### ARGS ###
def intNotNull(string):
	try:
		val = int(string)
		if val > 0:
			return string
		else:
			msg = "%r can't be null, zero or negative, try again" % string
			raise argparse.ArgumentTypeError(msg)
	except ValueError:
		msg = "ERROR: %r  - scale must be a number, try again" % string
		print(msg)

def CheckIsDir(directory):
	try:
		return stat.S_ISDIR(os.stat(directory).st_mode)
	except OSError as e:
		if e.errno == errno.ENOENT:
			return False
		raise

def dirExists(string):
	try:
		if CheckIsDir(string):
			return string
		else:
			msg = "%r doesn't exists" % string
			raise argparse.ArgumentTypeError(msg)
	except ValueError:
		msg = "ERROR: %r  - data_path must be a valid directory, try again" % string
		print(msg)

# parser of arguments on command line
parser = argparse.ArgumentParser()
#ordered arguments
parser.add_argument('scale', type=intNotNull, help="integer value to be used when invoking dbgen")
parser.add_argument('data_path', type=dirExists, help="filesystem directory that will contain the files that qgen will generate.")
parser.add_argument('db_name', help="name of database that contains the empty TPC-H tables.")

# parse the args
args = parser.parse_args()
### ARGS ###

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
	#runTbl2Csv(DBGEN.PATH,args.data_path)

	# execute runDropConstraints 
	runDropConstraints(args.db_name)

	# execute runTruncate 
	runTruncate(args.db_name)

	# execute runLoad 
	runLoad(args.data_path, args.db_name)

	# execute runAddConstraints 
	runAddConstraints(args.db_name)

### MAIN ###

### DBGEN ###
# desc: function to execute the DBGEN program with the args passed
# return: output of the STDOUT from the proess
def runDbgen(scale):
	print('runDbgen('+scale+'): START')

	# create a new object instance of the DBGEN class
	dbgen1 = DBGEN()
	# set the dbgen.ARGS to the value provided
	dbgen1.ARGS += scale
	# set the command 
	command = dbgen1.PATH+"/"+dbgen1.BIN+" -v -f "+dbgen1.ARGS
	command = shlex.split(command)

	# subprocess.check_output(args, *, stdin=None, stderr=None, shell=False, cwd=None, encoding=None, errors=None, universal_newlines=False, timeout=None)
	try:
		output = subprocess.check_output(command, cwd=dbgen1.PATH)
		success = True
	except subprocess.CalledProcessError as e:
		print('Handling run-time error:', e)
		success = False
		raise e

	print('runDbgen('+scale+'): END')
	
### DBGEN ###

### TBL2CSV ###
# desc: function to transform TBL files to CSV file to be ready to load them into POSTGRES DB
# return: list of files
def runTbl2Csv(src,dst):
	print('runTbl2Csv('+src+','+dst+'): START')
	# create a new object instance of the TBL2CSV class
	tbl2csv1 = TBL2CSV()
	# set the command 
	command = tbl2csv1.PATH+"/"+tbl2csv1.BIN+" "+src+" "+dst
	command = shlex.split(command)

	# subprocess.check_output(args, *, stdin=None, stderr=None, shell=False, cwd=None, encoding=None, errors=None, universal_newlines=False, timeout=None)
	try:
		output = subprocess.check_output(command, cwd=tbl2csv1.PATH,universal_newlines=True)
		print(output)
		success = True
	except subprocess.CalledProcessError as e:
		print('Handling run-time error:', e)
		success = False
		raise e

	print('runTbl2Csv('+src+','+dst+'): END')
	
### TBL2CSV ###

### runDropConstraints(database) ###
# desc: function to remove constraints
# return: none
def runDropConstraints(database):
	print('runDropConstraints('+database+'): START')
	# create a new object instance of the PSQL class
	psql1 = PSQL()
	# create a new object instance of the CONSTRAINT class
	constraint1 = CONSTRAINT()
	# set the command 
	command = "sudo -u "+psql1.USER+" "+psql1.BIN+" -f "+constraint1.PATH+"/"+constraint1.BIN_DROP+" "+database

	# subprocess.run(args, *, stdin=None, input=None, stdout=None, stderr=None, shell=False, cwd=None, timeout=None, check=False, encoding=None, errors=None)
	try:
		output = subprocess.run([command], stdout=subprocess.PIPE, cwd=constraint1.PATH,universal_newlines=True, shell=True)
		print (output)
		success = True
	except subprocess.CalledProcessError as e:
		print('Handling run-time error:', e)
		success = False
		raise e

	print('runDropConstraints('+database+'): END')
### runDropConstraints(database) ###

### runTruncate(database) ###
# desc: function to remove constraints
# return: none
def runTruncate(database):
	print('runTruncate('+database+'): START')
	# create a new object instance of the PSQL class
	psql1 = PSQL()
	# create a new object instance of the LOAD class
	truncate1 = TRUNCATE()
	# set the command 
	command = "sudo -u "+psql1.USER+" "+psql1.BIN+" -f "+truncate1.PATH+"/"+truncate1.BIN+" "+database

	# subprocess.run(args, *, stdin=None, input=None, stdout=None, stderr=None, shell=False, cwd=None, timeout=None, check=False, encoding=None, errors=None)
	try:
		output = subprocess.run([command], stdout=subprocess.PIPE, cwd=truncate1.PATH,universal_newlines=True, shell=True)
		print (output)
		success = True
	except subprocess.CalledProcessError as e:
		print('Handling run-time error:', e)
		success = False
		raise e

	print('runTruncate('+database+'): END')
### runTruncate(database) ###

### runLoad(data_path,database) ###
# desc: function to Load CSV files from data_path  to database
# return: none
def runLoad(data_path,database):
	print('runLoad('+data_path+','+database+'): START')
	# create a new object instance of the PSQL class
	psql1 = PSQL()
	# create a new object instance of the LOAD class
	load1 = LOAD()
	# set the command 
	command = "sudo -u "+psql1.USER+" "+psql1.BIN+" -f "+load1.PATH+"/"+load1.BIN+" "+database

	# subprocess.run(args, *, stdin=None, input=None, stdout=None, stderr=None, shell=False, cwd=None, timeout=None, check=False, encoding=None, errors=None)
	try:
		output = subprocess.run([command], stdout=subprocess.PIPE, cwd=load1.PATH,universal_newlines=True, shell=True)
		print (output)
		success = True
	except subprocess.CalledProcessError as e:
		print('Handling run-time error:', e)
		success = False
		raise e

	print('runLoad('+data_path+','+database+'): END')
### runLoad(database) ###

### runAddConstraints(database) ###
# desc: function to remove constraints
# return: none
def runAddConstraints(database):
	print('runAddConstraints('+database+'): START')
	# create a new object instance of the PSQL class
	psql1 = PSQL()
	# create a new object instance of the CONSTRAINT class
	constraint1 = CONSTRAINT()
	# set the command 
	command = "sudo -u "+psql1.USER+" "+psql1.BIN+" -f "+constraint1.PATH+"/"+constraint1.BIN_ADD+" "+database
	print(command)
	# subprocess.run(args, *, stdin=None, input=None, stdout=None, stderr=None, shell=False, cwd=None, timeout=None, check=False, encoding=None, errors=None)
	try:
		output = subprocess.run([command], stdout=subprocess.PIPE, cwd=constraint1.PATH,universal_newlines=True, shell=True)
		print (output)
		success = True
	except subprocess.CalledProcessError as e:
		print('Handling run-time error:', e)
		success = False
		raise e

	print('runAddConstraints('+database+'): END')
### runAddConstraints(database) ###

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
