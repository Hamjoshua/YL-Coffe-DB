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
        self.goOnForm.pressed.connect(self.changeForm)
        self.con = sqlite3.connect('coffee.sqlite')

    def changeForm(self):
        self.setWindowTitle('Change DB')
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.pushButton.pressed.connect(self.showDB)
        self.addNewLine.pressed.connect(self.add_new_line)
        self.loadButton.pressed.connect(self.load_to_db)

    def showDB(self):
        elems = self.con.execute('''SELECT * FROM Coffee''').fetchall()

        if self.tableWidget.columnCount() == 0:
            # init tablewidget for database
            self.tableWidget.setRowCount(len(elems))
            self.tableWidget.setColumnCount(len(elems[0]))
            self.headers = ('ID', 'название сорта', "степень обжарки",
                                                        "молотый/в зернах", "описание вкуса", "цена",
                                                        "объем упаковки")
            self.tableWidget.setHorizontalHeaderLabels(self.headers)

        for x, elem in enumerate(elems):
            for y, value in enumerate(elem):
                self.tableWidget.setItem(x, y, QtWidgets.QTableWidgetItem(str(value)))

    def add_new_line(self):
        if self.tableWidget.rowCount() == 0:
            self.show_help_label('Не загружена база данных, чтобы можно было добавлять строки!')
        else:
            self.tableWidget.insertRow(self.tableWidget.rowCount())
            cur = self.con.cursor()
            que = f'insert into Coffee {self.headers} values ({self.tableWidget.rowCount() + 1}, "", "", "", "", 0, 0)'
            cur.execute(que)
            self.con.commit()
            self.showDB()

    def load_to_db(self):
        if self.tableWidget.rowCount() == 0:
            self.show_help_label('Нечего выгружать!')
        else:
            que = 'update Coffee set \n'
            cur = self.con.cursor()
            for row in range(self.tableWidget.rowCount()):
                for column in range(self.tableWidget.columnCount()):
                    id = self.tableWidget.item(row, 0).text()
                    elem = self.tableWidget.item(row, column).text()
                    header = self.tableWidget.horizontalHeaderItem(column).text()
                    que += f'[{header}] = "{elem}"\nWHERE ID = {id}'
                    cur.execute(que)
                    self.con.commit()
                    que = 'update Coffee set \n'

            self.show_help_label('Данные успешно выгружены!')

    def show_help_label(self, text):
        self.label.setText(text)
        timer = QtCore.QTimer()
        timer.singleShot(3000, lambda: self.label.setText(''))



if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())