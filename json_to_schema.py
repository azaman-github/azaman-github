'''
The module is used to infer minimal schema(record type and attributes) from
a single or multiple json files in a directory
'''
#
# Name        : infer_minimal_json_schema.py
# Description : The program is used to infer json schema (record types and
#               attributes) from json files.

# Input       : json file directory path
# Notes       : 1. The script contains folllowng functions:
#                  -  load_json_file()
#                  -  flatten_dict_values         (key,val)
#                  -  flatten_list_values         (key,val)
#                  -  infer_schema                (key,val)
#                  -  print_schema_to_file        ()
#                  -  store_record_name           (record_name)
#                  -  check_for_dup_record_name   (record_name)
#                  -  store_att_name              (record_name)
#                  -  check_for_dup_att_name      (record_name, attname)
#                  -  extract_att_from_flattened_key_val_pair(key,val)
#                  -  main ()
#
# History
# Date         Author      Description
#
# 08/05/2022   Arif Zaman  Initial creation
#
#
import logging
import json
import os
import sys
import traceback
from datetime import datetime as dt
#
# module constants
#
MODULE_NAME=sys.argv[0]
SCHEMA_FILE="./schema.dat"
LOGFILE="./log/elv.log"
LOGIN=os.getlogin()
#
# globals
#
global lof

global schema_dict
schema_dict = {}

global key_sequence
key_sequence = 0

global cur_record_name
cur_record_name=""

global ignore_att
ignore_att =False

global rec_locator
# use this key segment to identify new record
rec_locator="entry-resource-resourceType"

global att_locator
# use this key segment to identify attribute
att_locator="entry-resource-"

#
# Name     :load_json_file
# Overview :The function is used to load json file into dictionary.
# Notes    :
#
def  load_json_file(file_path) :
    '''
    The function loads the input json file into a dictionary.
    '''
    #
    global work_schema_dict
    work_schema_dict={}
    try:
        with  open(file_path, "rt" ) as fh :
            work_schema_dict = json.load (fh)
            return True
    except  Exception as  e  :
        raise Exception(f"ERROR:Failed to load the json file{file_path} into \
        python dictionary because of {e}")

#
#
# Name     :flatten_list_values
# Overview :The function is used to flatten a list value for a json object
# Input    :key(string) , value(list)
# Notes    :1. The function calls itself.
#
def flatten_list_values (i_key,i_val):
    '''
    The function is used to flatten a list value for a json object
    '''

    for  li in i_val :

        if (str(type(li))).find("'dict'")  != -1:
            flatten_dict_values(i_key,li)

        elif (str(type(li))).find("'list'")  != -1:
            flatten_list_values (i_key,li)

        else :
            extract_att_from_flattened_key_val_pair (i_key,i_val)


#
# Name     :flatten__dict_values
# Overview :The function is used to flatten  dictionary values for a json object
# Input    :key(string) , value(dictionary)
# Notes    :1. The function calls itself.
#
def flatten_dict_values (i_key,i_val) :
    '''
    The function is used to flatten  dictionary values for a json object
    '''

    for k, v in i_val.items() :
        key=f"{i_key}-{k}"

        if  (str(type(v))).find("'list'")  != -1:
            flatten_list_values (key, v)

        elif  (str(type(v))).find("'dict'")  != -1 :
            flatten_dict_values(key,v)

        else:
            extract_att_from_flattened_key_val_pair (key,v)


#
# Name     : extract_att_from_flattened_key_val_pair
# Overview :The function is used to print key and value of a json object.
# Input    :key(string) , value(string)
# Notes    :
#
def extract_att_from_flattened_key_val_pair(i_key,i_val):
    '''
    The function is used to print key and value of a json object.
    '''
 
    global cur_record_name
    global key_sequence
    global ignore_att

    if i_key.find(rec_locator) !=  -1  :
        #
        # identfied  record type object
        # split the input, i_key
        #
        keys=i_key.split("-")
        #
        # check last segment of composite key
        #
        if keys[-1] == "resourceType"  :
            #
            # this is next record type object
            #
            if check_for_dup_record_name(i_val) :
                #
                # already captured this record type
                # ignore all its attributes
                #
                ignore_att = True
            else:
                # first occurrence of new record type
                ignore_att = False
                key_sequence=1
                store_record_name(i_val)
                cur_record_name=i_val
    else:
        #
        # processing attribute object
        #
        if ignore_att  :
            return True

        if i_key.find(att_locator) != -1  :
            if check_for_dup_att_name(cur_record_name, i_key) :
                #
                # flattened attribute
                # make it unique by appending a unique sequence
                #
                key=f"{i_key}-{key_sequence}"
                key_sequence += 1
            else:
                key=i_key

            store_att_name(cur_record_name,key)


