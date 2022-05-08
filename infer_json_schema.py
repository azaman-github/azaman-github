#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Name        : infer_json_schema.py 
# Description : The program is used to infer json schema (record types and attributes) from json file . 
# Input       : json file 
# Notes       : 1. Each record is fully flattened as follows :
#
# "extension": [
#      {
#        "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-race",
#        "extension": [ {
#          "url": "ombCategory",
#          "valueCoding": {
#            "system": "urn:oid:2.16.840.1.113883.6.238",
#            "display": "White"
#          }
#        }, {
#          "url": "text",
#          "valueString": "White"
#        } ]
#      },
#      {
#        "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity",
#        "extension": [ {
#          "url": "ombCategory",
#          "valueCoding": {
#            "system": "urn:oid:2.16.840.1.113883.6.238",
#            "display": "Not Hispanic or Latino"
#          }
#        }, {
#          "url": "text",
#          "valueString": "Not Hispanic or Latino"
#        } ]
#       }
#       ]
#resource-extension-url
#resource-extension-extension-url <----- first elemnt in the list
#resource-extension-extension-url-0  <-- flattend attribute (second element in the list)
#resource-extension-extension-valueCoding-system
#resource-extension-extension-valueCoding-display
#resource-extension-extension-valueString
#
#resource-extension-url-1
#resource-extension-extension-url-2
#resource-extension-extension-valueCoding-system-3
#resource-extension-extension-valueCoding-display-5
#resource-extension-extension-url-6
#resource-extension-extension-valueString-7
#
#
#
#2. The script contains folllowng functions:
#                  -  load_json_file() 
#                  -  process_dict_values         (key,val) 
#                  -  process_list_values         (key,val) 
#                  -  process_string_value        (key,val)
#                  -  infer_schema                (key,val)
#                  -  print_schema                (key,val)
#                  -  store_record_name           (record_name)
#                  -  check_for_dup_record_name   (record_name)
#                  -  store_att_name              (record_name)
#                  -  check_for_dup_att_name      (record_name, attname):
#                  -  main ()
#
# History
# Date         Author      Description
#----------------------------------------------------------------------------------------------------
# 08/05/2022   Arif Zaman  Initial creation
#
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import  json
import  os
import sys
import traceback

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Name     :load_json_file
# Overview :The function is used to load json file into dictionary.
# Notes    :
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def  load_json_file() :
     '''
      load the input json file
     ''' 
     global json_dict
     global fh
     #
     fh =  open (json_file, "rt" ) 
     try : 
           json_dict = json.load (fh) 
           return True
     except  Exception as  e  :
          print("ERROR:Failed to load the json file into python dictionary;see below for detaiils")
          traceback.print_exc()
          return False
#
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Name     :process_list_values 
# Overview :The function is used to flatten a list value for a json object
# Input    :key(string) , value(list)
# Notes    :1. The function calls itself.
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def process_list_values (i_key,i_val) :
    #
    #
    for  li in i_val :
                
        if ( (str(type(li))).find("'dict'")  != -1 ) :
            process_dict_values(i_key,li) 

        elif ( (str(type(li))).find("'list'")  != -1 ) :
            key=f"{i_key}-{str(seq_num)}"
            process_list_values (key,li) 

        else :
              process_string_value (i_key,i_val)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Name     :process_dict_values
