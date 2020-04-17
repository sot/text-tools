# Python Application which provides live (search as you type) MSID results
import re
import bs4
import requests
import os, os.path
import json
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
f = open('SSAWG_IDX.json','w')
MeetingIdx = []
mtgCnt = 0
for Meeting in Meetings:        # Text is NGRAMMED, link is stored
    MeetingIdx.append({'name' :str(Meeting['id']),'link':str(Meeting.a.get('href')),'text':str(Meeting.get_text())})
    #writer.add_document(MeetingLink=str(Meeting.a),Text=str(Meeting.text))  # assemble document               
    mtgCnt += 1
print('Num Meetings:' + str(mtgCnt))
json.dump(MeetingIdx,f)
f.close()
 
## Now searchs