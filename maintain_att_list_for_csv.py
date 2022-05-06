#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Name     :maintain_att_list_for_csv.py
# Overview :The function is used to maintain a list of attributes for different record types
#           that are to be included in csv files. 
#
# Notes    : 1. List of attributes stored in  here will be used to create csv files for each record type.
#            2. This script gives you option to add/remove attributes from the list.
#
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import sys
import os

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Name     :display_menu
# Overview :The function displays an interactive menu
# Notes    :
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def display_menu () : 

     while True:
          os.system("clear")

          print("#########################################")
          print("#    CSV Attributes Maintenance Menu    #")
          print("#                                       #") 
          print("#    5. Show list of attributes         #")
          print("#   10. Updates list attributes         #")
          print("#                                       #")
          print("#   99. Exit                            #") 
          print("#                                       #")
          print("#########################################")
     
          option=input("Please enter option-->") 
          if option == "5" :
               temp_file=f"/tmp/{csv_att_list_file_name}"
               command=f"rm -f  {temp_file}"
               os.system(command)
               command=f"cp {csv_att_list_file_name} {temp_file}"
               os.system(command)
               dummy=input("INFO:You're viewing the copy of original file;press any key to continue...")
               os.chmod(temp_file, 0o444)
               command=f"view {temp_file}"
               os.system(command)
               continue

          if option == "10" :
               command=f"vi {csv_att_list_file_name}"
               os.chmod(csv_att_list_file_name, 0o644)
               dummy=input("INFO:You're viewing/editing the original file;press any key to continue...")
               os.system(command)
               continue

          if option == "99" :
               sys.exit(0)
 
          dummy=input("ERROR:Invalid option entered;press any key to continue...")
     

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Name     : main
# Overview : The entry function
# Notes    :
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def main () :
   #
 
   global csv_att_list_file_name
   csv_att_list_file_name="csv_att_list.dat"
   #
   # perform sanity check
   #
   if not os.path.exists(csv_att_list_file_name) :
        print(f"ERROR:File,{csv_att_list_file_name} is missing from current directory")
        sys.exit(1)
   
   display_menu () 

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
main ()
