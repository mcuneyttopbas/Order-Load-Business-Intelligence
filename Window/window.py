from Window._window import Ui_MainWindow
from PyQt5 import QtGui,QtWidgets
from PyQt5.QtWidgets import QAction

class  Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window,self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.quit = QAction("Quit",self)
        self.quit.triggered.connect(self.closeEvent)
        self.setWindowIcon(QtGui.QIcon('icon.png'))

    def closeEvent(self,event):
        self.ui.check_close.setChecked(True)
        print("Close Event of the Main Window is activated.")


