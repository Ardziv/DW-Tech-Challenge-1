## DW Technical Challenge 1: Fun with TPC-H

TPC-H (http://www.tpc.org/information/current_specifications.asp) is considered the industry standard when benchmarking decision support systems. It consists of a well defined schema, a data population generator and updater, and various queries that, taken together, are a good representation of a common DSS environment.

For this challenge, we'd like for you to provide us with a throwaway AWS account that contains a running instance of a TPC-H database along with mechanisms to generate and load the data and run queries on them. We will score the challenge based on these deliverables:

1. [Environment](#markdown-header-environment)
1. [Data generation and loading](#markdown-header-data-generation-and-loading)
1. [Data verification](#markdown-header-data-verification)
1. [Ideal architecture](#markdown-header-ideal-architecture)
1. [Star schema](#markdown-header-star-schema)
1. [Extra queries](#markdown-header-extra-queries)

Please provide a `README` to describe what you've done, your reasoning and any instructions you want to provide. You may wish to provide us with IAM credentials (with billing turned off) in a separate channel.


### Environment

Your TPC-H database could be as simple as PostgreSQL hosted on an EC2 instance to RDS. Please describe how you set up your environment in your README. Bonus points if you use IaC tools such as Terraform or Ansible.

### Data generation and loading

Write a Python/Ruby/Perl script named `populate` (extension dependent on language) that will:

1. Invoke dbgen with a specfied scale to create the TPC-H input datasets.
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

If your script needs to connect to a remote database, it is up to you on how you'll connect to it and how to pass the credentials.

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
