# Order & Load Business Intelligence v1

This document presents the Order & Load BI Software in 3 main sections under the headings of Introduction, Desktop User Application, Server Application and Data Modeling with
MongoDB. It aims to enrich the content with Gifs and Screenshots.

In order to make sense of the codes, it is important to have basic knowledge of Python, pymongo and pyqt5.

This project aims to contribute to the fields of user interface, artificial intelligence, data collection, data analysis, data management and digitization of business processes, 
rather than making commercial gains.

**Note** : Instead of saying "it could have been better this way or that" many times in the document, I would like to state that I did not prepare much for the project in advance,
it grew on its own as I added new features and I did it to enjoy it. Therefore, in order to see the result,
you can see that I skipped some requirements when you take a look at the codes.
However, I would like to underline that it has features that can answer the questions of many developers I encountered during my research.
When I started the project, I was new to the libraries I used, but with my current knowledge, I believe that I can finish this project, which I finished in 3 weeks, in half time.

Navigate Chapters,
- [Introduction](#introduction)
- [User Interface](#userinterface)
  - [Main Window](#mainwindow)
- [Server App](#server)
- [Data Modelling](#db)

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

Below is a general summary of the program's functions and some questions that developers often ask and can find answers to in the project.

### Functions

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
