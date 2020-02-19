# Python Application which provides live (search as you type) MSID results
import csv
import os, os.path
from whoosh import index
from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED, NGRAM, NGRAMWORDS
from whoosh.qparser import QueryParser


## Input - CSV export from AccessDB
MSID_CSV_fname = 'TDB_MSID.csv'
with open(MSID_CSV_fname, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    fieldnames = reader.fieldnames



## Input - list of fieldnames what are to be NGRAMMED, all others are text
NgramList = ('MSID','TECHNICAL_NAME','DESCRIPTION')
NgramMin = 2  ## Min characters to search on
NgramMax = 8  ## Max characters to search on
## Create Empty Schema (could be pulled into a separate file and done once)
schema = Schema()                                                            # 
                  
## Create Index  (could be pulled into a separate file and done once)
MSID_index_dir = 'MSID_idx_7'                                #   Relative to current path.  
                                                            #   TBD: add cmdline flag to set/use a particular index
if not os.path.exists(MSID_index_dir):
     print("Not there")
     os.mkdir(MSID_index_dir)

  

 
 ## Add fields programmatically by parsing the first line of the file
Searchable = ('MSID','TECHNICAL NAME', 'DESCRIPTION')        ## List of fieldnames to search on, others are 
with open(MSID_CSV_fname, newline='') as csvfile:
    ix = index.create_in(MSID_index_dir, schema)
    writer = ix.writer() 
    reader = csv.DictReader(csvfile)
    for field in fieldnames:
        print(field)
        if field in Searchable:            
            writer.add_field(field, NGRAMWORDS(minsize=2,maxsize=8))   # May need to adjust size to allow for description 
        else:
            writer.add_field(field, TEXT(stored=True))                            
    for row in reader:                
        writer.add_document(**row)        
writer.commit()
 
 
## Now search