__author__ = 'mustafa'

import sys
from PySide.QtGui import *

class TruckWidget(QWidget):
    """
    Truck Data Widget
    """

    def __init__(self, name, number_of_goods):
        QWidget.__init__(self)

        #create the widgets
        self.truckHLayout = QHBoxLayout(self)
        self.truckName = QLabel(name)
        self.truckTypeComboBox = QComboBox(self)
        self.number_of_goods = number_of_goods
        self.goodTable = QTableWidget(1,number_of_goods,self)




        #combo box for truck type
        self.truckTypeComboBox.addItem('Inbound')
        self.truckTypeComboBox.addItem('Outbound')
        self.truckTypeComboBox.addItem('Compound')

        # add the widget elements to the layout
        self.truckHLayout.addWidget(self.truckName,0)
        self.truckHLayout.addWidget(self.truckTypeComboBox,0)
        self.truckHLayout.addWidget(self.goodTable,2)
        self.truckTypeComboBox.activated.connect(self.updateTable)
        self.updateTable()

    def updateTable(self):
        n = self.truckTypeComboBox.currentIndex()
        self.goodTable.setColumnCount(self.number_of_goods)

        self.goodTable.setSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.MinimumExpanding)
        if(n == 0):
            self.goodTable.setVerticalHeaderLabels(['Coming'])
            self.goodTable.setMaximumHeight(50)

            # inbound

        elif(n == 1):
            # outbound

            self.goodTable.setVerticalHeaderLabels(['Going'])
            self.goodTable.setMaximumHeight(52)

        elif(n == 2):
            self.goodTable.setRowCount(2)
            self.goodTable.setVerticalHeaderLabels(['Coming','Going'])
            self.goodTable.setMaximumHeight(88)

            # compound