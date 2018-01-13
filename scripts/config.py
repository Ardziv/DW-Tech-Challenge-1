# config.py
class PSQL:
    PORT = 5432
    DATABASE = 'tpch'
    DATABASE_TABLES = ['region', 'nation','part','partsupp','customer','lineitem','orders','supplier']

class DBGEN:
    LOCATION = '/srv/repo/DW-Tech-Challenge-1/TPCH/2.17.3/dbgen/dbgen'
    SCALE = '1'
    ARGS = '-s'+SCALE

