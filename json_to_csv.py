'''
The module is used to create csv files from json data files.

'''
#
# Name        : json_to_csv.py
# Description : The module is used to create csv files from json data files.
#               
#
# Input       : directiry path where all json files are stored
#
# Output      : csv files in the directory of json files
#
# Notes       :1. For each json file, there will be a number of csv files
#                 created, each of which will correspond to a specific record
#                 type. The content of each record type from different json 
#                 file will be appended to the same csv file.
#
#                 from the attribute list records stored in extrac_att_list.dat
#                 file in the same directory as this script.
#
#              2. The content of csv files can be adjusted by adding or
#                 removing attributes names from attribute list records
#                 in extract_att_list.dat file.
#
#              3. The script contains folllowng functions:
#                  -  load_att_ref_file()
#                  -  load_json_file         (fname)
#                  -  process_json_records   ()
#                  -  flatten_list_of_values (key,val)
#                  -  flatten_dict_values    (key,val)
#                  -  create_csv_records_and_files()
#                  -  att_required(att)
#                  -  store_record_type        (record_type) 
#                  -  check_for_dup_record_name(record_name) 
#                  -  store_att_name           (record_name,attname) 
#                  -  check_for_dup_att_name   (record_name, ttname)
#                  -  process_new_record_type  (key,val)
#                  -  process_next_record_type (key,val)
#                  -  process_next_attribute   (key,val)
#                  -  process_new_instance_of_same_record_type()
#                  -  write_to_last_csv_file()
#                  -  main()
#
#
# History
# Date       Author      Description
#
# 06/05/2022 Arif Zaman  Initial creation
#
#
import logging
import  json
import  os
import sys
import traceback
#
# module constant
#
# file that stores attributes for record type, required for extraction
#
EXT_ATT_LIST_FILE="./extract_att_list.dat"

MODULE_NAME = sys.argv[0]
LOGFILE = "./log/elv.log"
LOGIN = os.getlogin()
#
# globals
#
global dir_path
global schema_dict
schema_dict = {}
#
# header and data record for each record type
#
global data_rec
global header_rec
data_rec=""
header_rec = ""
global current_record_type
current_record_type = ""
#
# record type counter
#
global resource_no 
resource_no = 0
#
# used to identify header record for record type other than patient 
# in order to add patient id 
#
global new_record
new_record = False
global patient_id
patient_id = ""
# list of record type
#
global  lort 
lort=[]
   
global key_sequence
key_sequence = 0
global record_no
record_no = 0
#
# rec and att locators
#
global rec_locator
global att_locator
rec_locator="entry-resource-resourceType"  # use this composite key to identify new record type
att_locator="entry-resource-"              # use this composite key to identify attribute for record type
#


# Name     :load_json_file
# Input    :jason file path
# Overview :The function is used to load json file into dictionary.
# Notes    :
#
def load_json_file(fname):
    '''
    The function loads json file into dictionary
    '''
    global json_dict
    json_dict = {}
 
    fh = open (fname, "rt" )
    try:
        json_dict = json.load (fh) 
        fh.close()
        return True
    except  Exception as  e  :
        raise Exception(f"ERROR:Failed to load json file,{fname} into \
        dictionary because of {e}")


#
# Name     :flatten_list_of_values
# Overview :The function is used to flatten a list of values of json object
# Input    :key(string) , value(list)
# Notes    :1. The function calls itself.
#
def flatten_list_of_values (i_key, i_val):
    '''
    The function flattens dictionary value which is a list.
    '''
    for  li in i_val :

        if (str(type(li))).find("'dict'")  != -1:
            flatten_dict_values(i_key,li)

        elif (str(type(li))).find("'list'")  != -1:
            flatten_list_of_values(i_key,li)

        else:
            create_csv_records_and_files(i_key, li)


#
# Name     :flatten_dict_values
# Overview :The function is used to flatten a dictionary value for a json object
# Input    :key(string) , value(dictionary)
# Notes    :1. The function calls itself.
#
def flatten_dict_values (i_key,i_val) :
    '''
    The function flattens dictionary value which is a dictionary.
    '''
    for k, v in i_val.items() :
        key=f"{i_key}-{k}"

        if (str(type(v))).find("'list'")  != -1:
            flatten_list_of_values(key,v) 

        elif (str(type(v))).find("'dict'")  != -1:
               flatten_dict_values(key,v)

        else:
            create_csv_records_and_files(key, v)

#
# Name     :att_required
# Overview :The function is used to check if an attribute is required for
#           extraction for a specific record tytpe
# Input    :attribute name
# Returns  : 1  if attribute required
#          : 2  if attribute not required
#          : 3  record type not found

