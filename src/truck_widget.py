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
        self.truck_name = name
        #create the widgets
        self.truckHLayout = QHBoxLayout(self)
        self.truckNameLabel = QLabel(name)
        self.number_of_goods = number_of_goods
        self.goodTable = QTableWidget(1,number_of_goods,self)

        #combo box for truck type

        # add the widget elements to the layout
        self.truckHLayout.addWidget(self.truckNameLabel,0)
        self.truckHLayout.addWidget(self.goodTable,2)

        self.updateTable()

    def updateTable(self):

        self.goodTable.setColumnCount(self.number_of_goods)

        self.goodTable.setSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.MinimumExpanding)
        if(self.type == 'inbound'):
            self.goodTable.setVerticalHeaderLabels(['Coming'])
            self.goodTable.setMaximumHeight(50)

            # inbound

        elif(self.type == 'outbound'):
            # outbound

            self.goodTable.setVerticalHeaderLabels(['Going'])
            self.goodTable.setMaximumHeight(52)

        elif(self.type == 'compound'):
            self.goodTable.setRowCount(2)
            self.goodTable.setVerticalHeaderLabels(['Coming', 'Going'])
            self.goodTable.setMaximumHeight(88)

            # compound