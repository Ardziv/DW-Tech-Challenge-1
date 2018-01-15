## DW Technical Challenge 1: Fun with TPC-H - ANSWERS BY FREDERIC ALEX

1. [Environment](#markdown-header-environment)
1. [Data generation and loading](#markdown-header-data-generation-and-loading)
1. [Data verification](#markdown-header-data-verification)
1. [Ideal architecture](#markdown-header-ideal-architecture)
1. [Star schema](#markdown-header-star-schema)
1. [Extra queries](#markdown-header-extra-queries)


### Environment

#### 1- Create a EC2 T2.MICRO instance
#### ANSWER: I have manually created a first instance for this challenge, using the AMI:postgresql-ubuntu-16-04-hvm-22092017-201709220907 (ami-af92b0ca) that is available from Amazon. 
After reconfiguring it, I have created a private AMI: TPCH (ami-8e2309eb)

Then i have also wrote a playbook in YAML for Ansible to be able to deploy new instance based on my template AMI:TPCH (ami-8e2309eb)

#### 1bis - Create a EC2 T2.MICRO instance with Ansible  script with pre-configured Postgresql and Security Group
I have written a ANSIBLE script and seperated the AWS access keys and secret keys into a "vars_files" (ideally with more time i would have encrypted it with ansible-vault)

On GIT Repo:
* tpch_setup.yml: https://github.com/Ardziv/DW-Tech-Challenge-1/blob/master/scripts/ansible/tpch_setup.yml
* external_vars.yml: https://github.com/Ardziv/DW-Tech-Challenge-1/blob/master/scripts/ansible/external_vars.yml

##### Prerequisite:
* Ansible 
* BOTO

```sh 
# sudo apt-get update
# sudo apt-get install software-properties-common
# sudo apt-add-repository ppa:ansible/ansible
# sudo apt-get update
# sudo apt-get install ansible

BOTO:
# sudo apt-get install python-boto
```

##### Saling out with Ansible:
You can create new instance of the TPCH (ami-8e2309eb) by using the below command:

```sh
# ansible-playbook tpch_setup.yml

```

**Note: you have to modify the two variables "ec2_access_key" and "ec2_secret_key"  in "external_vars.yml" file prior launching this command.**


#### 2- Open Security Group port 22 to my local public IP

#### 3- Connect with SSH to the EC2 instance

```sh
# ssh -i <KEY.PEM> <DNS> -l root
```

#### 4- Quick configuration of the system:

```sh
# hostname tpch
# echo tpch > /etc/hostname
# apt-get install build-essential make gcc screen vim git
# mkdir -p  /srv/repo
# ssh-keygen -t rsa
```

#### 5- ADD OWN SSH pub key to GITHUB

#### 6- GIT clone repo & CONFIG SYMLINK IN /srv

```sh
# cd /srv/repo
# git clone git@github.com:Ardziv/DW-Tech-Challenge-1.git
# ln -s /srv/repo/DW-Tech-Challenge-1/scripts /srv/scripts
# ln -s /srv/repo/DW-Tech-Challenge-1/TPCH/2.17.3/dbgen /srv/dbgen
```

#### 7- SETUP POSTGRES

```sh
# apt-get install postgresql-9.3 postgresql-client-9.3 
# /etc/init.d/postgres start
# sudo passwd postgres
```

#### 8- CREATE DATABASE AND TABLES

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

First we build the tool dbgen that ships with TPCH

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
	* **ANSWER: the "tbl" files are generated by default on the same path as the dbgen binary. I will first transform them into CSV files, and then use psql binary to load them.**
	* **When reloading multiple times, i will use "drop_constraints.sql" and "truncate.sql" files described below, to clear the existing data.**
	* **I assume as well that the schema is pre-loaded into the database with empty data and no constraints (for the first load).**
1. Fail on any error.
	* **ANSWER: I use the logic "try ... except" in my code to catch any errors thrown by the underlying subprocess i am calling.**
1. Accept these ordered arguments:
    * `scale` -- integer value to be used when invoking dbgen
    * `data_path` -- filesystem directory that will contain the files that qgen will generate. Should fail if the destination is not empty. Create if it doesn't exist.
    * `db_name` -- name of database that contains the empty TPC-H tables.
	* **ANSWER: I use the module "argparse" and some extra checking functions to make sure that the arguments are existing and are of the proper type (scale: int, data_path: existing directory). I raise an error otherwise.**
        
As an example, the following will generate data at scale 1, store them inside the directory `data` and load into the database `tpch`.

```sh
python populate.py 1 ./data tpch
```

# ANSWER: all of the above has been done in the script `populate.py`.
it uses python 3.
```sh
python3 populate.py 1 /srv/data tpch
```

It has a helper for usage:
```
root@tpch:/srv/scripts# python3 populate.py -h
usage: populate.py [-h] scale data_path db_name

positional arguments:
  scale       integer value to be used when invoking dbgen
  data_path   filesystem directory that will contain the files that qgen will
              generate.
  db_name     name of database that contains the empty TPC-H tables.

optional arguments:
  -h, --help  show this help message and exit
```

It has to have the ordered args otherwise it is failing:
```sh
root@tpch:/srv/scripts# python3 populate.py
usage: populate.py [-h] scale data_path db_name
populate.py: error: the following arguments are required: scale, data_path, db_name
```

It get something like this as output:
```sh
root@tpch:/srv/scripts# python3 populate.py 1 /srv/data tpch
TPC-H Population Generator (Version 2.17.3)
Copyright Transaction Processing Performance Council 1994 - 2010
Generating data for suppliers table/
Preloading text ... 100%
done.
Generating data for customers tabledone.
Generating data for orders/lineitem tablesdone.
Generating data for part/partsupplier tablesdone.
Generating data for nation tabledone.
Generating data for region tabledone.

runTbl2Csv(/srv/dbgen,/srv/data): START
Converting file /srv/dbgen/customer.tbl
Converting file /srv/dbgen/lineitem.tbl
Converting file /srv/dbgen/nation.tbl
Converting file /srv/dbgen/orders.tbl
Converting file /srv/dbgen/part.tbl
Converting file /srv/dbgen/partsupp.tbl
Converting file /srv/dbgen/region.tbl
Converting file /srv/dbgen/supplier.tbl

runTbl2Csv(/srv/dbgen,/srv/data): END
runDropConstraints(tpch): START
CompletedProcess(args=['sudo -u postgres psql -f /srv/scripts/drop_constraints.sql tpch'], returncode=0, stdout='ALTER TABLE\nALTER TABLE\nALTER TABLE\nALTER TABLE\nALTER TABLE\nALTER TABLE\nALTER TABLE\nALTER TABLE\nALTER TABLE\nALTER TABLE\nALTER TABLE\nALTER TABLE\nALTER TABLE\nALTER TABLE\nALTER TABLE\nALTER TABLE\n')
runDropConstraints(tpch): END
runTruncate(tpch): START
CompletedProcess(args=['sudo -u postgres psql -f /srv/scripts/truncate.sql tpch'], returncode=0, stdout='TRUNCATE TABLE\n count \n-------\n     0\n(1 row)\n\nTRUNCATE TABLE\n count \n-------\n     0\n(1 row)\n\nTRUNCATE TABLE\n count \n-------\n     0\n(1 row)\n\nTRUNCATE TABLE\n count \n-------\n     0\n(1 row)\n\nTRUNCATE TABLE\n count \n-------\n     0\n(1 row)\n\nTRUNCATE TABLE\n count \n-------\n     0\n(1 row)\n\nTRUNCATE TABLE\n count \n-------\n     0\n(1 row)\n\nTRUNCATE TABLE\n count \n-------\n     0\n(1 row)\n\n')
runTruncate(tpch): END
runLoad(/srv/data,tpch): START
CompletedProcess(args=['sudo -u postgres psql -f /srv/scripts/load.sql tpch'], returncode=0, stdout='COPY 5\nCOPY 25\nCOPY 200000\nCOPY 10000\nCOPY 800000\nCOPY 1500000\nCOPY 6001215\nCOPY 150000\n')
runLoad(/srv/data,tpch): END
runAddConstraints(tpch): START
sudo -u postgres psql -f /srv/scripts/add_constraints.sql tpch
CompletedProcess(args=['sudo -u postgres psql -f /srv/scripts/add_constraints.sql tpch'], returncode=0, stdout='ALTER TABLE\nALTER TABLE\nALTER TABLE\nALTER TABLE\nALTER TABLE\nALTER TABLE\nALTER TABLE\nALTER TABLE\nALTER TABLE\nALTER TABLE\nALTER TABLE\nALTER TABLE\nALTER TABLE\nALTER TABLE\nALTER TABLE\nALTER TABLE\n')
runAddConstraints(tpch): END
```

More details on what I have done are show here below:

#### 9- CREATE CSV FROM TBL FILES

```sh
# /srv/scripts/tbl2csv.sh /srv/dbgen /srv/data
```

#### 10- LOAD CSV FILES

```sh
 postgres@tpch:/srv/scripts$ psql -f load.sql tpch
COPY 25
COPY 5
COPY 200000
COPY 10000
COPY 800000
COPY 150000
COPY 1500000
COPY 6001215
```

#### 11- MODIFY AND APPLY CONSTRAINT SCRIPT DSS.RI AND SAVE IT AS /srv/scripts/apply_constraints.sql

```sh
# cp /srv/dbgen/dss.ri /srv/scripts/apply_constraints.sql
# vim /srv/scripts/apply_constraints.sql
```

Modify the constraint script /srv/scripts/apply_constraints.sql:

1. Remove "CONNECT TO TPCD;"
1. remove the object before the "TPCD."
1. remove the foreign key name
1. remove the "COMMIT WORK;"

```sh
# su - postgres
# psql -f /srv/scripts/apply_constraints.sql tpch

postgres@tpch:/srv/dbgen$ psql -f /srv/scripts/apply_constraints.sql tpch
ALTER TABLE
ALTER TABLE
ALTER TABLE
ALTER TABLE
ALTER TABLE
ALTER TABLE
ALTER TABLE
ALTER TABLE
ALTER TABLE
ALTER TABLE
ALTER TABLE
ALTER TABLE
ALTER TABLE
ALTER TABLE
ALTER TABLE
ALTER TABLE 
```
 

#### 12- DROP CONSTRAINTS AND TRUNCATE TABLE PRIOR RELOAD

```sql
root@tpch:/srv/scripts# cat drop_constraints.sql

drop_constraints.sql:
--------------------

-- FOREIGN KEYS
ALTER TABLE NATION DROP CONSTRAINT nation_n_regionkey_fkey;
ALTER TABLE SUPPLIER DROP CONSTRAINT supplier_s_nationkey_fkey;
ALTER TABLE CUSTOMER DROP CONSTRAINT customer_c_nationkey_fkey;
ALTER TABLE PARTSUPP DROP CONSTRAINT partsupp_ps_suppkey_fkey;
ALTER TABLE PARTSUPP DROP CONSTRAINT partsupp_ps_partkey_fkey;
ALTER TABLE ORDERS DROP CONSTRAINT orders_o_custkey_fkey;
ALTER TABLE LINEITEM DROP CONSTRAINT lineitem_l_orderkey_fkey;
ALTER TABLE LINEITEM DROP CONSTRAINT lineitem_l_partkey_fkey;

-- PRIMARY KEYS
ALTER TABLE REGION DROP CONSTRAINT REGION_PKEY CASCADE;
ALTER TABLE NATION DROP CONSTRAINT NATION_PKEY CASCADE;
ALTER TABLE PART DROP CONSTRAINT PART_PKEY CASCADE;
ALTER TABLE SUPPLIER DROP CONSTRAINT SUPPLIER_PKEY CASCADE;
ALTER TABLE PARTSUPP DROP CONSTRAINT PARTSUPP_PKEY CASCADE;
ALTER TABLE ORDERS DROP CONSTRAINT ORDERS_PKEY CASCADE;
ALTER TABLE LINEITEM DROP CONSTRAINT LINEITEM_PKEY CASCADE;
ALTER TABLE CUSTOMER DROP CONSTRAINT CUSTOMER_PKEY CASCADE;

truncate.sql:
------------

TRUNCATE TABLE CUSTOMER CASCADE;
SELECT COUNT(*) FROM CUSTOMER;
TRUNCATE TABLE LINEITEM CASCADE;
SELECT COUNT(*) FROM LINEITEM;
TRUNCATE TABLE NATION CASCADE;
SELECT COUNT(*) FROM NATION;
TRUNCATE TABLE ORDERS CASCADE;
SELECT COUNT(*) FROM ORDERS;
TRUNCATE TABLE PART CASCADE;
SELECT COUNT(*) FROM PART;
TRUNCATE TABLE PARTSUPP CASCADE;
SELECT COUNT(*) FROM PARTSUPP;
TRUNCATE TABLE REGION CASCADE;
SELECT COUNT(*) FROM REGION;
TRUNCATE TABLE SUPPLIER CASCADE;
SELECT COUNT(*) FROM SUPPLIER;

```
 

#### 13- RELOAD ALGORITHM

Main algo for the populate.py script is as per below:

```sh
dbgen -s 1
tbl2csv.sh /srv/dbgen /srv/data
psql -f drop_constraints.sql tpch
psql -f truncate.sql tpch
psql -f load.sql  tpch
psql -f add_contraints.sql tpch
```

#### 14- Create populate.py script

On GIT repo:

https://github.com/Ardziv/DW-Tech-Challenge-1/blob/master/scripts/populate.py

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
#### ANSWER: all of the above has been done and the script output is as per below:

```sh
root@tpch:/srv/scripts# ./check_distribution.sh /srv/dbgen customer.tbl 7 tpch customer c_mktsegment
AUTOMOBILE 29752 29752
BUILDING 30142 30142
FURNITURE 29968 29968
HOUSEHOLD 30189 30189
MACHINERY 29949 29949
```
On GIT repo:

https://github.com/Ardziv/DW-Tech-Challenge-1/blob/master/scripts/check_distribution.sh

### Ideal architecture

Since there's a limitation on what services you can use under the free tier, please think of an ideal architecture for handling petabytes of data (end to end; all the way from data ingestion to loading it in a queryable service) and document it in your README.

#### ANSWER: I will propose here two possible "Ideal scenarios" with their respective architecture.
The Ideal architecture shall have the following key components to be solid and scalable:
1. ETL stack
1. Big Data / Large Storage / Data Warehouse
1. Query language
1. Visualization tool easily accesible

##### Scenario 1: Full AWS Stack (pros: well integrated with AWS, cons: vendor lockdown with ONLY AWS, difficult to move to other Cloud providers)
1. ETL stack
	* AWS GLUE:  AWS Glue is a fully managed ETL (extract, transform, and load) service that makes it simple and cost-effective to categorize your data, clean it, enrich it, and move it reliably between various data stores. 
1. Big Data / Large Storage / Data Warehouse
	* Amazon S3: to store the raw data into S3 buckets. these buckets can then be send through AWS GLUE to Kinetics Analytics for analysis
1. Query language
	* AWS ATHENA: query language to search on processed data stored on S3.
1. Visualization tool easily accesible
	* AWS QuickSight: Dashboard / reporting and visualization tool

##### Scenario 2: Full OpenSource Stack (pros: freedom to run anywhere, cons: N/A)
1. Real Time Data Feed
	* Apache KAFKA
	* LogStach
1. ETL stack

1. Big Data / Large Storage / Data Warehouse
	* Apache Hadoop
	* Apache Cassandra
	* Apache Hive
	* ELK
1. Query language
	* Apache Hive
	* Elastic Search
	* R
	* Python
	* Scala
1. Visualization tool easily accesible
	* QlickView: 
	* Tableau
	* Kibana

### Star schema

TPC-H tables are in 3NF. Provide a second set of tables in the dimensional model and the transformational logic to populate them. We shall award points even if this item is incomplete but clearly shows the beginnings of a viable solution.

#### ANSWER: based on the existing dimensions and facts tables available, and after looking at their data, i would suggest to develop a few more dimensions to help the business:
- Dimension: "promotion / fidelity": a dimension to track and analyse the behavior of the customer. it can be populated with following information:
	* customer_bought_this_alraedy: yes/no
	* does the customer buy more because product has more discount?
	* which supplier has a small discount? 
	* what is the average time betwen two orders from same customer?
- Dimension: "bestseller": a fact/dimension to track the most selled item and what changed
	* which product has higher unit sold?
	* how much net profit / net margins every month?
	* did we do some campaign to sell more of this product?
- Dimension: "bestprofit": a fact/dimension to track the proucts generating the most profit 
	* which product has higher margins?
	* how many of them are sold every month?
	* did we do some campaign to sell more of this product?
### Extra queries

Points, too, if you can provide a few more queries outside of the TPC-H set that demonstrate your understanding of the schema and its data.

#### ANSWER: I noticed during the compilation of the TPCH dbgen binary that there were as well a too called "qgen" which seems to stands for "query generator".
I have wrote a script to generate the template queries provided with the TPCH toolkit.
The results queries are available on GIT repo in the folder .../dbgen/finals/1.sql - 22.sql

```sh
root@tpch:/srv/dbgen# ls finals/
1.sql  10.sql  11.sql  12.sql  13.sql  14.sql  15.sql  16.sql  17.sql  18.sql  19.sql  2.sql  20.sql  21.sql  22.sql  3.sql  4.sql  5.sql  6.sql  7.sql  8.sql  9.sql
```

On GIT repo:
Reports Generated with QGEN:
https://github.com/Ardziv/DW-Tech-Challenge-1/tree/master/TPCH/2.17.3/dbgen/finals

Script to generate the reports:
https://github.com/Ardziv/DW-Tech-Challenge-1/blob/master/TPCH/2.17.3/dbgen/gen_query_sql.sh
