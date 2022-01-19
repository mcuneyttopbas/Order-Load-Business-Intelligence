"""
Author              :   M.Cüneyt Topbaş
Contact             :   cuneyttopbas@hotmail.com
Date                :   30.12.2021
Program Title       :   Order & Load
Aim                 :   Understanding Fundamentals of Business Intelligence Softwares
Major Requirements  :   General Knowledge of PyQt5, pymongo
"""

from PyQt5.QtWidgets import QMessageBox,QInputDialog,QTableWidgetItem,QLineEdit,QShortcut
from PyQt5 import QtWidgets, QtCore,QtGui
from PyQt5.QtGui import QKeySequence
from PyQt5.Qt import Qt

from pynput.keyboard import Key,Controller
from email.message import EmailMessage
from datetime import datetime, date
import smtplib, ssl
import pymongo
import json
import time
import sys

########### SELF-MADE GUI IMPORTS #########################
from splash.splash import SplashScreen
from Login.loginForm import LoginForm
from Window.window import Window
from Settings.settings import settings_widget
from Settings.settingForm import setting_form
from orderForm.order import OrderWindow
from searchingForm.searchingForm import SearchingForm
from report.report import ReportForm


class App:
    def __init__(self) -> None:
        print("App is started.")

        ################ SYS GUI APPLICATION #########################
        app = QtWidgets.QApplication(sys.argv)

        ################ CREATING GUI OBJECTS  #######################
        ##############################################################
        self.splash = SplashScreen()
        self.login = LoginForm()
        self.window = Window()
        self.order = OrderWindow()
        self.settings = settings_widget()
        self.setting_form = setting_form()
        self.searching_form = SearchingForm()
        self.report_form = ReportForm()
        ###############################################################
        self.keyboard = Controller()

        self.splash.show()
        self.splash.ui.check_close.stateChanged.connect(self.start)

        self.customer_data = {}
        self.cargo_data = {}
        self.order_data = {}

        ####################### LOGIN ###################################
        self.login.ui.btn_logIn.clicked.connect(self.check_user) 
        self.login.ui.btn_logIn.setShortcut("Return")
            
        ####################### WINDOW ###################################
        ##################################################################
        self.window.ui.check_close.stateChanged.connect(self.in_caseOfWindow_close)
        self.window.ui.action_exit.triggered.connect(self.window.close)
        self.window.ui.action_update.triggered.connect(self.load_data_to_windows)
        #################### NEW ORDER TABLE #############################
        self.window.ui.table_new_order.doubleClicked.connect(self.doubleClick_onNew)
        self.window.ui.btn_nw_prepare.clicked.connect(self.prepare_order)
        self.window.ui.btn_nw_remove.clicked.connect(self.remove_order)
        self.window.ui.btn_nw_note.clicked.connect(self.add_note)
        self.window.ui.btn_nw_wait.clicked.connect(self.sendOrder_fromNew_to_wait)
        #################### PREPARING TABLE #############################
        self.window.ui.table_preparing.doubleClicked.connect(self.doubleClick_onPre)
        self.window.ui.btn_pr_complete.clicked.connect(self.get_order_ready)
        self.window.ui.btn_pr_split.clicked.connect(self.split_order)
        self.window.ui.btn_pr_wait.clicked.connect(self.sendOrder_fromPre_to_wait),
        self.window.ui.btn_pr_cancel.clicked.connect(self.sendBack_fromPre_to_new)
        #################### WAITING TABLE #############################
        self.window.ui.table_waiting.doubleClicked.connect(self.doubleClick_onWait)
        self.window.ui.btn_wt_prepare.clicked.connect(self.prepare_waiting_order)
        self.window.ui.btn_wt_info.clicked.connect(self.add_info)
        self.window.ui.btn_wt_cancel.clicked.connect(self.sendBack_fromWt_to_new)
        #################### READY TABLE ################################
        self.window.ui.table_ready.doubleClicked.connect(self.doubleClick_onRdy)
        self.window.ui.btn_rdy_ship.clicked.connect(self.deliver_order)
        self.window.ui.btn_rdy_cancel.clicked.connect(self.sendBack_fromRdy_to_prep)
        self.window.ui.action_developer.triggered.connect(self.about)
        self.window.ui.action_version.triggered.connect(self.version)

        ###################### ORDER ######################################
        self.order.ui.check_close.stateChanged.connect(self.in_caseOfOrder_close)

        self.window.ui.action_order.triggered.connect(self.open_orderForm)
        self.order.ui.btn_save.clicked.connect(self.save_order)
        self.order.ui.btn_refresh.clicked.connect(self.refresh_form)
        
        self.shortcut_open1 = QShortcut(QKeySequence('F1'), self.order)
        self.shortcut_open1.activated.connect(self.open_searchingForm)

        self.shortcut_open2 = QShortcut(QKeySequence('Ctrl+S'), self.order)
        self.shortcut_open2.activated.connect(self.save_order)

        ##################### SEARCHING FORM IN ORDER ######################
        self.shortcut_open3 = QShortcut(QKeySequence(Qt.Key_Return), self.searching_form)
        self.shortcut_open3.activated.connect(self.get_searching_item)
        
        self.searching_form.ui.txt_search.setEnabled(False)
        self.searching_form.ui.searching_list.doubleClicked.connect(self.get_searching_item)

        ####################### REPORT FROM ################################
        self.window.ui.action_report.triggered.connect(self.open_reportForm)

        ####################### SETTINGS ###################################
        ####################################################################
        self.settings.ui.check_close.stateChanged.connect(self.in_caseOfSettings_close)
        self.window.ui.action_settings.triggered.connect(self.open_settings)
        ##################### CUSTOMER SETTINGS ############################
        self.settings.ui.btn_add_customer.clicked.connect(self.open_customer_settings_to_add)
        self.settings.ui.btn_edit_customer.clicked.connect(self.open_customer_settings_to_edit)
        self.settings.ui.btn_remove_customer.clicked.connect(self.remove_customer)
        self.setting_form.ui.btn_save_customer.clicked.connect(self.add_customer)
        ###################### CARGO SETTINGS ###############################
        self.settings.ui.btn_add_cargo.clicked.connect(self.open_cargo_settings_to_add)
        self.settings.ui.btn_edit_cargo.clicked.connect(self.open_cargo_settings_to_edit)
        self.settings.ui.btn_remove_cargo.clicked.connect(self.remove_cargo)
        self.setting_form.ui.btn_save_cargo.clicked.connect(self.add_cargo)
        #####################################################################
        
        #################### SYS GUI EXIT #####################################
        sys.exit(app.exec_())
    
    
    def start (self):
        self.login.show()

    def check_user(self):
        print("User informations is checked.")
        username_entry = self.login.ui.txt_username.text() 
        password_entry = self.login.ui.txt_password.text()
    
        #   To use this method, users must be already created at database 
        #   Thanks to that, mongodb database check if username and password is valid or not by itself.
        try:                         
            self.myclient = pymongo.MongoClient(f"mongodb+srv://{username_entry}:{password_entry}@cluster0.asdnj.mongodb.net/app_test?retryWrites=true&w=majority")
            self.mydb = self.myclient["order-load"]
            self.customer_coll = self.mydb["customers"]
            self.cargo_coll = self.mydb["cargos"]
            self.order_coll = self.mydb["orders"]
            self.product_coll = self.mydb["products"]
            self.setting_coll = self.mydb["settings"]
            result = self.customer_coll.find_one() #  This one is used to send a request to database to be sure if user is valid or not.
            
            self.username = self.login.ui.txt_username.text() 
            self.password = self.login.ui.txt_password.text()

            print(f"User '{self.username}' in online.")
            self.login.close()
            self.load_data_to_windows()

            if self.login.ui.checkBox.isChecked() == True:
                with open("settings.json","r",encoding="utf-8") as file:
                    settings = json.load(file) 
                settings["remember_me"]["isChecked"] = True
                settings["remember_me"]["username"] = self.username
                settings["remember_me"]["password"] = self.password
                with open("settings.json","w",encoding="utf-8") as file:
                    json.dump(settings, file)
            else:
                with open("settings.json","r",encoding="utf-8") as file:
                    settings = json.load(file) 
                settings["remember_me"]["isChecked"] = False
                settings["remember_me"]["username"] = ""
                settings["remember_me"]["password"] = ""
                with open("settings.json","w",encoding="utf-8") as file:
                    json.dump(settings, file)

            self.window.ui.lbl_user.setText(self.username)
            self.window.show()

        
        #   If Username or password is not valid mongodb throws a Authorizaiton error
        #   When program catch this error, that means username or password is not valid. 
        except pymongo.errors.OperationFailure and pymongo.errors.InvalidURI and pymongo.errors.OperationFailure:
            self.login.hide()
            msg = QMessageBox()
            msg.setWindowTitle("Geçersiz İşlem")
            msg.setText("Kullanıcı Adı veya Parola yanlış!")
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setWindowIcon(QtGui.QIcon('icon.png'))
            msg.activateWindow()
            msg.raise_()
            x = msg.exec_()
            self.login.show()
        except Exception:
            self.login.hide()
            msg = QMessageBox()
            msg.setWindowTitle("Geçersiz İşlem")
            msg.setText("İnternet bağlantınızı kontrol ediniz!")
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setWindowIcon(QtGui.QIcon('icon.png'))
            msg.activateWindow()
            msg.raise_()
            x = msg.exec_()
            self.login.show()
            


    ##################### GENERAL  ################################
    def in_caseOfWindow_close(self):
        self.order.close()
        self.report_form.close()
        self.settings.close()
        self.setting_form.close()

    def in_caseOfOrder_close(self):
        self.searching_form.close()
    
    def in_caseOfSettings_close(self):
        self.setting_form.close()

    def about(self):
        line1 = "Order & Load bir Akıllı İş zekası yazılımıdır." + "<br>" + "Çapraz platform desteğine sahiptir.<br>"
        line2 = "Bu program <b>Cüneyt Topbaş</b> tarafından açık kaynak kodlu oluşturulmuştur.<br>"
        line3 = "Lisans bilgilerini görmek için <a href=https://github.com/mcuneyttopbas>tıklayınız.</a><br>" 

        msg = QMessageBox()
        msg.setWindowTitle("Hakkında")
        msg.setText("<b>Order & Load Hakkında</b><br><br>"+ line1 +  line2 + line3)
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setWindowIcon(QtGui.QIcon('icon.png'))
        msg.raise_()
        x = msg.exec_()
    
    def version(self):
        self.feedback_messageBox("version : 1.0.0")

            
    class Dialog:
        def __init__(self,parent) -> None:
            self.parent = parent
            self.dialog = QInputDialog(self.parent)
            self.dialog.setWindowIcon(QtGui.QIcon('icon.png'))
            
        def close(self):
            self.dialog.close()
        
        def return_params(self,title,explanation):
            self.input, self.selection = self.dialog.getText(self.parent,title,explanation,QLineEdit.Normal)
            return self.input, self.selection

    def set_dialog(self,parent,title,explanation):
        dialog = QInputDialog(self.window)
        dialog.setWindowIcon(QtGui.QIcon('icon.png'))
        input,selection = dialog.getText(parent,title,explanation,QLineEdit.Normal)
        return input , selection

    def feedback_messageBox(self,item,event=""):
            msg = QMessageBox()
            msg.setWindowTitle("İşlem Raporu")
            msg.setText(f"{item} {event}.")
            msg.setIcon(QMessageBox.Information)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setWindowIcon(QtGui.QIcon('icon.png'))
            msg.raise_()
            x = msg.exec_()
    
    def warning_messageBox(self,explanation):
            msg = QMessageBox()
            msg.setWindowTitle("Uyarı")
            msg.setText(explanation)
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setWindowIcon(QtGui.QIcon('icon.png'))
            msg.raise_()
            x = msg.exec_()    

    def double_click_messageBox(self,order_code,item_id):
        try:
            order = self.order_coll.find_one({"_id":order_code})
            order_status = order["Order Details"][item_id]["Status"]
            order_item = order["Order Details"][item_id]["Item"]
            order_color = order["Order Details"][item_id]["Color"]
            order_meter = order["Order Details"][item_id]["Meter"]
            order_note = order["Order Details"][item_id]["Note"]
            if order_status == "waiting":
                waiting_cause = order["Order Details"][item_id]["Waiting_cause"]
                waiting_info = order["Order Details"][item_id]["Waiting_info"]
                info_by = order["Order Details"][item_id]["Info_by"]
                line  = f"\nBekleme Sebebi : {waiting_cause}\nBilgi Notu : {waiting_info}\nBilgi Ekleyen : {info_by}\n"
            else:
                line = ""
            creater = order["Crated_by"]
            order_receiver = order["Receiver Info"]["Receiver Name"]
            order_receiver_authority = order["Receiver Info"]["Authority"]
            order_receiver_gsm = order["Receiver Info"]["Company GSM"]
            order_receiver_adress = order["Receiver Info"]["Company Adress"]
            order_shipper = order["Shipping Info"]["Shipper Name"]
            order_customer_code = order["Shipping Info"]["Customer Code"]
            order_shipping_type = order["Shipping Info"]["Shipping Type"]
            order_shipping_phone = order["Shipping Info"]["Shipper Phone"]
            order_shipping_adress = order["Shipping Info"]["Shipper Adress"]
        
            if order_status == "new":
                order_status = "Yeni Sipariş"
            elif order_status == "preparing":
                order_status = "Hazırlanan Sipariş"
            elif order_status == "waiting":
                order_status = "Bekleyen Sipariş"
            elif order_status == "ready":
                order_status = "Tamamlanan Sipariş"
            elif order_status == "delivered":
                order_status = "Sevkedilmiş Sipariş"


            order_details = f"SİPARİŞ DETAYLARI\n\nSipariş Kodu : {order_code}\nDüzenleyen : {creater}\nSipariş ID : {item_id}\n\nDurum : {order_status}{line}\nÜrün : {order_item}\nRenk : {order_color}\nMetre : {order_meter}\nNot : {order_note}\n\n\n"
            receiver_details = f"ALICI BİLGİLERİ\n\nAdı : {order_receiver}\nYetkili Kişi : {order_receiver_authority}\nGSM : {order_receiver_gsm}\nAdres : {order_receiver_adress}\n\n\n"
            shipper_details = f"TESLİMAT BİLGİLERİ\n\nNakliyeci Adı : {order_shipper}\nMüşteri Kodu : {order_customer_code}\nTaşıma Tipi : {order_shipping_type}\nTel No: : {order_shipping_phone}\nAdres : {order_shipping_adress}\n\n\n"

            msg = QMessageBox()
            msg.setWindowTitle("Detay")
            msg.setText(order_details + receiver_details + shipper_details)
            msg.setIcon(QMessageBox.Information)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setWindowIcon(QtGui.QIcon('icon.png'))
            msg.raise_()
            x = msg.exec_()
        except  pymongo.errors.PyMongoError:
            self.warning_messageBox("İnternet bağlantınızı kontrol ediniz!")

    def isFloat(self,num):
        try:
            float(num)
            return True
        except ValueError:
            return False

    def isInt(self,num):
        try:
            int(num)
            return True
        except ValueError:
            return False

    def select_clicked_item(self,listWidget):
        index = listWidget.currentRow()
        item = listWidget.item(index)

        return item

    def send_notification(self,toList,ccList,subject,body):
        try:
            setting = self.setting_coll.find_one({"_id":"notifications"})
            From = setting["admin"][0]["mail"]
            Password = setting["admin"][0]["password"]

            msg = EmailMessage()
            msg.set_content(body)
            msg["Subject"] = subject
            msg["From"] = From
            msg["To"] = ",".join(toList)
            msg["Cc"] = ",".join(ccList)

            context=ssl.create_default_context()

            with smtplib.SMTP("smtp.gmail.com", port=587) as smtp:
                smtp.starttls(context=context)
                smtp.login(msg["From"], Password)
                smtp.send_message(msg)

        except Exception as ex:
            print(f"Hata Kodu:{ex}")

