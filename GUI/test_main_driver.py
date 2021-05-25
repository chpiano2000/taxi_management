from datetime import date, datetime
import time
import sys
import pymongo
from PyQt5 import QtCore, QtGui, QtWidgets

url = 'mongodb+srv://todoAppUser:Leanbichphuong0702@cluster0.oeozu.mongodb.net/TaxniManegement?retryWrites=true&w=majority'
mongo = pymongo.MongoClient(url)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 487)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(150, 10, 811, 431))
        self.tabWidget.setObjectName("tabWidget")
        self.BookingCheck = QtWidgets.QWidget()
        self.BookingCheck.setObjectName("BookingCheck")
        self.comboBox = QtWidgets.QComboBox(self.BookingCheck)
        self.comboBox.setGeometry(QtCore.QRect(170, 40, 191, 25))
        self.comboBox.setObjectName("comboBox")
        self.label = QtWidgets.QLabel(self.BookingCheck)
        self.label.setGeometry(QtCore.QRect(40, 40, 101, 31))
        self.label.setObjectName("label")
        self.button_c = QtWidgets.QPushButton(self.BookingCheck, clicked = lambda: self.Handel_Buttons())
        self.button_c.setGeometry(QtCore.QRect(400, 30, 131, 61))
        self.button_c.setObjectName("button_c")
        self.tableWidget_2 = QtWidgets.QTableWidget(self.BookingCheck)
        self.tableWidget_2.setGeometry(QtCore.QRect(0, 100, 991, 361))
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(7)
        self.tableWidget_2.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(6, item)
        self.tabWidget.addTab(self.BookingCheck, "")
        self.tab2 = QtWidgets.QWidget()
        self.tab2.setObjectName("tab2")
        self.tabWidget.addTab(self.tab2, "")
        self.PushButton = QtWidgets.QPushButton(self.centralwidget)
        self.PushButton.setGeometry(QtCore.QRect(20, 70, 121, 121))
        self.PushButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/booking.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.PushButton.setIcon(icon)
        self.PushButton.setIconSize(QtCore.QSize(80, 80))
        self.PushButton.setObjectName("PushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1000, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Taxi Driver"))
        self.button_c.setText(_translate("MainWindow", "Check"))
        item = self.tableWidget_2.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Booking id"))
        item = self.tableWidget_2.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Customers"))
        item = self.tableWidget_2.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Date"))
        item = self.tableWidget_2.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Location"))
        item = self.tableWidget_2.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Destination"))
        item = self.tableWidget_2.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Status"))
        item = self.tableWidget_2.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "Rating"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.BookingCheck), _translate("MainWindow", "Tab 2"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab2), _translate("MainWindow", "Tab 1"))

    def Handel_Buttons(self):
        self.button_c.clicked.connect(self.Show_Booking_Info())

    def Show_Taxi_Driver_Combobox(self):
        self.db = mongo.taxi_management
        data = list(self.db.drivers.find({}, {"name": 1}))

        for i in range(len(data)):
            self.comboBox.addItem(data[i]['name'])

    def Show_Booking_Info(self):
        self.db = mongo.taxi_management
        convert_datetime = lambda x: date(datetime.fromtimestamp(x).year, datetime.fromtimestamp(x).month,
                                              datetime.fromtimestamp(x).day)
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
                column += 1
            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

