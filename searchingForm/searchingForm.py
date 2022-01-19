from searchingForm._searching_form import Ui_Form
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QAction

class  SearchingForm(QtWidgets.QMainWindow):
    def __init__(self):
        super(SearchingForm,self).__init__()

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.quit = QAction("Quit",self)
        self.quit.triggered.connect(self.closeEvent)
        

    def closeEvent(self,event):
        print("Close Event of the Searching Form is activated.")

        self.ui.searching_list.clear()
        self.ui.txt_search.setText("")