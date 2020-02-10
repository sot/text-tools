# Python Application which provides live (search as you type) MSID results
import csv
import os, os.path
from whoosh import index




## Create Schema (could be pulled into a separate file and done once)


## Create Index  (could be pulled into a separate file and done once)
MSID_CSV_fname = 'MSIDs.csv'
MSID_index_dir = 'MSID_idx'                                 #   Relative to current path.  
                                                            #   TBD: add cmdline flag to set/use a particular index


if not os.path.exists(MSID_index_dir):
    os.mkdir(MSID_index_dir)
    ix = index.create_in(MSID_index_dir, schema)
    
 