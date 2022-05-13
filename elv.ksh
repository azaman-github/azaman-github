#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Name     : elv.ksh (Extarct Load Visualise)
# Overview : The shell script is used to execute python scripis to visiualise json data
#            in excel workbook.
# Notes    :
# History
# Date        Author    Description
#------------------------------------------------------------------------------------------
# 08/05/2022  A Zaman   Initial Creation
# 13/05/2022  A Zaman   Modified perform_sanity_check () 
#                       removed check for infer_minimal_json_schema.py 
#                       added check for json_to_schema.py 
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Name     :initialise_variables ()
# Overview :The function initialises all global variables 
# Notes    :
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
initialise_variables ()
{

TRUE=0
FALSE=1
#
# terminal capabilities
#
OS=`uname`
if [ "${OS}" = "Windows_NT"  ]
then
    BO="tput smso"
    BOO="tput smso"
else
    BO=`tput smso`
    BOO=`tput rmso`
fi
#
# coloir schema
#
RED="[1;31m"
BLUE="[0;34m"
NC="[0m"
#
BOLD=$(tput bold)
NORM=$(tput sgr0)
#
# menu details
#
ROOT_MENU="${BO}Extract Load Visualise Menu (root)${BOO}"
MENU_OPTION=""
#
# define extraction attribute list file name
#
ATT_LIST_FILE="./extract_att_list.dat"
SCHEMA_FILE="./schema.dat"
#
# define temporary directory
#
TEMP_DIR="./temp"
ERROR_FILE=${TEMP_DIR}/elv.err
#
# define log directory
#
LOG_DIR="./log"
#
ATTACHMENT_FILE="\${DIR_PATH}/emis_patient_data.xlsx"
#
}
#
#
##########################################################################################
# Name     :get_yn_acknowledgement ()
# Overview : The function obtains a Yes or No acknowledgement from user.
# Input    : Question
# Notes    :
#########################################################################################
get_yn_acknowledgement ()
{
MSG="${1}"
while true
do
  echo  -n "${BLUE}${BOLD}${MSG}${NC}${NORM}"
  read REPLY

  case $REPLY  in
   Y|y ) YN_FLAG="Y"  ; # return "Y" ;; #  $TRUE ;;
         return $TRUE ;;

   N|n ) YN_FLAG="N"   ; #  return "N" ;; #  $FALSE ;;
         return $FALSE;;

    *  ) echo -n "${RED}${BOLD}ERROR:Invalid option; Press any key to continue...${NC}${NORM}";
         read DUMMMY;;
  esac
