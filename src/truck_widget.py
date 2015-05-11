__author__ = 'mustafa'

import sys
from PySide.QtGui import *

class TruckWidget(QWidget):
    """
    Truck Data Widget
    """

    def __init__(self, name, number_of_goods, type):
        QWidget.__init__(self)
        self.type = type
        #create the widgets
        self.truckHLayout = QHBoxLayout(self)
        self.truckName = QLabel(name)
        self.number_of_goods = number_of_goods
        self.goodTable = QTableWidget(1,number_of_goods,self)




        #combo box for truck type


        # add the widget elements to the layout
        self.truckHLayout.addWidget(self.truckName,0)
        self.truckHLayout.addWidget(self.goodTable,2)

        self.updateTable()

    def updateTable(self):

        self.goodTable.setColumnCount(self.number_of_goods)

        self.goodTable.setSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.MinimumExpanding)
        if(self.type == 0):
            self.goodTable.setVerticalHeaderLabels(['Coming'])
            self.goodTable.setMaximumHeight(50)

            # inbound

        elif(self.type == 1):
            # outbound

            self.goodTable.setVerticalHeaderLabels(['Going'])
            self.goodTable.setMaximumHeight(52)

        elif(self.type == 2):
            self.goodTable.setRowCount(2)
            self.goodTable.setVerticalHeaderLabels(['Coming','Going'])
            self.goodTable.setMaximumHeight(88)

            # compound