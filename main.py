from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from datetime import date, datetime
import time
import sys
import pymongo

from PyQt5.uic import loadUiType

ui,_ = loadUiType('GUI/taxi.ui')
login,_ = loadUiType('GUI/login.ui')
signup,_ = loadUiType('GUI/signup.ui')

url = 'mongodb+srv://todoAppUser:Leanbichphuong0702@cluster0.oeozu.mongodb.net/TaxniManegement?retryWrites=true&w=majority'
mongo = pymongo.MongoClient(url)


class Signup(QWidget, signup):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.Handel_Signup)
        self.pushButton_2.clicked.connect(self.Switch_To_Login)
    
    def Handel_Signup(self):
        self.db = mongo.taxi_management

        name = self.lineEdit.text()
        gmail = self.lineEdit_2.text()
        sex = self.comboBox.currentText()
        password = self.lineEdit_3.text()
        confirm_password = self.lineEdit_4.text()

        data = {
            "name": name,
            "sex": sex,
            "gmail": gmail,
            "password": password,
            "histories": []
        }
        
        checker = list(self.db.users.find({"gmail": gmail}))

        if gmail == '' or password == '' or name=='' or confirm_password == '':
            self.label_6.setText('Please fill in the form')
        elif password != confirm_password:
            self.label_6.setText('Passwords not match')
        elif checker == []:
            self.db.users.insert_one(data)
            self.window2 = MainApp()
            self.close()
            self.window2.setEmail(gmail)
            self.window2.show()
        else: 
            self.label_6.setText("Gmail existed")
    
    def Switch_To_Login(self):
        self.window2 = Login()
        self.close()
        self.window2.show()


class Login(QWidget, login):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.Handel_Login)
        self.pushButton_2.clicked.connect(self.Switch_To_Signup)
    
    def Handel_Login(self):
        self.db = mongo.taxi_management
        gmail = self.lineEdit.text()
        password = self.lineEdit_2.text()

        data = list(self.db.users.find({"gmail": gmail}))

        if gmail == '' or password == '' :
            self.label.setText('Please fill in the form')
        elif data :
            if password != data[0]['password']:
                self.label.setText('Password or Email is not match')
            else: 
                self.window2 = MainApp()
                self.close()
                self.window2.setEmail(gmail)
                self.window2.show()
        else:
            self.label.setText('Password or Gmail is not match')
        
    def Switch_To_Signup(self):
        self.window2 = Signup()
        self.close()
        self.window2.show()
        

class MainApp(QMainWindow, ui):
    mail = ""
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handel_UI_Changes()
        self.Handel_Buttons()

        self.Show_Taxi_Driver_Combobox()
        self.dateTimeEdit.setDateTime(QDateTime.currentDateTime())

        self.Show_Booking_Info()

    def setEmail(self, mail):
        gmail = mail

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

        self.pushButton_4.clicked.connect(self.Dark_Blue_Theme)
        self.pushButton_5.clicked.connect(self.Dark_Grey_Theme)
        self.pushButton_6.clicked.connect(self.Dark_Orange_theme)
        self.pushButton_7.clicked.connect(self.Dark_Theme)

        self.pushButton_3.clicked.connect(self.Log_Out)

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
        
        location = self.lineEdit.setText('')
        destination = self.lineEdit_2.setText('')

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
    
    ############################
    """
        Change themes
    """
    def Dark_Blue_Theme(self):
        style = open('themes/darkblue.css')
        style = style.read()
        self.setStyleSheet(style)

    def Dark_Grey_Theme(self):
        style = open('themes/darkgrey.css')
        style = style.read()
        self.setStyleSheet(style)
    
    def Dark_Orange_theme(self):
        style = open('themes/darkorange.css')
        style = style.read()
        self.setStyleSheet(style)

    def Dark_Theme(self):
        style = open('themes/dark.css')
        style = style.read()
        self.setStyleSheet(style)
    
    ############################
    """
        Logout button
    """
    def Log_Out(self):
        self.window2 = Login()
        self.close()
        self.window2.show()



def main():
    app = QApplication(sys.argv)
    window = Login()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