#
done
}
#
#
#
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Name     :perform_sanity_check
# Overview :The function checks to see all expected files and scripts are in current
#           directory
# Notes    :
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
perform_sanity_check ()
{
#
ERROR_FILE="/tmp/elv.err"
#
# check for json_to_schema.py
#
if [ ! -f json_to_schema.py ]
then
     echo -n "${RED}ERROR:infer_json_schema.py script is missing from current directory;press any key to continue...${NC}"
     read DUMMY
     exit 1
fi
#
# check for schema.dat file
#
if [ ! -f ${SCHEMA_FILE}  ]
then
     echo -n "${RED}ERROR:${SCHEMA_FILE} file is missing from current directory;press any key to continue...${NC}"
     read DUMMY
     exit 1 
fi
#
# check for extract_att_list.dat
#
if [ ! -f extract_att_list.dat  ]
then
     echo -n "${RED}ERROR:extract_att_list.dat file is missing from current directory;press any key to continue...${NC}"
     read DUMMY
     exit 1     
fi
#
#
# check for json_to_csv.py
#
if [ ! -f json_to_csv.py ]
then
     echo -n "${RED}ERROR:json_to_csv.py script is missing from current directory;press any key to continue...${NC}"
     read DUMMY
     exit 1
fi
#
# check for csv_to_excel.py
#
if [ ! -f csv_to_excel.py ]
then
     echo -n "${RED}ERROR:csv_to_ecxcel.py script is missing from current directory;press any key to continue...${NC}"
     read DUMMY
     exit 1 
fi
#
# check for .temp directory
#
if [ ! -d ${TEMP_DIR} ]
then
     echo -n "${BLUE}INFO:Creating required temporary directory(${TEMP_DIR}}${NC}"
     mkdir ${TEMP_DIR} > ${ERROR_FILE} 2>&1
     if [ $? -ne 0 ]
     then
         echo "${RED}ERROR:Failed to create temporary directory(${TEMP_DIR})${NC}"
         echo -n "${RED}ERROR:`cat ${ERROR_FILE}`;press any key to continue...${NC}"
         read DUMMY
         exit 1
     fi
fi
#
#
# check for .log directory
#
if [ ! -d ${LOG_DIR} ]
then
     echo -n "${BLUE}INFO:Creating required log irectory(${LOG_DIR})${NC}"
     mkdir ${LOG_DIR} > ${ERROR_FILE} 2>&1
     if [ $? -ne 0 ]
     then
         echo -n "${RED}ERROR:Failed to create log directory(${TEMP_DIR})${NC}"
         echo -n "${RED}ERROR:`cat ${ERROR_FILE}`;press any key to continue...${NC}"
         read DUMMY
         exit 1
     fi
fi
#
#
if [ ! -f sm.ksh  ]
then
     echo -n "${RED}ERROR:sm.ksh script is missing from current directory;press any key to continue...${NC}"
     read DUMMY
     exit 1  
fi
#
#
return $TRUE
}
#
#
#
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Name     : execute_elv_scripts 
# Overview :The function executes following two python scripts and one shell script:
#              - json_to_csv.py
#              - csv_to_excel.py
#              - sm.ksh
# Notes    :
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
execute_elv_scripts ()
{
while true 
do
     clear
     echo -n "Enter json file directory path(q to quit):"
     read DIR_PATH 
     case $DIR_PATH  in
        q) return $FALSE ;;
       "") echo -n "${RED}ERROR:Must enter a directory path;press any key to continue...${NC}";
           read DUMMY ;
           continue ;;
        *) if [ ! -d ${DIR_PATH} ] ;
           then
                echo "${RED}ERROR:Directory path, ${DIR_PATH} does not exist${NC}";
                echo -n "Enter a valid directory path;press any key to continue...";
                read DUMMY ;
                continue ;
           else 
                break ;
           fi ;;
     esac
done
#
while true 
do
     clear
     echo -n "Enter recipient's email address(q to quit):"
     read EMAIL_ADDRESS in  
     case $EMAIL_ADDRESS   in
        q) return $FALSE ;;
       "") echo -n "${RED}ERROR::Must enter an email address;press any key to continue...${NC}";
           read DUMMY ;
           continue ;;
        *) break ;; 
     esac
done
#
#
echo  "${BLUE}${BOLD}INFO:Executing json_to_schema.py...${NC}${NORM}"
python json_to_schema.py ${DIR_PATH} > ${ERROR_FILE}  2>&1
if [ $? -ne 0 ]
then
    echo -n "${RED}${BOLD}ERROR:Failed to complete the execution of the script because of `cat ${ERROR_FILE}`;press any key to continue...${NC}${NORM}"
    read DUMMY
    return $FALSE
else
    echo "${BLUE}${BOLD}INFO:Successfully completed the execution of the script${NC}${NORM}"
fi
#
echo  "${BLUE}${BOLD}INFO:Executing json_to_csv.py...${NC}${NORM}"
python json_to_csv.py ${DIR_PATH} > ${ERROR_FILE}   2>&1
if [ $? -ne 0 ]
then
    echo -n "${RED}${BOLD}ERROR:Failed to complete the execution of the script because of `cat ${ERROR_FILE}`;press any key to continue...${NC}${NORM}"
    read DUMMY
    return $FALSE
else
    echo "${BLUE}${BOLD}INFO:Successfully completed the execution of the script${NC}${NORM}"
fi
#
echo  "${BLUE}${BOLD}INFO:Executing csv_to_excel.py...${NC}${NORM}"
python csv_to_excel.py ${DIR_PATH} > ${ERROR_FILE}  2>&1
if [ $? -ne 0 ]
then
    echo -n "${RED}${BOLD}ERROR:Failed to complete the execution of the script because of `cat ${ERROR_FILE}`;press any key to continue...${NC}${NORM}"
    read DUMMY
    return $FALSE
else
    echo  "${BLUE}${BOLD}INFO:Successfully completed the execution of the script${NC}${NORM}"
