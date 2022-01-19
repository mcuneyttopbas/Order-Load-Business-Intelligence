
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QAction
from orderForm._orderForm import Ui_MainWindow

class  OrderWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(OrderWindow,self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        
        self.quit = QAction("Quit",self)
        self.quit.triggered.connect(self.closeEvent)

    def closeEvent(self,event):
        print("Close Event of the Order Form is activated.")
        self.ui.check_close.setChecked(True)
        self.ui.cb_customers.clear()
        self.ui.cb_cargos.clear()
        #RECEIVER INFO 
        self.ui.txt_receiver_name.setText("")
        self.ui.txt_author.setText("")
        self.ui.txt_cust_tel.setText("")
        self.ui.txt_gsm_tel.setText("")
        self.ui.txt_cust_adress.setText("")

        #SHIPMENT INFO   
        self.ui.txt_customer_code.setText("")
        self.ui.txt_ship_type.setText("")
        self.ui.txt_ship_tel.setText("")
        self.ui.txt_ship_adress.setText("")
        
        self.ui.lbl_order_code.setText("")
        self.ui.lbl_date.setText("")
        
        self.ui.table_details.clear()
        
        rowCount = self.ui.table_details.rowCount()
        for row in range (rowCount):
            if self.ui.table_details.item(row,1) and self.ui.table_details.item(row,0) and self.ui.table_details.item(row,2) is not None:
                self.ui.table_details.item(row,0).setText("")
                self.ui.table_details.item(row,1).setText("")
                self.ui.table_details.item(row,2).setText("")
        self.ui.table_details.setRowCount(2)
        
    


       








