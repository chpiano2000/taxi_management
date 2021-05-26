from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType

from user.user import Login_User
from driver.driver import Login_Driver
from PyQt5.uic import loadUiType

begin,_ = loadUiType('GUI/begin.ui')

class Begin(QWidget, begin):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.Move_To_User)
        self.pushButton_2.clicked.connect(self.Move_To_Driver)
        self.pushButton_3.clicked.connect(self.Move_To_Admin)
    
    def Move_To_User(self):
        self.window2 = Login_User()
        self.close()
        self.window2.show()
    
    def Move_To_Driver(self):
        self.window2 = Login_Driver()
        self.close()
        self.window2.show()

    def Move_To_Admin(self):
        pass