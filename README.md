## DW Technical Challenge 1: Fun with TPC-H

TPC-H (http://www.tpc.org/information/current_specifications.asp) is considered the industry standard when benchmarking decision support systems. It consists of a well defined schema, a data population generator and updater, and various queries that, taken together, are a good representation of a common DSS environment.

For this challenge, we’d like for you to provide us with a VirtualBox image that contains a runnable instance of a TPC-H database along with mechanisms to generate and load the data and run queries on them. We will score the challenge based on these deliverables:

1. [Environment](environment)
1. [Data generation and loading](data-generation-and-loading)
1. [Data verification](data-verification)
1. [Star schema](star-schema)
1. [Extra queries](extra-queries)

Please provide a `README` that will let us know where the different components are and how to run them. 

We shall provide you with a Dropbox link to upload the virtual machine image or if you have an AWS account handy, do give us a link to an S3 bucket to download it from. 


### Environment

Prepare a Linux instance exported as a VirtualBox appliance. Maximum image size should be under 1.5 GB. The instance should also contain a PostgreSQL database that contains empty TPC-H tables.

### Data generation and loading

Write a Python/Ruby/Perl script named `populate` (extension dependent on language) that will:

1. Invoke dbgen with a specfied scale to create the TPC-H input datasets.
1. Take those input datasets and load them to the corresponding tables in the Pg database. Tables will have to be truncated prior to each load.
1. Fail on any error.
1. Accept these ordered arguments:
    * `scale` -- integer value to be used when invoking dbgen
    * `data_path` -- filesystem directory that will contain the files that qgen will generate. Should fail if the destination is not empty. Create if it doesn't exist.
    * `db_name` -- name of Pg database that contains the empty TPC-H tables. 
        
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
    * `db_name` -- name of the Pg database.
    * `table_name` -- The table name in the database.
    * `column_name` -- The column in `table_name`. 
    
1. In the database, get column aggregates via a query like:
    ```sql
    select column_name, count(*)
    from table_name
    group by column_name
    order by column_name
    ```

1. On the filesystem, also get the same aggregates for `field_position` within `file_name`. Hint: There are Linux commands to get this so you don't have to write your own function.
    
1. Join the counts from the database and file and tabulate. For example, we invoke this on the command line:
    ```sh
    check_distribution.sh ./data customer.tbl 7 tpch customer c_mktsegment
        ```

    And we get something like this as output:
    ```sh
    AUTOMOBILE 29752 29752
    BUILDING 30142 30142
    FURNITURE 29968 29968
    HOUSEHOLD 30189 30189
    MACHINERY 29949 29949
    ```

### Star schema

TPC-H tables are in 3NF. Provide a second set of tables in the dimensional model and the transformational logic to populate them. We shall award points even if this item is incomplete but clearly shows the beginnings of a viable solution.

### Extra queries

Points, too, if you can provide a few more queries outside of the TPC-H set that demonstrate your understanding of the schema and its data.

