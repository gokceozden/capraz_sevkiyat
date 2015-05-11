__author__ = 'mustafa'

from PySide.QtGui import *

from src.truck_widget import TruckWidget
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
        self.addTruckButton.setMaximumWidth(100)
        self.addTruckButton.clicked.connect(self.addTruck)



    def setupLayout(self):
        """
        Setup the layout for the data window
        :return:
        """
        self.mainVBox = QVBoxLayout()
        self.hBoxMainData = QHBoxLayout()
        self.vBoxTruckData = QVBoxLayout()

        self.numberGoodLabel = QLabel("Number of good types")
        self.numberGoodLabel.setMaximumWidth(150)
        self.numberGoodsSpin = QSpinBox()
        self.numberGoodsSpin.setMinimum(1)
        self.numberGoodsSpin.setMaximumWidth(70)

        self.hBoxMainData.addWidget(self.addTruckButton)
        self.hBoxMainData.addWidget(self.numberGoodLabel)
        self.hBoxMainData.addWidget(self.numberGoodsSpin)
        self.mainVBox.addLayout(self.hBoxMainData)
        self.addTruck()
        self.mainVBox.addLayout(self.vBoxTruckData)
        self.mainVBox.addStretch()
        self.setLayout(self.mainVBox)


    def setupConnections(self):
        self.numberGoodsSpin.valueChanged.connect(self.dataChange)


    def dataChange(self):
        self.model.number_of_goods = self.numberGoodsSpin.value()

        for truckWidget in self.truckList:
            truckWidget.number_of_goods = self.numberGoodsSpin.value()
            truckWidget.updateTable()



    def updateTruckList(self):
        """
        Updates the truck list on gui
        :return:
        """
        for i in range(self.model.number_of_trucks - len(self.truckList)):
            truck = TruckWidget('truck1', self.numberGoodsSpin.value())
            self.truckList.append(truck)
            self.vBoxTruckData.addWidget(truck)

        k = 0
        for truck_types, truck_data in self.model.truck_dictionary.items():
            for truck_name, trucks in truck_data.items():
                self.truckList[k].truckName.setText(truck_name)
                k = k +1
                #self.




    def addTruck(self):

        self.model.add_truck('inbound')
        print(self.model.truck_dictionary.values())
        self.updateTruckList()