# Overview :The function is used to flatten a dictionary value for a json object
# Input    :key(string) , value(dictionary)
# Notes    :1. The function calls itself.
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def process_dict_values (i_key,i_val) :

    for k, v in i_val.items() :

        key=f"{i_key}-{k}"

        if ( (str(type(v))).find("'list'")  != -1 ) :
           process_list_values (key, v)

        elif ( (str(type(v))).find("'dict'")  != -1 ) :
           process_dict_values(key,v)

        else :
              process_string_value (key,v)
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Name     :process_string_value
# Overview :The function is used to print key and value of a json object.
# Input    :key(string) , value(string)
# Notes    :
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def  process_string_value (i_key, i_val):
     # 
     global lort   # list of record types
     global loa    # list of attributes
     global  cur_record_name
     global  key_sequence
     global ignore_att
     # 
     rec_locator="entry-resource-resourceType"  # use this to identify new record 
     #att_locator="entry-resource-               "
     #                           15<---att name--->
     att_locator="entry-resource-"
     #
     if  i_key.find(rec_locator) !=  -1  :
         #
         # identfied  record type object
         # split the input, i_key
         #
         keys=i_key.split("-")
         if keys[-1] == "resourceType"  :
              # this is next record type object
              if  check_for_dup_record_name(i_val) :
                    #
                    # processed this record type
                    # ignore all its attributes
                    #
                    ignore_att = True
              else :
                   # first occurrence of new record type  
                   ignore_att = False
                   key_sequence=0
                   store_record_name(i_val)
                   cur_record_name=i_val
     else :
          # processing attribute object 
          if ignore_att  :
             return True
          if i_key.find(att_locator) != -1  :
               if  check_for_dup_att_name(cur_record_name, i_key) :
                   #
                   # flattened attribute
                   # make it unique by appending a unique sequence
                   #
                   key=f"{i_key}-{key_sequence}"
                   key_sequence += 1
               else :
                   key=i_key
               # 
               store_att_name(cur_record_name,key) 

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Name     : store_record_name
# Overview : The function is used to store record name in the schema dictionary
# Input    : record name
# Notes    :
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def store_record_name(record_name) :
     schema_dict[record_name] =[]

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Name     :check_for_dup_record_name
# Overview : The function is used to check whether schema dictionary already contains the record name .
# Input    : record name
# Notes    :
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def check_for_dup_record_name(record_name) :
    for  k  in schema_dict.keys()  :
        if k == record_name :
            return True
    else :
         return False

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Name     : store_att_name
# Overview : The function is used to store attribute name in the schema dictionary
# Notes    :
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def store_att_name(record_name,attname) :
     schema_dict[record_name].extend([attname])

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Name     : check_for_dup_att_name
# Overview : The function is used to check whether schema dictionary already contains this 
#            attribute name for this record.
# Notes    :
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def check_for_dup_att_name(record_name, attname):
    for  k, v in schema_dict.items() :
        if k == record_name :
           if  attname in v :
                return True
           else:
                return False
      
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Name     : infer_schema
# Overview : The function is used to infer schema from json data that is loaded into dictionary.
# Notes    :
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def infer_schema() :
    for k,v in  json_dict.items() :    
        #
        if ( (str(type(v))).find("'list'")  != -1 ) :
            process_list_value (k,v)
        #
        elif ( (str(type(v))).find("'dict'")  != -1 ) :
            process_dict_value (k, v)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Name     :print_schema
# Overview :The function is used to print the schema that is stored in the dictionary.
# Notes    :
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def print_schema() :
     att_no = 1
     for  k, v in schema_dict.items() :
           print(f"Record Name={k}")
           print("\n")
           print("List of Attributes")
           print("==================")
           for att in v :
               print(f"{att_no}.{att}")
               att_no +=1
           print("\n")
           att_no=1
    
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Name     : main 
# Overview : The function is used to implement control structure.
# Notes    :
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def main () :
     #
     global json_file
     global  lort # list of record type
     global  loa  # list of attributes
     lort=[]
     loa=[]
     global schema_dict
     schema_dict = {}
     global key_sequence
     key_sequence = 0
     global cur_record_name
     cur_record_name=""
     global ignore_att
     ignore_att =False
     #
     #
     if len( sys.argv ) != 2    :
          print("Usage : python jsg.py <json file>")
          sys.exit(1)

     else:
          json_file=sys.argv[1]
     #
     if not load_json_file ()  :
          sys.exit(1)
     #
     infer_schema()
     #
     print_schema()
    
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
main ()
