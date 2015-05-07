__author__ = 'mustafa'

import sys
from PySide.QtGui import *
from truck_widget import TruckWidget
from src.solver import Solver


class DataWindow(QWidget):
    """
    Data window widget
    """
    def __init__(self, model = Solver()):
        QWidget.__init__(self)
        self.model = model
        self.truckList = []
        self.setWindowTitle('Data Window')
        self.setupComponents()
        self.setGeometry(300,400,500,500)




    def setupComponents(self):
        """
        Setup all the components, statusbar, menubar, toolbar
        :return:
        """
        self.setupStatusBar()
        self.setupMenuBar()
        self.setupButtons()
        self.setupLayout()
        self.setupConnections()

    def setupStatusBar(self):
        pass

    def setupMenuBar(self):
        pass

    def setupButtons(self):
        self.addTruckButton = QPushButton('Add Truck', self)
        self.addTruckButton.clicked.connect(self.addTruck)


    def setupLayout(self):
        """
        Setup the layout for the data window
        :return:
        """
        self.mainVBox = QVBoxLayout()
        self.hBoxMainData = QHBoxLayout()
        self.vBoxTruckData = QVBoxLayout()

        self.numberGoodsSpin = QSpinBox()
        self.numberGoodsSpin.setMinimum(1)

        self.hBoxMainData.addWidget(self.addTruckButton)
        self.hBoxMainData.addWidget(self.numberGoodsSpin)
        self.mainVBox.addLayout(self.hBoxMainData)
        self.addTruck()
        self.mainVBox.addLayout(self.vBoxTruckData)

        self.setLayout(self.mainVBox)


    def setupConnections(self):
        self.numberGoodsSpin.valueChanged.connect(self.dataChange)


    def dataChange(self):
        self.model.number_of_goods = self.numberGoodsSpin.value()



    def updateTruckList(self):
        """
        Updates the truck list on gui
        :return:
        """
        for truck in self.truckList:
            self.vBoxTruckData.addWidget(truck)

    def addTruck(self):

        #self.model.add_truck(0)
        truck = TruckWidget('truck1')
        self.truckList.append(truck)
        self.updateTruckList()







