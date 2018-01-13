# config.py
class PSQL:
	PORT = 5432
	DATABASE = 'tpch'
	DATABASE_TABLES = ['region', 'nation','part','partsupp','customer','lineitem','orders','supplier']

class DBGEN:
	PATH = '/srv/dbgen'
	BIN = 'dbgen'
	ARGS = '-s '

class TBL2CSV:
	PATH = '/srv/scripts'
	BIN = 'tbl2csv.sh'
