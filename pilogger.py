#! /usr/bin/env python

import sys
import sqlite3
import hashlib
import ConfigParser
import os.path
import Queue
from PyQt4 import QtCore, QtGui, uic
from time import gmtime, strftime


#Globals to be read from config file
checkLog = ""
database = ""
myCall = ""
myOp = ""

#We need a queue to handle QSOs being inserted from both the local instance
#and networked instances
qso_queue = Queue.Queue()

#Load the UI file
qtCreatorFile = "pilogger.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

#need a method of collecting QSOs from peers and inserting into DB queue


def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

def createDB():

    create_table_qsos = """CREATE TABLE IF NOT EXISTS qsos (
        id TEXT PRIMARY KEY,
        band TEXT NOT NULL,
        mode TEXT NOT NULL,
        time TEXT NOT NULL,
        mycall TEXT NOT NULL,
        myexchange TEXT NOT NULL,
        theircall TEXT NOT NULL,
        theirexchange TEXT NOT NULL,
        opcall TEXT NOT NULL
        );"""

    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute(create_table_qsos)

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
        self.time =  strftime("%Y-%m-%d %H%M",gmtime())
        self.band = self.GetBand(freq)
        self.frequency = freq
        self.mode = mode
        self.myExchange = myexchange
        self.myCall = myCall
        self.opCall = myOp
        self.theirExchange = theirexchange
        self.theirCall = call
        self.qso_id = hashlib.md5().hexdigest()
 

    def qsoString(self):
        logstring = "{0},{1},{2},{3},{4},{5},{6},{7},{8}\n".format(self.qso_id,self.band,
            self.mode,self.time,self.myCall,self.myExchange,self.theirCall,self.theirExchange,self.opCall)
        print logstring 
        return logstring

    def GetBand(self,freq):
        #if freq is blablabla band = 
        mhz = freq
    
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
        elif mhz >= 24000 and mhz <= 24250:
            band = "24G"
        elif mhz >= 47000 and mhz <= 47200:
            band = "47G"
        elif mhz >= 71500 and mhz <= 81500:
            band = "75G"
        elif mhz >= 122250 and mhz <= 123000:
            band = "123G"
        elif mhz >= 134000 and mhz <= 141000:
            band = "134G"
        elif mhz >= 241000 and mhz <= 250000:
            band = "241G"
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
        self.showMaximized()
        #read anything in LEs and look for dupes/other bands
        #while we're at it, check for unsent Qs and send to peers
        self.log_button.clicked.connect(lambda: self.LogContact())
        #self.call_le.textChanged.connect(updateCallBox())

    def LogContact(self):
        #we need to fail out if one of 5 items is missing
        #read from mode/freq/call/grid

        if self.mode_le.text().isEmpty() or self.freq_le.text().isEmpty() or self.call_le.text().isEmpty() or self.mygrid_le.text().isEmpty() or self.theirgrid_le.text().isEmpty():
            print "Missing data from Q"
            return

        mode = self.mode_le.text()
        freq = self.freq_le.text().toFloat()
        call = self.call_le.text()
        mygrid = self.mygrid_le.text()
        theirgrid = self.theirgrid_le.text()
    
        #since we have that data, now create a QSO object

        contact = QSO(mode,myCall,mygrid,call,theirgrid,int(freq[0]))
   
        #write out to checklog
        writelog = open(checkLog,'a')
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
        #show us if it is a new mult, or if it is a new 

if __name__ == "__main__":

    Config = ConfigParser.ConfigParser()
    Config.read("mrlog.config")    

    myCall = ConfigSectionMap("Operator")['station_call']
    myOp = ConfigSectionMap("Operator")['operator_call'] 

    db_directory = ConfigSectionMap("Config")['db_directory']
    writelog_directory = ConfigSectionMap("Config")['writelog_directory']
   
    database = "{0}/mrlog.database".format(db_directory)
    checkLog = "{0}/checklog.log".format(writelog_directory)
 
    if not os.path.isfile(database):
        createDB()        


    app = QtGui.QApplication(sys.argv)
    window = piloggergui()
    window.show()
    sys.exit(app.exec_())
