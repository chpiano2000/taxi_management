from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from datetime import date, datetime
import socketservice
import time

from controller.controller import *

login_admin,_ = loadUiType('GUI/login_admin.ui')
ui_admin,_ = loadUiType('GUI/main_admin.ui')

class Login_Admin(QWidget, login_admin):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.Handel_Login)
    
    def Handel_Login(self):
        gmail = self.lineEdit.text()
        password = self.lineEdit_2.text()

        data = check_admin(gmail, password)

        if gmail == '' or password == '' :
            self.label.setText('Please fill in the form')
        elif data :
            if password != data[0]['password']:
                self.label.setText('Password or Email is not match')
            else: 
                self.window2 = MainApp_Admin()
                self.close()
                self.window2.show()
        else:
            self.label.setText('Password or Gmail is not match')

class MainApp_Admin(QMainWindow, ui_admin):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handel_UI_Changes()
        self.Handel_Buttons()
        self.handel_data_user()
        self.handel_data_driver()
    
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
        self.handel_data_user()
        self.handel_data_driver()
        print(n)
        self.statusBar().showMessage(str(n))
    
    def Handel_UI_Changes(self):
        self.Hiding_Themes()
        self.tabWidget.tabBar().setVisible(False)
    
    def Handel_Buttons(self):
        self.pushButton_8.clicked.connect(self.Show_Themes)
        self.pushButton_9.clicked.connect(self.Hiding_Themes)
        self.PushButton.clicked.connect(self.Open_Booking_Tab)
        self.pushButton_2.clicked.connect(self.Open_Setting_Tab)
        self.pushButton_3.clicked.connect(self.Log_Out)

        self.pushButton_4.clicked.connect(self.Dark_Blue_Theme)
        self.pushButton_5.clicked.connect(self.Dark_Grey_Theme)
        self.pushButton_6.clicked.connect(self.Dark_Orange_theme)
        self.pushButton_7.clicked.connect(self.Dark_Theme)
    
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
    
    def Show_Themes(self):
        self.groupBox_3.show()
    
    def Hiding_Themes(self):
        self.groupBox_3.hide()
    
    def Open_Booking_Tab(self):
        self.tabWidget.setCurrentIndex(0)

    def Open_Setting_Tab(self):
        self.tabWidget.setCurrentIndex(1)
    
    def Log_Out(self):
        self.close()

    def handel_data_user(self):
        data = query_by_user()
        
        convert_datetime = lambda x: date(datetime.fromtimestamp(x).year, datetime.fromtimestamp(x).month, datetime.fromtimestamp(x).day)


        final_data = []
        for i in range(len(data)):
            final_data.append(list(data[i].values()))
        
        self.tableWidget_2.setRowCount(0)        
        self.tableWidget_2.insertRow(0)

        for row, form in enumerate(final_data):
            for column, item in enumerate(form):
                if type(item) == int:
                    self.tableWidget_2.setItem(row, column, QTableWidgetItem(str(convert_datetime(item))))
                else:    
                    self.tableWidget_2.setItem(row, column, QTableWidgetItem(str(item)))
                column+=1
            row_position = self.tableWidget_2.rowCount()
            self.tableWidget_2.insertRow(row_position)
        
        self.signalUpdate()
    
    def handel_data_driver(self):
        data = query_by_driver()
        
        convert_datetime = lambda x: date(datetime.fromtimestamp(x).year, datetime.fromtimestamp(x).month, datetime.fromtimestamp(x).day)


        final_data = []
        for i in range(len(data)):
            final_data.append(list(data[i].values()))
        
        self.tableWidget.setRowCount(0)        
        self.tableWidget.insertRow(0)

        for row, form in enumerate(final_data):
            for column, item in enumerate(form):
                if type(item) == int:
                    self.tableWidget.setItem(row, column, QTableWidgetItem(str(convert_datetime(item))))
                else:    
                    self.tableWidget.setItem(row, column, QTableWidgetItem(str(item)))
                column+=1
            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)
        
        self.signalUpdate()
    
    def setting(self):
        old_name = self.lineEdit_3.test()
        new_name = self.lineEdit_4.text()
        password = self.lineEdit_5.text()

        if old_name == '' or new_name == '' or password == '':
            self.label.setText('please fill in the form')
        elif check_admin(old_name, password) == []:
            self.label.setText('old name or password is not correct')
        else:
            update_name_admin(old_name, new_name)
            self.label.setText('update success')

