#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Name        : json_to_csv.py 
# Description : The program is used to create csv file from normalised json file(meaning csv file for each record type)
# Input       : directiry path where all json files are stored
#
# Notes       :1. The data items that are included in the csv file are read from the attribute list trecords
#                  stored in xxxx  file in the same directory as this script.
#
#              2. The content of csv files can be adjusted by adding or removing attribyes names from
#                  attribute list records.
# 
#             3. The script contains folllowng functions:
#                  -  load_json_file         (fname      ) 
#                  -  flatten_list_of_values (i_key,i_val)
#                  -  flatten_dict_values    (i_key,i_val)
#                  -  create_csv_file()
#                  -  build_csv_file ()
#                  -  process_record_type              (i_key, i_val) 
#                  -  process_attribute_for_record_type(i_key, i_val) 
#                  -  main()
#
# History
# Date       Author      Description
#-----------------------------------------------------------------------------------------------------
# 06/05/2022 Arif Zaman  Initial creation
#
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import  json
import  os
import sys
import traceback

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Name     :load_json_file
# Input    :jason file name
# Overview :The function is used to load json file into dictionary.
# Notes    :
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def load_json_file(fname) :
     '''
     The function loads json file into dictionary
     ''' 
     print("loading json file")

     global json_dict
     json_dict={}
 
     fh = open (fname, "rt" ) 
     try : 
           json_dict = json.load (fh) 
           return True
     except  Exception as  e  :
          print("ERROR:Failed to load the json file into python dictionary;see below for detaiils")
          traceback.print_exc()
          return False
#
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Name     :flatten_list_of_values 
# Overview :The function is used to flatten a list of values of json object
# Input    :key(string) , value(list)
# Notes    :1. The function calls itself.
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def flatten_list_of_values (i_key,i_val) :
     '''
     The function flattens dictionary value which is a list.
     '''
     #
     #
     print(f"DEBUG3: calling flattening_dict() with {i_key} {i_val}")
     for  li in i_val :
                
        if ( (str(type(li))).find("'dict'")  != -1 ) :
            flatten_dict_values(i_key,li) 

        elif ( (str(type(li))).find("'list'")  != -1 ) :
            flatten_list_of_values(i_key,li) 

        else :
             build_csv_file (i_key,i_val)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Name     :flatten_dict_values
# Overview :The function is used to flatten a dictionary value for a json object
# Input    :key(string) , value(dictionary)
# Notes    :1. The function calls itself.
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def flatten_dict_values (i_key,i_val) :
     '''
     The function flattens dictionary value which is a dictionary.
     '''

     print(f"DEBUG3: calling flattening_dict() with {i_key} {i_val}")
     for k, v in i_val.items() :
          key=f"{i_key}-{k}"

          if ( (str(type(v))).find("'list'")  != -1 ) :
               flatten_list_of_values(key,v) 

          elif ( (str(type(v))).find("'dict'")  != -1 ) :
               #flatten_dict_value(key,v)
               flatten_dict_values(key,v)

          else :
               #if not build_csv_file (key,v) :
                   # return False
               build_csv_file (key,v) 

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Name     :att_required
# Overview :The function is used to check if an attribute is required for a specific record tytpe
# Input    :attribute name
# Returns  : 1  if attribute required
#          : 2  if attribute not required
#          : 3  record type not found
# Notes    :
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def att_required(att) :
     '''
     The function is used to check if an attribute is required for a specific record tytpe
     '''
     for tup in lot_for_att  :
           record_type=tup[0]
           if record_type != current_record_type :
                continue
           #
           if att in tup :
                return 1 
           else:
                return 2
     else :
           return 3
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Name     :process_record_type
# Overview :The function is used to process record type, read from the json_dict.
# Input    :key(string) , value(dictionary)
# Notes    :
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def process_record_type(i_key, i_val)  :
     '''
     The function is used to process record type,read from the json_dict.
     '''
     print(f"DEBUG4:process record type {i_key} {i_val}")
     global lort
     global resource_no
     global fh
     global current_record_type
     global  header_rec
     global  data_rec
     #
     # split the key into its constituent parts
     #
     keys=i_key.split("-")
     #
     # check last key name
     #
     if keys[-1] == "resourceType"  :
          current_record_type=i_val
          # this is the next record type object
          if i_val in lort :  
               # already identified this record type
               pass  
          else :     
               # first occurrence of new record type 
               if resource_no > 0 :
                    #
                    # finished processing all attributes of last record type
                    #
                    fh.write(header_rec)
                    fh.write("\n")
                    fh.write(data_rec)
                    fh.close () 
                    header_rec=""
                    data_rec=""
               #
               # increment resource counter
               #
               resource_no += 1
               #
               # open csv file for current record type
               # open file in the directory where json files are stored
               #
               csv_file_name=f"{dir_path}/{i_val}.csv"
               if os.path.exists(csv_file_name) :
                    fh = open (csv_file_name, "a")
               else:
                    fh = open (csv_file_name, "w")
               #
               # store current record type          
               #
               lort.append(i_val)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Name     :process_attribute_for_record_type
