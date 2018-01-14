## DW Technical Challenge 1: Fun with TPC-H - ANSWERS BY FREDERIC ALEX

1. [Environment](#markdown-header-environment)
1. [Data generation and loading](#markdown-header-data-generation-and-loading)
1. [Data verification](#markdown-header-data-verification)
1. [Ideal architecture](#markdown-header-ideal-architecture)
1. [Star schema](#markdown-header-star-schema)
1. [Extra queries](#markdown-header-extra-queries)


### Environment

1- Create a EC2 T2.MICRO instance

1bis - Create a EC2 T2.MICRO instance with Ansible / Terraform / CloudFormation script with pre-configured Postgresql and Security Group

2- Open Security Group port 22 to my local public IP

3- Connect with SSH to the EC2 instance

```sh
# ssh -i <KEY.PEM> <DNS> -l root
```

4- Quick configuration of the system:

```sh
# hostname tpch
# echo tpch > /etc/hostname
# apt-get install build-essential make gcc screen vim git
# mkdir -p  /srv/repo
# ssh-keygen -t rsa
```

5- ADD OWN SSH pub key to GITHUB

6- GIT clone repo & CONFIG SYMLINK IN /srv

```sh
# cd /srv/repo
# git clone git@github.com:Ardziv/DW-Tech-Challenge-1.git
#  ln -s /srv/repo/DW-Tech-Challenge-1/scripts /srv/scripts
# ln -s /srv/repo/DW-Tech-Challenge-1/TPCH/2.17.3/dbgen /srv/dbgen
```

7- SETUP POSTGRES

```sh
# /etc/init.d/postgres start
# sudo passwd postgres
```

8- CREATE DATABASE AND TABLES

```sh
# su - postgres
postgres# createdb tpch
postgres@tpch:/srv/dbgen$ psql -f dss.ddl tpch
CREATE TABLE
CREATE TABLE
CREATE TABLE
CREATE TABLE
CREATE TABLE
CREATE TABLE
CREATE TABLE
CREATE TABLE
```


### Data generation and loading
Write a Python/Ruby/Perl script named `populate` (extension dependent on language) that will:

1. Invoke dbgen with a specfied scale to create the TPC-H input datasets.

```sh
cd /srv/dbgen
cp makefile.suite makefile
EDIT variables in makefile:
	CC      =  gcc
	DATABASE= SQLSERVER
	MACHINE = LINUX
	WORKLOAD = TPCH
make
```

1. Take those input datasets and load them to the corresponding tables in the database. Tables will have to be truncated prior to each load.
1. Fail on any error.
1. Accept these ordered arguments:
    * `scale` -- integer value to be used when invoking dbgen
    * `data_path` -- filesystem directory that will contain the files that qgen will generate. Should fail if the destination is not empty. Create if it doesn't exist.
    * `db_name` -- name of database that contains the empty TPC-H tables.
        
As an example, the following will generate data at scale 1, store them inside the directory `data` and load into the database `tpch`.

```sh
python populate.py 1 ./data tpch
```

ANSWER: all of the above has been done in the script `populate.py`.
it uses python 3.
```sh
python3 populate.py 1 /srv/data tpch
```

It get something like this as output:
```
```

### Data verification


Write a Linux shell script named `check_distribution.sh` that will compare counts between data in the source files and the target tables. The script shall:
    
1. Take these ordered arguments:
    * `data_path` -- filesystem directory where the source files from qgen are located.
    * `source_filename` -- One of the files created by dbgen (i.e. `customer.tbl` corresponds to table `CUSTOMER`).
    * `field_position` -- The nth field within `source_filename` (i.e. within `customer.tbl`, the 7th field corresponds to the `CUSTOMER.C_MKTSEGMENT` column).
    * `db_name` -- name of the database.
    * `table_name` -- The table name in the database.
    * `column_name` -- The column in `table_name`. 
    
1. In the database, get column aggregates via a query like:

```
#!sql

   select column_name, count(*)
   from table_name
   group by column_name
   order by column_name
```

1. On the filesystem, also get the same aggregates for `field_position` within `source_filename`. Hint: There are Linux commands to get this so you don't have to write your own function.
    
1. Join the counts from the database and file and tabulate. For example, we invoke this on the command line:

```
#!sh

   check_distribution.sh ./data customer.tbl 7 tpch customer c_mktsegment
```

   And we get something like this as output:
    
```
#!sh
    AUTOMOBILE 29752 29752
    BUILDING 30142 30142
    FURNITURE 29968 29968
    HOUSEHOLD 30189 30189
    MACHINERY 29949 29949
```

### Ideal architecture

Since there's a limitation on what services you can use under the free tier, please think of an ideal architecture for handling petabytes of data (end to end; all the way from data ingestion to loading it in a queryable service) and document it in your README.

### Star schema

TPC-H tables are in 3NF. Provide a second set of tables in the dimensional model and the transformational logic to populate them. We shall award points even if this item is incomplete but clearly shows the beginnings of a viable solution.

### Extra queries

Points, too, if you can provide a few more queries outside of the TPC-H set that demonstrate your understanding of the schema and its data.
