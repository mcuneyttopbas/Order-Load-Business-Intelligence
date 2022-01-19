from Login._loginForm import Ui_form_login
from PyQt5 import QtCore,QtWidgets
from PyQt5.QtWidgets import QAction
from PyQt5 import QtGui
import json

class  LoginForm(QtWidgets.QMainWindow):
    def __init__(self):
        super(LoginForm,self).__init__()

        self.ui = Ui_form_login()
        self.ui.setupUi(self)
        self.additional_UiSetup()

        self.ui.btn_closeSelf.clicked.connect(self.close)

        self.quit = QAction("Quit",self)

        with open("settings.json","r",encoding="utf-8") as file:
            settings = json.load(file) 
        if settings["remember_me"]["isChecked"] == True :
            self.ui.txt_username.setText(settings["remember_me"]["username"])
            self.ui.txt_password.setText(settings["remember_me"]["password"])
            self.ui.checkBox.setChecked(True)      
    
    def additional_UiSetup(self):
        
        # FOR FRAMLESS WIDGET
        flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(flags)
        # TO REMOVE BACKGROUND OF THE WIDGET
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)


