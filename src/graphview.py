__author__ = 'mustafa'

from src.truck_info import TruckInfo
from src.door_info import DoorInfo
from src.station_info import StationInfo

from PySide.QtGui import *
from src.solver import Solver

class GraphView(QGraphicsView):
    def __init__(self, scn):
        QGraphicsView.__init__(self, scn)
        self.scn = scn
        self.model = None
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
        for truck_name, truck_item in self.inbound_truck_images.items():
            if truck_item == item:
                truck_info = TruckInfo(self.model.inbound_trucks[truck_name])
                truck_info.exec_()

        for truck_name, truck_item in self.outbound_truck_images.items():
            if truck_item == item:
                truck_info = TruckInfo(self.model.outbound_trucks[truck_name])
                truck_info.exec_()

        for truck_name, truck_item in self.compound_truck_images.items():
            if truck_item == item:
                truck_info = TruckInfo(self.model.compound_trucks[truck_name])
                truck_info.exec_()

        for door_name, door_item in self.coming_door_images.items():
            if door_item == item:
                door_info = DoorInfo(self.model.station.receiving_doors[door_name])
                door_info.setWindowTitle(door_name)
                door_info.exec_()

        for door_name, door_item in self.shipping_door_images.items():
            if door_item == item:
                door_info = DoorInfo(self.model.station.shipping_doors[door_name])
                door_info.setWindowTitle(door_name)
                door_info.exec_()

        if self.storage_image == item:
            station_info = StationInfo(self.model.station)
            station_info.exec_()

    def init_image(self, model):
        self.model = model
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
        for door_name, doors in self.model.station.receiving_doors.items():
            door_image = self.scn.addPixmap(self.doorPixmap)
            door_image.scale(0.4, 0.4)
            self.coming_door_images[door_name] = door_image
            door_image.setPos(20, 280 + i*100)
            i += 1

        i = 0
        for door_name, doors in self.model.station.shipping_doors.items():
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