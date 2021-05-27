from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from datetime import date, datetime
import random
import pymongo
import socketservice
import time


from controller.controller import *

ui_user,_ = loadUiType('GUI/main_user.ui')
login_user,_ = loadUiType('GUI/login_user.ui')
signup_user,_ = loadUiType('GUI/signup_user.ui')

######################## USER #####################################

class Signup_User(QWidget, signup_user):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.Handel_Signup)
        self.pushButton_2.clicked.connect(self.Switch_To_Login)
    
    def Handel_Signup(self):
        
        name = self.lineEdit.text()
        gmail = self.lineEdit_2.text()
        sex = self.comboBox.currentText()
        password = self.lineEdit_3.text()
        confirm_password = self.lineEdit_4.text()

        data = {
            "name": name,
            "sex": sex,
            "gmail": gmail,
            "password": password
        }

        checker = check_user(gmail)

        if gmail == '' or password == '' or name=='' or confirm_password == '':
            self.label_6.setText('Please fill in the form')
        elif password != confirm_password:
            self.label_6.setText('Passwords not match')
        elif checker == []:
            add_users(data)
            self.window2 = MainApp_User(gmail=gmail)
            self.close()
            self.window2.show()
        else: 
            self.label_6.setText("Gmail existed")
    
    def Switch_To_Login(self):
        self.window2 = Login_User()
        self.close()
        self.window2.show()


class Login_User(QWidget, login_user):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.Handel_Login)
        self.pushButton_2.clicked.connect(self.Switch_To_Signup)
    
    def Handel_Login(self):
        gmail = self.lineEdit.text()
        password = self.lineEdit_2.text()
        
        data = check_user(gmail)

        if gmail == '' or password == '' :
            self.label.setText('Please fill in the form')
        elif data :
            if password != data[0]['password']:
                self.label.setText('Password or Email is not match')
            else: 
                self.window2 = MainApp_User(gmail=gmail)
                self.close()
                self.window2.show()
        else:
            self.label.setText('Password or Gmail is not match')
        
    def Switch_To_Signup(self):
        self.window2 = Signup_User()
        self.close()
        self.window2.show()
        

class MainApp_User(QMainWindow, ui_user):
    def __init__(self, gmail):
        self.gmail = gmail
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handel_UI_Changes()
        self.Handel_Buttons()

        self.dateTimeEdit.setDateTime(QDateTime.currentDateTime())

        self.Show_Booking_Info()

    ##### Signal update event start #####
        outside = socketservice.Outside(self, "", "")
        socketservice.mess=""
        self.thread = outside
        self.thread.update.connect(self.update)
        self.thread.start()

    def signalUpdate(self):
        socketservice.mess= "Updated database " + str(datetime.now())

    def closeEvent(self, event):
        # do stuff
        socketservice.mess="stop"
        print("exiting")
        time.sleep(1)
        self.thread.stop()
        event.accept()

    tempbookingid = ""
    def update(self,n):
        #call the table refresh here
        self.Show_Booking_Info()
        try:
            check = check_status(self.tempbookingid)
            if check[0]['status'] == 'true':
                self.label_12.setText('found your driver')
        except Exception as e:
            print(e)
        print(n)
        self.statusBar().showMessage(str(n))

    ##### Signal update event stop ######

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
    
    def status(self):
        self.label_12.setText('Driver received your booking')
    
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
        name = self.lineEdit_3.text()
        gmail = self.lineEdit_4.text()
        password = self.lineEdit_5.text()
        confirm_password = self.lineEdit_6.text()

        if name == '' or gmail == '' or password == 'None' or confirm_password == 'None':
            self.statusBar().showMessage('Please fill in the form')
        elif password != confirm_password:
            self.statusBar().showMessage('Password is not match')
        elif check_user(self.gmail):
            update_name(password, name, gmail)
            self.statusBar().showMessage('Information Changed')
        
        name = self.lineEdit_3.setText('')
        gmail = self.lineEdit_4.setText('')
        password = self.lineEdit_5.setText('')
        confirm_password = self.lineEdit_6.setText('')
    
    ############################
    """
        Detail in booking: booking tab
    """    
    def Input_Booking_Info(self):
        convert_unix = lambda x: int(datetime.timestamp(x))

        self.label_12.setText('')
        time = self.dateTimeEdit.dateTime()
        location = self.lineEdit.text()
        destination = self.lineEdit_2.text()
        booking_id = str(convert_unix(time.toPyDateTime()))

        data = {
            "booking_id": booking_id,
            "gmail_user": self.gmail,
            "time": convert_unix(time.toPyDateTime()),
            "location": location,
            "destination": destination,
            "status": "false"
        }
        if location == '' :
            self.statusBar().showMessage('Please fill in the location')
        elif destination == '':
            self.statusBar().showMessage('Please fill in the destination')
        else:
            insert_histories(data)
            self.tempbookingid = booking_id
            self.label_12.setText('Your request has been sent, please wait')
        
        location = self.lineEdit.setText('')
        destination = self.lineEdit_2.setText('')

        self.signalUpdate()
        self.Show_Booking_Info()
        
    def Show_Booking_Info(self):
        convert_datetime = lambda x: date(datetime.fromtimestamp(x).year, datetime.fromtimestamp(x).month, datetime.fromtimestamp(x).day)
        
        data = query_histories()

        self.tableWidget.setRowCount(0)        
        self.tableWidget.insertRow(0)

        for row, form in enumerate(data):
            for column, item in enumerate(list(form['histories'].values())):
                if type(item) == int:
                    self.tableWidget.setItem(row, column, QTableWidgetItem(str(convert_datetime(item))))
                else:    
                    self.tableWidget.setItem(row, column, QTableWidgetItem(str(item)))
                column+=1
            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)

    
    ############################
    """
        Detail in booking: rating tab
    """
    def Rating(self):
        star = self.comboBox_3.currentText()
        rating = self.plainTextEdit.toPlainText()
        driver = self.comboBox.currentText()

        update_driver_rating(star, rating, driver)
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
        self.close()