#
# Name     : store_record_name
# Overview : The function is used to store record name in the schema dictionary
# Input    : record name
# Notes    :
#
def store_record_name(record_name) :
    '''
    The function is used to store record name in the schema dictionary
    '''
    global schema_dict
    schema_dict[record_name] =[]


#
# Name     :check_for_dup_record_name
# Overview :The function is used to check whether schema dictionary already
#           contains the record name .
# Input    :record name
# Notes    :
#
def check_for_dup_record_name(record_name) :
    '''
    The function is used to check whether schema dictionary already contains the record name .
    '''
    for k in schema_dict.keys()  :
        if k == record_name :
            return True
    else:
        return False


#
# Name     : store_att_name
# Overview : The function is used to store attribute name in the schema dictionary
# Notes    :
#
def store_att_name(record_name,attname) :
    '''
    The function is used to store attribute name in the schema dictionary
    '''
    global schema_dict
    schema_dict[record_name].extend([attname])


#
# Name     : check_for_dup_att_name
# Overview : The function is used to check whether schema dictionary already contains this
#            attribute name for this record.
# Notes    :
#
def check_for_dup_att_name(record_name, attname):
    '''
     The function is used to check whether schema dictionary already contains this
    '''
    for k, v in schema_dict.items() :
        if k == record_name :
            if  attname in v :
                return True
            else:
                return False


#
# Name     : infer_schema
# Overview : The function is used to infer schema from json data that is loaded into dictionary.
# Notes    :
#
def infer_schema() :
    '''
    The function is used to infer schema from json data that is loaded into dictionary.
    '''

    for k,v in work_schema_dict.items() :
        if (str(type(v))).find("'list'")  != -1:
            flatten_list_values (k,v)

        elif (str(type(v))).find("'dict'")  != -1:
            flatten_dict_values (k, v)


#
# Name     :print_schema_to_file
# Overview :The function is used to print the schema that is stored in the dictionary
#           to the file.
# Notes    :
#
def print_schema_to_file() :
    '''
    The function is used to print the schema that is stored in the dictionary
    '''
    #
    # sort dictionary
    #
    sd={k: sorted(schema_dict[k]) for k in sorted(schema_dict) }

    fname = SCHEMA_FILE
    with open(fname, "w") as fh :
        #
        # print records types
        #
        file_no=1
        ts = dt.now().strftime("%d/%m/%Y at %H:%M:%S")
        fh.write(f"                          Schema Generated on {ts}\n")
        fh.write("List of Files Analysed\n")
        fh.write("======================\n")
        for fname in lof :
            fh.write(f"{file_no}.{fname}\n")
            file_no += 1
        fh.write("\n")
        #
        att_no = 1
        fh.write("List of Record Types\n")
        fh.write("====================\n")
        for k in sd.keys() :
            fh.write(f"{att_no}.{k}\n")
            att_no +=1
        fh.write("\n\n")
        #
        att_no = 1
        for k, v in sd.items() :
            fh.write("\n")
            fh.write(f"Record Type={k}\n")
            fh.write("\n")
            fh.write("List of Attributes\n")
            fh.write("==================\n")
            for att in v :
                fh.write(f"{att_no}.{att}\n")
                att_no +=1

            att_no = 1
#
# Name     : main
# Overview : The function is used to implement control structure.
# Notes    :
#
def main () :
    '''
    The function is used to implement control structure.
    '''
    global lof
    global schema_dict
    try:
 
        logging.root.name = LOGIN
        logging.basicConfig(
            level=logging.INFO, filename=LOGFILE, filemode="a",
            format="%(asctime)s %(name)s - %(levelname)s - %(message)s")

        logging.info(f"Module-{MODULE_NAME} Execution Starting")
     
        if len( sys.argv ) != 2    :
            print("Usage : python infer_json_schema.py <json file dir path>")
            sys.exit(1)
          
        json_file_dir_path=sys.argv[1]
        lof=[ ( json_file_dir_path + "/" + fname) for fname in os.listdir(json_file_dir_path) if "json" in  fname.split(".")  ]
 
        for fname in lof :
            load_json_file (fname) 
            infer_schema()

        print_schema_to_file()

        logging.info(f"Module-{MODULE_NAME} Execution Completed")

    except Exception as e :
        logging.exception("Exception:")
        traceback.print_exc()


main()
