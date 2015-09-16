__author__ = 'mustafa'

from PySide.QtGui import *
from PySide.QtCore import *
from solver import Solver
from itertools import chain
from src.algorithms import Algorithms

class TruckDataTable(QWidget):
    """
    shows goods and time data of trucks in runtime
    """
    def __init__(self, algorithm = Algorithms, model = Solver ):
        QWidget.__init__(self)
        self.model = model
        self.algorithm = algorithm

        self.truck_table = QTableView()
        self.truck_header = ['truck name', 'current state', 'state change time', 'coming goods', 'going goods']
        self.truck_list = []
        self.truck_vertical = []
        self.truck_table_view = RunTimeTruckTableModel(self, self.truck_list, self.truck_header, self.truck_vertical)
        self.truck_table.setModel(self.truck_table_view)

        self.good_table = QTableView()
        good_numbers = []
        for i in range(self.model.number_of_goods):
            good_numbers.append(i)
            good_numbers.append('reserved')
        self.good_header = ['truck name']
        self.good_header.extend(good_numbers)
        self.good_list = [[0, 0, 0]]
        self.good_vertical = []
        self.good_table_view = RunTimeTruckTableModel(self, self.good_list, self.good_header, self.good_vertical)
        self.good_table.setModel(self.good_table_view)

        self.sequence_table = QTableView()
        self.sequence_header = []
        self.sequence_vertical = ['current coming', 'current going', 'best coming', 'best going']
        number_coming_sequence = self.model.number_of_inbound_trucks + self.model.number_of_compound_trucks + self.model.number_of_receiving_doors - 1
        number_giong_sequence = self.model.number_of_inbound_trucks + self.model.number_of_compound_trucks + self.model.number_of_shipping_doors - 1
        self.sequence_list = [[0]* number_coming_sequence, [0] * number_giong_sequence, [0] * number_coming_sequence, [0] * number_coming_sequence]

        self.sequence_table_view = RunTimeTruckTableModel(self, self.sequence_list, self.sequence_header, self.sequence_vertical)
        self.sequence_table.setModel(self.sequence_table_view)

        self.update_tables()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.truck_table)
        self.layout.addWidget(self.good_table)
        self.layout.addWidget(self.sequence_table)
        self.setLayout(self.layout)

    def update_tables(self):
        temp_list = []
        for truck in self.model.all_trucks.values():
            list_item = [truck.truck_name, truck.state_list[truck.current_state], truck.finish_time, str(truck.coming_good_amounts.values()), str(truck.going_good_amounts.values())]
            temp_list.append(list_item)
        self.truck_table_view.truck_list = temp_list

        temp_list = []
        temp_list.append(self.algorithm.solution_sequence['inbound'])
        temp_list.append(self.algorithm.solution_sequence['outbound'])
        temp_list.append(self.algorithm.best_sequence['inbound'])
        temp_list.append(self.algorithm.best_sequence['outbound'])
        self.sequence_table_view.truck_list = temp_list
        print(self.sequence_table_view.truck_list)


class RunTimeTruckTableModel(QAbstractTableModel):
    def __init__(self, parent, mylist, header, vertical):
        QAbstractTableModel.__init__(self, parent)
        self.truck_list = mylist
        self.truck_header = header
        self.truck_vertical = vertical

    def rowCount(self, parent):
        if self.truck_list:
            return len(self.truck_list)
        return 0

    def columnCount(self, parent):
        if self.truck_list:
            return len(self.truck_list[0])
        return 0

    def data(self, index, role):
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole:
            return None
        return self.truck_list[index.row()][index.column()]

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if self.truck_header:
                return self.truck_header[col]
        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            if self.truck_vertical:
                return self.truck_vertical[col]
        return None

    def sort(self, col, order):
        """sort table by given column number col"""
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.mylist = sorted(self.mylist,
            key=operator.itemgetter(col))
        if order == Qt.DescendingOrder:
            self.mylist.reverse()
        self.emit(SIGNAL("layoutChanged()"))