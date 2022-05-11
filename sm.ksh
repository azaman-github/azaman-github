#! /bin/ksh
###################################################################################################################################
# Name     : sm.ksh ( send mail )
# Overview : The script is used to send a mail with an attachment .
# Notes    : 
#
#  History
#  Date         Author     Description
#  ------------------------------------------------------------------------------------------------------------------------------
#  06/05/2022   Arif Zaman    Inital creation
#
###################################################################################################################################
#
##################################################################################################################################
# Name     : initialise_variables
# Overview : The function initialises all variables
# Notes    :
#
##################################################################################################################################
initialise_variables ()
{
USAGE="Usage:sm.ksh <attachment file name> <recipient email address>"
SUBJECT="Your Requested Data"
TRUE=0
FALSE=1
TEMP_FILE=/tmp/$$.dat
}
#
#
#
##################################################################################################################################
# Name     : send_mail
# Overview : The function sends mail to a list of recipients.
# Notes    :
#
##################################################################################################################################
send_mail ()
{
#
echo "File name=${FILE_NAME}"
echo "Email Address=${EMAIL_ADDRESS}"
#
mailx  -s "${SUBJECT}" -a ${FILE_NAME} ${EMAIL_ADDRESS}   <<EOF    > ${TEMP_FILE}  2>&1
Please see attached for your requested data.
Please contact Arif at Arif.Zaman@hotmail.co.uk for any clarifications.

Kind Regards
Arif Zaman

EOF
#
if [ $? -ne 0 ]
then
     echo "ERROR:Failed to send the email to ${EMAIL_ADDRESS} because of `cat ${TEMP_FILE}`"
     echo -n "Press any key to continue..."
     read DUMMY
fi
  
#
#
}
#
#
##################################################################################################################################
# Name     : main
# Overview : The entry function.
# Notes    :
##################################################################################################################################
main ()
{
initialise_variables 
#
# check argument count
#
if [ $ARGC -ne 2  ]
then
     echo "Invalid number of arguments"
     echo "${USAGE}"
     echo -n "Press any key to continue..."
     read DUMMY
     exit 1
fi
#
# parse command line
#
FILE_NAME=`echo ${ARGV} | cut -d" " -f1`
EMAIL_ADDRESS=`echo ${ARGV} | cut -d" " -f2`
#
send_mail
#
}
#
# package the command line arguments
#
ARGC=$#
ARGV=$@
#
# invoke main
#
main

