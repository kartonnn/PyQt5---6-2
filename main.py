import sys
from PyQt5 import uic
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QMainWindow
from PyQt5.QtGui import QPixmap, QIcon

SC = [500, 500]
dic_val = {'USD': 95, 'EUR': 101}
dic = {}


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('logo.jpg'))
        uic.loadUi('logg.ui', self)
        self.vot.clicked.connect(self.vxod)
        self.zareg.clicked.connect(self.zaregg)
        self.setGeometry(500, 500, *SC)
        self.setWindowTitle('ВХОД')
        self.password_input.setEchoMode(QLineEdit.Password)

    def vxod(self):
        con = sqlite3.connect('vhod2.db')
        cur = con.cursor()
        res = cur.execute(f"""SELECT login FROM vhod
                                WHERE login = '{self.log_input.text()}'""").fetchone()
        res2 = cur.execute(f"""SELECT password FROM vhod
                                WHERE password = '{self.password_input.text()}'""").fetchone()
        con.commit()
        if res and res2 and (res[0] == self.log_input.text() and res2[0] == self.password_input.text()):
            ex2.show()
            ex.close()
        else:
            msg1 = QMessageBox()
            msg1.setWindowTitle('Неверный вход')
            msg1.setText('Такого пользователя нет / логин не правильный / пароль не правильный. Попробуйте зарегестрироваться. ')
            msg1.exec_()
            self.log_input.setText('')
            self.password_input.setText('')

    def zaregg(self):
        connect = sqlite3.connect('vhod2.db')
        cur = connect.cursor()
        cur.execute(f"""INSERT INTO vhod VALUES('{self.log_input.text()}', '{self.password_input.text()}')""")
        connect.commit()
        self.log_input.setText('')
        self.password_input.setText('')


class SecondWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('logo.jpg'))
        uic.loadUi('tor.ui', self)
        self.showw.clicked.connect(self.showw_r)
        self.change_kurs.clicked.connect(self.update_rates)
        self.change_log.clicked.connect(self.change_log_r)
        self.save.clicked.connect(self.save_r)
        self.nalog.clicked.connect(self.nalog_r)
        self.setGeometry(700, 700, 600, 600)
        self.setWindowTitle('ПОДСЧЁТ РАСХОДОВ')
        self.third_window = ThirdWindow()

    def update_rates(self):
        ex3.show()

    def save_r(self):
        name = self.trat_input.text()
        self.trat_input.setText('')
        name2 = self.type_trat_input.text()
        self.type_trat_input.setText('')
        if name2 not in dic:
            dic[name2] = int(name)
        else:
            dic[name2] += int(name)

    def showw_r(self):
        msg = QMessageBox()
        msg.setWindowTitle('Расходы')
        msg.setText(str(dic))
        msg.exec_()

    def nalog_r(self):
        self.third_window.show()

    def change_log_r(self):
        ex.show()
        ex2.close()


class ThirdWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('logo.jpg'))
        uic.loadUi('nal.ui', self)
        self.setGeometry(700, 700, 610, 610)
        self.opl.clicked.connect(self.put)
        self.setWindowTitle('НАЛОГИ')

    def put(self):
        ex4.show()


class Pict(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('logo.jpg'))
        self.setGeometry(500, 400, 500, 400)
        self.setWindowTitle('НУ РАЗ ВСЁ ОПЛАЧЕНО')
        self.pixmap = QPixmap('ptin.jpg')
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(500, 450)
        self.image.setPixmap(self.pixmap)


class Change(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('logo.jpg'))
        self.setWindowTitle('КОНВЕРТЕР ВАЛЮТ')
        uic.loadUi('change_kurs.ui', self)
        self.setGeometry(700, 700, 550, 550)
        self.ihavekurs.setPlaceholderText('Из валюты:')
        self.ihavemon.setPlaceholderText('У меня есть:')
        self.iwankurs.setPlaceholderText('В валюту:')
        self.ihavafter.setPlaceholderText('Я получу:')
        self.change.clicked.connect(self.change_r)

    def change_r(self):
        if self.ihavekurs.text() == 'USD' and self.iwankurs.text() == 'RUB':
            self.ihavafter.setText(str(int(self.ihavemon.text()) / dic_val['USD']))
        elif self.ihavekurs.text() == 'EUR' and self.iwankurs.text() == 'RUB':
            self.ihavafter.setText(str(int(self.ihavemon.text()) / dic_val['EUR']))
        elif self.ihavekurs.text() == 'RUB' and self.iwankurs.text() == 'USD':
            self.ihavafter.setText(str(int(self.ihavemon.text()) * dic_val['USD']))
        elif self.ihavekurs.text() == 'RUB' and self.iwankurs.text() == 'EUR':
            self.ihavafter.setText(str(int(self.ihavemon.text()) * dic_val['EUR']))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex2 = SecondWindow()
    ex3 = Change()
    ex4 = Pict()
    ex.show()
    sys.exit(app.exec())