################################## TABLES ############################################
######################################################################################
######################################################################################

    def load_data_to_windows(self):
        try:
            ###################### COLUMN SETTINGS #######################################
            ##############################################################################

            ############## "NEW ORDERS" TABLE COLUMN SETTINGS ############################
            self.window.ui.table_new_order.setColumnCount(9)      
            self.window.ui.table_new_order.setHorizontalHeaderLabels(("Sipariş Kodu","Firma","Kargo","Alıcı","ID","Ürün","Ürün Kodu","Metre","Not"))
            self.window.ui.table_new_order.setColumnWidth(0,150)
            self.window.ui.table_new_order.setColumnWidth(1,100)
            self.window.ui.table_new_order.setColumnWidth(2,125)
            self.window.ui.table_new_order.setColumnWidth(3,100)
            self.window.ui.table_new_order.setColumnWidth(4,50)
            self.window.ui.table_new_order.setColumnWidth(5,100)
            self.window.ui.table_new_order.setColumnWidth(6,100)
            self.window.ui.table_new_order.setColumnWidth(7,50)
            self.window.ui.table_new_order.setColumnWidth(8,175)

            ############# "PREPARING" ORDERS TABLE COLUMN SETTINGS #######################
            self.window.ui.table_preparing.setColumnCount(5)      
            self.window.ui.table_preparing.setHorizontalHeaderLabels(("Sipariş Kodu","ID","Ürün","Ürün Kodu","Metre"))
            self.window.ui.table_preparing.setColumnWidth(0,75)
            self.window.ui.table_preparing.setColumnWidth(1,10)
            self.window.ui.table_preparing.setColumnWidth(2,100)
            self.window.ui.table_preparing.setColumnWidth(3,100)
            self.window.ui.table_preparing.setColumnWidth(4,10)

            ############# "WAITING" ORDERS TABLE COLUMN SETTINGS ##########################
            self.window.ui.table_waiting.setColumnCount(5)      
            self.window.ui.table_waiting.setHorizontalHeaderLabels(("Sipariş Kodu","ID","Ürün","Ürün Kodu","Metre"))
            self.window.ui.table_waiting.setColumnWidth(0,75)
            self.window.ui.table_waiting.setColumnWidth(1,10)
            self.window.ui.table_waiting.setColumnWidth(2,100)
            self.window.ui.table_waiting.setColumnWidth(3,100)
            self.window.ui.table_waiting.setColumnWidth(4,10)

            ############# "READY" ORDERS TABLE COLUMN SETTINGS ############################
            self.window.ui.table_ready.setColumnCount(9)      
            self.window.ui.table_ready.setHorizontalHeaderLabels(("Sipariş Kodu","Firma","Kargo","Alıcı","ID","Ürün","Ürün Kodu","Metre","Not"))
            self.window.ui.table_ready.setColumnWidth(0,150)
            self.window.ui.table_ready.setColumnWidth(1,100)
            self.window.ui.table_ready.setColumnWidth(2,125)
            self.window.ui.table_ready.setColumnWidth(3,100)
            self.window.ui.table_ready.setColumnWidth(4,50)
            self.window.ui.table_ready.setColumnWidth(5,75)
            self.window.ui.table_ready.setColumnWidth(6,100)
            self.window.ui.table_ready.setColumnWidth(7,100)
            self.window.ui.table_ready.setColumnWidth(8,175)

            ###################### ROW SETTINGS ##########################################
            ##############################################################################

            ####################### ROW COUNTING #########################################
            newOrder_rowCount = 0
            preparingOrder_rowCount = 0
            waitingOrder_rowCount = 0
            readyOrder_rowCount = 0
            shippedOrder_rowCount = 0

            for order in self.order_coll.find():
                for order_items in order["Order Details"]:
                    if order['Order Details'][order_items]['Status'] == "new":
                        newOrder_rowCount += 1
                    elif order['Order Details'][order_items]['Status'] == "preparing":
                        preparingOrder_rowCount += 1
                    elif order['Order Details'][order_items]['Status'] == "waiting":
                        waitingOrder_rowCount += 1
                    elif order['Order Details'][order_items]['Status'] == "ready":
                        readyOrder_rowCount += 1
                    elif order['Order Details'][order_items]['Status'] == "shipped":
                        shippedOrder_rowCount += 1

            self.window.ui.table_new_order.setRowCount(newOrder_rowCount)
            self.window.ui.table_preparing.setRowCount(preparingOrder_rowCount)
            self.window.ui.table_waiting.setRowCount(waitingOrder_rowCount)
            self.window.ui.table_ready.setRowCount(readyOrder_rowCount)
            #self.window.ui.table_preparing.setRowCount(shippedOrder_rowCount) # HENÜZ YOK

            ####################### SETTING ITEMS TO ROWS #################################
            newOrder_rowIndex = 0
            preparingOrder_rowIndex = 0
            waitingOrder_rowIndex = 0
            readyOrder_rowIndex = 0

            for order in self.order_coll.find():
                for order_items in order["Order Details"]:
                    if order['Order Details'][order_items]['Status'] == "new":
                        self.window.ui.table_new_order.setItem(newOrder_rowIndex,0,QTableWidgetItem(order['_id']))
                        self.window.ui.table_new_order.setItem(newOrder_rowIndex,1,QTableWidgetItem(order['Company Name']))
                        self.window.ui.table_new_order.setItem(newOrder_rowIndex,2,QTableWidgetItem(order["Shipping Info"]["Shipper Name"]))
                        self.window.ui.table_new_order.setItem(newOrder_rowIndex,3,QTableWidgetItem(order["Receiver Info"]["Receiver Name"]))
                        self.window.ui.table_new_order.setItem(newOrder_rowIndex,4,QTableWidgetItem(order_items))
                        self.window.ui.table_new_order.setItem(newOrder_rowIndex,5,QTableWidgetItem(order['Order Details'][order_items]['Item']))
                        self.window.ui.table_new_order.setItem(newOrder_rowIndex,6,QTableWidgetItem(order['Order Details'][order_items]['Color']))
                        self.window.ui.table_new_order.setItem(newOrder_rowIndex,7,QTableWidgetItem(order['Order Details'][order_items]['Meter']))
                        self.window.ui.table_new_order.setItem(newOrder_rowIndex,8,QTableWidgetItem(order['Order Details'][order_items]['Note']))
                        newOrder_rowIndex += 1

                    elif order['Order Details'][order_items]['Status'] == "preparing":
                        self.window.ui.table_preparing.setItem(preparingOrder_rowIndex,0,QTableWidgetItem(order['_id']))
                        self.window.ui.table_preparing.setItem(preparingOrder_rowIndex,1,QTableWidgetItem(order_items))
                        self.window.ui.table_preparing.setItem(preparingOrder_rowIndex,2,QTableWidgetItem(order['Order Details'][order_items]['Item']))
                        self.window.ui.table_preparing.setItem(preparingOrder_rowIndex,3,QTableWidgetItem(order['Order Details'][order_items]['Color']))
                        self.window.ui.table_preparing.setItem(preparingOrder_rowIndex,4,QTableWidgetItem(order['Order Details'][order_items]['Meter']))
                        preparingOrder_rowIndex += 1

                    elif order['Order Details'][order_items]['Status'] == "waiting":
                        self.window.ui.table_waiting.setItem(waitingOrder_rowIndex,0,QTableWidgetItem(order['_id']))
                        self.window.ui.table_waiting.setItem(waitingOrder_rowIndex,1,QTableWidgetItem(order_items))
                        self.window.ui.table_waiting.setItem(waitingOrder_rowIndex,2,QTableWidgetItem(order['Order Details'][order_items]['Item']))
                        self.window.ui.table_waiting.setItem(waitingOrder_rowIndex,3,QTableWidgetItem(order['Order Details'][order_items]['Color']))
                        self.window.ui.table_waiting.setItem(waitingOrder_rowIndex,4,QTableWidgetItem(order['Order Details'][order_items]['Meter']))
                        waitingOrder_rowIndex += 1

                    elif order['Order Details'][order_items]['Status'] == "ready":
                        self.window.ui.table_ready.setItem(readyOrder_rowIndex,0,QTableWidgetItem(order['_id']))
                        self.window.ui.table_ready.setItem(readyOrder_rowIndex,1,QTableWidgetItem(order['Company Name']))
                        self.window.ui.table_ready.setItem(readyOrder_rowIndex,2,QTableWidgetItem(order["Shipping Info"]["Shipper Name"]))
                        self.window.ui.table_ready.setItem(readyOrder_rowIndex,3,QTableWidgetItem(order["Receiver Info"]["Receiver Name"]))
                        self.window.ui.table_ready.setItem(readyOrder_rowIndex,4,QTableWidgetItem(order_items))
                        self.window.ui.table_ready.setItem(readyOrder_rowIndex,5,QTableWidgetItem(order['Order Details'][order_items]['Item']))
                        self.window.ui.table_ready.setItem(readyOrder_rowIndex,6,QTableWidgetItem(order['Order Details'][order_items]['Color']))
                        self.window.ui.table_ready.setItem(readyOrder_rowIndex,7,QTableWidgetItem(order['Order Details'][order_items]['Meter']))
                        self.window.ui.table_ready.setItem(readyOrder_rowIndex,8,QTableWidgetItem(order['Order Details'][order_items]['Note']))
                        readyOrder_rowIndex += 1

            self.window.ui.txt_lastUpdate.setText(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        except  pymongo.errors.PyMongoError:
            self.warning_messageBox("İnternet bağlantınızı kontrol ediniz!")

    ######################### GENERAL SETTINGS OF TABLES #####################################
    def get_selected_item_on_table(self, tableWidget,orderCode_col_index, id_col_index):
        index = tableWidget.currentRow()
        order_code = tableWidget.item(index,orderCode_col_index)
        item_id = tableWidget.item(index,id_col_index)

        if order_code is not None and item_id is not None:
            return order_code.text(), item_id.text()
        else:
            print("not selected properly")

    def update_order_status(self, order_code, item_id, status):
        try:
            query = {"_id": order_code}
            new_value = {"$set": { f"Order Details.{item_id}.Status" : status}}

            self.order_coll.update_one(query, new_value)
        except  pymongo.errors.PyMongoError:
            self.warning_messageBox("İnternet bağlantınızı kontrol ediniz!")    
    
    ######################### NEW ORDER BUTTON FUNCTIONS ########################################
    def doubleClick_onNew(self):
        order_code, item_id = self.get_selected_item_on_table(self.window.ui.table_new_order, 0,4)
        self.double_click_messageBox(order_code,item_id)

    def prepare_order(self):
        order_code, item_id = self.get_selected_item_on_table(self.window.ui.table_new_order, 0,4)
        print(f"seçilen order code :{order_code} seçilen id {item_id}")
        self.update_order_status(order_code, item_id, "preparing")
        self.feedback_messageBox(f"{order_code}/{item_id} hazırlanmaya başladı.")
        self.load_data_to_windows()

    def add_note(self):
        order_code, item_id = self.get_selected_item_on_table(self.window.ui.table_new_order, 0, 4)
        print(f"seçilen order code :{order_code} seçilen id {item_id}")
        try:       
            note , ok = QInputDialog.getText(self.window,"Not Ekle","Not",QLineEdit.Normal)
            if note and ok is not None:
                query = {"_id": order_code}
                new_value = {"$set": { f"Order Details.{item_id}.Note" : note}}
                self.order_coll.update_one(query, new_value)

                self.feedback_messageBox(f"{order_code}/{item_id} not eklendi.\n\nNot: {note}")
            self.load_data_to_windows()

        except  pymongo.errors.PyMongoError:
            self.warning_messageBox("İnternet bağlantınızı kontrol ediniz!")
            

    def sendOrder_fromNew_to_wait(self):
        try :
            cause , ok = QInputDialog.getText(self.window,"Bekleyene Al","Bekleme Sebebi",QLineEdit.Normal)
            if cause and ok is not None:
                order_code, item_id = self.get_selected_item_on_table(self.window.ui.table_new_order, 0, 4)
                self.update_order_status(order_code, item_id, "waiting")
                query = {"_id": order_code}
                new_value = {"$set": { f"Order Details.{item_id}.Waiting_cause" : cause,
                                        f"Order Details.{item_id}.Waiting_info" : "",
                                        f"Order Details.{item_id}.Info_by" : ""
                }}
                self.order_coll.update_one(query, new_value)
                ###################### NOTIFICATION #######################
                index = self.window.ui.table_preparing.currentRow()
                item_name = self.window.ui.table_preparing.item(index,2)
                item_color = self.window.ui.table_preparing.item(index,3)
                item_meter = self.window.ui.table_preparing.item(index,4)

                toList = []
                ccList = []

                settings = self.setting_coll.find_one({"_id":"notifications"})
                for setting in settings:
                    if setting == "supplying_departmant":
                        for adress in settings[setting]:
                            toList.append(adress["mail"])
                    elif setting == "executive":
                        for adress in settings[setting]:
                            toList.append(adress["mail"])

                subject = f"{order_code} / {item_id} BEKLEYENE ALINDI"
                line = f"Aşağıda belirtilen ürün beklemeye alındı,\n\n{cause.capitalize()}.\n\n"
                body =  line + f"{item_name.text()} {item_color.text()}  {item_meter.text()} MT"

                self.send_notification(toList,ccList,subject,body)
                self.feedback_messageBox(f"{order_code}/{item_id} beklemeye alındı.")
                self.load_data_to_windows()
            else:
                raise Exception("Bekleme sebebi belirtilmedi!")

        except  pymongo.errors.PyMongoError:
            self.warning_messageBox("İnternet bağlantınızı kontrol ediniz!")
        except Exception as ex:
            self.warning_messageBox(f"Hatalı İşlem : {ex} ")    


    def remove_order(self):
        order_code, item_id = self.get_selected_item_on_table(self.window.ui.table_new_order, 0,4)
        print(f"seçilen order code :{order_code} seçilen id {item_id}")
        self.update_order_status(order_code, item_id, "removed")

        ################# NOTIFICATION ###########################
        index = self.window.ui.table_new_order.currentRow()
        item_name = self.window.ui.table_new_order.item(index,5)
        item_color = self.window.ui.table_new_order.item(index,6)
        item_meter = self.window.ui.table_new_order.item(index,7)

        toList = []
        ccList = []

        settings = self.setting_coll.find_one({"_id":"notifications"})
        for setting in settings:
            if setting == "operation_departmant":
                for adress in settings[setting]:
                    toList.append(adress["mail"])
            elif setting == "executive":
                for adress in settings[setting]:
                    ccList.append(adress["mail"])
            elif setting == "supplying_departmant":
                for adress in settings[setting]:
                    ccList.append(adress["mail"])

        subject = f"{order_code} / {item_id} SİLİNDİ!"
        line = f"Aşağıda detayları belirtilen ürün silindi,\n\n"
        body =  line + f"{item_name.text()} {item_color.text()}  {item_meter.text()} MT"

        self.send_notification(toList,ccList,subject,body)
        self.feedback_messageBox(f"{order_code}/{item_id} silindi.")
        self.load_data_to_windows()

    ######################### PREPARING BUTTON FUNCTIONS ########################################

    def doubleClick_onPre(self):
        order_code, item_id = self.get_selected_item_on_table(self.window.ui.table_preparing, 0,1)
        self.double_click_messageBox(order_code,item_id)

    def get_order_ready(self):
        order_code, item_id = self.get_selected_item_on_table(self.window.ui.table_preparing, 0,1)
        self.update_order_status(order_code, item_id, "ready")
        self.feedback_messageBox(f"{order_code}/{item_id} tamamlandı.")
        self.load_data_to_windows()

    def split_order(self):
        #item bilgilerini al
        try:
            print("split order fonksyionu çalıştı")
            index = self.window.ui.table_preparing.currentRow()
            order_code = self.window.ui.table_preparing.item(index,0).text()
            item_id = self.window.ui.table_preparing.item(index,1).text()
            item_name = self.window.ui.table_preparing.item(index,2).text()
            item_color = self.window.ui.table_preparing.item(index,3).text()
            item_meter = self.window.ui.table_preparing.item(index,4).text()

            dialog = self.Dialog(self.window)
            piece_amount , ok = dialog.return_params("Parçala", "Kaç Parçaya Bölünecek")
            if piece_amount and ok is not None:
                print(f"{piece_amount} parçaya bölünecek")
                if self.isInt(piece_amount) == True:
                    repeat = 0
                    pieces = []
                    total_meter = 0
                    while repeat < int(piece_amount):
                        line = ""
                        total_line = ""
                        total = 0
                        
                        for i in range(len(pieces)):
                            if len(pieces) != 0:
                                line += f"{i+1}.Parça :{pieces[i]}\n"
                                total += pieces[i]
                                total_line = f"Kesilen Parçalar Toplamı:{total} MT"
                        
                        piece_meter , ok = dialog.return_params("Parçala",f"{line}\n{total_line}\n\nAna Parça:{item_meter} MT\n\n{repeat+1}.Parça(MT)")
                        if piece_meter and ok is not None:
                            if self.isInt(piece_meter) == True:
                                pieces.append(int(piece_meter))
                                repeat += 1
                                total_meter += int(piece_meter)
                            elif self.isFloat(piece_meter) == True:
                                pieces.append(float(piece_meter))
                                repeat += 1
                                total_meter += float(piece_meter)
                            else:
                                self.warning_messageBox("Lütfen Sayı Giriniz.")
                        else:
                            dialog.close()
                            break
                    print(total)
                    print(pieces)
                else:
                    self.warning_messageBox("Lütfen Tam Sayı Giriniz.")
                    print("Lütfen tam sayı giriniz.")
                    dialog.close()
            else:
                print("kapanıyor")
                dialog.close()
        except Exception:
            pass

        try:

            if total_meter != int(item_meter):
                self.warning_messageBox("Parçaların toplam miktarı Ana toplam ile tutmuyor!\n\nLütfen tekrar deneyiniz.")
            else:
            
                # To find Order Note for splitted items
                filter = {"_id": order_code}
                order = self.order_coll.find_one(filter)
                order_note = order["Order Details"][item_id]["Note"]
                feedback = f"Ana Parça : {order_code}/{item_id} : {item_meter} MT\n\n"

                for i in range(len(pieces)):
                    print(f"Order Code: {order_code} Item Id: {item_id} Item: {item_name} Color: {item_color} Meter {pieces[i]}")
                    
                    query = {"_id": order_code}
                    new_value = {"$set": { 
                                        f"Order Details.{item_id + '-' + str(i+1)}.Status" : "preparing",   
                                        f"Order Details.{item_id + '-' + str(i+1)}.Item" : item_name,
                                        f"Order Details.{item_id + '-' + str(i+1)}.Color" : item_color,
                                        f"Order Details.{item_id + '-' + str(i+1)}.Meter" : str(pieces[i]),
                                        f"Order Details.{item_id + '-' + str(i+1)}.Note" : order_note,
                                        f"Order Details.{item_id + '-' + str(i+1)}.Delivered_at" : "Henüz Teslim Edilmedi"
                    }}
                    feedback += f"Parça {i+1} : {str(pieces[i])} MT\n"
                    self.order_coll.update_one(query, new_value)
                
                self.order_coll.update_one({"_id":order_code},{"$unset":{f"Order Details.{item_id}":""}})  
                self.feedback_messageBox(feedback + "\nşekilde parçalandı.")
            self.load_data_to_windows()

        except ValueError:
            if total_meter != float(item_meter):
                 self.warning_messageBox("Parçaların toplamı Ana Parçadan daha fazla!\n\nLütfen tekrar deneyiniz.")
            else:
                 # To find Order Note for splitted items
                filter = {"_id": order_code}
                order = self.order_coll.find_one(filter)
                order_note = order["Order Details"][item_id]["Note"]
                feedback = f"Ana Parça : {order_code}/{item_id} : {item_meter} MT\n\n"

                for i in range(len(pieces)):
                    print(f"Order Code: {order_code} Item Id: {item_id} Item: {item_name} Color: {item_color} Meter {pieces[i]}")
                    
                    query = {"_id": order_code}
                    new_value = {"$set": { 
                                        f"Order Details.{item_id + '-' + str(i+1)}.Status" : "preparing",   
                                        f"Order Details.{item_id + '-' + str(i+1)}.Item" : item_name,
                                        f"Order Details.{item_id + '-' + str(i+1)}.Color" : item_color,
                                        f"Order Details.{item_id + '-' + str(i+1)}.Meter" : str(pieces[i]),
                                        f"Order Details.{item_id + '-' + str(i+1)}.Note" : order_note,
                                        f"Order Details.{item_id + '-' + str(i+1)}.Delivered_at" : "Henüz Teslim Edilmedi"
                    }}
                    feedback += f"Parça {i+1} : {str(pieces[i])} MT\n"
                    self.order_coll.update_one(query, new_value)

                self.order_coll.update_one({"_id":order_code},{"$unset":{f"Order Details.{item_id}":""}}) 
                self.feedback_messageBox(feedback + "\nolacak şekilde parçalandı.")
            self.load_data_to_windows()
        except  pymongo.errors.PyMongoError:
            self.warning_messageBox("İnternet bağlantınızı kontrol ediniz!")
        except Exception:
            pass

    def sendOrder_fromPre_to_wait(self):
        try :
            cause , ok = QInputDialog.getText(self.window,"Bekleyene Al","Bekleme Sebebi",QLineEdit.Normal)
            if cause and ok is not None:
                order_code, item_id = self.get_selected_item_on_table(self.window.ui.table_preparing, 0, 1)
                self.update_order_status(order_code, item_id, "waiting")
                query = {"_id": order_code}
                new_value = {"$set": { f"Order Details.{item_id}.Waiting_cause" : cause,
                                        f"Order Details.{item_id}.Waiting_info" : "",
                                        f"Order Details.{item_id}.Info_by" : ""
                }}
                self.order_coll.update_one(query, new_value)
            
                ###################### NOTIFICATION #######################
                index = self.window.ui.table_preparing.currentRow()
                item_name = self.window.ui.table_preparing.item(index,2)
                item_color = self.window.ui.table_preparing.item(index,3)
                item_meter = self.window.ui.table_preparing.item(index,4)

                toList = []
                ccList = []

                settings = self.setting_coll.find_one({"_id":"notifications"})
                for setting in settings:
                    if setting == "supplying_departmant":
                        for adress in settings[setting]:
                            toList.append(adress["mail"])
                    elif setting == "executive":
                        for adress in settings[setting]:
                            toList.append(adress["mail"])

                subject = f"{order_code} / {item_id} BEKLEYENE ALINDI"
                line = f"Aşağıda belirtilen ürün beklemeye alındı,\n\n{cause.capitalize()}.\n\n"
                body =  line + f"{item_name.text()} {item_color.text()}  {item_meter.text()} MT"

                self.send_notification(toList,ccList,subject,body)
                self.feedback_messageBox(f"{order_code}/{item_id} beklemeye alındı.")
                self.load_data_to_windows()

            else:
                raise Exception("Bekleme sebebi belirtilmedi!")
        
        except Exception as ex:
            self.warning_messageBox(f"Hatalı İşlem : {ex} ")

    def sendBack_fromPre_to_new(self):
        order_code, item_id = self.get_selected_item_on_table(self.window.ui.table_preparing, 0, 1)
        self.update_order_status(order_code, item_id, "new")
        self.feedback_messageBox(f"{order_code}/{item_id} hazırlık iptal edildi.")
        self.load_data_to_windows()       

    ######################### WAITING BUTTON FUNCTIONS ########################################
    def doubleClick_onWait(self):
        order_code, item_id = self.get_selected_item_on_table(self.window.ui.table_waiting, 0,1)
        self.double_click_messageBox(order_code,item_id)

    def prepare_waiting_order(self):
        try:
            order_code, item_id = self.get_selected_item_on_table(self.window.ui.table_waiting, 0, 1)
            self.update_order_status(order_code, item_id, "preparing")
            self.order_coll.update_one({"_id":order_code},{"$unset":{f"Order Details.{item_id}.Waiting_cause":""}}) 
            self.order_coll.update_one({"_id":order_code},{"$unset":{f"Order Details.{item_id}.Waiting_info":""}}) 
            self.order_coll.update_one({"_id":order_code},{"$unset":{f"Order Details.{item_id}.Info_by":""}}) 
            self.feedback_messageBox(f"{order_code}/{item_id} hazırlanmaya başladı.")
            self.load_data_to_windows() 
        except  pymongo.errors.PyMongoError:
            self.warning_messageBox("İnternet bağlantınızı kontrol ediniz!") 

    def add_info(self):
        try:
            order_code, item_id = self.get_selected_item_on_table(self.window.ui.table_waiting, 0, 1)
            info , ok = QInputDialog.getText(self.window,"Bilgi Ekle","Bilgi",QLineEdit.Normal)
            if info and ok is not None:
                query = {"_id": order_code}
                new_value = {"$set": { f"Order Details.{item_id}.Waiting_info" : info,
                                    f"Order Details.{item_id}.Info_by" : self.username
                }}
                self.order_coll.update_one(query, new_value)
                self.feedback_messageBox(f"{order_code}/{item_id} bilgi eklendi.")
        except  pymongo.errors.PyMongoError:
            self.warning_messageBox("İnternet bağlantınızı kontrol ediniz!")
            
    def sendBack_fromWt_to_new(self):
        try:
            order_code, item_id = self.get_selected_item_on_table(self.window.ui.table_waiting, 0, 1)
            self.update_order_status(order_code, item_id, "new")
            self.order_coll.update_one({"_id":order_code},{"$unset":{f"Order Details.{item_id}.Waiting_cause":""}}) 
            self.order_coll.update_one({"_id":order_code},{"$unset":{f"Order Details.{item_id}.Waiting_info":""}}) 
            self.order_coll.update_one({"_id":order_code},{"$unset":{f"Order Details.{item_id}.Info_by":""}}) 
            self.feedback_messageBox(f"{order_code}/{item_id} bekleme iptal edildi.")
            self.load_data_to_windows() 
        except  pymongo.errors.PyMongoError:
            self.warning_messageBox("İnternet bağlantınızı kontrol ediniz!") 

    ######################### READY BUTTON FUNCTIONS ########################################
    def doubleClick_onRdy(self):
        order_code, item_id = self.get_selected_item_on_table(self.window.ui.table_ready, 0,4)
        self.double_click_messageBox(order_code,item_id)

    def deliver_order(self):
        try:
            order_code, item_id = self.get_selected_item_on_table(self.window.ui.table_ready, 0, 4)
            self.update_order_status(order_code, item_id, "delivered")
            delivered_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            query = {"_id": order_code}
            new_value = {"$set": { f"Order Details.{item_id}.Delivered_at" : delivered_at}}

            self.order_coll.update_one(query, new_value)
            self.feedback_messageBox(f"{order_code}/{item_id} sevk edildi.")
            self.load_data_to_windows()
        except  pymongo.errors.PyMongoError:
            self.warning_messageBox("İnternet bağlantınızı kontrol ediniz!") 

    def sendBack_fromRdy_to_prep(self):
        order_code, item_id = self.get_selected_item_on_table(self.window.ui.table_ready, 0, 4)
        self.update_order_status(order_code, item_id, "preparing")
        self.feedback_messageBox(f"{order_code}/{item_id} tamamlama iptal edildi.")
        self.load_data_to_windows() 


#################################### ORDER ############################################
#######################################################################################
#######################################################################################

    def loadTableUi(self):
        try:
            self.order.ui.cb_cargos.clear()
            self.order.ui.cb_customers.clear()

            #TO LOAD COMPANY COMBOBOX
            self.order.ui.cb_customers.addItem(" ")
            for customer in self.customer_coll.find():
                customer_name = customer["_id"]
                self.order.ui.cb_customers.addItem(customer_name)
            
            #TO LOAD CARGO COMBOBOX
            self.order.ui.cb_cargos.addItem(" ")
            for cargo in self.cargo_coll.find():
                cargo_name = cargo["_id"]
                self.order.ui.cb_cargos.addItem(cargo_name)      

            #self.ui.table_details.setRowCount(len(products))
            self.order.ui.table_details.setHorizontalHeaderLabels(("ÜRÜN","KOD","METRE"))
            self.order.ui.table_details.setColumnWidth(0,110)
            self.order.ui.table_details.setColumnWidth(1,110)
            self.order.ui.table_details.setColumnWidth(2,75)

            today = date.today()
            year = today.year
            month = today.month
            day = today.day

            self.order.ui.order_date.setDate(QtCore.QDate(year, month, day))
      

            # When user tabs to last cell, one more row is crated by itself
            self.order.ui.table_details.selectionModel().selectionChanged.connect(self.on_selectionChanged)
            self.order.ui.cb_cargos.currentTextChanged.connect(self.transfer_info_on_form)
            self.order.ui.cb_customers.currentTextChanged.connect(self.transfer_info_on_form)
        except pymongo.errors.PyMongoError:
            self.warning_messageBox("İnternet bağlantınızı kontrol ediniz!")
            self.order.close()

    def on_selectionChanged(self,selected):
        for ix in selected.indexes():
            print(f"Selected Cell Location Row {ix.row()} , Column {ix.column()}")
            self.selected_column = ix.column()
            print(f"selected column {self.selected_column}")
            self.selected_row = ix.row()
            print(f"selected row {self.selected_row}")
            rowCount = self.order.ui.table_details.rowCount()
            columnCount = self.order.ui.table_details.columnCount()
            if ix.row() == (rowCount-1) and ix.column() == (columnCount-1):
                self.order.ui.table_details.insertRow(rowCount)

    def transfer_info_on_form(self):
        try:
            if self.cargo_coll.find_one({"_id":self.order.ui.cb_cargos.currentText()}) is not None:
                cargo = self.cargo_coll.find_one({"_id":self.order.ui.cb_cargos.currentText()})
                if self.order.ui.cb_cargos is not None:
                    self.order.ui.txt_ship_adress.setText(cargo["adress"])
                    self.order.ui.txt_ship_tel.setText(cargo["phone"])
            else:
                self.order.ui.txt_ship_adress.clear()
                self.order.ui.txt_ship_tel.clear()              

            if self.customer_coll.find_one({"_id":self.order.ui.cb_customers.currentText()}) is not None:
                customer = self.customer_coll.find_one({"_id":self.order.ui.cb_customers.currentText()})
                if self.order.ui.cb_cargos is not None:
                    self.order.ui.txt_receiver_name.setText(customer["_id"])
            else:
                self.order.ui.txt_receiver_name.setText("")

        except  pymongo.errors.PyMongoError:
            self.warning_messageBox("İnternet bağlantınızı kontrol ediniz!")
            self.order.close()
   
    def set_focus(self):
        self.keyboard.press(Key.enter)
        self.keyboard.release(Key.enter)
        self.keyboard.press(Key.tab)
        self.keyboard.release(Key.tab)
        self.keyboard.press(Key.enter)
        self.keyboard.release(Key.enter)
        self.keyboard.press(Key.shift_l)
        self.keyboard.press(Key.tab)
        self.keyboard.release(Key.tab)
        self.keyboard.release(Key.shift_l)
        self.keyboard.press(Key.enter)
        self.keyboard.release(Key.enter)
    
    def get_searching_item(self):
        item = self.select_clicked_item(self.searching_form.ui.searching_list)
        if item is not None:
                self.order.ui.table_details.setItem(self.selected_row, self.selected_column,QTableWidgetItem(item.text()))
                self.searching_form.close()
            
    def open_searchingForm(self):
        try:
            if self.selected_column == 0:
                text = self.order.ui.table_details.item(self.selected_row, self.selected_column)
                if text is not None:
                    print(text.text())
                    self.searching_form.ui.txt_search.setText(text.text())
                    for product in self.product_coll.find({"_id":{"$regex": f"^{text.text().upper()}"}}):
                        product_name = product["_id"]
                        self.searching_form.ui.searching_list.addItem(str(product_name))
                    self.searching_form.show()
                else:
                    self.searching_form.ui.txt_search.setText("")
                    for product in self.product_coll.find().sort("_id",1):
                        product_name = product["_id"]
                        self.searching_form.ui.searching_list.addItem(str(product_name))
                    self.searching_form.show()
            
            elif self.selected_column == 1:
                text = self.order.ui.table_details.item(self.selected_row, self.selected_column)
                if text is not None:
                    self.searching_form.ui.txt_search.setText(text.text())
                    product_name = self.order.ui.table_details.item(self.selected_row, 0)
                    if product_name is not None:
                        for product in self.product_coll.find({"_id": product_name.text().upper}):
                            lenght = len(product["color_codes"])
                            for i in range(lenght):
                                if text.text() in product["color_codes"][i][-2:]:
                                    self.searching_form.ui.searching_list.addItem(product["color_codes"][i])
                        self.searching_form.show()
                    else:
                        self.warning_messageBox("Ürün seçimi yapılmadı!")

                else:
                    product_name = self.order.ui.table_details.item(self.selected_row, 0)
                    if product_name is not None:
                        for product in self.product_coll.find({"_id": product_name.text().upper()}):
                            lenght = len(product["color_codes"])
                            for i in range(lenght):
                                self.searching_form.ui.searching_list.addItem(product["color_codes"][i])
                        self.searching_form.show()
                    else:
                        self.warning_messageBox("Ürün seçimi yapılmadı!")

        except AttributeError:
            print("F1 Kynaklı attribute error çalıştı")
            self.set_focus()
        except  pymongo.errors.PyMongoError:
            self.warning_messageBox("İnternet bağlantınızı kontrol ediniz!")
            self.order.close()

    def open_orderForm(self):
        self.order.show()  
        self.loadTableUi()

    def create_orderCode(self,company):
        try:
            order_date = self.order.ui.order_date.text().split(".")
            if len(order_date[0]) == 1:
                day = order_date[0] 
                order_date[0] = "0" + day
            ##### check if any other order at the same time
            repeat = 1

            for order in self.order_coll.find():
                while company[:3] + order_date[0] + order_date[1] + order_date[2][2:] + "-" + str(repeat) == order["_id"]:
                    repeat +=1
            
            customer = self.customer_coll.find_one({"_id":company})
            isSubscribe = customer["extra_code"]
            if isSubscribe == True:
                text, ok = QInputDialog.getText(self.order,"Ek Sipariş Kodu","Kodu Gir:")
                if ok and text is not None:
                        repeat = text
            ###############################################

            return company[:3] + order_date[0] + order_date[1] + order_date[2][2:] + "-" + str(repeat)

        except TypeError:
            print("TypeError: Company Info is None")
            self.warning_messageBox("Lütfen Firma Seçimi Yapınız!")

    def not_freeze_the_form(self,True_False):

        self.order.ui.cb_customers.setEnabled(True_False)
        #RECEIVER INFO 
        self.order.ui.txt_receiver_name.setEnabled(True_False)
        self.order.ui.txt_author.setEnabled(True_False)
        self.order.ui.txt_cust_tel.setEnabled(True_False)
        self.order.ui.txt_gsm_tel.setEnabled(True_False)
        self.order.ui.txt_cust_adress.setEnabled(True_False)

        #SHIPMENT INFO   
        self.order.ui.cb_cargos.setEnabled(True_False)
        self.order.ui.txt_customer_code.setEnabled(True_False)
        self.order.ui.txt_ship_type.setEnabled(True_False)
        self.order.ui.txt_ship_tel.setEnabled(True_False)
        self.order.ui.txt_ship_adress.setEnabled(True_False)

        #ORDER DATE
        self.order.ui.order_date.setEnabled(True_False)

        #LABELS
        self.order.ui.lbl_order_code.setEnabled(True_False)
        self.order.ui.lbl_date.setEnabled(True_False)
        self.order.ui.label.setEnabled(True_False)
        self.order.ui.label_2.setEnabled(True_False)
        self.order.ui.label_3.setEnabled(True_False)
        self.order.ui.label_4.setEnabled(True_False)
        self.order.ui.label_5.setEnabled(True_False)
        self.order.ui.label_6.setEnabled(True_False)
        self.order.ui.label_7.setEnabled(True_False)
        self.order.ui.label_8.setEnabled(True_False)
        self.order.ui.label_11.setEnabled(True_False)
        self.order.ui.label_12.setEnabled(True_False)
        self.order.ui.label_13.setEnabled(True_False)
        self.order.ui.label_14.setEnabled(True_False)
        self.order.ui.label_15.setEnabled(True_False)
        self.order.ui.label_16.setEnabled(True_False)
        self.order.ui.label_17.setEnabled(True_False)
        self.order.ui.label_18.setEnabled(True_False)

        #BUTTONS
        self.order.ui.btn_save.setEnabled(True_False)
        self.order.ui.btn_refresh.setEnabled(True_False)

        #TABLE
        self.order.ui.table_details.setEnabled(True_False)

    def refresh_form(self):

        #RECEIVER INFO 
        self.order.ui.txt_receiver_name.setText("")
        self.order.ui.txt_author.setText("")
        self.order.ui.txt_cust_tel.setText("")
        self.order.ui.txt_gsm_tel.setText("")
        self.order.ui.txt_cust_adress.setText("")

        #SHIPMENT INFO   
        self.order.ui.txt_customer_code.setText("")
        self.order.ui.txt_ship_type.setText("")
        self.order.ui.txt_ship_tel.setText("")
        self.order.ui.txt_ship_adress.setText("")
        
        self.order.ui.lbl_order_code.setText("")
        self.order.ui.lbl_date.setText("")
        
        #refresh the table ???
        rowCount = self.order.ui.table_details.rowCount()
        for row in range (rowCount):
            if self.order.ui.table_details.item(row,1) and self.order.ui.table_details.item(row,0) and self.order.ui.table_details.item(row,2) is not None:
                self.order.ui.table_details.item(row,0).setText("")
                self.order.ui.table_details.item(row,1).setText("")
                self.order.ui.table_details.item(row,2).setText("")
        self.order.ui.table_details.setRowCount(2)
    
    def save_order(self):
        try:
            #COMPANY
            company = self.order.ui.cb_customers.currentText()
            #RECEIVER INFO 
            receiver = self.order.ui.txt_receiver_name.text()
            authority = self.order.ui.txt_author.text()
            company_phone = self.order.ui.txt_cust_tel.text()
            company_gsm = self.order.ui.txt_gsm_tel.text()
            company_adress = self.order.ui.txt_cust_adress.text()

            #SHIPMENT INFO   
            shipper_name = self.order.ui.cb_cargos.currentText()
            customer_code = self.order.ui.txt_customer_code.text()
            ship_type = self.order.ui.txt_ship_type.text()
            ship_phone = self.order.ui.txt_ship_tel.text()
            ship_adress = self.order.ui.txt_ship_adress.text()

            #ORDER DATE
            order_date = self.order.ui.order_date.text()

            #CREATING DATE
            created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            #to create a specific code for each order
            order_code = self.create_orderCode(company)

            #veritabanına aktarım
            self.order_data = {
                "_id": order_code,
                "Company Name" : company,
                "Crated_by":self.username,
                "Created_at": created_at,
                "Order_at" : order_date,
                "Receiver Info" : {
                    "Receiver Name" : receiver,
                    "Authority" : authority,
                    "Company Phone" : company_phone,
                    "Company GSM" : company_gsm,
                    "Company Adress" : company_adress
                },
                "Shipping Info" : {
                    "Shipper Name" : shipper_name,
                    "Customer Code": customer_code,
                    "Shipping Type" : ship_type,
                    "Shipper Phone" : ship_phone,
                    "Shipper Adress":ship_adress
                },
                "Order Details" : {}
            }

            #↓table
            rowCount = self.order.ui.table_details.rowCount()
            print(rowCount)

            for row in range(rowCount):
                for column in range(3):
                    if self.order.ui.table_details.item(row,column) is None:
                        print(f"{self.order.ui.table_details.item(row,column)} was None")
                        self.order.ui.table_details.setItem(row,column,QTableWidgetItem(""))
                    else:
                        print("buldu")
            feedback = ""
            line = 1
            for row in range (rowCount):
                if self.order.ui.table_details.item(row,1) is None and self.order.ui.table_details.item(row,0) is None and self.order.ui.table_details.item(row,2) is None:
                    print("skipped the row")
                elif self.order.ui.table_details.item(row,1).text() == "" and self.order.ui.table_details.item(row,0).text() == ""  and self.order.ui.table_details.item(row,2).text() == "":
                    print("skipped the row")
                else:
                    if self.order.ui.table_details.item(row,1).text() != "" and self.order.ui.table_details.item(row,0).text() != "" and self.order.ui.table_details.item(row,2).text() != "":
                        product_name = self.order.ui.table_details.item(row,0).text().upper()
                        color = self.order.ui.table_details.item(row,1).text()
                        meter = self.order.ui.table_details.item(row,2).text()

                        
                        product = self.product_coll.find_one({"_id":product_name})
                        if product is not None:
                            if color in product["color_codes"]:
                                if self.isFloat(meter) == True:
                                    self.order_data["Order Details"][str(line)] = {
                                        "Status": "new",
                                        "Item" : product_name,
                                        "Color" : color,
                                        "Meter" : meter,
                                        "Note"  :   "",
                                        "Delivered_at":"Henüz Teslim Edilmedi"
                                    }   
                                    line += 1
                                    feedback += f"{str(row + 1):3}{product_name:10}{color:10}  {meter:5}MT\n"
                                else:
                                    if self.isInt(meter) == True:
                                        self.order_data["Order Details"][str(line)] = {
                                            "Status": "new",
                                            "Item" : product_name,
                                            "Color" : color,
                                            "Meter" : meter,
                                            "Note"  :   "",
                                            "Delivered_at":"Henüz Teslim Edilmedi"
                                        }

                                        line += 1
                                        feedback += f"{str(row + 1):3}{product_name:10}{color:10}  {meter:5}MT\n"  
                                    else:
                                        raise Exception(f"Metre Bilgisi doğru girilmedi\n\nHatalı İşlem: {meter}\nSatır Sırası: {row+1}")
                            else:
                                raise Exception(f"Ürün Kodu Bulunamadı\n\nHatalı İşlem: {color}\nSatır Sırası: {row+1}")
                        else:
                            raise Exception(f"Ürün Bulunamadı\n\nHatalı İşlem: {product_name}\nSatır Sırası: {row+1}")
                    else:
                        raise Exception(f"Detay bulunamadı\n\nSatır Sırası: {row+1}")


            if order_code is None :
                raise AttributeError
            if len(self.order_data["Order Details"]) == 0:
                raise Exception(f"Sipariş Detayı Bulunamadı")

            self.order.ui.lbl_order_code.setText(order_code)
            self.order.ui.lbl_date.setText(created_at)
                
            print(self.order_data)
            self.not_freeze_the_form(False)
            time.sleep(1)
            self.feedback_messageBox(order_code,"eklendi")
            self.order.close()
            self.refresh_form()
            self.not_freeze_the_form(True)
            self.order_coll.insert_one(self.order_data)

            
            ################## MAIL NOTIFICATION #############################################
            ##################################################################################
            ################## FINDING SUBSCRIBERS ###########################################
            toList = []
            ccList = []

            settings = self.setting_coll.find_one({"_id":"notifications"})
            for setting in settings:
                if setting == "operation_departmant":
                    for adress in settings[setting]:
                        toList.append(adress["mail"])
                elif setting == "executive":
                    for adress in settings[setting]:
                        ccList.append(adress["mail"])
                elif setting == "customer_service":
                    for adress in settings[setting]:
                        ccList.append(adress["mail"])
                    
            customer = self.customer_coll.find_one({"_id":company})
            for info in customer:
                if "mail" in info:
                    if customer[info] != "":
                        ccList.append(customer[info])

            ################### SIMPLE MAIL STYLING ###############################################
            subject = f"SİPARİŞ / ORDER : {order_code}"
            
            intro1 = f"{'Sipariş Kodu:':20}{order_code}\n"
            intro2 = f"{'Firma:':20}{company}\n"
            intro3 = f"{'Sipariş Tarih:':20}{order_date}\n"
            intro4 = f"{'Düzenlenme Tarih:':20}{created_at}\n"
            intro5 = f"{'Düzenleyen:':20}{self.username}\n"
            intros = intro1 + intro2 + intro3 + intro4 + intro5

            receiver_head = f"{'ALICI BİLGİLERİ':20}\n"
            receiver_info1 = f"{'Alıcı Adı:':20}{receiver}\n"
            receiver_info2 = f"{'Yetkili Kişi:':20}{authority}\n"
            receiver_info3 = f"{'Tel No:':20}{company_phone}\n"
            receiver_info4 = f"{'GSM:':15}{company_gsm}\n"
            receiver_info5 =  f"{'Adres:':20}{company_adress}\n"
            receiver_infos = receiver_head + receiver_info1 + receiver_info2 + receiver_info3 + receiver_info4 + receiver_info5

            shipment_head = f"{'TESLİMAT BİLGİLERİ':20}\n"
            shipment_info1 = f"{'Nakliyeci Adı:':20}{shipper_name}\n"
            shipment_info2 = f"{'Müşteri No:':20}{customer_code}\n"
            shipment_info3 = f"{'Taşıma Tipi:':20}{ship_type}\n"
            shipment_info4 = f"{'Tel No':20}{ship_phone}\n"
            shipment_info5 = f"{'Adres:':20}{ship_adress}\n"
            shipment_infos = shipment_head + shipment_info1 + shipment_info2 + shipment_info3 + shipment_info4 + shipment_info5

            body = "\n" + intros + "\n\n" + feedback + "\n\n" + receiver_infos + "\n" + shipment_infos

            self.send_notification(toList,ccList,subject,body)

            #######################################################################################
            self.load_data_to_windows()
        
        except pymongo.errors.DuplicateKeyError:
            self.warning_messageBox("Bu sipariş kodu daha önce eklenmiş.")
        except  pymongo.errors.PyMongoError:
            self.warning_messageBox("İnternet bağlantınızı kontrol ediniz!")
        except Exception as ex:
            self.warning_messageBox(f"Hata Kodu: {ex}")
        except AttributeError:
            print("Firma Bilgisi Girilmedi!")


################################ REPORT WINDOW ########################################
    def open_reportForm(self):
        self.report_form.start(self.username,self.password)
        self.report_form.show()
        

################################ SETTING WINDOW ########################################
########################################################################################
########################################################################################

    def load_settings_data(self):
        try:
            for customer in self.customer_coll.find():
                customer_name = customer["_id"]
                self.settings.ui.customer_listWidget.addItem(customer_name)

            for cargo in self.cargo_coll.find():
                cargo_name = cargo["_id"]
                self.settings.ui.cargo_listWidget.addItem(cargo_name)
        except  pymongo.errors.PyMongoError:
            self.warning_messageBox("İnternet bağlantınızı kontrol ediniz!")

    def open_settings(self):
        self.settings.ui.customer_listWidget.clear()
        self.settings.ui.cargo_listWidget.clear()

        self.load_settings_data()
        self.settings.show()

    def refresh_setting(self):
        self.settings.ui.customer_listWidget.clear()
        self.settings.ui.cargo_listWidget.clear()
        self.load_settings_data()


##################################### CUSTOMER SETTINGS ##################################
##########################################################################################

    def clear_customer_settings(self):
        self.setting_form.ui.txt_company.setText("")
        self.setting_form.ui.txt_company.setEnabled(True)
        self.setting_form.ui.txt_mail1.setText("") 
        self.setting_form.ui.txt_mail2.setText("")
        self.setting_form.ui.txt_mail3.setText("")
        self.setting_form.ui.cb_extra_code.setChecked(False)
        self.setting_form.ui.cb_notification.setChecked(False)       

    def open_customer_settings_to_add(self):
        self.setting_form.ui.stackedWidget.setCurrentIndex(0)
        self.setting_form.show()

    def open_customer_settings_to_edit(self):
        try:
            item = self.select_clicked_item(self.settings.ui.customer_listWidget)
            customer = self.customer_coll.find_one({"_id":item.text()})

            self.setting_form.ui.txt_company.setText(item.text())
            self.setting_form.ui.txt_company.setEnabled(False)
            self.setting_form.ui.txt_mail1.setText(customer["mail1"]) 
            self.setting_form.ui.txt_mail2.setText(customer["mail2"])
            self.setting_form.ui.txt_mail3.setText(customer["mail3"])
            self.setting_form.ui.cb_extra_code.setChecked(customer["extra_code"])
            self.setting_form.ui.cb_notification.setChecked(customer["notification"])

            self.setting_form.ui.stackedWidget.setCurrentIndex(0)
            self.setting_form.show()
        except  pymongo.errors.PyMongoError:
            self.warning_messageBox("İnternet bağlantınızı kontrol ediniz!")

    def remove_customer(self):
        try:
            item = self.select_clicked_item(self.settings.ui.customer_listWidget)
            if item is not None:
                self.customer_coll.delete_one({"_id":item.text()})
                self.feedback_messageBox(item.text(),"silindi")
                self.refresh_setting()
        except  pymongo.errors.PyMongoError:
            self.warning_messageBox("İnternet bağlantınızı kontrol ediniz!")

    def add_customer(self):

        #   Burada kullanılan try-except edit fonksiyonu için çalışmaktadır.
        try:
            if self.setting_form.ui.txt_company is not None:
                print("not none olduğu tespit edildi")
                company = self.setting_form.ui.txt_company.text()
                mail1 = self.setting_form.ui.txt_mail1.text()
                mail2 = self.setting_form.ui.txt_mail2.text()
                mail3 = self.setting_form.ui.txt_mail3.text()
                extra_code = self.setting_form.ui.cb_extra_code.isChecked()
                notification = self.setting_form.ui.cb_notification.isChecked()

                self.customer_data = {
                    "_id"  :company,
                    "mail1" :mail1,
                    "mail2" :mail2,
                    "mail3" :mail3,
                    "extra_code":extra_code,
                    "notification":notification
                } 
                self.customer_coll.insert_one(self.customer_data)
                self.feedback_messageBox(company,"eklendi")
                self.setting_form.close()
                self.clear_customer_settings()

        except pymongo.errors.DuplicateKeyError:
            self.customer_coll.update_one(
                {"_id" : company,},
                {"$set": {
                 "mail1":mail1,
                 "mail2":mail2,
                 "mail3":mail3,
                 "extra_code":extra_code,
                 "notification":notification
                }}
            )
            self.feedback_messageBox(company,"düzenlendi")
            self.setting_form.close()
            self.clear_customer_settings()
        self.refresh_setting()

##################################### CARGO SETTINGS #####################################    
##########################################################################################

    def clear_cargo_settings(self):

        self.setting_form.ui.txt_cargo_name.setText("")
        self.setting_form.ui.txt_cargo_name.setEnabled(True)
        self.setting_form.ui.txt_cargo_authority.setText("") 
        self.setting_form.ui.txt_cargo_phone.setText("")
        self.setting_form.ui.txt_cargo_adress.setPlainText("")


    def open_cargo_settings_to_add(self):
        self.setting_form.ui.stackedWidget.setCurrentIndex(1)
        self.setting_form.show()

    def open_cargo_settings_to_edit(self):
        item = self.select_clicked_item(self.settings.ui.cargo_listWidget)
        cargo = self.cargo_coll.find_one({"_id":item.text()})

        self.setting_form.ui.txt_cargo_name.setText(item.text())
        self.setting_form.ui.txt_cargo_name.setEnabled(False)
        self.setting_form.ui.txt_cargo_authority.setText(cargo["authority"]) 
        self.setting_form.ui.txt_cargo_phone.setText(cargo["phone"])
        self.setting_form.ui.txt_cargo_adress.setPlainText(cargo["adress"])

        self.setting_form.ui.stackedWidget.setCurrentIndex(1)
        self.setting_form.show()

    def remove_cargo(self):
        item = self.select_clicked_item(self.settings.ui.cargo_listWidget)
        if item is not None:
            self.cargo_coll.delete_one({"_id":item.text()})
            self.feedback_messageBox(item.text(),"silindi")
            self.refresh_setting()

    def add_cargo(self):

        #   Burada kullanılan try-except edit fonksiyonu için çalışmaktadır.
        try:
            if self.setting_form.ui.txt_cargo_name is not None:
                print("not none olduğu tespit edildi")
                cargo = self.setting_form.ui.txt_cargo_name.text()
                cargo_authority = self.setting_form.ui.txt_cargo_authority.text()
                cargo_phone = self.setting_form.ui.txt_cargo_phone.text()
                cargo_adress = self.setting_form.ui.txt_cargo_adress.toPlainText()

                self.cargo_data = {
                    "_id"  :cargo,
                    "authority" :cargo_authority,
                    "phone" :cargo_phone,
                    "adress" :cargo_adress,
                } 
                self.cargo_coll.insert_one(self.cargo_data)
                self.feedback_messageBox(cargo,"eklendi")
                self.setting_form.close()
                self.clear_cargo_settings()

        except pymongo.errors.DuplicateKeyError:
            self.cargo_coll.update_one(
                {"_id" : cargo},
                {"$set": {
                 "authority":cargo_authority,
                 "phone":cargo_phone,
                 "adress":cargo_adress
                }}
            )
            self.feedback_messageBox(cargo,"düzenlendi.")
            self.clear_cargo_settings() 
            self.setting_form.close()
        self.refresh_setting()



lets_go = App()

