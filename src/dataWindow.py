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
        self.inboundView = []
        self.outboundView = []
        self.compoundView = []
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
        self.numberGoodLabel = QLabel("Number of good types")
        self.numberGoodLabel.setMaximumWidth(150)
        self.numberGoodsSpin = QSpinBox()
        self.numberGoodsSpin.setMinimum(1)
        self.numberGoodsSpin.setMaximumWidth(70)

        self.numberInbound = QLabel("Number of inbound trucks")
        self.numberInbound.setMaximumWidth(150)
        self.numberInboundSpin = QSpinBox()
        self.numberInboundSpin.setMinimum(1)

        self.numberOutbound = QLabel("Number of outbound trucks")
        self.numberOutbound.setMaximumWidth(150)
        self.numberOutboundSpin = QSpinBox()
        self.numberOutboundSpin.setMinimum(1)

        self.numberCompound = QLabel("Number of compound trucks")
        self.numberCompound.setMaximumWidth(150)
        self.numberCompoundSpin = QSpinBox()
        self.numberCompoundSpin.setMinimum(1)


    def setupLayout(self):
        """
        Setup the layout for the data window
        :return:
        """
        self.mainVBox = QVBoxLayout()
        self.truckForm = QFormLayout()
        self.hBoxMainData = QHBoxLayout()
        self.vBoxTruckData = QVBoxLayout()
        self.vInboundTruck = QVBoxLayout()
        self.vOutBoundTruck = QVBoxLayout()
        self.vCompoundTruck = QVBoxLayout()
        self.inboundLabel = QLabel('Inbound Trucks')
        self.outboundLabel = QLabel('Outbound Trucks')
        self.compoundLabel = QLabel('Compound Trucks')

        self.vInboundTruck.addWidget(self.inboundLabel)
        self.vOutBoundTruck.addWidget(self.outboundLabel)
        self.vCompoundTruck.addWidget(self.compoundLabel)

        self.truckForm.addRow(self.numberInbound, self.numberInboundSpin)
        self.truckForm.addRow(self.numberOutbound, self.numberOutboundSpin)
        self.truckForm.addRow(self.numberCompound, self.numberCompoundSpin)
        self.hBoxMainData.addLayout(self.truckForm)
        self.hBoxMainData.addWidget(self.numberGoodLabel)
        self.hBoxMainData.addWidget(self.numberGoodsSpin)
        self.mainVBox.addLayout(self.hBoxMainData)
        self.addTruck()
        self.mainVBox.addLayout(self.vInboundTruck)
        self.mainVBox.addLayout(self.vOutBoundTruck)
        self.mainVBox.addLayout(self.vCompoundTruck)
        self.mainVBox.addStretch()
        self.setLayout(self.mainVBox)
        self.dataChange()


    def setupConnections(self):
        self.numberGoodsSpin.valueChanged.connect(self.dataChange)
        self.numberInboundSpin.valueChanged.connect(self.dataChange)
        self.numberOutboundSpin.valueChanged.connect(self.dataChange)
        self.numberCompoundSpin.valueChanged.connect(self.dataChange)


    def dataChange(self):
        self.model.number_of_goods = self.numberGoodsSpin.value()

        for i in range(self.numberInboundSpin.value() - len(self.inboundView)):
            self.inboundView.append(TruckWidget('truck1', self.numberGoodsSpin.value(),0))
            self.vInboundTruck.addWidget(self.inboundView[-1])

        for i in range(len(self.inboundView) - self.numberInboundSpin.value()):
            self.inboundView.pop()
            b = self.vInboundTruck.itemAt(len(self.inboundView))
            b.widget().deleteLater()

        for i in range(self.numberOutboundSpin.value() - len(self.outboundView)):

            self.outboundView.append(TruckWidget('truck1', self.numberGoodsSpin.value(),1))
            self.vOutBoundTruck.addWidget(self.outboundView[-1])


        for i in range(self.numberCompoundSpin.value() - len(self.compoundView)):
            truck = TruckWidget('truck1', self.numberGoodsSpin.value(),2)
            self.compoundView.append(truck)
            self.vCompoundTruck.addWidget(truck)



        for trucks in self.inboundView:
            trucks.number_of_goods = self.numberGoodsSpin.value()
            trucks.updateTable()

        for trucks in self.outboundView:
            trucks.number_of_goods = self.numberGoodsSpin.value()
            trucks.updateTable()

        for trucks in self.compoundView:
            trucks.number_of_goods = self.numberGoodsSpin.value()
            trucks.updateTable()


        # for truckWidget in self.truckList:
        #     truckWidget.number_of_goods = self.numberGoodsSpin.value()
        #     truckWidget.updateTable()



    def updateTruckList(self):
        """
        Updates the truck list on gui
        :return:
        """
        pass



    def addTruck(self):

        pass






