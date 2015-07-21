__author__ = 'mustafa'

from PySide.QtGui import *
from PySide.QtCore import *
from src.graphview import GraphView

class GeneralInfo(QWidget):
    """
    General information screen in main gui
    """
    def __init__(self):
        """
        init text screen for info
        :return:
        """
        QWidget.__init__(self)
        self.data = None
        self.infoText = QTextEdit()
        self.infoText.setReadOnly(True)
        # self.scn = QGraphicsScene()
        # self.simulation = GraphView(self.scn, self.data)

        self.layout = QGridLayout()
        self.layout.addWidget(self.infoText, 1, 1)

        # self.layout.addWidget(self.simulation, 1, 2)
        self.setLayout(self.layout)

    def print_data(self):
        self.infoText.clear()
        self.data_string = "deneme"
        self.infoText.setText(self.data_string)

