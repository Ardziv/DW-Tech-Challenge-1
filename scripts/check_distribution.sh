#!/usr/bin/env bash

while getopts ":data_path:source_filename:field_position:db_name:table_name:column_name" opt; do
  case $opt in
    data_path)
      echo "-data_path was triggered!" >&2
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      ;;
  esac
done
