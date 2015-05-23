__author__ = 'mustafa'

from PySide.QtGui import *
from PySide.QtCore import * 

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
        self.setWindowTitle('Truck Data Window')
        self.setupComponents()
        self.setGeometry(300,400,500,500)
        self.setWindowModality(Qt.ApplicationModal)


    def setupComponents(self):
        """
        Setup all the components, statusbar, menubar, toolbar
        :return:
        """
        self.setupStatusBar()
        self.setupMenuBar()
        self.setupButtons()
        self.setupLayout()
        self.prev_data()
        self.setupConnections()
        self.dataChange()

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

        self.numberReceiveDoorLabel = QLabel("Number of receiver doors")
        self.numberReceiveDoorLabel.setMaximumWidth(150)
        self.numberReceiveDoorSpin = QSpinBox()
        self.numberReceiveDoorSpin.setMinimum(1)
        self.numberReceiveDoorSpin.setMaximumWidth(70)

        self.numberShippingDoorLabel = QLabel("Number of shipping doors")
        self.numberShippingDoorLabel.setMaximumWidth(150)
        self.numberShippingDoorSpin = QSpinBox()
        self.numberShippingDoorSpin.setMinimum(1)
        self.numberShippingDoorSpin.setMaximumWidth(70)

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

        self.doneButton = QPushButton("Done")



    def setupLayout(self):
        """
        Setup the layout for the data window
        :return:
        """
        self.mainVBox = QVBoxLayout()
        self.truckForm = QFormLayout()
        self.doorForm = QFormLayout()
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
        self.doorForm.addRow(self.numberReceiveDoorLabel, self.numberReceiveDoorSpin)
        self.doorForm.addRow(self.numberShippingDoorLabel, self.numberShippingDoorSpin)
        self.doorForm.addRow(self.numberGoodLabel, self.numberGoodsSpin)

        self.hBoxMainData.addLayout(self.truckForm)
        self.hBoxMainData.addLayout(self.doorForm)
        self.hBoxMainData.addWidget(self.doneButton)
        self.mainVBox.addLayout(self.hBoxMainData)

        self.mainVBox.addLayout(self.vInboundTruck)
        self.mainVBox.addLayout(self.vOutBoundTruck)
        self.mainVBox.addLayout(self.vCompoundTruck)
        self.mainVBox.addStretch()
        self.setLayout(self.mainVBox)



    def setupConnections(self):

        self.numberGoodsSpin.valueChanged.connect(self.dataChange)
        self.numberInboundSpin.valueChanged.connect(self.dataChange)
        self.numberOutboundSpin.valueChanged.connect(self.dataChange)
        self.numberCompoundSpin.valueChanged.connect(self.dataChange)
        self.numberShippingDoorSpin.valueChanged.connect(self.dataChange)
        self.numberReceiveDoorSpin.valueChanged.connect(self.dataChange)
        
        self.doneButton.clicked.connect(self.save_data)



    def save_data(self):

        missing_data = False
        
        
        for i in range(self.numberGoodsSpin.value()):
            for inbound_truck in self.inboundView:
                data = inbound_truck.goodTable.item(0,i)
                if data:
                    new_good = Good(i, int(data.text()))
                    self.model.inbound_trucks[inbound_truck.truck_name].coming_goods[i] = new_good
                else:
                    missing_data = True

            for outbound_truck in self.outboundView:
                data = outbound_truck.goodTable.item(0,i)
                if data:
                    new_good = Good(i, int(data.text()))
                    self.model.outbound_trucks[outbound_truck.truck_name].going_goods[i] = new_good
                else:
                    missing_data = True

            for compound_truck in self.compoundView:
                data = compound_truck.goodTable.item(0, i)
                if data:
                    new_good = Good(i, int(data.text()))
                    self.model.compound_trucks[compound_truck.truck_name].coming_goods[i] = new_good
                else:
                    missing_data = True

                data = compound_truck.goodTable.item(1,i)
                if data:
                    new_good = Good(i, int(data.text()))
                    self.model.compound_trucks[compound_truck.truck_name].going_goods[i] = new_good

                else:
                    missing_data = True



    def prev_data(self):

        self.numberGoodsSpin.setValue(self.model.number_of_goods)

        self.numberInboundSpin.setValue(len(self.model.inbound_trucks))
        self.numberOutboundSpin.setValue(len(self.model.outbound_trucks))
        self.numberCompoundSpin.setValue(len(self.model.compound_trucks))
        self.numberShippingDoorSpin.setValue(self.model.number_of_shipping_doors)
        self.numberReceiveDoorSpin.setValue(self.model.number_of_receiving_doors)
        
        self.update_good_table()


        for i in range(len(self.model.inbound_trucks)):
            name = 'inbound' + str(i)
            self.inboundView.append(TruckWidget(name, self.numberGoodsSpin.value(), 'inbound'))
            self.vInboundTruck.addWidget(self.inboundView[-1])
            self.update_good_table()
            for k in range(self.numberGoodsSpin.value()):
                new_item = QTableWidgetItem()
                new_item.setText(str(self.model.inbound_trucks[name].coming_goods[k].amount))
                self.inboundView[-1].goodTable.setItem(0,k,new_item)


        for i in range(len(self.model.outbound_trucks)):
            name = 'outbound' + str(i)
            self.outboundView.append(TruckWidget(name, self.numberGoodsSpin.value(), 'outbound'))
            self.vOutBoundTruck.addWidget(self.outboundView[-1])
            self.update_good_table()
            for k in range(self.numberGoodsSpin.value()):
                new_item = QTableWidgetItem()
                new_item.setText(str(self.model.outbound_trucks[name].going_goods[k].amount))
                self.outboundView[-1].goodTable.setItem(0,k,new_item)

        for i in range(len(self.model.compound_trucks)):
            name = 'compound' + str(i)
            self.compoundView.append(TruckWidget(name, self.numberGoodsSpin.value(), 'compound'))
            self.vCompoundTruck.addWidget(self.compoundView[-1])
            self.update_good_table()
            for k in range(self.numberGoodsSpin.value()):
                new_coming_item = QTableWidgetItem()
                new_coming_item.setText(str(self.model.compound_trucks[name].coming_goods[k].amount))
                self.compoundView[-1].goodTable.setItem(0, k, new_coming_item)
                new_going_item = QTableWidgetItem()
                new_going_item.setText(str(self.model.compound_trucks[name].going_goods[k].amount))
                self.compoundView[-1].goodTable.setItem(1, k, new_going_item)


        #for view in



    def dataChange(self):

        self.model.number_of_goods = self.numberGoodsSpin.value()
        self.model.number_of_shipping_doors = self.numberShippingDoorSpin.value()
        self.model.number_of_receiving_doors = self.numberReceiveDoorSpin.value()

        

        if (self.numberInboundSpin.value() > len(self.inboundView)):
            name = self.model.add_truck('inbound')
            self.inboundView.append(TruckWidget(name, self.numberGoodsSpin.value(), 'inbound'))
            self.vInboundTruck.addWidget(self.inboundView[-1])


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


        self.update_good_table()

    def update_good_table(self):
        for truck_widget in self.inboundView:
            truck_widget.number_of_goods = self.numberGoodsSpin.value()
            truck_widget.updateTable()

        for truck_widget in self.outboundView:
            truck_widget.number_of_goods = self.numberGoodsSpin.value()
            truck_widget.updateTable()

        for truck_widget in self.compoundView:
            truck_widget.number_of_goods = self.numberGoodsSpin.value()
            truck_widget.updateTable()


