### DW Technical Challenge 1: Fun with TPC-H

TPC-H (http://www.tpc.org/information/current_specifications.asp) is considered the industry standard when benchmarking decision support systems. It consists of a well defined schema, a data population generator and updater, and various queries that, taken together, are a good representation of a common DSS environment.

For this challenge, we’d like for you to provide us with a VirtualBox image that contains a runnable instance of a TPC-H database along with mechanisms to generate and load the data and run queries on them. Specifically:

1. A database of your choice (i.e. Pg, GP, MySQL, etc) that is properly set up and contains empty TPC-H tables.
1. A way to invoke dbgen at scale 1 and load the data files into the database. The loaders can take the form of shell scripts, compiled/interpreted programs, or GUI-based ETL toolset jobs (i.e. Pentaho, Informatica, etc). Consider this as the E and L in ETL. Please include the source code in the image for review.
1. A set of TPC-H queries from qgen and a shell script to run them against the database.
1. A README to let us know where things are located and how to run the different components.
1. Be prepared to discuss aspects of TPC-H in general and this challenge in particular when you come in for our face-to-face. 

We shall provide you with a Dropbox link to upload the virtual machine image or if you have an AWS account handy, do give us a link to an S3 bucket to download it from. 

Bonus points:

1. TPC-H tables are in 3NF. Major bonus points if you can provide a second set of tables in the dimensional model and the transformational logic to populate them. We shall award points even if this item is incomplete but clearly shows the beginnings of a viable solution.
1. Points, too, if you can provide a few more queries outside of the TPC-H set that demonstrate your understanding of the schema and its data.