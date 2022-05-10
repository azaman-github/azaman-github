#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Name     :create_excel_workbook_from_csv_files.py
# Overview :The script is used to create an excel workbook with multiple worksheets from
#           a number of csv files. 
# Notes    :
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from openpyxl import Workbook
import sys
import os
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Name     :intialise_workbook 
# Overview :The function is used to initialise a workbook using global variable, wb.
# Notes    :
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def intialise_workbook () :
     global wb
     wb = Workbook()

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Name     :save_workbook 
# Overview :The function is used to save the workbook in the current directory.
# Notes    :
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def save_workbook () :
     wb_name="emis_patient_data.xlsx"
     wb.save(filename=wb_name )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Name     :create_worksheet
# Overview :The function is used to create a new worksheet from a given csv file 
# Notes    :
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def create_worksheet (csv_file) :
     #
     # define worksheet name
     # 
     ws_name=os.path.basename(csv_file).split(".")[0]
     print(f"ws_name={ws_name}")
     ws = wb.create_sheet(ws_name)
     next_row=1
     next_col=1
     with open (csv_file, "r") as fh : 
          for rec in fh :

               lov=rec.split(",")
               for val in lov :
                   cell = ws.cell(row = next_row, column = next_col)
                   cell.value = val
                   next_col += 1

               next_col=1

               next_row += 1

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Name     :main
# Overview :The entry function.
# Notes    :
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def main () :
     #
     # check for argument
     #
     if len(sys.argv)  != 2  :
          print("Usage:create_excel_spreadsheets_from_csv_files.py <dir path>")
          sys.exit(1)

     dir_path=sys.argv[1]
     #
     # validate directory path
     #
     if not ( os.path.exists(dir_path)) :
          print("ERROR:Invalid directory path")
          sys.exit(1)
     #
     # get all the csv file names
     # lof=list of files
     #
     lof=[ fname for fname in  os.listdir(dir_path) if "csv" in  fname.split(".") ] 

     intialise_workbook()

     for  fname in lof :
         create_worksheet(fname)

     save_workbook()
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
main ()