fi
#
# evaluate attachment file
#
ATTACHMENT_FILE=`eval echo ${ATTACHMENT_FILE}`
echo "${BLUE}${BOLD}INFO:Sensing email to ${EMAIL_ADDRESS} with attachment, ${ATTACHMENT_FILE} ...${NC}${NORM}"
#
#
sm.ksh ${ATTACHMENT_FILE}  ${EMAIL_ADDRESS} > ${ERROR_FILE}   2>&1
if [ $? -ne 0 ]
then
    echo -n "${RED}${BOLD}ERROR:Failed to send the mail because of `cat ${ERROR_FILE}`;press any key to continue...${NC}${NORM}"
    read DUMMY
    return $FALSE
else
    echo -n  "${BLUE}${BOLD}INFO:Successfully sent the email;press any key to continue...${NC}${NORM}"
    read DUMMY
    return $TRUE
fi
#
#
return $TRUE
#
#
}
#
#
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Name     : view_att_list
# Overview :The function is used to view attribute list for extraction
# Notes    :
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
view_att_list ()
{
#
# make a copy of the original file
#
cp ${ATT_LIST_FILE}  ${TEMP_DIR}/${ATT_LIST_FILE}
echo -n "${BLUE}${BOLD}INFO:You're viewing copy of the original file ;press any key to continue...${NC}${NORM}"
read DUMMY
#
view  ${TEMP_DIR}/${ATT_LIST_FILE}
}
#
#
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Name     : edit_att_list
# Overview :The function is used to edit attribute list for extraction
# Notes    :
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
edit_att_list ()
{
#
# make a copy of the original file
#
cp ${ATT_LIST_FILE}  ${TEMP_DIR}/${ATT_LIST_FILE}
echo -n "${BLUE}${BOLD}INFO:You're editing the copy of the original file ;press any key to continue...${NC}${NORM}"
read DUMMY
#
view  ${TEMP_DIR}/${ATT_LIST_FILE}
#
if get_yn_acknowledgement "Do you wish to save the edit(Y/N):"
then
     cp ${TEMP_DIR}/${ATT_LIST_FILE} ./${ATT_LIST_FILE} 
     echo -n "${BLUE}${BOLD}INFO:Successfully saved the edit;press any key to continue...${NC}${NORM}"
     read DUMMY
fi
#
#
}
#
#
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Name     :view_schema_file 
# Overview :The function is used to view inferred schema file.
# Notes    :
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
view_schema_file  ()
{
#
# make a copy of the original file
#
cp ${SCHEMA_FILE}  ${TEMP_DIR}/${SCHEMA_FILE}
echo -n "${BLUE}${BOLD}INFO:You're viewing the copy of the original file,(${SCHEMA_FILE});press any key to continue...${NC}${NORM}"
read DUMMY
#
view ${TEMP_DIR}/${SCHEMA_FILE}
#
#
}
#
#
#
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Name     : process_menu_options 
# Overview :The function processes menu options.
# Notes    :
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
process_menu_options ()
{
case ${MENU_OPTION}  in
      5)execute_elv_scripts ;;

     10)view_att_list ;;

     15)edit_att_list ;;

     20)view_schema_file ;;

     99) exit 0 ;;

      *) echo  -n "${RED}ERROR:Invalid option entered;press any key to continue...${NC}";
        read DUMMY ;;
esac
#
}
#
#
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Name     :display_root_menu
# Overview :The function displays the menu.
# Notes    :
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
display_root_menu ()
{
#
MENU_NAME=ROOT
while true
do
     clear
     echo -e  "\n\n"
     echo   "######################################"
     echo   "# ${ROOT_MENU} #"
     echo   "#                                    #"
     echo   "#  5. Run ELV scripts                #"
     echo   "# 10. View Att List for Extraction   #"
     echo   "# 15. Edit Att List for Extraction   #"
     echo   "# 20. View Inferred Schema           #"
     echo   "#                                    #"
     echo   "# 99. Exit                           #"
     echo   "#                                    #"
     echo   "#                                    #"
     echo   "######################################"
     echo  -n "      Enter Option--->"
     read MENU_OPTION
     process_menu_options
done

}
#
#
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Name     :handle_interrupt ()
# Overview :The function handles keyboard interrupt
# Notes    :
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
handle_interrupt ()
{
echo "INFO:Session interrupted;quitting early"
exit 1

}
#
#
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Name     :main
# Overview :The entry function
# Notes    :
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
main ()
{

initialise_variables 

if ! perform_sanity_check 
then
     exit 1
fi
#
#
display_root_menu 
#
#
}
#
#invoke main
#
trap "handle_interrupt"  HUP INT QUIT
main
