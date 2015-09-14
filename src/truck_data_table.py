__author__ = 'mustafa'

from PySide.QtGui import *
from PySide.QtCore import *
from solver import Solver
from itertools import chain

class TruckDataTable(QWidget):
    """
    shows goods and time data of trucks in runtime
    """
    def __init__(self, model = Solver):
        QWidget.__init__(self)
        self.model = model

        self.truck_table = QTableView()
        self.truck_header = ['truck name', 'current state', 'state change time']
        self.truck_list = []
        self.truck_table_view = RunTimeTruckTableModel(self, self.truck_list, self.truck_header)
        self.update_tables()
        self.truck_table.setModel(self.truck_table_view)

        self.good_table = QTableView()
        self.good_header = ['truck name', 'current state', 'state change time']
        self.good_list = [0, 1, 2]
        self.good_table_view = RunTimeTruckTableModel(self, self.good_list, self.truck_header)
        self.update_tables()
        self.good_table.setModel(self.good_table_view)


        self.layout = QVBoxLayout()
        self.layout.addWidget(self.truck_table)
        self.layout.addWidget(self.good_table)
        self.setLayout(self.layout)

        # self.update_tables()

    def update_tables(self):
        self.setFocus()
        temp_list = []
        for truck in self.model.all_trucks.values():
            list_item = [truck.truck_name, truck.state_list[truck.current_state], truck.finish_time]
            temp_list.append(list_item)
        self.truck_table_view.truck_list = temp_list

class RunTimeTruckTableModel(QAbstractTableModel):
    def __init__(self, parent, mylist, header):
        QAbstractTableModel.__init__(self, parent)
        self.truck_list= mylist
        self.truck_header = header

    def rowCount(self, parent):
        return len(self.truck_list)

    def columnCount(self, parent):
        return len(self.truck_list[0])

    def data(self, index, role):
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole:
            return None
        return self.truck_list[index.row()][index.column()]

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.truck_header[col]
        return None

    def sort(self, col, order):
        """sort table by given column number col"""
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.mylist = sorted(self.mylist,
            key=operator.itemgetter(col))
        if order == Qt.DescendingOrder:
            self.mylist.reverse()
        self.emit(SIGNAL("layoutChanged()"))