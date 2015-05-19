__author__ = 'mustafa'

from PySide.QtGui import *

from src.truck_widget import TruckWidget
from src.solver import Solver
from src.good import Good

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
        self.prev_data()


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
        self.numberInboundSpin.setMinimum(0)

        self.numberOutbound = QLabel("Number of outbound trucks")
        self.numberOutbound.setMaximumWidth(150)
        self.numberOutboundSpin = QSpinBox()
        self.numberOutboundSpin.setMinimum(0)

        self.numberCompound = QLabel("Number of compound trucks")
        self.numberCompound.setMaximumWidth(150)
        self.numberCompoundSpin = QSpinBox()
        self.numberCompoundSpin.setMinimum(0)


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


    def prev_data(self):

        self.numberGoodsSpin.setValue(self.model.number_of_goods)
        for i in range(len(self.model.inbound_trucks)):
            name = 'inbound' + str(i)
            self.inboundView.append(TruckWidget(name, self.numberGoodsSpin.value(), 'inbound'))
            self.vInboundTruck.addWidget(self.inboundView[-1])


        for i in range(len(self.model.outbound_trucks)):
            name = 'outbound' + str(i)
            self.inboundView.append(TruckWidget(name, self.numberGoodsSpin.value(), 'outbound'))
            self.vOutBoundTruck.addWidget(self.inboundView[-1])

        for i in range(len(self.model.compound_trucks)):
            name = 'compound' + str(i)
            self.inboundView.append(TruckWidget(name, self.numberGoodsSpin.value(), 'compound'))
            self.vCompoundTruck.addWidget(self.inboundView[-1])


        #for view in



    def dataChange(self):

        self.model.number_of_goods = self.numberGoodsSpin.value()

        if (self.numberInboundSpin.value() > len(self.inboundView)):
            name = self.model.add_truck('inbound')
            self.inboundView.append(TruckWidget(name, self.numberGoodsSpin.value(), 'inbound'))
            self.vInboundTruck.addWidget(self.inboundView[-1])

        for val in self.inboundView:
            for i in range(self.numberGoodsSpin.value()):
                data = val.goodTable.item(0,i)
                if data:
                    print(data.text())
                    new_good = Good(i, data.text())
                    self.model.inbound_trucks[val.truck_name].coming_goods[i] = new_good



        if (self.numberInboundSpin.value() < len(self.inboundView)):

            self.model.remove_truck('inbound')
            delete_widget = self.inboundView.pop()
            delete_widget.deleteLater()

        if (self.numberOutboundSpin.value() > len(self.outboundView)):
            name = self.model.add_truck('outbound')
            self.outboundView.append(TruckWidget(name, self.numberGoodsSpin.value(), 'outbound'))
            self.vOutBoundTruck.addWidget(self.outboundView[-1])

        if (self.numberOutboundSpin.value() < len(self.outboundView)):

            self.model.remove_truck('outbound')
            delete_widget = self.outboundView.pop()
            delete_widget.deleteLater()

        if (self.numberCompoundSpin.value() > len(self.compoundView)):
             name = self.model.add_truck('compound')
             self.compoundView.append(TruckWidget(name, self.numberGoodsSpin.value(),'compound'))
             self.vCompoundTruck.addWidget(self.compoundView[-1])

        if (self.numberCompoundSpin.value() < len(self.compoundView)):

            self.model.remove_truck('compound')
            delete_widget = self.compoundView.pop()
            delete_widget.deleteLater()

        for truck_widget in self.inboundView:
            truck_widget.number_of_goods = self.numberGoodsSpin.value()
            truck_widget.updateTable()

        for truck_widget in self.outboundView:
            truck_widget.number_of_goods = self.numberGoodsSpin.value()
            truck_widget.updateTable()

        for truck_widget in self.compoundView:
            truck_widget.number_of_goods = self.numberGoodsSpin.value()
            truck_widget.updateTable()


