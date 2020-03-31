# Python Application which provides live (search as you type) MSID results
import re
import bs4
import requests
import os, os.path
from whoosh import index
from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED, NGRAM, NGRAMWORDS
from whoosh.qparser import QueryParser
## TBD: Script Version of index creation, Need to functionify

## Input - url from OccWeb
SSAWG_IDX_URL = 'https://asc.harvard.edu/mta/ASPECT/twiki-wg/ssawg_index.html'
try:
    response = requests.get(SSAWG_IDX_URL)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
except:
    response = []
    soup = []
    print('Bad URL')
    
## Process to each meeting's tag
Meetings = soup.find_all(id=re.compile('StarWorkingGroupMeeting*'))

# Get ready to add to index
fieldnames = ['MeetingLink','Text',]

print('TO NGRAMS')
## Input - list of fieldnames what are to be NGRAMMED, all others are text
NgramList = ('Text',) # only search the text field
NgramMin = 3  ## Min characters to search on
NgramMax = 10  ## Max characters to search on
## Create Empty Schema (could be pulled into a separate file and done once)
## Create Index  (could be pulled into a separate file and done once)
schema = Schema()                                                            # 
SSAWG_index_dir = 'SSAWG_idx_2'                                #   Relative to current path.  
                                                            #   TBD: add cmdline flag to set/use a particular index
if not os.path.exists(SSAWG_index_dir):
     print("Creating index folder...")
     os.mkdir(SSAWG_index_dir)
 
 ## Add fields programmatically by parsing the first line of the file

Searchable = ('Text',)

ix = index.create_in(SSAWG_index_dir, schema)
writer = ix.writer() 
for field in fieldnames:
    if field in Searchable: 
        print(field)
        writer.add_field(field, NGRAMWORDS(minsize=NgramMin,maxsize=NgramMax,stored=True))   # May need to adjust size to allow for description            
    else:
        writer.add_field(field, TEXT(stored=True,chars=True))        
mtgCnt = 0
for Meeting in Meetings:        # Text is NGRAMMED, link is stored
    #print('-----------------')
    #print(str(Meeting.text))
    StrippedText = ''
    for item in Meeting.find_all('li'):     # for each list item...
        if item.text:
            CurStrip = item.text
        else:
            CurStrip =''
        StrippedText += CurStrip.strip() + '\n'
    writer.add_document(MeetingLink=str(Meeting.a),Text=StrippedText)  # assemble document
    #writer.add_document(MeetingLink=str(Meeting.a),Text=str(Meeting.text))  # assemble document               
    mtgCnt += 1
print('Num Meetings:' + str(mtgCnt))
writer.commit()
 
 
## Now searchs