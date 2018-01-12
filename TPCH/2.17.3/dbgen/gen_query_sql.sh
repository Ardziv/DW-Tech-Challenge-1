#!/bin/sh
# generate queries from query templates with qgen
DIR=.
mkdir $DIR/finals
cp $DIR/queries/*.sql $DIR
for FILE in $(find $DIR -maxdepth 1 -name "[0-9]*.sql")
do
    DIGIT=$(echo $FILE | tr -cd '[[:digit:]]')
    ./qgen $DIGIT > $DIR/finals/$DIGIT.sql
done
rm *.sql
