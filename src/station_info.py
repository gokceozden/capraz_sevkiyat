__author__ = 'mustafa'

from PySide.QtGui import *

class StationInfo(QMessageBox):
    def __init__(self, station):
        self.station = station
        QMessageBox.__init__(self)
        good_text = "Goods:\n"
        for good_name, goods in self.station.station_goods.items():
            good_text += good_name + ': '
            total = 0
            for good in goods:
                total += good.amount
            good_text += str(total) + '\n'

        self.setText(good_text)