# Notes    : 1. Retrive records are tuples of record names and attributes.
#
def att_required(att):
    '''
    The function is used to check if an attribute is required for a specific record tytpe
    '''
    rc=0
    for tup in lot_for_att  :
        record_type=tup[0]
        if record_type != current_record_type :
            continue
        # found current record type
        if att in tup :
            # attribute is in the list for extraction
            rc = 1
            break
        else:
            # attribute is not in the list for extraction
            rc = 2
            break
    else:
        rc = 3  # record type not found in extract_att_list.dat file
 
    return rc


#
# Name     : store_record_type
# Overview : The function is used to store record type in the schema dictionary
# Input    : record  type
# Notes    : 1. The function stores record name as ley and an empty
#               list for values ( attributes) to be stored
#
def store_record_type(record_type) :
    '''
    The function is used to store record type in the schema dictionary
    '''
    global schema_dict
    schema_dict[record_type] = []


#
# Name     :check_for_dup_record_name
# Overview : The function is used to check whether schema dictionary already
#            contains the record name .
# Input    : record name
# Notes    :
#
def check_for_dup_record_name(record_name) :
    '''
    The function is used to check whether schema dictionary already
    contains the record name .
    '''
    for k in schema_dict.keys()  :
        if k == record_name :
            break
    else :
         # key not found
         return False

    # key found
    return True


#
# Name     : store_att_name
# Overview : The function is used to store attribute name in the schema
#            dictionary
# Notes    :
#
def store_att_name(record_name,attname) :
    '''
    The function is used to store attribute name in the schema
    dictionary
    '''
    global schema_dict
    schema_dict[record_name].extend([attname])


#
# Name     : check_for_dup_att_name
# Overview : The function is used to check whether schema dictionary already contains this
#            attribute name for this record.
#
# Notes    : 1. The attributes are duplicated when list values are flattened 
#            2. In order to treat these attributes as normal attributes, 
#               unique sequences are  appended to these attributes
#
def check_for_dup_att_name(record_name, attname):
    for  k, v in schema_dict.items() :
        if k == record_name :
           if  attname in v :
               break
           else:
                # no duplicate found
                return False

    return True # duplicate found


#
# Name     : def process_new_record_type
# Overview : The function is used to process first instance of new record  type
# Notes    :
#
def process_new_record_type(i_key, i_val):
    '''
    The function is used to process first instance of new record  type
    '''
    global key_sequence
    global fh
    global file_append
    global header_rec
    global data_rec
    global record_no
    global current_record_type
    global new_record
    #
    #
    new_record = True
    current_record_type=i_val
    store_record_type(current_record_type)
    #
    # write already processed csv record
    # when processing very first record, there will not be any previous record
    #
    if record_no > 0  :
        #
        #
        if file_append :
            fh.write(data_rec)
            fh.write("\n")
            fh.flush()
            fh.close()
            header_rec=""
            data_rec=""
        else:
            fh.write(header_rec)
            fh.write("\n")
            fh.write(data_rec)
            fh.write("\n")
            fh.flush()
            fh.close()
            header_rec=""
            data_rec=""
    #
    #
    #
    csv_file_name=f"{dir_path}/{i_val}.csv"
    if os.path.exists(csv_file_name) :
        fh = open (csv_file_name, "a")
        file_append=True
    else:
        fh = open (csv_file_name, "w")
        file_append=False

    key_sequence = 1
    record_no += 1


#
# Name     : process_new_instance_of_same_record_type ()
# Overview : The function processes new instance of previous record
# Notes    :
#
def process_new_instance_of_same_record_type():
    '''
    The function write csv record for previous instance of the same record type
    '''
    #
    #
    global header_rec
    global data_rec
    #
    # write csv record for previous instance
    #
    if not fh.closed  :
        if file_append :
            fh.write(data_rec)
            fh.write("\n")
            fh.flush()
            fh.close()
            header_rec=""
            data_rec=""
        else:
            fh.write(header_rec)
            fh.write("\n")
            fh.write(data_rec)
            fh.write("\n")
            fh.flush()
            fh.close()
            header_rec=""
            data_rec=""


#
# Name     : process_next_record_type
# Overview : The function is used to direct processing for next record type.
# Notes    :
#
def process_next_record_type (i_key, i_val):
    '''
    The function is used to direct processing for next record type.
    '''
    if not check_for_dup_record_name(i_key) :
        process_new_record_type(i_key,i_val)
    else:
        process_new_instance_of_same_record_type ()


