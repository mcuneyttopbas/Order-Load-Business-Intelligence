import sys
from splash._splash import Ui_MainWindow
from PyQt5 import QtCore,QtGui,QtWidgets
from PyQt5.QtWidgets import QGraphicsDropShadowEffect

class  SplashScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(SplashScreen,self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.additional_UiSetup()

        self.ui.label_softwareName.setText("ORDER & LOAD BUSINESS INTELLIGENCE SOFTWARE v1")
        
        
        #STARTING VALUE OF PROGRESS BAR
        self.counter = 0

    def additional_UiSetup(self):
        
        # FOR FRAMLESS WIDGET
        flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(flags)
        # TO REMOVE BACKGROUND OF THE WIDGET
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        #FOR SHADOW EFFECT ON THE WIDGET
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QtGui.QColor(0,0,0,60))
        self.ui.dropShadowFrame.setGraphicsEffect(self.shadow)

        #TIMER FOR PROGRESS ON THE BAR
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)
        self.timer.start(35)
    
    def progress(self):
        #SETTING STARTING VALUE OF SPLASH SCREEN
        self.ui.progressBar.setValue(self.counter)
        
        #FOR THE PROGRESS OF PROGRESS BAR
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




