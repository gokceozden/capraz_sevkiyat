__author__ = 'mustafa'

from PySide.QtGui import *
from PySide.QtCore import *

class Greeting(QDialog):
    """
    greeting screen of the application
    """
    def __init__(self):
        """
        init buttons and actions
        :return:
        """
        QDialog.__init__(self)
        self.setWindowTitle("Start a solver")
        self.setGeometry(300,400,500,500)

        # buttons
        self.newButton = QPushButton("New")
        self.loadButton = QPushButton("Load")

        # connect
        self.newButton.clicked.connect(self.new_data)
        self.loadButton.clicked.connect(self.load_data)

        # layout
        self.vlayout = QVBoxLayout()
        self.vlayout.addWidget(self.newButton)
        self.vlayout.addWidget(self.loadButton)

        self.setLayout(self.vlayout)
        self.setWindowModality(Qt.ApplicationModal)

    def new_data(self):
        """
        start a new data set
        :return:
        """
        self.accept()

    def load_data(self):
        """
        load a previously saved data set
        :return:
        """
        self.reject()