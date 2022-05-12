List of Contents
================
1.  Requirements
2.  Constraints
3.  Attribute Selection
4.  Data Validation
5.  Data Analysis
6.  Testing Approach
7.  Requirement of Automated Testing for Inferred Schema
8.  Requirement of Automated Testing for Extracted Data
9.  Solution
10. Solution outlines
11. List of  Modules
12. Module Details
13. Furthe Development of Solution
14. List of Deliverables
15. Run instructions


REQUIREMENTS
============
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

2. The solution presented here gives the functionality to maintain a list of attributes that are to be extracted.

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

3. The attribute counts for each record type for individual file  varies from file to file

4. The aggregated count for each record from all the files are as follows:

Record Type=CarePlan Attribute Count=22
Record Type=CareTeam Attribute Count=26
Record Type=Claim Attribute Count=25
Record Type=Condition Attribute Count=17
Record Type=DiagnosticReport Attribute Count=23
Record Type=DocumentReference Attribute Count=28
Record Type=Encounter Attribute Count=31
Record Type=ExplanationOfBenefit Attribute Count=63
Record Type=Immunization Attribute Count=13
Record Type=MedicationRequest Attribute Count=16
Record Type=Observation Attribute Count=19
Record Type=Patient Attribute Count=87
Record Type=Procedure Attribute Count=13
Record Type=Provenance Attribute Count=840


Testing Approach
================
1. No auotomated testing has been performed for inferred schema because it's a big undertaking.
2. No auotomated testing has been performed for data extraction because it's a big undertaking.
3. Manual checks and use of shell script

Requirement of Automated Testing for Inferred Schema
====================================================
1. create test data set of each recoord type with all its complexity.
2. Flatten out all the nested structures 
3. Prepare list of of  all attributes , making duplicate attributes unique by appending unique sequence.
4. This will constitute the baseline records for record types and attributes.
5. Populate these structures with data 
6. Execute the script json_to_schema.py
7. Compare the output with baseline records.
 

Requirement of Automated Testing for Extracted Data
===================================================
1. create test data set of each recoord type with all its complexity
2. Keep the test dataset small and because a baseline record for data extraction needs to be created manuuly 
2. Execute the script json_to_csv.py to create csv files
4. Compare the outputs



SOLUTION DETAILS
================

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

Overview
========
The script infers minimal schema(record types and attributes) by examining all json files in a specific directory 
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

Processing Outline
==================
1. READ all json files from the specified directory

2. DEFINE record and attribute locator as follows:
     record_loc="entry-resource-resourceType"
     att_loc="entry-resource-"

3. FOR each json file
      LOAD content into python dictionary
      FOR eack key, value pair
         FLATTEN  key if it's dict
         FLATTEN  key if it's list
         IDENTIFY new record type
            FOR this record type 
               IDENTIFY attribute
               IF duplicate found ( there will be if list values are flattened)
                  MAKE it unique by appending a sequence 
         
   

            
Output   : A file called schema.dat in the current directory ( directory from which elv.ksh script is launched)    

----------------------------------------------------------------------------------------------------------------------------
Name     : json_to_csv.py
Type     : Python
input    : json file directory

Overview
========
The script creates csv files for each record type.
           For each record type,it retrievs the list of required attributes from the file and
           creates a csv file with those attributes only.
           Additionally, for child record, it adds the patient id to the csv record.

Processing Outline
==================
1. READ all json files from the specified directory
2. DEFINE record and attribute locator as follows:
     record_loc="entry-resource-resourceType"
     att_loc="entry-resource-"

3. FOR each json file
      LOAD content into python dictionary
      FOR eack key, value pair
         FLATTEN  key if it's dict
         FLATTEN  key if it's list
         IDENTIFY new record type
         CLOSE  any open file for previous record type
            FOR this record type 
               IF a csv file already exists
                   OPEN the file in append mode
                   BUILD data record
                   APPEND data record to file
               ELSE
                   OPEN the file in write  mode
                   BUILD header and data record
                   WRITE header record 
                   WRITE data record
               

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

Overview
========
The script creates an excel workbook with dedicated worksheet for each csv file.

Processing Outline
==================
INITIALISE workbook object
FOR each csv filk
   CREATE new workshhet
   POPULATE rows with csv records


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

Furthe Development of Solution
==============================
1. Develop automated testing as mentioned at the top the document

2. There is a greate deal of common processing betwwen json_to_schema.py and json_to_csv.py

3. When json_to_csv.py runs, it internally infers the schema and then proceeds to selecting the attributes  and
   credate the csv files.

4. These two scripts can be merged into a single script that will have command line switch to direct its processing.

5. I have tried to do that and then realised that by doing this increases the  processing complexity. 

6. Anyway, the solution can be extened in following ways :
          - implement a web module that will maintain the list of attributes for extraction in the database 
          - add additional visualisation tool but I think excel should stay as the tool for first line of data invetigation 
          - as well as dictating the attribute list for extraction, similar idea can be implement for source files where 
            user asks for specific data sets.


LIST OF DELIVERABLES
====================
1. Application Modules

2. Static file
     - schema.dat
     - extract_att_list.dat
     - 
3. Analysis document:
     - individual_file_att_count.dat
     - aggregated_att_count.dat 

4. Powerpoint slide for solution architecture

5. requirements.txt

6. emis_patient_data.xlsx ( sample file output)

7. ejrt.ksh (extract json record type)

RUN INSTRUCTIONS
================
1. Make the shell scriot, elv.ksh executable

2. Execute the script, elv.ksh and select option 5.
   The script will ask for a directory path where all the json files are and 
   an email address to which an email with an attachment of data extraction, will be sent.

3. The script will keep displaying progress report

4. The option, 10, 15, and 20 are self explanatory.

5. Optionally, you can try running option, 10, 15, 20.
