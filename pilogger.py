#! /usr/bin/env python

#CREATE TABLE "qsos"("id" INTEGER PRIMARY KEY,"date" VARCHAR NOT NULL,
#"time" VARCHAR NOT NULL,"freq" REAL NOT NULL,"rx_freq" REAL NULL,
#"mode" VARCHAR NOT NULL,"dxcc" INTEGER NULL,"grid" VARCHAR NULL,
#"state" VARCHAR NULL,"name" VARCHAR NULL,"notes" VARCHAR NULL,
#"xc_in" VARCHAR NULL,"xc_out" VARCHAR NULL,"rst_rcvd" VARCHAR NOT NULL,
#"rst_sent" VARCHAR NOT NULL,"itu" INTEGER NULL,"waz" INTEGER NULL,
#"call" VARCHAR NOT NULL,"prop_mode" VARCHAR NULL,"sat_name" VARCHAR NULL,
#"antenna" VARCHAR NULL,"my_call" VARCHAR NOT NULL,
#"my_qth" VARCHAR NOT NULL,"power" INTEGER NULL);

import sys
import sqlite3
import hashlib
from PyQt4 import QtCore, QtGui, uic
from time import gmtime, strftime

qtCreatorFile = "/home/swaite/Hacking/pilogger/pilogger.ui"
checkLog = "/home/swaite/Hacking/pilogger/checklog.log"
myCall = "K1SIG/R"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

#need a method of collecting QSOs from peers and inserting into DB queue
#requires way to read basic info from config file

class QSO:
    time = ""
    mode = ""
    myCall = ""
    myExchange = ""
    theirExchange = ""
    frequency = ""
    band = ""
    qso_id = ""
    theirCall = ""

    def __init__(self,mode,myCall,myexchange,call,theirexchange,freq):
        self.time =  strftime("%Y-%m-%d %H%M")
        self.band = self.GetBand(freq)
        self.frequency = freq
        self.mode = mode
        self.myExchange = myexchange
        self.myCall = myCall
        self.theirExchange = theirexchange
        self.theirCall = call
        self.qso_id = hashlib.md5().hexdigest()
 
    def qsoString():
        logstring = "{0},{1},{2},{3},{4},{5},{6}".format(self.qso_id,self.band,
            self.mode,self.time,self.myCall,self.mygrid,self.call,self.theirgrid)
        print logstring 
        return logstring

    def GetBand(freq):
        #if freq is blablabla band = 
        mhz = int(freq)
    
        if mhz >= 50 and mhz <=54:
            band = "50"
        elif mhz >= 144 and mhz <= 148:
            band = "144"
        elif mhz >= 220 and mhz <= 225:
            band = "222"
        elif mhz >= 420 and mhz <=450:
            band = "432"
        elif mhz >= 902 and mhz <= 928:
            band = "902"
        elif mhz >= 1240 and mhz <= 1300:
            band = "1.2G" 
        elif mhz >= 2300 and mhz <= 2450:
            band = "2.3G"
        elif mhz >= 3300 and mhz <= 3500:
            band = "3.4G"
        elif mhz >= 5650 and mhz <= 5925:
            band = "5.7G"
        elif mhz >= 10000 and mhz <= 10500:
            band = "10G"
        else:
            band = "INVALID"

        return band

class DBQueue:
    def __init__(self):
        print "init"

class piloggergui(QtGui.QMainWindow, Ui_MainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        #read anything in LEs and look for dupes/other bands
        #while we're at it, check for unsent Qs and send to peers
        self.log_button.clicked.connect(self.LogContact())
        #self.call_le.textChanged.connect(updateCallBox())

    def LogContact(self):
        #we need to fail out if one of 5 items is missing
        #read from mode/freq/call/grid
#(self,mode,myCall,myexchange,call,theirexchange,freq)
#        currentQ = QSO(self.mode_le.text(),myCall,self.mygrid_le.text())
        mode = self.mode_le.text()
        freq = self.freq_le.text().toFloat()
        call = self.call_le.text()
        mygrid = self.mygrid_le.text()
        theirgrid = self.theirgrid_le.text()
        myCall = "WA1TE"
    
        #since we have that data, now create a QSO object
        contact = QSO.__init__(mode,myCall,mygrid,call,theirgrid,freq)
   
        #write out to checklog
        writelog = open(checkLog,'w')
        writelog.write(contact.qsoString())
        
        #insert it into the db write queue
                
        #clear call and grid
        self.call_le.clear()
        self.theirgrid_le.clear()

        #foo = self.lineedit.text() where lineedit is the name of the linedit object

    def SearchContact():
        print "Not implemented"
        #read from call, find db entries with that call
        #display in lookup box with warning if dupe (otherwise, just where else
        #they have been worked)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = piloggergui()
    window.show()
    sys.exit(app.exec_())
