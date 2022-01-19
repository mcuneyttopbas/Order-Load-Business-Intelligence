import sys
from Settings._settings import Ui_settings
from PyQt5.QtWidgets import QAction
from PyQt5 import QtWidgets,QtGui


class  settings_widget(QtWidgets.QMainWindow):
    def __init__(self):
        super(settings_widget,self).__init__()

        self.ui = Ui_settings()
        self.ui.setupUi(self)

        self.setWindowIcon(QtGui.QIcon('icon.png'))

        self.quit = QAction("Quit",self)
        self.quit.triggered.connect(self.closeEvent)

    def closeEvent(self,event):
        print("Close Event of the Settings is activated.")
        self.ui.check_close.setChecked(True)



