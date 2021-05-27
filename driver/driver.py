from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from datetime import date, datetime
import pymongo
import socketservice
import time
from controller.controller import *
ui_driver,_ = loadUiType('GUI/main_driver.ui')
login_driver,_ = loadUiType('GUI/login_driver.ui')
signup_driver,_ = loadUiType('GUI/signup_driver.ui')

url = 'mongodb+srv://todoAppUser:Leanbichphuong0702@cluster0.oeozu.mongodb.net/TaxniManegement?retryWrites=true&w=majority'
mongo = pymongo.MongoClient(url)


######################## Driver #####################################
class Signup_Driver(QWidget, signup_driver):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.Handel_Signup)
        self.pushButton_2.clicked.connect(self.Switch_To_Login)
    
    def Handel_Signup(self):
        name = self.lineEdit.text()
        gmail = self.lineEdit_5.text()
        sex = self.comboBox.currentText()
        password = self.lineEdit_3.text()
        confirm_password = self.lineEdit_4.text()
        car = self.lineEdit_5.text()

        data = {
            "name": name,
            "sex": sex,
            "car": car,
            "gmail": gmail,
            "password": password,
        }
        
        checker = check_driver(gmail)

        if gmail == '' or password == '' or name=='' or confirm_password == '':
            self.label_6.setText('Please fill in the form')
        elif password != confirm_password:
            self.label_6.setText('Passwords not match')
        elif checker == []:
            add_driver(data)
            self.window2 = MainApp_Driver(gmail=gmail)
            self.close()
            self.window2.show()
        else: 
            self.label_6.setText("Gmail existed")
    
    def Switch_To_Login(self):
        self.window2 = Login_Driver()
        self.close()
        self.window2.show()

class Login_Driver(QWidget, login_driver):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.Handel_Login)
        self.pushButton_2.clicked.connect(self.Switch_To_Signup)
    
    def Handel_Login(self):
        self.db = mongo.taxi_management
        gmail = self.lineEdit.text()
        password = self.lineEdit_2.text()

        data = list(self.db.drivers.find({"gmail": gmail}))

        if gmail == '' or password == '' :
            self.label.setText('Please fill in the form')
        elif data :
            if password != data[0]['password']:
                self.label.setText('Password or Email is not match')
            else: 
                self.window2 = MainApp_Driver(gmail=gmail)
                self.close()
                self.window2.show()
        else:
            self.label.setText('Password or Gmail is not match')
        
    def Switch_To_Signup(self):
        self.window2 = Signup_Driver()
        self.close()
        self.window2.show()
    
class MainApp_Driver(QMainWindow, ui_driver):
    def __init__(self, gmail):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.gmail = gmail
        self.handel_ui_change()
        self.Handel_Buttons()
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

    def update(self,n):
        #call the table refresh here
        self.Show_Booking_Info()
        print(n)
        self.statusBar().showMessage(str(n))

    def handel_ui_change(self):
        self.Hiding_Themes()
        self.tabWidget.tabBar().setVisible(False)

    def Handel_Buttons(self):
        self.pushButton_8.clicked.connect(self.Show_Themes)
        self.pushButton_9.clicked.connect(self.Hiding_Themes)
        self.pushButton_2.clicked.connect(self.Open_Setting_Tab)
        self.PushButton.clicked.connect(self.Open_Booking_Tab)
        self.pushButton_3.clicked.connect(self.Log_Out)

        self.pushButton_4.clicked.connect(self.Dark_Blue_Theme)
        self.pushButton_5.clicked.connect(self.Dark_Grey_Theme)
        self.pushButton_6.clicked.connect(self.Dark_Orange_theme)
        self.pushButton_7.clicked.connect(self.Dark_Theme)

        self.pushButton.clicked.connect(self.response_booking)
    
    def Show_Themes(self):
        self.groupBox_3.show()
    
    def Hiding_Themes(self):
        self.groupBox_3.hide()
    
    def Open_Booking_Tab(self):
        self.tabWidget.setCurrentIndex(0)

    def Open_Setting_Tab(self):
        self.tabWidget.setCurrentIndex(1)
    
    def Log_Out(self):
        from begin.begin import Begin
        self.window2 = Begin()
        self.close()
        self.window2.show()
    
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
    
    
    def Show_Booking_Info(self):
        convert_datetime = lambda x: date(datetime.fromtimestamp(x).year, datetime.fromtimestamp(x).month, datetime.fromtimestamp(x).day)
        
        data = show_history_driver()
        
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
    
    def response_booking(self):
        booking_id = self.lineEdit.text()

        if check_id(booking_id) != []:
            update_status(booking_id, self.gmail)
            self.signalUpdate()
        
    ############################
    """
        Logout button
    """
    def Log_Out(self):
        self.close()
