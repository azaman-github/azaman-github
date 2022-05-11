Requirement
===========
1. We have a number of json data files that are heavily nested.
2. Provide a solution that will help the visualisation and querying of this data

Constraints
===========
1. No jason schema available
2. No data dictionary available 

Attribute Selection
====================
1. Quite often than not, analysts want to view a subset of data , specially when
   the data record is too long and contains less important data.

2. For this exercise, following attributes are selected for viewing :
Record Type    Attribute Name
1. Patient     Gender
               birthDate
               maritalStatus-text
               multipleBirthBoolean
               address-city 
               address-state
               address-country
               address-postcode

2. Claim


3. Observation



Data  Validation
================

1. Due to not having any specified business rules, no validation will be performed

Data Analysis
=============
1. Each json file has one Patient record (master) and any nunmber of child records of following record types :

   - AllergyIntolerance
   - CarePlan
   - CareTeam
   - Claim
   - Condition
   - Device
   - DiagnosticReport
   - DocumentReference
   - Encounter
   - ExplanationOfBenefit
   - ImagingStudy
   - Immunization
   - Medication
   - MedicationAdministration
   - MedicationRequest
   - Observation
   - Procedure
   - Patient <--- master record
   - Provenance
   - SupplyDelivery

2. The child record may vary in their contents espicially in list of values for an attribute.



sample file
===========

List of record types
====================

2. Generate schema from existing files iusing python module called pyspark

sample file
===========

List of record types
====================


3. Generate schema from existing files using  python module cvalled genson 
 
sample file
===========

List of record types
====================




Solution
========
Outlines
========
1. Infer minimal schema by examining all json files

2. Store the list of attributes for all record types ( master and child record) that have ben requested, in a file 

3. Obtain email address of data requestor

4. Create csv files ( as many as there are child record types and one for master record) from each json data file.

5. Create excel workbook with each spreadsheet dedicated to a single csv file

6. Email the excel workbook to requester of data extract

7. Write a log in the logfile for this extraction

List of  Modules
================
1. json_to_schema.py 
2. json_to_csv.py       
3. csv_to_excel.py     
4. sm.ksh             
5. elv.ksh       

Module Details
==============
Name     : json_to_schema.py
Type     : Python
input    : json file directory

Overview : The script infers minimal schema(record types and attributes) by examining all json files in a specific directory 
           It flattens out dictionary and list values.
           For list values, it makes second and subsequent elements unique by appending a unique number to it.
           Example
           =======
           {
             "Patient" :
                       { "id" : "xxxx",  "gender" : "Male" },
              "visits"  : [ 
                           { "visit_date" : "xxxx", "hospital"  : "xxx" }, 
                           { "visit_date" : "xxxx", "hospital"  : "xxx" }
                          ]
           }
           Patient-id 
           Patient-gender
            
Output   : A file called schema.dat in the current directory ( directory from which elv.ksh script is launched)    

----------------------------------------------------------------------------------------------------------------------------
Name     : json_to_csv.py
Type     : Python
input    : json file directory

Overview : The script creates csv files for each record type.
           For each record type,it retrievs the list of required attributes from the file and
           creates a csv file with those attributes only.
           Additionally, for child record, it adds the patient id to the csv record.

Output   : Following csv files are created in the json file directory.
                      -  AllergyIntolerance.csv
                      -  CarePlan.csv
                      -  CareTeam.csv
                      -  Claim.csv
                      -  Condition.csv
                      -  Device.csv
                      -  DiagnosticReport.csv
                      -  DocumentReference.csv
                      -  Encounter.csv
                      -  ExplanationOfBenefit.csv
                      -  ImagingStudy.csv
                      -  Immunization.csv
                      -  Medication.csv
                      -  MedicationAdministration.csv
                      -  MedicationRequest.csv
                      -  Observation.csv
                      -  Procedure.csv
                      -  Patient..csv 
                      -  Provenance.csv
                      -  SupplyDelivery.csv

----------------------------------------------------------------------------------------------------------------------------

Name     : csv_to_excel.py
Type     : Python 
Input    : all csv files created by json_to_csv,py module
Overview : The script creates an excel workbook with dedicated worksheet for each csv file.
Output   : Excel workbook in the directory of csv files.

----------------------------------------------------------------------------------------------------------------------------
Name     : sm.ksh
Type     : ksh
Input    : Attachment and email address
Overview : The script is used to send extracted data as an attachment to requestor of data.
Output   : None
----------------------------------------------------------------------------------------------------------------------------
Name     : elv.ksh 
Type     : ksh
Input    : Depends on selected menu option 
Overview : elv stands for extract,load and visulaise
           It's a simple menu driven, single user script to perform activities related to data extraction.
           It has following menu options :
                    -  Run luv scripts                     ( run all the modules listed above in that order)              
                    -  View Attribute List for Extraction  ( allows user to view list of attributes for each record type
                                                             that will be extracted)  
                    -  Edit Attribute List for Extraction  ( allows user to edit (add/remove attributes from the list) 
                    -  View Inferred Schema                ( allows use to view the generated schema ) 
Output   : None

----------------------------------------------------------------------------------------------------------------------------


Run Instruction
===============
1. Execute the script, elv.ksh

