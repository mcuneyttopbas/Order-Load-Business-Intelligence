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
    - [PyQt5](#pyqt5)
    - [MongoDB](#mongodb)
    - [Others](#others)
- [User Interface](#user-interface)
  - [Splash & Login](#splash--login) 
  - [Main Window](#mainwindow)
- [Server App](#server)
- [Data Modelling](#data-modelling)
  - [Customers](#customers) 
  - [Cargos](#cargos)
  - [Products](#products)
  - [Orders](#orders)
  - [Notifications](#notifications)
  - [Server Log](#server-log)

  

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
Below you can see some of the frequently asked questions by the developers, which you can find answers to or get ideas from in this project.
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
## Server Application
The main purpose of the Server Application is to send a report which contains daily loadings to the relevant customers at the end of the day.
For this reason, **timer**, **filter**, **recorder** and **notifier** functions in this application are important. We will evaluate this application under these headings.

![server](https://user-images.githubusercontent.com/69144354/149890024-821fbed0-1021-4442-94a5-f3c1ff1ac4f4.gif)


##### Timer
##### Filter
##### Recorder
##### Notifier
In order for it to continue its function stably, we need to be instantly aware of any errors that may occur. Possible error and shutdown events are sent to the technical team with the notification function.

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