#
# Name     : process_next_attribute
# Overview : The function is used to process next attribute from the file.
# Notes    :
#
def process_next_attribute  (i_key,i_val):
    '''
    The function is used to process next attribute from the file.
    '''
    global header_rec
    global data_rec
    global key_sequence
    global new_record
    global patient_id
    #
    if current_record_type == "Patient"  and i_key == "entry-resource-id" :
        patient_id = i_val
    if check_for_dup_att_name(current_record_type, i_key) :
        #
        # flattened attribute
        # make it unique by appending a unique sequence
        #
        key=f"{i_key}-{key_sequence}"
        key_sequence += 1
    else :
        key=i_key
    #
    store_att_name(current_record_type,key)
    extract_key_format=i_key[15:]
    rc=att_required(extract_key_format)
    if rc == 2 :
        return True
    elif rc == 3 :
         # record type not in the reference file
         raise Exception(f"ERROR:Failed to locate record type,\
         {current_record_type} in reference file for record type=\
         {current_record_type}" )

    if current_record_type != "Patient" and new_record == True :
        new_record = False
        header_item = "patient_id"  +  ","
        data_item = patient_id + ","
        header_rec += header_item
        data_rec   += data_item
    #
    # add key to header item
    #
    header_item= extract_key_format + ","
    #
    # add val as data item
    #
    data_item=str(i_val)  + ","
    #
    # build header record
    #
    header_rec += header_item
    #
    #build data record
    #
    data_rec   += data_item
    #
    return True


#
# Name     :create_csv_records_and_files (i_key, i_val):
# Overview :The function direct processing for creating csv records and files.
# Input    :key(string) , value(string)
# Notes    :
#
def create_csv_records_and_files(i_key, i_val):
    '''
    The function direct processing for creating csv records and files.
    '''
    #
    # identify record type
    #
    if i_key.find(rec_locator) != -1:
        #
        # identfied next record type object
        #
        # process_record_type(i_key, i_val) 
        process_next_record_type(i_key, i_val) 

    elif i_key.find(att_locator) !=  -1:
        process_next_attribute(i_key, i_val) 


#
# Name     : process_json_records
# Overview : The function is used to loop through all records in the dictionary
#            for a specific json file.
# Notes    :
#
def process_json_records():
    '''
    The function processes json record
    '''
    for k,v in  json_dict.items() :    
        if ((str(type(v))).find("'list'")  != -1) :
            flatten_list_of_values (k,v)

        elif (str(type(v))).find("'dict'")  != -1 :
            flatten_dict_values (k, v)
        else:
            create_csv_records_and_files(k,v)

#
# Name     : write_last_csv_record
# Overview : The function is used to write the last csv record which
#            will not be processed in the main loop.

# Notes    : 1. csv record is built during the processing of attributes and
#             therefore, the last record  must be written outside the 
#             main processing loop which terminates with the completion 
#             of the last csv record without wrting it to file.
#
def write_last_csv_record():
    '''
    The function is used to write the last csv record which
    will not be processed in the main loop.
    '''
    #
    #
    if file_append :
        fh.write(data_rec)
        fh.write("\n")
        fh.flush()
        fh.close()
    else:
         fh.write(header_rec)
         fh.write("\n")
         fh.write(data_rec)
         fh.write("\n")
         fh.flush()
         fh.close()

#
# Name     : load_att_ref_file :
# Overview : The function is used to load the required attribute list for for
#            extraction into memory.
# Notes    :
#
def load_att_ref_file():
    '''
    The function is used to load the required attribute list for extraction
    into memory.
    '''     
    #
    # list of tuples for required attributes for each record type
    #
    global lot_for_att
    #
    lot_for_att=[]
    #
    #
    # file is expected in the current directory
    #
    if not os.path.exists(EXT_ATT_LIST_FILE):
        raise Exception(f"ERROR:Attribute reference file,{fname} does not exist")
    with open(EXT_ATT_LIST_FILE, "r") as fh :
        for rec in fh :
            # loa=list of attributes
            loa=rec.strip("\n").split(",") 
            if len(loa) == 1 :
                # it's an empty line
                continue
            elif loa[0][0] == "#"  :
                # it's a command
                continue
            else : 
                    tup=tuple(loa)
                    lot_for_att.append(tup)


#
# Name     : main 
# Overview : The function is used to implement control structure.
# Notes    :
#
def main():
    try:
        logging.root.name = LOGIN
        logging.basicConfig(
            level=logging.INFO, filename=LOGFILE, filemode="a",
            format="%(asctime)s %(name)s - %(levelname)s - %(message)s")

        logging.info(f"Module-{MODULE_NAME} Execution Starting")

        global dir_path
        #
        # check argument
        #
        if len( sys.argv ) != 2    :
            raise Exception("Usage:python json_to_csv.py <dir path containg json files>")
        #
        # validate directory path
        #
        dir_path=sys.argv[1]
        if not os.path.exists(dir_path) :
            raise Exception(f"ERROR:Directory path,{dir_path} does not exist")
        #    
        load_att_ref_file()
        #
        # load and process each file
        # lof=list of json files.
        #
        lof=[fname for fname in os.listdir(dir_path) if "json" in fname.split(".") ]
        if len(lof) == 0 :
            raise Exception(f"INFO:Directory,{dir_path} does not contain any json files")

        for fname in lof :
            file=f"{dir_path}/{fname}"
            load_json_file (file)  
            process_json_records() 
        #
        write_last_csv_record()
    
        logging.info(f"Module-{MODULE_NAME} Execution Completed")

    except Exception as e:
        logging.exception("Exception:")
        traceback.print_exc()

#
main ()
