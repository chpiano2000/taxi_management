from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from datetime import date, timedelta, datetime
import sys
import pymongo

from PyQt5.uic import loadUiType

ui,_ = loadUiType('taxi.ui')

url = 'mongodb+srv://todoAppUser:Leanbichphuong0702@cluster0.oeozu.mongodb.net/TaxniManegement?retryWrites=true&w=majority'
mongo = pymongo.MongoClient(url)

class MainApp(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handel_UI_Changes()
        self.Handel_Buttons()

        self.Show_Taxi_Driver_Combobox()
        self.dateTimeEdit.setDateTime(QDateTime.currentDateTime())

        self.Show_Booking_Info()

    def Handel_UI_Changes(self):
        self.Hiding_Themes()
        self.tabWidget.tabBar().setVisible(False)

    def Handel_Buttons(self):
        self.pushButton_8.clicked.connect(self.Show_Themes)
        self.pushButton_9.clicked.connect(self.Hiding_Themes)

        self.PushButton.clicked.connect(self.Open_Booking_Tab)
        self.pushButton_2.clicked.connect(self.Open_Setting_Tab)

        self.pushButton_10.clicked.connect(self.Change_Info)
        self.pushButton_11.clicked.connect(self.Rating)
        self.pushButton.clicked.connect(self.Input_Booking_Info)

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
    """
        Detail in settings
    """
    def Change_Info(self):
        self.db = mongo.taxi_management

        name = self.lineEdit_3.text()
        gmail = self.lineEdit_4.text()
        password = self.lineEdit_5.text()
        confirm_password = self.lineEdit_6.text()

        if name == '' or gmail == '' or password == 'None' or confirm_password == 'None':
            self.statusBar().showMessage('Please fill in the form')
        elif password != confirm_password:
            self.statusBar().showMessage('Password is not match')
        elif list(self.db.users.find({'password': password})):
            self.db.users.update_one({'password': password}, {"$set": {"name": name, "gmail": gmail}})
            self.statusBar().showMessage('Information Changed')
        
        name = self.lineEdit_3.setText('')
        gmail = self.lineEdit_4.setText('')
        password = self.lineEdit_5.setText('')
        confirm_password = self.lineEdit_6.setText('')
    
    ############################
    """
        Detail in booking: booking tab
    """
    def Show_Taxi_Driver_Combobox(self):
        self.db = mongo.taxi_management
        data = list(self.db.drivers.find({}, {"name": 1}))

        for i in range(len(data)):
            self.comboBox.addItem(data[i]['name'])
    
    def Input_Booking_Info(self):
        self.db = mongo.taxi_management
        convert_unix = lambda x: int(datetime.timestamp(x))
        
        time = self.dateTimeEdit.dateTime()
        driver = self.comboBox.currentText()
        location = self.lineEdit.text()
        destination = self.lineEdit_2.text()

        data = {
            "time": convert_unix(time.toPyDateTime()),
            "driver": driver,
            "location": location,
            "destination": destination
        }
        if location == '' :
            self.statusBar().showMessage('Please fill in the location')
        elif destination == '':
            self.statusBar().showMessage('Please fill in the destination')
        else:
            self.db.users.update_one({"name": 'aiden'}, {"$push": {'histories': data}})

        self.Show_Booking_Info()
        
    def Show_Booking_Info(self):
        self.db = mongo.taxi_management
        convert_datetime = lambda x: date(datetime.fromtimestamp(x).year, datetime.fromtimestamp(x).month, datetime.fromtimestamp(x).day)
        pipeline = [
            {
                '$unwind': {
                    'path': '$histories'
                }
            }, {
                '$project': {
                    'time': '$histories.time', 
                    'driver': '$histories.driver', 
                    'location': '$histories.location', 
                    'destination': '$histories.destination'
                }
            }
        ]

        data = list(self.db.users.aggregate(pipeline))

        self.tableWidget.setRowCount(0)        
        self.tableWidget.insertRow(0)

        for row, form in enumerate(data):
            # print(data)
            for column, item in enumerate(list(form.values())):
                self.tableWidget.setItem(row, column, QTableWidgetItem(str(item)))
                column+=1
            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)

    
    ############################
    """
        Detail in booking: rating tab
    """
    def Rating(self):
        self.db = mongo.taxi_management

        star = self.comboBox_3.currentText()
        rating = self.plainTextEdit.toPlainText()
        driver = self.comboBox.currentText()

        self.db.drivers.update_one({"name": driver}, {"$push": {"star": {"star": star, "rating": rating}}})
        self.statusBar().showMessage('Saved rating information')

        rating = self.plainTextEdit.setPlainText('') 


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()