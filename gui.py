#!/usr/bin/python
__author__ = 'Robotes'

import sys
from PySide.QtGui import *
from src.dataWindow import DataWindow
from src.solver import Solver
from src.data_set_window import *
import pickle
from src.truck_info import TruckInfo
from src.door_info import DoorInfo
from src.station_info import StationInfo

class GraphView(QGraphicsView):
    def __init__(self, scn, model = Solver()):
        QGraphicsView.__init__(self, scn)
        self.scn = scn
        self.model = model
        self.inbound_truck_images = {}
        self.outbound_truck_images = {}
        self.compound_truck_images = {}
        self.coming_door_images = {}
        self.shipping_door_images = {}
        self.doors = []
        self.goods = []
        self.truckPixmap = QPixmap("images/truck.png")
        self.doorPixmap = QPixmap("images/door_icon.png")
        self.storagePixmap = QPixmap("images/storage.png")

    def mousePressEvent(self, event):
        item = self.itemAt(event.pos())
        for truck_name, truck_item in self.inbound_truck_images.iteritems():
            if truck_item == item:
                truck_info = TruckInfo(self.model.inbound_trucks[truck_name])
                truck_info.exec_()

        for truck_name, truck_item in self.outbound_truck_images.iteritems():
            if truck_item == item:
                truck_info = TruckInfo(self.model.outbound_trucks[truck_name])
                truck_info.exec_()

        for truck_name, truck_item in self.compound_truck_images.iteritems():
            if truck_item == item:
                truck_info = TruckInfo(self.model.compound_trucks[truck_name])
                truck_info.exec_()

        for door_name, door_item in self.coming_door_images.iteritems():
            if door_item == item:
                door_info = DoorInfo(self.model.station.receiving_doors[door_name])
                door_info.setWindowTitle(door_name)
                door_info.exec_()

        for door_name, door_item in self.shipping_door_images.iteritems():
            if door_item == item:
                door_info = DoorInfo(self.model.station.shipping_doors[door_name])
                door_info.setWindowTitle(door_name)
                door_info.exec_()

        if self.storage_image == item:
            station_info = StationInfo(self.model.station)
            station_info.exec_()

    def init_image(self):
        self.storage_image = self.scn.addPixmap(self.storagePixmap)
        self.storage_image.scale(0.7,0.7)
        self.storage_image.setPos(150,300)

        self.inbound_truck_images = {}
        self.outbound_truck_images = {}
        self.compound_truck_images = {}

        for trucks in self.model.inbound_trucks.values():
            truck_image = self.scn.addPixmap(self.truckPixmap)
            truck_image.scale(0.2,0.2)
            self.inbound_truck_images[trucks.truck_name] = truck_image

        for trucks in self.model.outbound_trucks.values():
            truck_image = self.scn.addPixmap(self.truckPixmap)
            truck_image.scale(0.2,0.2)
            self.outbound_truck_images[trucks.truck_name] = truck_image

        for trucks in self.model.compound_trucks.values():
            truck_image = self.scn.addPixmap(self.truckPixmap)
            truck_image.scale(0.2,0.2)
            self.compound_truck_images[trucks.truck_name] = truck_image

        i = 0
        for door_name, doors in self.model.station.receiving_doors.iteritems():
            door_image = self.scn.addPixmap(self.doorPixmap)
            door_image.scale(0.4, 0.4)
            self.coming_door_images[door_name] = door_image
            door_image.setPos(20, 280 + i*100)
            i += 1

        i = 0
        for door_name, doors in self.model.station.shipping_doors.iteritems():
            door_image = self.scn.addPixmap(self.doorPixmap)
            door_image.scale(0.4, 0.4)
            self.shipping_door_images[door_name] = door_image
            door_image.setPos(380, 280 + i*100)
            i += 1

        self.update_image()

    def update_image(self):
        self.calculate_trucks()
        self.show()


    def calculate_trucks(self):
        i = 0
        for truck_name, truck_image in self.inbound_truck_images.items():
            if self.model.inbound_trucks[truck_name].current_state == 0:
                truck_image.setPos(-600, 100*i)
            if self.model.inbound_trucks[truck_name].current_state == 1:
                y = self.coming_door_images[self.model.inbound_trucks[truck_name].receiving_door_name].pos().y()
                truck_image.setPos(-200, y)
            if self.model.inbound_trucks[truck_name].current_state == 2:
                y = self.coming_door_images[self.model.inbound_trucks[truck_name].receiving_door_name].pos().y()
                truck_image.setPos(-100, y)
            if self.model.inbound_trucks[truck_name].current_state == 4:
                truck_image.setPos(100, 800)
            i += 1

        i = 0
        for truck_name, truck_image in self.compound_truck_images.items():
            if self.model.compound_trucks[truck_name].current_state == 0:
                truck_image.setPos(-600, 800 - 100*i)
            if self.model.compound_trucks[truck_name].current_state == 1:
                y = self.coming_door_images[self.model.compound_trucks[truck_name].receiving_door_name].pos().y()
                truck_image.setPos(-200, y)
            if self.model.compound_trucks[truck_name].current_state == 2:
                y = self.coming_door_images[self.model.compound_trucks[truck_name].receiving_door_name].pos().y()
                truck_image.setPos(-100, y)
            if self.model.compound_trucks[truck_name].current_state == 4:
                truck_image.setPos(100, 0)
            if self.model.compound_trucks[truck_name].current_state == 6:
                y = self.shipping_door_images[self.model.compound_trucks[truck_name].shipping_door_name].pos().y()
                truck_image.setPos(500, y)
            if self.model.compound_trucks[truck_name].current_state == 7:
                truck_image.setPos(300, 800)
            i += 1

        i = 0
        for truck_name, truck_image in self.outbound_truck_images.items():
            if self.model.outbound_trucks[truck_name].current_state == 0:
                truck_image.setPos(900, 100*i)
            if self.model.outbound_trucks[truck_name].current_state == 1:
                y = self.shipping_door_images[self.model.outbound_trucks[truck_name].shipping_door_name].pos().y()
                truck_image.setPos(500, y)
            if self.model.outbound_trucks[truck_name].current_state == 2:
                y = self.shipping_door_images[self.model.outbound_trucks[truck_name].shipping_door_name].pos().y()
                truck_image.setPos(500, y)
            if self.model.outbound_trucks[truck_name].current_state == 4:
                truck_image.setPos(300, 800)
            i += 1

