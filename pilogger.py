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
from PyQt4 import QtCore, QtGui, uic

qtCreatorFile = "/home/swaite/Hacking/pilogger/pilogger.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class piloggergui(QtGui.QMainWindow, Ui_MainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.log_button.clicked.connect(self.LogContact)
        self.lookup_button.clicked.connect(self.SearchContact)

    def LogContact():
        #read from mode/freq/call/grid and write to db
        #update last 3
        #clear call and grid


        #foo = self.lineedit.text() where lineedit is the name of the linedit object

    def SearchContact():
        #read from call, find db entries with that call
        #display in lookup box with warning if dupe (otherwise, just where else
        #they have been worked)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = piloggergui()
    window.show
    sys.exit(app.exec_())