# Overview :The function is used to process next record type, read from the json_dict.
# Input    :key(string) , value(dictionary)
# Notes    :
#           att_locator="entry-resource-                 "
#                                       15<---att name--->
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def process_attribute_for_record_type(i_key, i_val)  :
     '''
     The function is used to process attrubute for record type.
     '''
     print(f"DEBUG5:process record type attribute {i_key} {i_val}")
     global header_rec
     global data_rec

     this_att=""
     if i_key.find(att_locator) != -1  :
          this_att=i_key[15:]
          #
          # check if this attribute is required for csv file
          #
          rc=att_required(this_att) 
          if rc == 2 :
               # att not required
               return True
          elif rc == 3 :
               # record type not found
             raise Exception(f"ERROR:Failed to locate record type,{current_record_type} in file,{att_list_file}")
          #
          header_item= this_att + ","
          data_item=str(i_val)  + ","
          header_rec += header_item
          data_rec   += data_item
          #
     return True

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Name     :build_csv_file (i_key, i_val):
# Overview :The function is used to build csv files from individual attributes 
# Input    :key(string) , value(string)
# Notes    :
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def build_csv_file (i_key, i_val):
     '''
     The function builds csv file using individual json object attributes for its associated record type
     '''
     print(f"DEBUG6:Called build_csv_file() {i_key} ") 
     #
     # identify record type
     #
     if  i_key.find(rec_locator) !=  -1  :
         #
         # identfied next record type object
         # split the input, i_key
         #
         process_record_type(i_key, i_val) 
     else :
         if not process_attribute_for_record_type(i_key, i_val) :
              return False
  

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Name     : create_csv_file
# Overview : The function is used to create csv file for a json file which is loaded into a dictionary.
# Notes    :
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def create_csv_file() :
     '''
     The function creates csv file
     '''
     try :
          for k,v in  json_dict.items() :    
               print(f"DEBUG1: calling flattening_list_of_values() with {k} {v}")
               if ( (str(type(v))).find("'list'")  != -1 ) :
                    flatten_list_of_values (k,v)
        
               elif ( (str(type(v))).find("'dict'")  != -1 ) :
                    print(f"DEBUG2: calling flattening_dict() with {k} {v}")
                    flatten_dict_values (k, v)
               else:
                    build_csv_file (k, v)
     except Exception as e :
          print(f"ERROR:Failed to create csv file because of {str(e)}")
          return False

     return True

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Name     : load_att_ref_file :
# Overview : The function is used to load the required attribute reference file into memory.
# Notes    :
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def load_att_ref_file() :
     '''
     The function is used to load the required attribute reference file into memory.
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
     fname="./csv_att_list.dat"
     if not os.path.exists(fname):
         print(f"ERROR:Attribute reference file,{fname} does not exist")
         return False
     
     with open(fname, "r") as fh :
          for rec in fh :
               #loa=list of attributes
               loa=rec.strip("\n").split(",") 
               if len(loa) == 0 :
                    #it's an empty line
                    continue
               elif loa[0][0] == "#"  :
                    #it's a command
                    continue
               else : 
                    tup=tuple(loa)
                    lot_for_att.append(tup)
     #
     return True           

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Name     : main 
# Overview : The function is used to implement control structure.
# Notes    :
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def main () :
     #
     global dir_path
     #
     # header and data record for each record type
     #
     global data_rec
     global header_rec
     data_rec=""
     header_rec=""
     #
     # record type counter
     #
     global resource_no 
     resource_no = 0
     #
     #list of record type
     #
     global  lort # list of record type
     lort=[]
     #
     # compound keys
     #
     global rec_locator
     global att_locator
     rec_locator="entry-resource-resourceType"  # use this compound key to identify new record type
     att_locator="entry-resource-"              # use this compound key to identify attribute for record type
     #
     # check argument
     #
     if len( sys.argv ) != 2    :
          print("Usage:python json_to_csv.py <dir path containg json files>")
          sys.exit(1)
     #
     # validate directory path
     #
     dir_path=sys.argv[1]
     if not os.path.exists(dir_path) :
          print(f"ERROR:Directory path,{dir_path} does not exist")
          sys.exit(1)
     #    
     if not load_att_ref_file()  :
          sys.exit(1)
     #
     # load and process each file
     # lof=list of json files.
     #
     lof=[fname for fname in os.listdir(dir_path) if "json" in fname.split(".") ]
     if len(lof) == 0 :
          print(f"INFO:Directory,{dir_path} does not contain any json files")
          sys.exit(1)

     for fname in lof :
          file=f"{dir_path}/{fname}"
          if not load_json_file (file)  :
               sys.exit(1)
         
          if not create_csv_file() :
               sys.exit(1)
    
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
main ()
