from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import pymongo

from PyQt5.uic import loadUiType

ui,_ = loadUiType('taxi.ui')

mongo = pymongo.MongoClient('mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false')
db = mongo.form

class MainApp(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handel_UI_Changes()
        self.Handel_Buttons()

    def Handel_UI_Changes(self):
        self.Hiding_Themes()
        self.tabWidget.tabBar().setVisible(False)

    def Handel_Buttons(self):
        self.pushButton_8.clicked.connect(self.Show_Themes)
        self.pushButton_9.clicked.connect(self.Hiding_Themes)

        self.PushButton.clicked.connect(self.Open_Booking_Tab)
        self.pushButton_2.clicked.connect(self.Open_Setting_Tab)

    def Show_Themes(self):
        self.groupBox_3.show()
    
    def Hiding_Themes(self):
        self.groupBox_3.hide()
    
    ############################
    """
        Opening Tab
    """

    def Open_Booking_Tab(self):
        self.tabWidget.setCurrentIndex(0)

    def Open_Setting_Tab(self):
        self.tabWidget.setCurrentIndex(1)
    
    ############################

def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()