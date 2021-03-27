from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(556, 381)
        Form.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.image_label = QtWidgets.QLabel(Form)
        self.image_label.setObjectName("image_label")
        self.image_label.setStyleSheet("font: 75 14pt \"Aharoni\";")
        self.verticalLayout.addWidget(self.image_label)
        self.control_bt = QtWidgets.QPushButton(Form)
        self.control_bt.setObjectName("control_bt")
        self.control_bt.setStyleSheet("background-color: rgb(0, 85, 255);\n"
                                      "color: rgb(255, 255, 255);")
        self.verticalLayout.addWidget(self.control_bt)
        self.control_bt2 = QtWidgets.QPushButton(Form)
        self.control_bt2.setObjectName("control_bt2")
        self.control_bt2.setStyleSheet("background-color: rgb(0, 85, 255);\n"
                                      "color: rgb(255, 255, 255);")
        self.control_bt2.setGeometry(QtCore.QRect(530, 43, 100, 28))
        self.control_bt3 = QtWidgets.QPushButton(Form)
        self.control_bt3.setObjectName("control_bt3")
        self.control_bt3.setStyleSheet("background-color: rgb(0, 85, 255);\n"
                                       "color: rgb(255, 255, 255);")
        self.control_bt3.setGeometry(QtCore.QRect(530, 10, 100, 28))
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "АНТИЧИТЕР.НЕЙРО"))
        self.image_label.setText(_translate("Form", "Здравствуйте! Нажмите на кнопку для того, чтобы начать"))
        self.control_bt.setText(_translate("Form", "Начать"))
        self.control_bt2.setText(_translate("Form", "отправить отчет"))
        self.control_bt3.setText(_translate("Form", "Авторизация"))

