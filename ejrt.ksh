#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Name     : ejrt.ksh ( extract jason record type")
# Overview : The script is used to extract record type from json file.
# Notes    : 1. The record type are stored as follows :
#                       <------5 spaces--->"resourceType": "<value>" 
#
#            2. The script is meant to work for json files, included in the assessment because it
#               uses specific json object name.
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
INPUT_FILE=${1}
#
if [ "${INPUT_FILE}" = "" ]
then
     echo "INFO:Usage:ejrt.ksh <json file>"
     exit 1

elif  [ ! -f "${INPUT_FILE}" = "" ]
then
     echo "ERROR:Invalid file, (${INPUT_FILE}}"
     exit 1

elif [ `echo "${INPUT_FILE}" |  cut -d"." -f2` != "json"  ]
then
     echo "ERROR:Invalid file extension"
     exit 1

elif [ `cat  "${INPUT_FILE}"  |  head -1` != "{" ] 
then
     echo "ERROR:Not a json file"
     exit 1

elif cat  "${INPUT_FILE}"  | grep '"resourceType"'  > /dev/null 2>&1
then
     : # valid emis json data file
else
     echo "ERROR:Not a valis emis json data file"
     exit 1
fi
#
#
S=" "
SIX_SPACES="${S}${S}${S}${S}${S}${S}"
#
clear
echo "Record Type"
echo "==========="
cat ${INPUT_FILE} | grep "^${SIX_SPACES}\"resourceType\":" | sort -u |\
         sed s/'"resourceType":'//g | sed s/'"'//g | sed s/","//g | sed s/'^ *'//

