import pymongo
from datetime import datetime, date
from email.message import EmailMessage
import smtplib, ssl
import sys
from _server import Ui_Form
from PyQt5.QtWidgets import QAction,QShortcut
from PyQt5 import QtWidgets,QtGui
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import QTimer, QTime

class ServerWidget(QtWidgets.QMainWindow):
    def __init__(self,username,password):
        super(ServerWidget,self).__init__()

        self.username = username
        self.password = password

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.set_time()

        self.setWindowIcon(QtGui.QIcon('icon.png'))

        self.quit = QAction("Quit",self)
        self.quit.triggered.connect(self.closeEvent)

        self.connect_db()
        self.load_screen()
        
        timer = QTimer(self)
        timer.timeout.connect(self.display_time)
        timer.start(1000)

        self.ui.txt_time.textChanged.connect(self.check_time)

        self.shortcut = QShortcut(QKeySequence('F1'), self)
        self.shortcut.activated.connect(self.start_console)

        self.write_on_records("Application is activated.")

    def set_time(self):
        ################## TAKES START OF THE DAY ########################
        ##################################################################
        self.today = date.today()
        self.year = self.today.year
        self.month = self.today.month
        self.day = self.today.day
        self.this_date_object = datetime(int(self.year), int(self.month),int(self.day-1),int(18))
        ###################################################################
        self.now = datetime.now().strftime('%Y-%m-%d %H:%M:%S') ##### NOW ######
        
    def connect_db(self):
        try:
            self.myclient = pymongo.MongoClient(f"mongodb+srv://{self.username}:{self.password}@cluster0.asdnj.mongodb.net/app_test?retryWrites=true&w=majority")
            self.mydb = self.myclient["order-load"]
            self.customer_coll = self.mydb["customers"]
            self.order_coll = self.mydb["orders"]
            self.setting_coll = self.mydb["settings"]
            self.write_on_records("Database connection is activated.")
        except Exception as ex:
            self.send_notification("ERROR OCCURED AT THE SERVER",f"Hello,\n\nError while connecting to Database is shared below,\n{ex}\n\nLast Seen: {self.now}\n\n\nPlease do not reply this e-mail.")
            self.write_on_records(f"Error occured while connecting to Database, {ex}")
    
    def load_screen(self):
        try:
            ############ TO LIMIT LIST WIDGET'S AMOUNT IF ITEM UNDER THE 100 ###########
            ############################################################################
            file = open("records.txt", "r")
            line_count = 0
            for line in file:
                if line != "\n":
                    line_count += 1
            file.close()

            if line_count >= 100 :
                a_file = open("records.txt", "r")
                # get list of lines
                lines = a_file.readlines()
                a_file.close()
                new_file = open("records.txt", "w")
                # Deleting oldest record
                count = 0
                for line in lines:
                    if count != 1:
                        count += 1
                        continue
                    new_file.write(line)
                new_file.close()
            ################################################################################

            self.ui.list_records.clear()
            # Using readlines()
            file1 = open("records.txt", 'r')
            Lines = file1.readlines()
            count = 0
            # Strips the newline character
            for line in Lines:
                count += 1
                self.ui.list_records.addItem(line.strip())
            self.ui.txt_console.setText("")
            self.ui.list_records.scrollToBottom()
        except Exception as ex:
            self.send_notification("ERROR OCCURED AT THE SERVER",f"Hello,\n\nError while loading the screen is shared below,\n{ex}\n\nLast Seen: {self.now}\n\n\nPlease do not reply this e-mail.")

    def display_time(self):
        try:
            current_time = QTime.currentTime()
            display_text = current_time.toString("hh:mm:ss")
            self.ui.txt_time.setText(display_text)
        except Exception as ex:
            self.send_notification("ERROR OCCURED AT THE SERVER",f"Hello,\n\nError while displaying the time is shared below,\n{ex}\n\nLast Seen: {self.now}\n\n\nPlease do not reply this e-mail.")
            self.write_on_records(f"Error occured while displaying the time: {ex}")

    def send_notification(self,subject,body):
        try:
            setting = self.setting_coll.find_one({"_id":"notifications"})
            From = setting["admin"][0]["mail"]
            Password = setting["admin"][0]["password"]

            toList = []
            ccList = []

            settings = self.setting_coll.find_one({"_id":"notifications"})
            for setting in settings:
                if setting == "executive":
                    for adress in settings[setting]:
                        ccList.append(adress["mail"])
                elif setting == "technic":
                    for adress in settings[setting]:
                        toList.append(adress["mail"])

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
            self.write_on_records(f"Error occured while sending notification to technic: {ex}")

    def send_notification_to_customer(self,toList,ccList,subject,body):
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
            self.write_on_records(f"Error occured while sending notification to customer: {ex}")
    
    def write_on_records(self, record):
        try:
            print(record)
            with open("records.txt","r+", encoding="utf-8") as file:
                    content = file.read()
                    content = content + "\n" + f"{str(self.now)}: " + record
                    file.seek(0)
                    file.write(content) 
            self.load_screen()

            settings  = self.setting_coll.find({"_id":"server_log"})
            for setting in settings:
                count = 0
                for line in setting["records"]:
                    count += 1
            if count >= 50:
                delete_amount = count - 50 
                settings  = self.setting_coll.find({"_id":"server_log"})
                for setting in settings:
                    del_rpt = 0
                    for line in setting["records"]:
                        if del_rpt < delete_amount:
                            self.setting_coll.update_one({"_id":"server_log"},{"$pull":{"records" : line}}) 
                            del_rpt += 1

            self.setting_coll.update_one({"_id":"server_log"},{"$push":{"records" :str(self.now)+ " " + str(record)}}) 
            self.setting_coll.update_one({"_id":"server_log"},{"$set":{"last_seen":str(self.now)}})
            
        except Exception as ex:
            self.send_notification("ERROR OCCURED AT THE SERVER",f"Hello,\n\nError while writing records is shared below,\n{ex}\n\nLast Seen: {self.now}\n\n\nPlease do not reply this e-mail.")
            
    def check_time(self):
        self.set_time()
        if self.ui.txt_time.text() == "18:00:00":
            self.write_on_records("Time is matched to send loading reports.")
            self.send_reports()

    def send_reports(self):
        self.write_on_records("Sending Report Process is started.")
        try:
            loading_count = 0
            for company in self.customer_coll.find():
                delivered_items = []
                for order in self.order_coll.find():
                    if order["Company Name"] == company["_id"]:
                        counter = 1
                        for order_items in order["Order Details"]:
                            if order['Order Details'][order_items]['Delivered_at'] != "Henüz Teslim Edilmedi":
                                deliver_date = order['Order Details'][order_items]['Delivered_at']
                                deliver_date_object = datetime.strptime(deliver_date, '%Y-%m-%d %H:%M:%S')
                                if deliver_date_object >= self.this_date_object:
                                    cargo_recevier = f"LOADING ID: {counter}\nCARGO: {order['Shipping Info']['Shipper Name']}  RECEIVER: {order['Receiver Info']['Receiver Name']}\n"
                                    delivered_items.append(f"{cargo_recevier}{order['_id']}/{order_items}: {order['Order Details'][order_items]['Item']} {order['Order Details'][order_items]['Color']} {order['Order Details'][order_items]['Meter']} MT") 
                                    counter += 1 
                if len(delivered_items)  > 0:
                    toList = []
                    ccList = []

                    customer = self.customer_coll.find_one({"_id":company["_id"]})
                    for info in customer:
                        if "mail" in info:
                            if customer[info] != "":
                                toList.append(customer[info])

                    settings = self.setting_coll.find_one({"_id":"notifications"})
                    for setting in settings:
                        if setting == "executive":
                            for adress in settings[setting]:
                                ccList.append(adress["mail"])
                
                    subject = f"LOADING REPORT: {company['_id']} {self.day}{self.month}{str(self.year)[-2:]}"
                    body = "Hello,\n\nThe details of your loading done today are shared below,\n\n\n"
                    for item in delivered_items:
                        body += (item + "\n\n")
                    body += "\n\nPlease do not reply this e-mail."

                    self.send_notification_to_customer(toList,ccList,subject,body)
                    self.write_on_records(f"Information of the Loading of {len(delivered_items)} item succesfully sent to {company['_id']}.")
                    loading_count += 1
            if loading_count == 0:
                self.write_on_records("There was no any loading today to send as a report.")
            self.write_on_records("Sending Report Process is completed.")

        except Exception as ex:
                self.write_on_records(f"Failed while sending loading report to {company['_id']}! Error:{ex}.")
                subject = "ERROR OCCURED AT THE SERVER"
                body = f"Hello,\n\nError is shared below,\n{ex}\n\nLast Seen: {self.now}\n\n\nPlease do not reply this e-mail."
                self.send_notification(subject,body)
    
    def start_console(self):
        try:
            console_log = self.ui.txt_console.text() 
            if console_log == "test":
                self.write_on_records("Application is tested successfully.")
            elif console_log == "send_reports":
                self.write_on_records("sent_reports method is called from the console.")
                self.send_reports()
            elif console_log == "send_records":
                self.write_on_records("send_records method is called from the console.")
                with open("records.txt","r+", encoding="utf-8") as file:
                        content = file.read()
                subject = f"ORDER&LOAD SERVER RECORDS: {self.now}"
                body = f"Hello,\n\nServer records are shared below,\n\n\n{content}\n\n\nPlease do not reply this e-mail."
                self.send_notification(subject,body)
                self.write_on_records("Records are sent successfully from the console.")
            else:
                self.write_on_records("Invalid entrance is detected at the console.")
        except Exception as ex:
            self.write_on_records(f"System is failed while starting console. Error :{ex}")
                   
    def closeEvent(self,event):
        subject = "APPLICATION OF ORDER & LOAD IS CLOSED AT THE SERVER"
        body = f"Hello,\n\nClose Event of the App is activated.\nLast Seen: {self.now}\n\nPlease do not reply this e-mail."
        self.send_notification(subject,body)
        self.write_on_records("Close Event of the Server App is successfully activated.")

    
if __name__ == "__main__":
    def app():
        app = QtWidgets.QApplication(sys.argv)
        win = ServerWidget(MongoDB_username,MongoDB_password)
        win.show()
        sys.exit(app.exec_())

    app()

