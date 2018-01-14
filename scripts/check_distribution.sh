#!/usr/bin/env bash

# ARGS
#    data_path -- filesystem directory where the source files from qgen are located.
#    source_filename -- One of the files created by dbgen (i.e. customer.tbl corresponds to table CUSTOMER).
#    field_position -- The nth field within source_filename (i.e. within customer.tbl, the 7th field corresponds to the CUSTOMER.C_MKTSEGMENT column).
#    db_name -- name of the database.
#    table_name -- The table name in the database.
#    column_name -- The column in table_name.
# ARGS

help_message() {
	echo "$(basename "$0") [-h] -dp -sf -fp -db -tb -col 
with:
    -p | --data_path -- filesystem directory where the source files from qgen are located.
    -s | --source_filename -- One of the files created by dbgen (i.e. customer.tbl corresponds to table CUSTOMER).
    -f | --field_position -- The nth field within source_filename (i.e. within customer.tbl, the 7th field corresponds to the CUSTOMER.C_MKTSEGMENT column).
    -d | --db_name -- name of the database.
    -t | --table_name -- The table name in the database.
    -c | --column_name -- The column in table_name.
"
}

### OLSCHOOL
AWK='/usr/bin/awk'
SORT='/usr/bin/sort'
CAT='/bin/cat'
PSQL='/usr/bin/psql'
SUDO='/usr/bin/sudo'
GREP='/bin/grep'

PATH=$1
FILENAME=$2
FIELDPOS=$3
DBNAME=$4
TBNAME=$5
COLNAME=$6
### OLSCHOOL

### GETOPTS
#echo "OPTIND starts at $OPTIND"
##while getopts ":hhelp:dp:data_path:sf:source_filename:fp:field_position:db:db_name:tb:table_name:col:column_name:" opt; do
#while getopts ":hpsfdtc:" opt; do
#  case $opt in
#	h|help )
#		echo "OPTIND is now $OPTIND"
#		echo "Option $opt has value $OPTARG"
#		help_message >&2
#		exit 1
#		;;
#    #dp|data_path )
#    p )
#		echo "OPTIND is now $OPTIND"
#		echo "Option $opt has value $OPTARG"
#		echo "-data_path was triggered!" >&2
#		PATH=${OPTARG}
#		;;
#    #sf|source_filename )
#    s )
#		echo "OPTIND is now $OPTIND"
#		echo "Option $opt has value $OPTARG"
#		echo "-source_filename was triggered!" >&2
#		FILENAME=${OPTARG}
#		;;
#    #fp|field_position )
#    f )
#		echo "OPTIND is now $OPTIND"
#		echo "Option $opt has value $OPTARG"
#		echo "-field_position was triggered!" >&2
#		FIELDPOS=${OPTARG}
#		;;
#    #db|db_name )
#    d )
#		echo "OPTIND is now $OPTIND"
#		echo "Option $opt has value $OPTARG"
#		echo "-db_name was triggered!" >&2
#		DBNAME=${OPTARG}
#		;;
#    #tb|table_name )
#    t )
#		echo "OPTIND is now $OPTIND"
#		echo "Option $opt has value $OPTARG"
#		echo "-table_name was triggered!" >&2
#		TABLENAME=${OPTARG}
#		;;
#    #col|column_name )
#    c )
#		echo "OPTIND is now $OPTIND"
#		echo "Option $opt has value $OPTARG"
#		echo "-column_name was triggered!" >&2
#		COLNAME=${OPTARG}
#		;;
#    \? )
#		echo "OPTIND is now $OPTIND"
#		echo "Option $opt has value $OPTARG"
#		echo "Invalid option: -$OPTARG" >&2
#		;;
#	: )
#		echo "OPTIND is now $OPTIND"
#		echo "Option $opt has value $OPTARG"
#		help_message >&2
#		exit 1
#		;;
#  esac
#  echo "OPTIND is now $OPTIND"
#done
### GETOPTS


### MAIN
## COUNT & GROUP AGGREGATES ON TBL FILE
${AWK} -F "|" -f /srv/scripts/tblcount.awk -v field_pos="$FIELDPOS" ${PATH}/${FILENAME} | ${SORT} -n -k1 > /srv/scripts/t1
## COUNT & GROUP AGGREGATES ON TBL FILE

## TABLE SQL COUNT
echo "select $COLNAME, count(*)
from $TBNAME
group by $COLNAME
order by $COLNAME" > /srv/scripts/tblcount.sql
${SUDO} -u postgres ${PSQL} -f /srv/scripts/tblcount.sql ${DBNAME} -t > /srv/scripts/t2
## TABLE SQL COUNT

## DISPLAY
for i in `${AWK} '{print $1}' /srv/scripts/t1`; do   
	RESULT=`echo -n $i`; 
	RESULT+=`${GREP} $i /srv/scripts/t1 | ${AWK} '{ print " "$2}'` ; 
	RESULT+=`${GREP} $i /srv/scripts/t2 | ${AWK} -F "|" '{print " "$2'}`; 
	echo $RESULT; 
done
## DISPLAY

#EOF
