import speech_recognition as sr

import sys

import numpy as np

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QWidget, QLineEdit, QLabel, QPushButton
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QTimer, Qt
from mail import send_mail
import cv2

from ui_main_window import *
import keyboard
import pyautogui
import sqlite3

from werkzeug.security import generate_password_hash, check_password_hash
import re


class MainWindow(QWidget):

    def __init__(self, *args):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.face_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_alt.xml')
        if self.face_cascade.empty():
            QMessageBox.information(self, "Error Loading cascade classifier",
                                    "Unable to load the face	cascade classifier xml file")
            sys.exit()


        self.timer = QTimer()
        self.timer.timeout.connect(self.detectFaces)
        self.out = cv2.VideoWriter("data/output.avi", cv2.VideoWriter_fourcc(*"XVID"), 20.0, (1920, 1080))
        self.ui.control_bt.clicked.connect(self.controlTimer)
        self.ui.control_bt2.clicked.connect(self.open_second_form)
        self.ui.control_bt3.clicked.connect(self.open_auth_form)

        if args:
            if args[1]:
                self.ui.control_bt.setEnabled(True)
                self.ui.control_bt2.setEnabled(True)
                self.name = args[2][1]
                self.ui.control_bt3.setEnabled(False)
        else:
            self.ui.control_bt2.setEnabled(False)
            self.ui.control_bt.setEnabled(False)


    def detectFaces(self):
        '''Определение лиц'''
        ret, frame = self.cap.read()

        scaling_factor = 0.8
        frame = cv2.resize(frame, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_rects = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        print(len(face_rects))
        if len(face_rects) > 1:
            write_file('Больше одного человека')
            print('Писать необходимо самому')
        elif len(face_rects) < 1:
            write_file('Нет на месте')
            print('Вернитесь на место')
        for (x, y, w, h) in face_rects:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        height, width, channel = frame.shape
        step = channel * width
        qImg = QImage(frame.data, width, height, step, QImage.Format_RGB888)
        self.ui.image_label.setPixmap(QPixmap.fromImage(qImg))

        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.out.write(frame)


    def controlTimer(self):
        '''Таймер'''
        if not self.timer.isActive():
            self.cap = cv2.VideoCapture(0)
            self.timer.start(20)
            self.ui.control_bt.setText("Остановить")
        else:
            self.timer.stop()
            self.cap.release()
            self.ui.control_bt.setText("Начать")
            self.out.release()

    def open_second_form(self):
        self.second_form = SecondForm(self, self.name)
        self.second_form.show()

    def open_auth_form(self):
        self.auth_form = AuthForm(self)
        self.auth_form.show()
        self.close()


class SecondForm(QWidget):
    '''Окно отправки отчёта'''
    def __init__(self, *args):
        super().__init__()
        self.name = args[1]
        self.initUI(args)

    def initUI(self, args):
        self.setGeometry(300, 300, 300, 116)
        self.setWindowTitle('Данные для отправки отчета')

        self.lbl2 = QLabel(self)
        self.lbl2.move(10, 10)
        self.lbl2.setText('Укажите email получателя')
        self.edit2 = QLineEdit(self)
        self.edit2.move(10, 30)

        self.btn1 = QtWidgets.QPushButton(self)
        self.btn1.setText('Отправить')
        self.btn1.clicked.connect(self.run)
        self.btn1.setStyleSheet("background-color: rgb(0, 85, 255);\n"
                                "color: rgb(255, 255, 255);")
        self.btn1.setGeometry(QtCore.QRect(10, 70, 80, 28))

    def run(self):
        '''Функция заполняет данные в файл'''
        f1 = open('data/violations.txt', 'r', encoding='utf8')
        text = f1.readlines()
        text_out = [None]
        for el in text:
            if el != text_out[-1]:
                text_out.append(el)
        text_out = ''.join(text_out[1:])
        to = self.edit2.text()
        if self.name and to:
            send_mail(self.name, text_out, self.edit2.text())
        f1.close()


class AuthForm(QWidget):
    '''Окно авторизации'''
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)

    def initUI(self, *args):
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Авторизация')

        self.lbl1 = QLabel(self)
        self.lbl1.move(10, 20)
        self.lbl1.setText('Почта')
        self.edit1 = QLineEdit(self)
        self.edit1.move(10, 40)
        self.lbl2 = QLabel(self)
        self.lbl2.move(10, 80)
        self.lbl2.setText('Пароль')
        self.edit2 = QLineEdit(self)
        self.edit2.setEchoMode(QLineEdit.Password)
        self.edit2.move(10, 100)

        self.btn1 = QtWidgets.QPushButton(self)
        self.btn1.setText('Войти')
        self.btn1.clicked.connect(self.run)
        self.btn1.setStyleSheet("background-color: rgb(0, 85, 255);\n" "color: rgb(255, 255, 255);")
        self.btn1.setGeometry(QtCore.QRect(10, 140, 130, 35))

        self.btn2 = QtWidgets.QPushButton(self)
        self.btn2.setText('Регистрация')
        self.btn2.clicked.connect(self.open_checkin_form)
        self.btn2.setStyleSheet("background-color: rgb(0, 85, 255);\n" "color: rgb(255, 255, 255);")
        self.btn2.setGeometry(QtCore.QRect(160, 140, 130, 35))

    def open_checkin_form(self):
        self.checkin_form = CheckinForm(self)
        self.checkin_form.show()

    def run(self):
        email = self.edit1.text()
        password = self.edit2.text()
        pattern = r"^[a-zA-Z0-9]{1,100}[@][a-z]{2,6}\.[a-z]{2,4}"
        number_re = re.compile(pattern)
        if number_re.findall(email):
            con = sqlite3.connect("data\mydatabase.db")
            cur = con.cursor()
            res = cur.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchall()
            if not res:
                s = QMessageBox.question(self, "Ошибка", "Данной почты не существует", QMessageBox.Yes)
            else:
                if check_password_hash(res[0][3], password):
                    self.main_form = MainWindow(self, True, res[0])
                    self.close()
                    self.main_form.show()
                else:
                    s = QMessageBox.question(self, "Ошибка", "Неправильно введен пароль", QMessageBox.Yes)
        else:
            s = QMessageBox.question(self, "Ошибка", "Неправильно введен email", QMessageBox.Yes)


