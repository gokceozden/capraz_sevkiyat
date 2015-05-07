__author__ = 'mustafa'

import sys
from PySide.QtGui import *

class TruckWidget(QWidget):
    """
    Truck Data Widget
    """

    def __init__(self, name):
        QWidget.__init__(self)

        #create the widgets
        self.truckHLayout = QHBoxLayout(self)
        self.truckName = QLineEdit(name)
        self.truckTypeComboBox = QComboBox(self)
        self.createTable()


        #combo box for truck type
        self.truckTypeComboBox.addItem('Inbound')
        self.truckTypeComboBox.addItem('Outbound')
        self.truckTypeComboBox.addItem('Compound')

        # add the widget elements to the layout
        self.truckHLayout.addWidget(self.truckName)
        self.truckHLayout.addWidget(self.truckTypeComboBox)
        self.truckHLayout.addWidget(self.goodTable)

    def createTable(self):

        self.goodTable = QTableView()
        self.goodModel = QStandardItemModel()
        a = [1,2,3,4]
        self.goodModel.insertRow(5)
        self.goodTable.setModel(self.goodModel)







