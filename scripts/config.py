# config.py
class PSQL:
	PORT = 5432
	DATABASE = 'tpch'
	DATABASE_TABLES = ['region', 'nation','part','partsupp','customer','lineitem','orders','supplier']
	USER = 'postgres'
	BIN = 'psql'

class DBGEN:
	PATH = '/srv/dbgen'
	BIN = 'dbgen'
	ARGS = '-s '

class TBL2CSV:
	PATH = '/srv/scripts'
	BIN = 'tbl2csv.sh'

class TRUNCATE:
	PATH = '/srv/scripts'
	BIN = 'truncate.sql'

class LOAD:
	PATH = '/srv/scripts'
	BIN = 'load.sql'

class CONSTRAINT:
	PATH = '/srv/scripts'
	BIN_ADD = 'add_constraints.sql'
	BIN_DROP = 'drop_constraints.sql'

