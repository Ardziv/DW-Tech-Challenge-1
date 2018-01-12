## DW Technical Challenge 1: Fun with TPC-H - ANSWERS BY FREDERIC ALEX

1. [Environment](#markdown-header-environment)
1. [Data generation and loading](#markdown-header-data-generation-and-loading)
1. [Data verification](#markdown-header-data-verification)
1. [Ideal architecture](#markdown-header-ideal-architecture)
1. [Star schema](#markdown-header-star-schema)
1. [Extra queries](#markdown-header-extra-queries)


### Environment

I will setup a RedShift (RDS)
I have used "ansible-vault" to secure my credentials to the AWS account.

The prerequisites of my code are:
1. boto (pip install boto).
1. ansible-vault 

I have used the following Ansible code to provision my instance:


```sh
# tpch_setup.yml

- hosts: localhost
  connection: local
  gather_facts: False

  tasks:

    - name: Provision a set of instances
      ec2:
         key_name: my_key
         group: test
         instance_type: t2.micro
         image: "{{ ami_id }}"
         wait: true
         exact_count: 5
         count_tag:
            Name: Demo
         instance_tags:
            Name: Demo
      register: ec2
```

### Data generation and loading
Write a Python/Ruby/Perl script named `populate` (extension dependent on language) that will:

1. Invoke dbgen with a specfied scale to create the TPC-H input datasets.

```sh
cd 2.1
cp makefile.basis Makefile
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
