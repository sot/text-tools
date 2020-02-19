# Python Application which provides live (search as you type) MSID results
import csv
import os, os.path
from whoosh import index
from whoosh.qparser import MultifieldParser
from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED, NGRAM, NGRAMWORDS
from whoosh.qparser import QueryParser

## Constants
NgramList = ('MSID','TECHNICAL_NAME','DESCRIPTION')   # fields to search
## Input - what am I searching for?
MyQuery = "CCDM"
MSID_index_dir = 'MSID_idx_7'                               #   Relative to current path.                   
## Open Index 
ix = index.open_dir(MSID_index_dir)                         #   TBD: add cmdline flag to set/use a particular index
Searchable = ('MSID','TECHNICAL NAME', 'DESCRIPTION')        ## List of fieldnames to search on, others are 
qp = MultifieldParser(Searchable, schema=ix.schema)
q = qp.parse(MyQuery)
ix = index.open_dir(MSID_index_dir)  
with ix.searcher() as s:    
    results = s.search(q)
    print(len(results))
    for res in results:
        print(res['TECHNICAL_NAME'])
    