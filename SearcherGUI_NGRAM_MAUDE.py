#!/usr/bin/env python


#############################################################################
##
## Copyright (C) 2013 Riverbank Computing Limited.
## Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
## All rights reserved.
##
## This file is part of the examples of PyQt.
##
## $QT_BEGIN_LICENSE:BSD$
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
##     the names of its contributors may be used to endorse or promote
##     products derived from this software without specific prior written
##     permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
## $QT_END_LICENSE$
##
#############################################################################

from PyQt5 import QtGui
from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget)
from whoosh import index
from whoosh.qparser import MultifieldParser
from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED, NGRAM, NGRAMWORDS
from whoosh.qparser import QueryParser
from whoosh.qparser import FuzzyTermPlugin
from whoosh import scoring
from whoosh.collectors import TimeLimitCollector
from whoosh.highlight import WholeFragmenter
import json
import urllib.parse
import urllib.request
import urllib.response
import csv
def getLatestValues(results,MaudeList):
    """ returns the latest values for the list of search results
    parameter res:  list of Whoosh Results with 'msid' field
    return returnDict: Dictionary of MSID : Latest Value
    """
    url_base = 'https://occweb.cfa.harvard.edu/maude/mrest/FLIGHT/msid.json?jsonfmt=PW&'
    msid_tuples = []  # build string for encoding
    returnDict = {}
    for res in results:
        if res.upper() in MaudeList:        # only ask for data in Maude
            msid_tuples.append(('m', res.upper()))
            returnDict[res.upper()] = 'NO DATA'
        else:
            returnDict[res.upper()] = 'NOT IN MAUDE'
    url_full = url_base + urllib.parse.urlencode(msid_tuples)
    print(results)
    print(url_full)
    if len(msid_tuples) > 0:
        MaudeGet = urllib.request.urlopen(url_full)
        jsonRaw = MaudeGet.read()
        if len(jsonRaw) > 0:
            jsonData = json.loads(jsonRaw)            
            points = jsonData['data-fmt-6']['points']  # strip time data for now, just return msid /value pairs
            for el in points:
                returnDict = {**returnDict, **el['v']}    #Dictonary append
    return returnDict
    
        
    
   
class WidgetGallery(QDialog):
    def __init__(self, parent=None):
        super(WidgetGallery, self).__init__(parent)

        self.originalPalette = QApplication.palette()

        searchTextBox = QLineEdit()
        

        searchLabel = QLabel("&Search:")
        searchLabel.setBuddy(searchTextBox)
        # Whoosh constructs
        # MSID_index_dir = 'MSID_idx_TEXTONLY'                             #   Currently hard-coded, should be configurable or passed at the command line   
        MSID_index_dir = 'MSID_idx_TDB_CDB' 
        self.ix = index.open_dir(MSID_index_dir)                         #  
        Searchable = ('msid','technical_name','description')             # Currently hard-coded, should be configurable or passed at the command line
        self.qp = MultifieldParser(Searchable, schema=self.ix.schema)    # Search all the specified fields 
        self.MaxResults = 100
        searchTextBox.textChanged[str].connect(self.doSearch)            # hook up as-you-type event to query function
        # Maude Data 
        self.MaudeList =[] 
        with open('MAUDE_MSIDs.csv', newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                self.MaudeList.append(row[0].upper())
        #Throttle MAUDE requests
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.QueryMaudeTimer)
        self.timer.start(500)
        self.results = []
        self.AllowMaude = True
        # QT widgets,  layout and style
        self.useStylePaletteCheckBox = QCheckBox("&Use style's standard palette")
        self.useStylePaletteCheckBox.setChecked(True)
        self.useStylePaletteCheckBox.toggled.connect(self.changePalette)
        self.searchResults = QTextEdit()
        self.MaudeResults  = QTextEdit()
        
        topLayout = QHBoxLayout()
        topLayout.addWidget(searchLabel)
        topLayout.addWidget(searchTextBox)

        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0, 1, 6)
        mainLayout.addWidget(self.searchResults, 1, 0,3,4)
        mainLayout.addWidget(self.MaudeResults, 1, 5,3,2)     
        mainLayout.setColumnStretch(1,4)
        mainLayout.setColumnStretch(5,1)
        mainLayout.setColumnStretch(6,1)
        self.setLayout(mainLayout)
        
        self.setWindowTitle("MSID Live Search")
        QApplication.setStyle(QStyleFactory.create("Fusion"))
        self.changePalette()
        
    def QueryMaudeTimer(self):
        numMaude = min(8,len(self.results))
        if len(self.results) > 0:
            MaudeVals = getLatestValues(self.results[0:numMaude],self.MaudeList)
            self.MaudeResults.clear()
            for res in self.results[0:numMaude]:    
                self.MaudeResults.append(MaudeVals[res.upper()])
            cursor = self.MaudeResults.moveCursor(QtGui.QTextCursor.Start)     # return cursor to beginning of search results     
        self.results = [] # once displayed clear results to disable redundant queries
        self.timer.start(1000)
        
    def doSearch(self, text):
        q = self.qp.parse(text)          # build query with event-provided search key
        with self.ix.searcher(weighting = scoring.BM25F) as s:    # there are several NLP style scorers for Whoosh
            c = s.collector(limit=self.MaxResults)                # The "collector" allows setting the timeout for a search. In this case it's 0.5 seconds which is a little long...
            c = TimeLimitCollector(c,0.5)               
            try:
                s.search_with_collector(q,c)
            except:
                print("TIMEOUT!")                       # DEBUG out put to console if we're timing out a lot  
            results = c.results()                       # If we do get a timeout, still return whatever we've got, i.e. partial results 
                                                        #-----------------------------------------------------
            self.searchResults.clear()                  # ** Now format the results for display ** 
            results.fragmenter = WholeFragmenter()      # we want the full technical name not just the local context.
            self.MaudeResults.clear()                  # Clear
            if len(results)> 0:
                self.results = [] 
                for res in results:
                    self.results.append(res['msid'])
                    HighLightedMsid = res.highlights('msid')  # construct MSID string with highlights, if that's where the match is... 
                    if len(HighLightedMsid) >0:
                        msid_str = HighLightedMsid
                    else:
                        msid_str = res['msid']
                    HighLightedTechName = res.highlights('technical_name')  # construct technical_name string with highlights, if relevant
                    if len(HighLightedTechName) >0:
                        tech_str = HighLightedTechName
                    else:
                        tech_str = res['technical_name']
                    self.searchResults.append(msid_str + ' - ' + tech_str)
            cursor = self.searchResults.moveCursor(QtGui.QTextCursor.Start)     # return cursor to beginning of search results     
     


    def changePalette(self):
        if (self.useStylePaletteCheckBox.isChecked()):
            QApplication.setPalette(QApplication.style().standardPalette())
        else:
            QApplication.setPalette(self.originalPalette)

    

  

   

   

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    gallery = WidgetGallery()
    gallery.show()
    sys.exit(app.exec_()) 