class MainWindow(QMainWindow):
    """
    Main window class for capraz_sevkiyat project
    """
    def __init__(self):
        QMainWindow.__init__(self)
        self.model = Solver()
        self.setWindowTitle("Capraz Sevkiyat Projesi")
        self.setGeometry(400,400,400,400)


        self.setupComponents()
        self.init_simulation()

    def init_simulation(self):
        self.scn = QGraphicsScene()
        self.simulation = GraphView(self.scn, self.model)
        self.setCentralWidget(self.simulation)


        self.setup_simulation()
        self.truck_image_list = {}

        # remember to add an icon for the application
        # self.setWindowIcon()

    def setup_simulation(self):

        # self.truckPixmap = QPixmap("images/truck.png")
        # self.truck1 = self.scn.addPixmap(self.truckPixmap)
        # self.truck2 = self.scn.addPixmap(self.truckPixmap)
        # self.truck1.scale(0.2,0.2)
        # self.truck1.setPos(100,800)
        # self.truck2.scale(0.2,0.2)
        # self.truck2.setPos(800,800)
        self.simulation.init_image()
        self.simulation.show()

    def simulation_cycle(self):
        i = 0
        for inbound_trucks in self.model.inbound_trucks.values():
            truck_name = inbound_trucks.truck_name
            self.truck_image_list[truck_name] = self.scn.addPixmap(self.truckPixmap)
            self.truck_image_list[truck_name].scale(0.2,0.2)
            self.truck_image_list[truck_name].setPos(-600,i*100)
            i = i +1
        self.simulation.show()

    def loadModel(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open file',
                                                     '/home')
        
        self.model = pickle.load(open(file_name, 'rb'))
        self.simulation.model = self.model
        self.scn.clear()
        self.model.init_data()
        self.simulation.init_image()

    def saveModel(self):
            
        file_name, _ = QFileDialog.getSaveFileName(self, 'Save file',
                                                     '/home')
            
        pickle.dump(self.model,  open(file_name, 'wb'))

    def setupComponents(self):
        """
        Setup all the components, statusbar, menubar, toolbar
        :return:
        """

        self.setupStatusBar()
        self.setupMenuBar()
        self.setupButtons()
        self.setupToolBar()
        self.setupLayout()

    def setupLayout(self):
        """
        Sets up the layout of the main window
        """

        self.mainGrid = QGridLayout()
        self.mainVBox = QVBoxLayout()
        self.mainGrid.addWidget(self.dataButton)
        self.setLayout(self.mainGrid)

    def setupButtons(self):
        """
        Setting the buttons for the main windows
        :return:
        """

        self.dataButton = QPushButton('Set/Inspect Data')
        self.dataButton.adjustSize()
        self.dataButton.clicked.connect(self.showTruckDataWindow)
        self.loadButton = QPushButton('Load Data')
        #self.loadButton.adjustSize()
        self.loadButton.clicked.connect(self.loadModel)

        self.saveButton = QPushButton('Save Data')
        #self.saveButton.adjustSize()
        self.saveButton.clicked.connect(self.saveModel)

    def showTruckDataWindow(self):
        self.truckDataWindow = DataWindow(self.model)
        self.truckDataWindow.show()
        self.scn.clear()
        self.simulation.init_image()

    def showDataWindow(self):
        self.dataWindow = DataSetWindow(self.model)
        self.dataWindow.show()
        self.simulation.init_image()

    def setupStatusBar(self):

        self.mainStatusBar = QStatusBar()
        self.setStatusBar(self.mainStatusBar)
        self.mainStatusBar.showMessage('Ready')

    def setupMenuBar(self):
        self.setupActions()
        self.setupMenus()

    def newModel(self):
        msgBox = QMessageBox()
        msgBox.setText('Would you like to save the old data')
        msgBox.setStandardButtons(QMessageBox.Save | QMessageBox.Cancel)
        msgBox.setDefaultButton(QMessageBox.Save)
        ret = msgBox.exec_()

        if ret == QMessageBox.Save:
            self.saveModel()
        elif ret == QMessageBox.Cancel:
            pass
        self.model = Solver()
        self.scn.clear()

    def setupActions(self):
        
        self.newAction = QAction(QIcon('images/new.png'), '&New', self, shortcut = QKeySequence.New, statusTip = "New data set", triggered = self.newModel)
        self.loadAction = QAction(QIcon('images/load.png'), '&Load', self,
                                   shortcut=QKeySequence.Open, statusTip = 'Load a saved data set', triggered = self.loadModel)

        self.saveAction = QAction(QIcon('images/save.png'), '&Save', self,
                                   shortcut=QKeySequence.Save, statusTip = 'Save data set', triggered = self.saveModel)

        self.truckDataAction = QAction(QIcon('images/truck.png'), '&Truck Data', self,
                                   shortcut=QKeySequence.New, statusTip = 'See truck data set', triggered = self.showTruckDataWindow)

        self.dataAction = QAction(QIcon('images/data.png'), '&Data', self, shortcut=QKeySequence.New, statusTip = 'Set data set', triggered = self.showDataWindow)

        self.showDataAction = QAction(QIcon('images/data.png'), '&Show Data', self, statusTip = "See Data Set", triggered = self.showDataSet)

        self.stepAction = QAction(QIcon('images/step.png'), 'Step forward', self, statusTip = 'One step in simulation', triggered = self.stepForward)

    def stepForward(self):
        self.model.step()
        self.statusBar().showMessage(str(self.model.current_time))
        self.simulation.update_image()

    def showDataSet(self):
        self.model.init_iteration(0)
        self.simulation.update_image()

    def setupMenus(self):
        pass

    def setupToolBar(self):
        self.mainToolBar = self.addToolBar('Main')
        self.mainToolBar.addAction(self.newAction)
        self.mainToolBar.addAction(self.loadAction)
        self.mainToolBar.addAction(self.saveAction)
        self.mainToolBar.addAction(self.truckDataAction)
        self.mainToolBar.addAction(self.dataAction)
        self.mainToolBar.addAction(self.showDataAction)
        self.mainToolBar.addAction(self.stepAction)

if __name__ == '__main__':

    myApp = QApplication(sys.argv)
    mainWindow = MainWindow()
    #mainWindow.show()
    mainWindow.showMaximized()
    myApp.exec_()
    sys.exit(0)