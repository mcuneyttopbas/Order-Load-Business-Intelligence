# Order & Load Business Intelligence v1

This document presents the Order & Load BI Software in 4 main chapters under the headings of Introduction, Desktop User Application, Server Application and Data Modeling with
MongoDB. It aims to enrich the content with Gifs and Screenshots.

In order to make sense of the codes, it is important to have basic knowledge of Python, pymongo and pyqt5.

This project aims to contribute to the fields of user interface, artificial intelligence, data collection, data analysis, data management and digitization of business processes, 
rather than making commercial gains.

**Note** : Instead of saying "it could have been better this way or that" many times in the document, I would like to state that I did not prepare much for the project in advance,
it grew on its own as I added new features and I did it to enjoy it. Therefore, in order to see the result,
I skipped some requirements when you take a look at the codes.
However, I would like to underline that it has features that can answer the questions of many developers I encountered during my research.
When I started the project, I was new to the libraries I used, but with my current knowledge, I believe that I can finish this project in half time, which I finished in 3 weeks.

Navigate Chapters,
- [Introduction](#introduction)
  - [Functions](#functions)
  - [FAQ](#faq)
- [User Interface](#user-interface)
  - [Splash & Login](#splash--login) 
  - [Settings Forms](#settings-forms)
  - [Order Form](#order-form)
  - [Main Window](#main-window)
  - [Report Form](#report-form)
- [Server Application](#server-application)
  - [Timer](#timer) 
  - [Filter](#filter) 
  - [Recorder](#recorder) 
  - [Notifier](#recorder) 
- [Data Modelling](#data-modelling)
  - [Customers](#customers) 
  - [Cargos](#cargos)
  - [Products](#products)
  - [Orders](#orders)
  - [Notifications](#notifications)
  - [Server Log](#server-log)
- [How to Contribute?](#how-to-contribute)

  
## Introduction

It enables to make processes safer and faster in terms of operation and follow-up until the added orders are shipped.
Thanks to its easy use, it aims to save time for the departments. In short, it contributes to the transformation of raw data into a meaningful business process.

On the **Artificial Intelligence** side of the project, enhanced thinking and data analysis capability was emphasized during the design of the processes. <br>
**Search Algorithm**, which enables the user to avoid mistakes and take faster action during the product selection phase,<br>
**Root Finding Algorithms** that check whether the inputs received from the user are of Integer or Float data type,<br>
**Sorting Algorithm** that offers dynamic use of filtering and display settings while browsing reports,<br>
**Genetic Algorithms**, which provide only relevant data by e-mail in formats that change from event to event, at the stages where follow-up is very important,
as a addition, **functions that only work on** the server side at **certain times** and **conditions** show that this program makes serious use of artificial intelligence.

On the **User Interface** side, the principle of simplicity has been acted upon and it is aimed to perform all operations with the keyboard as much as possible.
The classes of windows are imported into the main file(**main.py**), and objects are derived from these classes in the App class.
Most of functions except closeEvent functions are defined in the main file so that they can be observed together.
Only the functions of the splash and report classes are defined in the source file from which they are imported.
This build was not intentionally created, but gave the developers a chance to experiment with two different methods. <br>
Please be aware that aesthetic concerns have been ignored.

One of the most important points in applications like this is the correct **Data Modelling**. 
Applications that are successful in this regard are likely to produce more practical solutions on the user interface and backend.
As a result, it is necessary to prepare environments where faster and less error-prone queries can be made for successful analysis and management of data.

Except for internet outages, most possible **Error** situations have been brought under control.
In any case, if there is no disconnection during the query phases, data corruption will not occur.

### Functions
Below is a general summary of the program's functions.
-	Adding, Editing and Deleting Customer and Cargo Informations.
-	Automatic Assignment and Sorting of Order Code
-	Adding an Order
-	Automatic Transmission of the details of the added order to the relevant customer and operation team in e-mail format
-	Thanks to the well-designed MongoDB Database Model, Tracking and Management of the order on a product basis, even if it is entered in bulk
-	Instant Tracking of All Orders from the Main Screen
-	Adding Note to an order after adding
-	Splitting Orders
-	Managing Orders (Cancellation, Preparation, Holding, Completion and Loading)
-	In case the order cannot be supplied, Adding a Reason for Waiting to the Holding Order
-	Automatic Transmission of the Holding Order to the supply unit in e-mail format along with the reason for the waiting
-	Adding an Information Note to the Holding Order about when or how it will be supplied
-	Detailed Reporting of Orders
-	Customized Settings in Order Reports (Filtering, Display Settings)
-	Converting Order Reports as an Excel File
-	Server Application Automatically Forwarding the loading details made during the day to the relevant customers at the end of the day in e-mail format
-	Automatically Transmitting Shutdown or Error situations that may occur in the Server Application to the technical unit in an instant mail format

### FAQ
Below you can see some of the frequently asked questions by the developers in several platform, which you can find answers to or get ideas from in this project.
#### PyQt5
-	How to make a multi-window application with PyQt5?
-	What kind of errors need to be avoided when developing a multi-window application with PyQt5?
-	How to assign signal-slots in PyQt5?
-	How to dynamically pass data to QTableWidget?
-	How to add close event in widgets?
-	How to create shortcut object with QShorcut on windows?
-	How can I access the information in the selected row on the QTableWidget?
-	How can I get a new row to be added when it comes to the last row in QTableWidget?
#### MongoDB
-	How should user name and password control be provided via MongoDB?
-	How to access, filter and sort fields in nested dictionary data type?
-	How to add new values, update and delete fields in nested dictionary data type?
-	How to add new keys and values to arrays?
-	How can arrays be updated?
-	How to associate documents in different collections?
#### Others
-	How to send mail with Python?
-	How to control keyboard keys with Python?
-	How to manage settings locally with json file?
-	How to read file and apply data with Pandas library?
-	How to synchronize data and export to excel file with Openpyexcel library?

## User Interface

In this chapter, the windows that represent the front-end of the application, the structure that makes it functional, and the database management will also be mentioned. 
This UI is designed in Turkish to be able to be tested by users.

### Splash & Login
It would be more appropriate to evaluate the Splash and Login screens together because users cannot intervene until the login screen is opened.

![splash-login](https://user-images.githubusercontent.com/69144354/149879188-f9296f40-b7d1-43ca-be83-8ed56147ce7f.gif)

#### Splash 
The Splash Screen has been added to the program symbolically. It is aimed to give an idea about how creative work can be done on the frontend with the PyQt library.
##### Progress Bar Animation
```python
class  SplashScreen(QtWidgets.QMainWindow):
  def __init__(self):
      super(SplashScreen,self).__init__()

      self.ui = Ui_MainWindow()
      self.ui.setupUi(self)
      self.additional_UiSetup()

      self.ui.label_softwareName.setText("ORDER & LOAD BUSINESS INTELLIGENCE SOFTWARE v1")
      
      # Starting Value of the Progress Bar
      self.counter = 0

      # Timer 
      self.timer = QtCore.QTimer()
      self.timer.timeout.connect(self.progress) # That is a signal which detect the timeout to call the function of the "progress"
      self.timer.start(35)

  def progress(self):
  # Setting Starting Value of the Splash Screen
  self.ui.progressBar.setValue(self.counter)
  
  # To rise the Value of the Progress Bar
  self.counter += 1 

  if self.counter > 70:
      self.ui.lbl_loading.setText("configurations setting...")

  if self.counter > 80:
      self.ui.lbl_loading.setText("data proccessing...")

  if self.counter > 95:
      self.ui.lbl_loading.setText("app started.")

  if self.counter > 100:
      self.ui.check_close.setChecked(True)
      self.timer.stop()
      self.close()
 ```
##### Frameless Design
```python
def additional_UiSetup(self):
  # To set the Widget Frameless
  flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
  self.setWindowFlags(flags)

  # To remove the background of the Widget
  self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

  # To set Shadow Effect on the Widget
  self.shadow = QGraphicsDropShadowEffect(self)
  self.shadow.setBlurRadius(20)
  self.shadow.setXOffset(0)
  self.shadow.setYOffset(0)
  self.shadow.setColor(QtGui.QColor(0,0,0,60))
  self.ui.dropShadowFrame.setGraphicsEffect(self.shadow)
```
#### Login
It is important to mention two important functions in this section. One of them is Username and Password control and the other is the storage of these information.
##### Control Mechanism
Verifying user information is the most important part of applications in terms of security. As a method, it may be possible to read the scripts of some encrypted files from an online repo. However, it would be more practical and secure for an application of this scale to have MongoDB do this control phase.

To summarize, every time the login button is pressed, it places the username and password information in the MongoDB **Connection String** and sends a query. If an **Authorization Error** is returned, it indicates incorrect information.

```python
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
```
##### Storage of Username and Password
In order to store this information, there is a json type document waiting locally.
###### settings.json
```json
{
  "remember_me": {
  "isChecked": true,
  "username": "cuneyttopbas",
  "password": "cuneyttopbas123"
  }
}
```
The codes below are read without opening the login screen. The structure constructed here is based on reading the **settings.json** page first. If the value of the **"isChecked"** key is **"true"**, it transfers the user information from the same file directly to the login screen.
```python
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
```
### Settings Forms
Assuming there is no data in the database yet except products, customer and shipping information must be added first to take advantage of the program's functions.

![settings](https://user-images.githubusercontent.com/69144354/149901521-f0b5e4f3-03a5-47e1-a1dc-9159cc0f2404.gif)

In order to create the structure above, some important steps are shared below.
#### Management of the Data
##### Add a Customer
###### Step 1
A Stacked Widget is set to organize Customers and Cargos Menus at the same widget so if a user information is going to be added, then we need to set a current index detail for the stacked widget.
```python
def open_customer_settings_to_add(self):
    self.setting_form.ui.stackedWidget.setCurrentIndex(0)
    self.setting_form.show()
```

###### Step 2
Signal-Slot to detect a press on the **Save** Button
```python
self.setting_form.ui.btn_save_customer.clicked.connect(self.add_customer)
```
Function
```python
def add_customer(self):
  try:
    if self.setting_form.ui.txt_company is not None:  # It must be sure that at least Company name is entered to make a query
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

  except pymongo.errors.DuplicateKeyError: # This Exception is used when editing the customer document. 
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
```
##### Edit a Customer
###### Step 1
```python
def open_customer_settings_to_edit(self):
        item = self.select_clicked_item(self.settings.ui.customer_listWidget)
        customer = self.customer_coll.find_one({"_id":item.text()})
        
        # Details of the Customer is coming from the Database via "_id" info that we can access from List Widget
        self.setting_form.ui.txt_company.setText(item.text())     
        self.setting_form.ui.txt_company.setEnabled(False)
        self.setting_form.ui.txt_mail1.setText(customer["mail1"]) 
        self.setting_form.ui.txt_mail2.setText(customer["mail2"])
        self.setting_form.ui.txt_mail3.setText(customer["mail3"])
        self.setting_form.ui.cb_extra_code.setChecked(customer["extra_code"])
        self.setting_form.ui.cb_notification.setChecked(customer["notification"])

        self.setting_form.ui.stackedWidget.setCurrentIndex(0)
        self.setting_form.show()
```
Cick on this link to see how to select a item of QListWidget, [Selecting Items of QListWidget](#selecting-items-of-qlistwidget)
###### Step 2
As you can see below, same fuction which is used adding is used here as well, thanks to Exception function can detect if it is a adding or editing. If MongoDb throws a **"Duplicate"** error that means there is one more with the same "_id" so this is a editing.

Signal-Slot to detect a press on the **Save** Button
```python
self.setting_form.ui.btn_save_customer.clicked.connect(self.add_customer)
```
Function
```python
def add_customer(self):
  try:
    if self.setting_form.ui.txt_company is not None:  # It must be sure that at least Company name is entered to make a query
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

  except pymongo.errors.DuplicateKeyError: # This Exception is used when editing the customer document. 
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
```
##### Remove a Customer
```python
item = self.select_clicked_item(self.settings.ui.customer_listWidget)
if item is not None:
    self.customer_coll.delete_one({"_id":item.text()})
    self.feedback_messageBox(item.text(),"silindi")
    self.refresh_setting()
```

#### Selecting Items of QListWidget
```python
def select_clicked_item(self,listWidget):
    index = listWidget.currentRow()
    item = listWidget.item(index)

    return item
```
#### Display Settings of QListWidget
```python 
def load_settings_data(self):
    for customer in self.customer_coll.find():
        customer_name = customer["_id"]
        self.settings.ui.customer_listWidget.addItem(customer_name)

    for cargo in self.cargo_coll.find():
        cargo_name = cargo["_id"]
        self.settings.ui.cargo_listWidget.addItem(cargo_name)
```
### Order Form
An order can be added as it has Customer and Cargo information as well. The Order Form was created to add an order. Some partial edits can be performed from the [Main Window](#main-window).

![order](https://user-images.githubusercontent.com/69144354/149923071-f4e49d7c-0e83-435d-85e7-eaf0905e052d.gif)
#### Searching Products or Codes
In cases where the number of products and their variants is high, the best way to perform fast and error-free transactions is to create a good search mechanism.
##### Shortcut to Access Searching Form
From imported class named OrderWindow(), a "self.order" object is created.
Documents which is imported in the codes below can be seen in source files.
```python
from orderForm.order import OrderWindow 
self.order = OrderWindow()
```
Object of QShortcut is created as a child of Order Form class 
```python
self.shortcut_open1 = QShortcut(QKeySequence('F1'), self.order)
self.shortcut_open1.activated.connect(self.open_searchingForm)
```
###### Function
```python
def open_searchingForm(self):
  try:
      if self.selected_column == 0: # If selected Column is "0", that means the user is looking for a product
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

      elif self.selected_column == 1: #If selected Column is "1", it assumes that the user is looking for color codes of a product already choosen
          text = self.order.ui.table_details.item(self.selected_row, self.selected_column)
          if text is not None:
              self.searching_form.ui.txt_search.setText(text.text())
              product_name = self.order.ui.table_details.item(self.selected_row, 0)
              if product_name is not None: # It check if product is choosen or not
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
```

#### UI of the Form
Important interface features such as loading of customer and cargo details in the combobox of Order Form and, if selected, accompanying their information and adding a new line automatically as the line progresses, are mentioned below.

##### Loading Necessary Datas to Form
###### Step 1
```python
self.order.ui.cb_cargos.clear()
self.order.ui.cb_customers.clear()

# If any item is selected 
# To load Customer Combobox with customer infos
self.order.ui.cb_customers.addItem(" ")
for customer in self.customer_coll.find():
    customer_name = customer["_id"]
    self.order.ui.cb_customers.addItem(customer_name)

# To load Cargo Combobox with cargo infos
self.order.ui.cb_cargos.addItem(" ")
for cargo in self.cargo_coll.find():
    cargo_name = cargo["_id"]
    self.order.ui.cb_cargos.addItem(cargo_name)  
    
    
today = date.today()
year = today.year
month = today.month
day = today.day

self.order.ui.order_date.setDate(QtCore.QDate(year, month, day)) # Load the current date to QtDate 

self.order.ui.table_details.selectionModel().selectionChanged.connect(self.on_selectionChanged) # When user tabs to last cell, one more row is crated by itself
self.order.ui.cb_cargos.currentTextChanged.connect(self.transfer_info_on_form)                  # Transfer selected customer's info to relevant QtLineEdits
self.order.ui.cb_customers.currentTextChanged.connect(self.transfer_info_on_form)               # Transfer selected cargo's info to relevant QtLineEdits
```
###### Step 2
This function is called only if item of combobox of customer or cargo is changed, change actually means user choosed a one
```python
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
```
##### Automatic Row Adding to QTableWidget
###### Step 1
That line of code is written to detect ant change of selection on the QTableWidget
```python
self.order.ui.table_details.selectionModel().selectionChanged.connect(self.on_selectionChanged)
```
###### Step 2
After detecting change on the QTableWidget, function below is check if selected row and column are the last ones. If it is True, then add a new row.
```python
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
```
#### Adding Order
When adding an order, it is sufficient to enter the company name and at least one product with all its information. As it is a sensitive stage as well as important,that is why management of errors is also a imperative.

```python
def save_order(self):
    try:
        
        company = self.order.ui.cb_customers.currentText()
        # Receiver Details
        receiver = self.order.ui.txt_receiver_name.text()
        authority = self.order.ui.txt_author.text()
        company_phone = self.order.ui.txt_cust_tel.text()
        company_gsm = self.order.ui.txt_gsm_tel.text()
        company_adress = self.order.ui.txt_cust_adress.text()

        # Shipment Details 
        shipper_name = self.order.ui.cb_cargos.currentText()
        customer_code = self.order.ui.txt_customer_code.text()
        ship_type = self.order.ui.txt_ship_type.text()
        ship_phone = self.order.ui.txt_ship_tel.text()
        ship_adress = self.order.ui.txt_ship_adress.text()

        # Order Date
        order_date = self.order.ui.order_date.text()

        # Order Creation Date
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # To create a specific code for each order
        order_code = self.create_orderCode(company)

        # Transferring datas to a dictionary to send database together
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
```

#### Generating & Ordering Order Codes
###### Algorithm
Order codes must be unique. At the same time, the codes should give the user an idea about the details of the order. For this reason, each time an order is entered, an order code that is different but contains information such as **Company Name** and **Date** should be generated.
```
Order Code = First 3 Letter Of the Company Name + Date + Amount of Repeat
```
However, some customers may want to add the codes they have determined to the order code in order to track the work. In order to respond to such requests, Order & Load offers the opportunity to choose the extra order code while adding customers. 

![extra_code](https://user-images.githubusercontent.com/69144354/149934221-9714073a-d709-4565-8121-5e5cecdbfe09.jpg)

That **Extra Code** is asked with QDialog when **Save** button is clicked. In this case, if **Extra Code** is selected Order Code logic will be like below,
```
Order Code = First 3 Letter Of the Company Name + Date + Extra Code
```
###### Function
```python
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

      return company[:3] + order_date[0] + order_date[1] + order_date[2][2:] + "-" + str(repeat)

  except TypeError:
      print("TypeError: Company Info is None")
      self.warning_messageBox("Lütfen Firma Seçimi Yapınız!")
```


### Main Window 
![main](https://user-images.githubusercontent.com/69144354/149923111-59dbb7b8-d875-4268-8980-a02a9b109007.gif)

### Report Form


![report](https://user-images.githubusercontent.com/69144354/149923139-d512d177-0763-423c-a85e-33d1063c7cc6.gif)


## Server Application
The main purpose of the Server Application is to send a report which contains daily loadings to the relevant customers at the end of the day.
For this reason, **timer**, **filter**, **recorder** and **notifier** functions in this application are important. We will evaluate this application under these headings.

![server](https://user-images.githubusercontent.com/69144354/149890024-821fbed0-1021-4442-94a5-f3c1ff1ac4f4.gif)

##### Timer
It is necessary to wait for the end of the shift at least in order to transmit the daily reports. It is necessary to have at least one timer to wait for the end of the shift.
```python
from PyQt5.QtCore import QTimer, QTime
from datetime import datetime, date

class ServerWidget(QtWidgets.QMainWindow):
    def __init__(self,username,password):
        super(ServerWidget,self).__init__()
        
        timer = QTimer(self)
        timer.timeout.connect(self.display_time)
        timer.start(1000)  
        
    def set_time(self):
        self.today = date.today()
        self.year = self.today.year
        self.month = self.today.month
        self.day = self.today.day
        self.this_date_object = datetime(int(self.year), int(self.month),int(self.day-1),int(18))
        self.now = datetime.now().strftime('%Y-%m-%d %H:%M:%S') # Now
        
    def check_time(self):
        self.set_time()
        if self.ui.txt_time.text() == "18:00:00":
            self.write_on_records("Time is matched to send loading reports.")
            self.send_reports()
    
```
##### Filter
This is crucial to have an efficient filtering function that first separates customers from each other, then separates the shipped from all orders, and now separates the shipped from all.
```python
loading_count = 0
for company in self.customer_coll.find(): # Call customers one by one to filter
    delivered_items = []
    for order in self.order_coll.find():
        if order["Company Name"] == company["_id"]: # Reaching relevant customer's orders
            counter = 1
            for order_items in order["Order Details"]:
                if order['Order Details'][order_items]['Delivered_at'] != "Not Shipped Yet": # Filtering Shipped Orders than other orders
                    deliver_date = order['Order Details'][order_items]['Delivered_at']
                    deliver_date_object = datetime.strptime(deliver_date, '%Y-%m-%d %H:%M:%S')
                    if deliver_date_object >= self.this_date_object:                         # Filtering Shipped Orders which is made today from all shipped orders
                        cargo_recevier = f"LOADING ID: {counter}\nCARGO: {order['Shipping Info']['Shipper Name']}  RECEIVER: {order['Receiver Info']['Receiver Name']}\n"
                        delivered_items.append(f"{cargo_recevier}{order['_id']}/{order_items}: {order['Order Details'][order_items]['Item']} {order['Order Details'][order_items]['Color']} {order['Order Details'][order_items]['Meter']} MT") 
                        counter += 1 
```
##### Recorder
This application is basically designed to work on its own,that is why it is very important to keep records to ensure that it works correctly or to be aware of errors.
However, we cannot be completely sure how the errors will occur so it would be more accurate to keep these records both locally and in the cloud. For example, if we only kept logs in the cloud, we would not be aware of errors related to queries.
```python
def write_on_records(self, record):
    print(record)
    with open("records.txt","r+", encoding="utf-8") as file:
            content = file.read()
            content = content + "\n" + f"{str(self.now)}: " + record
            file.seek(0)
            file.write(content) 

    self.setting_coll.update_one({"_id":"server_log"},{"$push":{"records" :str(self.now)+ " " + str(record)}}) 
    self.setting_coll.update_one({"_id":"server_log"},{"$set":{"last_seen":str(self.now)}})
```
###### Outputs:
###### records.txt
```txt
2021-12-30 21:32:22: Failed while sending loading report to Company 1! Error:send_notification() takes 3 positional arguments but 5 were given.
2021-12-30 21:32:22: Application is closed.
2021-12-30 21:36:46: Application is closed.
2021-12-30 21:37:11: Information of the Loading of 1 item succesfully sent to Company 1.
2021-12-30 21:37:11: Information of the Loading of 1 item succesfully sent to Company 2.
2021-12-30 21:37:11: Information of the Loading of 1 item succesfully sent to Company 3.
2021-12-30 21:37:11: Application is closed.
2021-12-30 21:58:37: Application is activated.
2021-12-30 21:58:37: Information of the Loading of 1 item succesfully sent to Company 2.
2021-12-30 21:58:37: Information of the Loading of 1 item succesfully sent to Company 5.
2021-12-30 21:58:37: Information of the Loading of 1 item succesfully sent to Comapny 6.
2021-12-30 21:58:37: Application is closed.
2021-12-31 13:04:56: Application is activated.
2021-12-31 13:04:56: Application is tested.
2021-12-31 13:04:56: Application is closed.
```
To see the output at the Cloud, click this link [Server Log](#server-log)

##### Notifier
In order for it to continue its function stably, we need to be instantly aware of any errors that may occur. Possible error and close events are sent to the technical team with the notification function.
```python
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
```
###### Examples For Usage
In case of Error  :
```python
except Exception as ex:
        self.write_on_records(f"Failed while sending loading report to {company['_id']}! Error:{ex}.")
        subject = "ERROR OCCURED AT THE SERVER"
        body = f"Hello,\n\nError is shared below,\n{ex}\n\nLast Seen: {self.now}\n\n\nPlease do not reply this e-mail."
        self.send_notification(subject,body)
```
In case of Unexpected Exit  :
```python
def closeEvent(self,event):
    subject = "APPLICATION OF ORDER & LOAD IS CLOSED AT THE SERVER"
    body = f"Hello,\n\nClose Event of the App is activated.\nLast Seen: {self.now}\n\nPlease do not reply this e-mail."
    self.send_notification(subject,body)
    self.write_on_records("Close Event of the Server App is successfully activated.")
```

## Data Modelling

**MongoDB**, which is a NoSQL database, was preferred in the project. With this feature, MongoDB allows you to create non-relational data collections containing documents. Of course, there will always be data that needs to be associated with each other, but completing this association on the side where the queries are sent provides significant flexibility to the developers. When needed, dictionary-type data with key-value relationships, arrays or arrays of dictionary-type data can be added to the documents.
At the same time, with this structure, you can perform innovations much faster because you do not have to add the newly added fields to all the documents in the collection.
It should be added independently of the project that NoSQL databases are more preferred in projects where large volumes of data are managed.

**Note** : Since information such as Customer Name, Shipping Name, Product Name and Order Code is unique, this information is used in the **"_id"** field instead of **"ObjectId"**. Thanks to this method, queries have become easier to do.

### Connection
If the login is successful in the Username and Password entries in Login Form, takes place at the connection string displayed. Then connection to collections are completing as it seen below.
```python
self.myclient = pymongo.MongoClient(f"mongodb+srv://{username_entry}:{password_entry}@cluster0.asdnj.mongodb.net/app_test?retryWrites=true&w=majority")
self.mydb = self.myclient["order-load"]
self.customer_coll = self.mydb["customers"]
self.cargo_coll = self.mydb["cargos"]
self.order_coll = self.mydb["orders"]
self.product_coll = self.mydb["products"]
self.setting_coll = self.mydb["settings"]
```

### Customers
There is some information requested by the program when storing customer data,

| Name          | Mail 1        | Mail 2        | Mail 3        | Extra Code    | Notifications |
| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |
| Company 1     | company1@...  | company1@...  |    None       | False         | True          |
| Company 2     | company2@...  | None          | None          | True          | True          |

At least the name entry is enough for the following structure to be formed on the MongoDB side.

```json
{
  "_id":"Company 2",
  "mail1":"company2@company.com",
  "mail2":"",
  "mail3":"",
  "extra_code":true,
  "notification":true
}
```
### Cargos
```json
{
  "_id":"Cargo 1",
  "authority":"James Thompson",
  "phone":"+90 212 586 86 21",
  "adress":"Hayriye Tüccarı Cad. Kızıltaş Sok. No:57/1 Nişanca/Kumkapı/ İstanbul"
}
```
### Products 
```json
{
  "_id":"Product A",
  "code":"2201.1D",
  "supplier":"Company ABC",
  "supplier_product_name":"Product A",
  "type":"Fabric",
  "usage":"Curtain",
  "width":300,
  "weight":258,
  "composition":"%72 Polyester %28 Viskon",
  "color_codes":[
      "2201.1D.78",
      "2201.1D.34",
      "2201.1D.67",
      "2201.1D.23",
      "2201.1D.28",
      "2201.1D.14",
      "2201.1D.36",
      "2201.1D.38",
      "2201.1D.55",
      "2201.1D.88",
      "2201.1D.32"
      ]
}
```
##### Synchronization of Products
Business intelligence Software should often have a database or dataset into which products are integrated.
In large-volume management information systems such as a ERP, products can also be added from the system. In this project, products were entered by using the **pandas** library from a ready dataset.

Sample Dataset which is in same format with the one used in this project can be founded in the source file.
```python
import pandas as pd
import pymongo

#   Username and Password is needed to send a request to database
username = ""
password = ""
#   File we want to sync with our database has to be shared here as a path
file = r"C:\Users\Asus\Desktop\sample_products.xlsx"

def synchronize(username,password,file,sheet_index):
    myclient = pymongo.MongoClient(f"mongodb+srv://{username}:{password}@cluster0.asdnj.mongodb.net/app_test?retryWrites=true&w=majority")
    mydb = myclient["order-load"]
    product_coll = mydb["products"]

    xl = pd.ExcelFile(file)

    data_frame1 = xl.parse(sheet_index) 
    index = data_frame1.index
    number_of_rows = len(index) 

    products = {}

    for i in range(number_of_rows):

        product_name = data_frame1["AD"][i]
        product_code = str(data_frame1["RENK KOD"][i])[:-3]
        color_code = data_frame1["RENK KOD"][i]
        width = data_frame1["EN"][i]
        composition = data_frame1["KOMPOZİSYON"][i]
        weight = data_frame1["GR/M²"][i]
        product_type = data_frame1["ÜRÜN CİNSİ"][i]
        usage = data_frame1["KULLANIM ALANI"][i]
        supplier_name = data_frame1["TEDARİKÇİ"][i]
        supplier_product_name = data_frame1["TEDARİKÇİ AD"][i]
        supplier_product_color = data_frame1["TEDARİKÇİ RENK KOD"][i]

        if product_name is not None:
            if product_name in products:
                products[product_name]["color_codes"].append({"color_code":color_code})
            else: 
                products[product_name] = {
                    "code":product_code,
                    "supplier":supplier_name,
                    "supplier_product_name":supplier_product_name,
                    "type":product_type,
                    "usage":usage,
                    "width":width,
                    "weight":weight,
                    "composition":composition,
                    "color_codes" : [{"color_code":color_code}]
                 }
        else:
            continue
        
    product_data = {}

    for product in products:
        try:
            product_data = {
                "_id" : product,
                "code":products[product]["code"],
                "supplier":products[product]["supplier"],
                "supplier_product_name":products[product]["supplier_product_name"],
                "type":products[product]["type"],
                "usage":products[product]["usage"],
                "width":products[product]["width"],
                "weight":products[product]["weight"],
                "composition":products[product]["composition"],
                "color_codes" : []
                }
            for i in range(len(products[product]['color_codes'])):
                product_data["color_codes"].append(products[product]['color_codes'][i]['color_code'])
            product_coll.insert_one(product_data)
        except pymongo.errors.DuplicateKeyError:
            continue
            
if __name__ == "__main__":
    synchronize(username,password,file,0)
    synchronize(username,password,file,1)
```

### Orders

Below is an example of **correlating data**. In the Company Name field, **customers** collection must match the information in the **"_id"** field. This matching takes place when the order is entered. The same applies to cargo and product informations.

```json
{
  "_id":"COM100122-2",
  "Company Name":"Company 1",
  "Crated_by":"cuneyttopbas",
  "Created_at":"2022-01-10 13:32:20",
  "Order_at":"10.01.2022",
  "Receiver Info":{
      "Receiver Name":"ABC Textile Co.",
      "Authority":"Hannah Simpson",
      "Company Phone":"+90 530 0354 6",
      "Company GSM":"+25 441 25 544",
      "Company Adress":"Moscow, Russia"
      },
  "Shipping Info":{
      "Shipper Name":"Cargo 1 ",
      "Customer Code":"690",
      "Shipping Type":"Air Shipment",
      "Shipper Phone":"+452 22 4 5 55 ",
      "Shipper Adress":"Neslişah Mah. Vatan Cad. Banka Evleri C1 Blok No 82/1 Fatih"
      },
  "Order Details":{
      "1":{
          "Status":"delivered",
          "Item":"Product A",
          "Color":"2201.1D.78",
          "Meter":"35",
          "Note":"Free of Charge",
          "Delivered_at":"2022-01-11 16:41:14"
          },
      "2":{
        "Status":"new",
        "Item":"Product B",
        "Color":"1828.1D.03",
        "Meter":"1.7",
        "Note":"",
        "Delivered_at":"Not Shipped yet"
      }
      "3-1":{
        "Status":"preparing",
        "Item":"Product C",
        "Color":"1898.1D.05",
        "Meter":"10.5",
        "Note":"Be careful with this one",
        "Delivered_at":"Not Shipped yet"
      }
      "3-2":{
        "Status":"waiting",
        "Item":"Product C",
        "Color":"1898.1D.05",
        "Meter":"4.5",
        "Note":"Be careful with this one",
        "Delivered_at":"Not shipped yet",
        "Info_by" : "operation_departmant",
        "Waiting_cause" :"We dont have it now, not able to prepare!",
        "Waiting_info": "We will have it in two weeks."
      }
   }
}
```
To reinforce with an example, it has matched this information, which is actually still unrelated and consists of a string data, preventing a different selection in the user interface,

##### Matching Products while Adding an Order

```python
product = self.product_coll.find_one({"_id":product_name}) # Filter with "_id" which the name of the Product
if product is not None:
    if color in product["color_codes"]:
        if self.isFloat(meter) == True:
            self.order_data["Order Details"][str(line)] = {
                "Status": "new",
                "Item" : product_name,
                "Color" : color,
                "Meter" : meter,
                "Note"  :   "",
                "Delivered_at":"Not Shipped Yet"
            }   
```
##### Matching All Datas while Sending Loading Report at the Server side

```python

for company in self.customer_coll.find():           # Step 1-  Reaching to "customers" collection
    delivered_items = []                    
    for order in self.order_coll.find():            # Step 2-  Reaching to "orders" collection
        if order["Company Name"] == company["_id"]: # Step 3-  Matching a document's "_id" field from customers with document's "Company Name" from orders
            counter = 1
            for order_items in order["Order Details"]:
                if order['Order Details'][order_items]['Delivered_at'] != "Henüz Teslim Edilmedi":
                    deliver_date = order['Order Details'][order_items]['Delivered_at']
                    deliver_date_object = datetime.strptime(deliver_date, '%Y-%m-%d %H:%M:%S')
                    if deliver_date_object > self.this_date_object:
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
        self.load_screen()

self.write_on_records("Sending Report Process is completed.")

```
### Notifications
The program sends automatic mails at many stages. According to the subject of the stages, the people to whom the e-mail will be sent also vary.

```json
{
  "_id":"notifications",
  "operation_departmant":[
    {"mail":"operator_1@company.com"},
    {"mail":"operator_2@company.com"}
    ],
  "customer_service":[
    {"mail":"customer_service@company.com"}
    ],
  "executive":[
    {"mail":"cuneyt.topbas@company.com"},
    ],
  "supplying_departmant":[
    {"mail":"supplying@company.com"}
    ],
  "technic":[
    {"mail":"technic@company.com"}
    ],
    "admin":[
    {"mail":"admin@gmail.com","password":"Admin123"}
  ],
}
```
##### Selecting Relevant Adresses
If the Operation, Customer Service and Executive units within the company need to take action or be informed at the time of placing the order, it will be useful to create the structure below.

```python
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
```

### Server Log
Taking advantage of Artificial Intelligence provides serious convenience in our lives. So much so that these conveniences can turn into habits over time. For this reason, stability is very important at this stage.

In order to ensure stability, it is important to be aware of errors quickly as well as to avoid errors. This can only be possible with close monitoring. In order to achieve this, it was deemed appropriate to create a structure like the one below.
```json
{
  "_id":"server_log",
  "last_seen":"2022-01-14 18:00:00",
  "records":[
      "2022-01-10 09:29:01 Database connection is activated.",
      "2022-01-10 09:29:01 Application is activated.",
      "2022-01-10 09:29:09 Application is tested successfully.",
      "2022-01-10 09:29:40 Close Event of the Server App is successfully activated.",
      "2022-01-10 09:37:15 Database connection is activated.",
      "2022-01-10 09:37:15 Application is activated.",
      "2022-01-10 18:00:00 Time is matched to send loading reports.",
      "2022-01-10 18:00:00 Sending Report Process is started.",
      "2022-01-10 18:00:00 Information of the Loading of 3 item succesfully sent to Company 1.",
      "2022-01-10 18:00:00 Sending Report Process is completed.",
      "2022-01-11 18:00:00 Time is matched to send loading reports.",
      "2022-01-11 18:00:00 Sending Report Process is started.",
      "2022-01-11 18:00:00 Information of the Loading of 8 item succesfully sent to Company 1.",
      "2022-01-11 18:00:00 Information of the Loading of 3 item succesfully sent to Company 2.",
      "2022-01-11 18:00:00 Information of the Loading of 2 item succesfully sent to Company 3.",
      "2022-01-11 18:00:00 Sending Report Process is completed.",
      "2022-01-12 18:00:00 Time is matched to send loading reports.",
      "2022-01-12 18:00:00 Sending Report Process is started.",
      "2022-01-12 18:00:00 There was no any loading today to send as a report.",
      "2022-01-12 18:00:00 Sending Report Process is completed.",
      "2022-01-13 18:00:00 Time is matched to send loading reports.",
      "2022-01-13 18:00:00 Sending Report Process is started.",
      "2022-01-13 18:00:00 Information of the Loading of 5 item succesfully sent to Company 2.",
      "2022-01-13 18:00:00 Information of the Loading of 3 item succesfully sent to Company 1.",
      "2022-01-13 18:00:00 Information of the Loading of 2 item succesfully sent to Company 5.",
      "2022-01-13 18:00:00 Sending Report Process is completed.",
      "2022-01-14 11:43:45 Database connection is activated.",
      "2022-01-14 11:43:45 Application is activated.",
      "2022-01-14 11:44:12 Close Event of the Server App is successfully activated.",
      "2022-01-14 11:44:24 Database connection is activated.",
      "2022-01-14 11:44:24 Application is activated.",
      "2022-01-14 11:44:43 Application is tested successfully.",
      "2022-01-14 11:44:49 send_records method is called from the console.",
      "2022-01-14 11:44:49 Records are sent successfully from the console.",
      "2022-01-14 11:44:55 Invalid entrance is detected at the console.",
      "2022-01-14 11:45:24 Invalid entrance is detected at the console.",
      "2022-01-14 11:45:31 Close Event of the Server App is successfully activated.",
      "2022-01-14 18:00:00 Time is matched to send loading reports.",
      "2022-01-14 18:00:00 Sending Report Process is started.",
      "2022-01-14 18:00:00 There was no any loading today to send as a report.",
      "2022-01-14 18:00:00 Sending Report Process is completed."
      ]
}
```
To go back, click this link [Recorder](#recorder)
##### Refreshing the Array of Records
Over time, the data here will grow and the old data will become meaningless. Therefore, there is a need to create a self-cleaning algorithm like the one below.
```python
 settings  = self.setting_coll.find({"_id":"server_log"})
  for setting in settings:              # Step 1- Checks the amount of line
      count = 0
      for line in setting["records"]:
          count += 1
  if count >= 50:                       
      delete_amount = count - 50          # Step 2- If amoutn is more than 50, it calculates the amount of line has to be deleted
      settings  = self.setting_coll.find({"_id":"server_log"})
      for setting in settings:
          del_rpt = 0
          for line in setting["records"]:
              if del_rpt < delete_amount: # Step 3- Unwanted(Oldest) records are pulled from the array of the records
                  self.setting_coll.update_one({"_id":"server_log"},{"$pull":{"records" : line}}) 
                  del_rpt += 1
```