class CheckinForm(QWidget):
    '''Окно регистрации'''
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)

    def initUI(self, *args):
        self.setGeometry(300, 300, 300, 350)
        self.setWindowTitle('Регистрация')
        self.lbl1 = QLabel(self)
        self.lbl1.move(10, 30)
        self.lbl1.setText('ФИО')
        self.edit1 = QLineEdit(self)
        self.edit1.move(10, 50)
        self.lbl2 = QLabel(self)
        self.lbl2.move(10, 100)
        self.lbl2.setText('Почта')
        self.edit2 = QLineEdit(self)
        self.edit2.move(10, 120)
        self.lbl3 = QLabel(self)
        self.lbl3.move(10, 170)
        self.lbl3.setText('Пароль')
        self.edit3 = QLineEdit(self)
        self.edit3.setEchoMode(QLineEdit.Password)
        self.edit3.move(10, 190)
        self.lbl4 = QLabel(self)
        self.lbl4.move(10, 230)
        self.lbl4.setText('Повторите пароль')
        self.edit4 = QLineEdit(self)
        self.edit4.setEchoMode(QLineEdit.Password)
        self.edit4.move(10, 250)
        self.btn1 = QtWidgets.QPushButton(self)
        self.btn1.setText('Зарегистрироваться')
        self.btn1.clicked.connect(self.run)
        self.btn1.setStyleSheet("background-color: rgb(0, 85, 255);\n" "color: rgb(255, 255, 255);")
        self.btn1.setGeometry(QtCore.QRect(10, 290, 190, 35))

    def run(self):
        name = self.edit1.text()
        email = self.edit2.text()
        pass1 = self.edit3.text()
        pass2 = self.edit4.text()
        pattern = r"^[a-zA-Z0-9]{1,100}[@][a-z]{2,6}\.[a-z]{2,4}"
        number_re = re.compile(pattern)
        if name and number_re.findall(email) and pass1 == pass2 and pass1:
            con = sqlite3.connect("data\mydatabase.db")
            cur = con.cursor()
            res = cur.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchall()
            if res:
                s = QMessageBox.question(self, "Ошибка", "Указанная почта существует", QMessageBox.Yes)
            else:
                cur.execute("INSERT INTO users(name, email, password) VALUES(?, ?, ?)",
                            (name, email, generate_password_hash(pass1)))
                con.commit()
            con.close()
            self.close()
        else:
            s = QMessageBox.question(self, "Ошибка", "Неправильно введены данные", QMessageBox.Yes)


def write_file(s):
    '''Функция создаёт файл'''
    f1 = open('data/violations.txt', 'a', encoding='utf8')
    f1.write(s + '\n')
    f1.close()


def command():
    '''Функция определяет шум'''
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
        print('dont speak')
        write_file('Посторонние звуки')


if __name__ == '__main__':
    f1 = open('data/violations.txt', 'w', encoding='utf8')
    f1.write('')
    f1.close()
    app = QApplication(sys.argv)
    keyboard.add_hotkey('ctrl + c', lambda: write_file('Произошло копирование'))
    keyboard.add_hotkey('ctrl + c', lambda: print('Произошло копирование'))
    keyboard.add_hotkey('ctrl + v', lambda: write_file('Произошло копирование'))
    keyboard.add_hotkey('ctrl + v', lambda: print('Произошло копирование'))
    mainWindow = MainWindow()
    mainWindow.show()
    cv2.destroyAllWindows()
    sys.exit(app.exec_())
