 #! /usr/bin/env python3 
from PyQt5 import QtCore, QtGui, QtWidgets, QtSerialPort
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon

from PyQt5.QtCore import Qt,QDate, QTime, QDateTime
from datetime import datetime
import sys
import serial
import serial.tools.list_ports

class SerialThread(QtCore.QThread):
    dataChanged = QtCore.pyqtSignal(str)
    def __init__(self, *args, **kwargs):
        QtCore.QThread.__init__(self, *args, **kwargs)
        com_port = "/dev/"+ "ttyACM0"  # this depends on the com port in which arduino connected. 
        baudrate = 9600
        self.ser = serial.Serial(port = com_port, baudrate=baudrate, timeout = 120, writeTimeout = 1)   
        
    def run(self):
        while True:
            if self.ser.inWaiting() > 0:
                inputValue = self.ser.readline().decode('ascii').strip()
                self.dataChanged.emit(inputValue)

class Battery_UI(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent = parent)        
        self.setWindowTitle("Battery Monitoring")
        self.setGeometry(1100,580, 250,150 )
        self.setStyleSheet("""
        QWidget{
            color: #b1b1b1;
            background-color: #323232;
        }
        QLabel{
            font-family:Operator Mono Bold;
            font:16px;          
        } 
        QPushButton
        {
            color: #b1b1b1;
            background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #565656, stop: 0.1 #525252, stop: 0.5 #4e4e4e, stop: 0.9 #4a4a4a, stop: 1 #464646);
            border-width: 1px;
            border-color: #1e1e1e;
            border-style: solid;
            border-radius: 6;
            padding: 3px;
            font-size: 15px;
            padding-left: 5px;
            padding-right: 5px;
            min-width: 40px;
            font-family: Operator Mono;
            font:  15px;
        }
        QPushButton:pressed
        {
            background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2d2d2d, stop: 0.1 #2b2b2b, stop: 0.5 #292929, stop: 0.9 #282828, stop: 1 #252525);
        }

        QComboBox{
                background-color:rgb(64,64,64); 
                font: 15px Operator Mono Book; 
                color: rgb(102,175,255); 
                selection-color:rgb(10, 45, 85);
                selection-background-color:rgb(255,153,51);
        }
        QComboBox:hover,QPushButton:hover
        {
            border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);
        }
        QProgressBar
        {
            border: 2px solid grey;
            border-radius: 5px;
            text-align: center;
        }      
        QLineEdit
        {
            background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #4d4d4d, stop: 0 #646464, stop: 1 #5d5d5d);
            padding: 1px;
            border-style: solid;
            border: 1px solid #1e1e1e;
            border-radius: 5;
            font: 18px Operator Mono Book;
            color: #d7801a;
        }
        QLCDNumber{
            color: #d7801a;
        }
        """)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint,False)
        self.UI()
        self.thread = SerialThread(self)
        self.thread.dataChanged.connect(
            self.handleSerialUpdate
        )
        self.connectButton.clicked.connect(self.startThread)
        

    def UI(self):        
        voltDisplay = QHBoxLayout()
        self.voltmeter = QLineEdit()
        self.voltmeter.setReadOnly(True)
        self.voltmeter.setMaximumHeight(60)
        label = QLabel()
        label.setText("Bat. Voltage:")
        voltDisplay.addWidget(label)
        voltDisplay.addWidget(self.voltmeter)

        self.batteryLevel = QProgressBar()
        self.batteryLevel.setMinimumHeight(30)        

        buttonGroup = QHBoxLayout()  
        self.chargingState = QPushButton()  
        self.chargingState.setMinimumHeight(35)    
        # self.port = QComboBox()
        # self.port.setMinimumHeight(35)

        # for  info in QtSerialPort.QSerialPortInfo.availablePorts():
        #     self.port.addItem(info.portName())      

        self.connectButton = QPushButton('Connect')
        self.connectButton.setCheckable(True)
        self.connectButton.setMinimumHeight(35)
        
        exitButton = QPushButton("Exit")
        exitButton.setMinimumHeight(35)
        exitButton.clicked.connect(self.exitWindow)

        #buttonGroup.addWidget(self.port)
        buttonGroup.addWidget(self.chargingState)
        buttonGroup.addWidget(self.connectButton)    
        buttonGroup.addWidget(exitButton)

        layout = QVBoxLayout()        
        layout.addLayout(voltDisplay)
        layout.addWidget(self.batteryLevel)
        layout.addLayout(buttonGroup)
        self.setLayout(layout)

    def startThread(self):
        self.thread.start()

    def handleSerialUpdate(self, inputValue):
        #print(inputValue)
        printValue =inputValue.split(" ")        
        self.voltmeter.setText(printValue[0] + " " + printValue[1])
        value = float(printValue[0])
        chargingState = printValue[2]
        if value > 12.7:            
            self.batteryLevel.setProperty("value", 100)
            self.batteryLevel.setStyleSheet("""QProgressBar::chunk{
            background: green;
            width: 4px;
            margin: 0.5px;
            }""")
        elif value > 12.5:
            self.batteryLevel.setProperty("value", 90)
            self.batteryLevel.setStyleSheet("""QProgressBar::chunk{
            background: green;
            width: 2.15px;
            margin: 0.5px;
            }""")
        elif value > 12.42:
            self.batteryLevel.setProperty("value", 80)
            self.batteryLevel.setStyleSheet("""QProgressBar::chunk{
            background: green;
            width: 2.15px;
            margin: 0.5px;
            }""")
        elif value > 12.32:
            self.batteryLevel.setProperty("value", 70)
            self.batteryLevel.setStyleSheet("""QProgressBar::chunk{
            background:  #d7801a;
            width: 2.15px;
            margin: 0.5px;
            }""")
        elif value > 12.20:
            self.batteryLevel.setProperty("value", 60)
            self.batteryLevel.setStyleSheet("""QProgressBar::chunk{
            background:  #d7801a;
            width: 2.15px;
            margin: 0.5px;
            }""")
        elif value > 12.06:
            self.batteryLevel.setProperty("value", 50)
            self.batteryLevel.setStyleSheet("""QProgressBar::chunk{
            background:  #d7801a;
            width: 2.15px;
            margin: 0.5px;
            }""")
        elif value > 11.9:
            self.batteryLevel.setProperty("value", 40)
            self.batteryLevel.setStyleSheet("""QProgressBar::chunk{
            background:  yellow;
            width: 2.15px;
            margin: 0.5px;
            }""")
        elif value > 11.75:
            self.batteryLevel.setProperty("value", 30)
            self.batteryLevel.setStyleSheet("""QProgressBar::chunk{
            background:  yellow;
            width: 2.15px;
            margin: 0.5px;
            }""")
        elif value > 11.58:
            self.batteryLevel.setProperty("value", 20)
            self.batteryLevel.setStyleSheet("""QProgressBar::chunk{
            background: yellow;
            width: 2.15px;
            margin: 0.5px;
            }""")
        elif value > 11.31:
            self.batteryLevel.setProperty("value", 10)
            self.batteryLevel.setStyleSheet("""QProgressBar::chunk{
            background:  red;
            width: 2.15px;
            margin: 0.5px;
            }""")
        else:
            self.batteryLevel.setProperty("value", 0)
            self.batteryLevel.setStyleSheet("""QProgressBar::chunk{
            background:  red;
            width: 2.15px;
            margin: 0.5px;
            }""")
        if( chargingState == "1"):
            self.chargingState.setStyleSheet("background: red; ") 
            self.chargingState.setIcon(QIcon("icons/battery-charging.svg"))                             
            
        else:
            self.chargingState.setStyleSheet("background: green; ") 
            self.chargingState.setIcon(QIcon("icons/battery-full.svg"))             
            

    def exitWindow(self):
        self.close()
        sys.exit()        
    
    # def serialConnect(self):    
    #     com_port = "/dev/"+ self.port.currentText() 
    #     baudrate = 9600 
    #     try:
    #         self.arduino = serial.Serial(port = com_port, baudrate=baudrate, timeout = 120, writeTimeout = 1)
            
    #     except serial.SerialException as e:
    #         print ("Error when connecting to collimator: ", e)  
        
# main method
if __name__ == '__main__':      
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  
    # create the instance of our Window
    window = Battery_UI()  
    # showing the window
    window.show()  
    # start the app
    sys.exit(app.exec())