from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from begin.begin import Begin
import sys

def main():
    app = QApplication(sys.argv)
    window = Begin()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
