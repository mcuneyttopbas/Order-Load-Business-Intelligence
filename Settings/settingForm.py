import sys
from Settings._settingForm import Ui_settingForm
from PyQt5 import QtGui,QtWidgets
from PyQt5 import QtGui
from PyQt5.QtWidgets import QAction


class  setting_form(QtWidgets.QMainWindow):
    def __init__(self):
        super(setting_form,self).__init__()

        self.ui = Ui_settingForm()
        self.ui.setupUi(self)

        self.setWindowIcon(QtGui.QIcon('icon.png'))

        self.quit = QAction("Quit",self)
        self.quit.triggered.connect(self.closeEvent)

    def closeEvent(self,event):
        print("Close Event of the Setting Form is activated.")

        self.ui.txt_company.setText("")
        self.ui.txt_company.setEnabled(True)
        self.ui.txt_mail1.setText("") 
        self.ui.txt_mail2.setText("")
        self.ui.txt_mail3.setText("")
        self.ui.cb_extra_code.setChecked(False)
        self.ui.cb_notification.setChecked(False)      

        self.ui.txt_cargo_name.setText("")
        self.ui.txt_cargo_name.setEnabled(True)
        self.ui.txt_cargo_authority.setText("") 
        self.ui.txt_cargo_phone.setText("")
        self.ui.txt_cargo_adress.setPlainText("")
        
