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
from WhooshWrap import WhooshWrap

class WidgetGallery(QDialog):
    def __init__(self, parent=None):
        super(WidgetGallery, self).__init__(parent)

        self.originalPalette = QApplication.palette()

        searchTextBox = QLineEdit()
        

        searchLabel = QLabel("&Search:")
        searchLabel.setBuddy(searchTextBox)
        # Whoosh constructs
        MSID_index_dir = 'MSID_idx_TEXTONLY'                             #   Currently hard-coded, should be configurable or passed at the command line   
        Searchable = ('msid','technical_name','description')    
        self.WhooshWrapper = WhooshWrap('MSID_idx_TDB_CDB',Searchable)      
        self.MaxResults = 100
        self.Timeout = 0.5
        searchTextBox.textChanged[str].connect(self.doSearch)            # hook up as-you-type event to query function
        
        # QT widgets,  layout and style
        self.useStylePaletteCheckBox = QCheckBox("&Use style's standard palette")
        self.useStylePaletteCheckBox.setChecked(True)
        self.useStylePaletteCheckBox.toggled.connect(self.changePalette)
        self.searchResults = QTextEdit()
        
        topLayout = QHBoxLayout()
        topLayout.addWidget(searchLabel)
        topLayout.addWidget(searchTextBox)

        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0, 1, 4)
        mainLayout.addWidget(self.searchResults, 1, 0)                
        self.setLayout(mainLayout)

        self.setWindowTitle("MSID Live Search")
        QApplication.setStyle(QStyleFactory.create("Fusion"))
        self.changePalette()
        

    def doSearch(self, text):
        CurResults = self.WhooshWrapper.doSearch(text,self.MaxResults,self.Timeout,['msid','technical_name'])   # perform Search, use wrapper dict return so Whoosh API is totally hidden        
        self.searchResults.clear()
        for msid,tech_name in zip(CurResults['msid'],CurResults['technical_name']):  
            self.searchResults.append(msid + ' - ' + tech_name)           
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