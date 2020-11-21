import sys
import sqlite3
from PyQt5 import uic, QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.setWindowTitle('Espresso DB')
        self.pushButton.pressed.connect(self.showDB)

    def showDB(self):
        con = sqlite3.connect('coffee.sqlite')
        elems = con.execute('''SELECT * FROM Coffee ''').fetchall()

        if self.tableWidget.columnCount() == 0:
            # init tablewidget for database
            for x in range(len(elems)):
                self.tableWidget.insertRow(x)
            for y in range(len(elems[0])):
                self.tableWidget.insertColumn(y)

            self.tableWidget.setHorizontalHeaderLabels(['ID', 'название сорта', "степень обжарки",
                                                        "молотый/в зернах", "описание вкуса", "цена",
                                                        "объем упаковки"])

        for x, elem in enumerate(elems):
            for y, value in enumerate(elem):
                self.tableWidget.setItem(x, y, QtWidgets.QTableWidgetItem(str(value)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())