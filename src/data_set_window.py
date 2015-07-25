__author__ = 'robotes'

from PySide.QtGui import *
from PySide.QtCore import *

from src.solver import Solver
from src.data_store import DataStore

class DataSetWindow(QDialog):
    """
    Data set window widget
    """
    def __init__(self, data=DataStore()):
        QDialog.__init__(self)
        self.data = data
        self.setWindowTitle('Data Set Window')
        self.setWindowModality(Qt.ApplicationModal)        
        self.setupComponents()

        self.setupButtons()
        self.setupComponents()
        self.setupConnections()
        self.setup_layout()
        self.load_data()

    def setupConnections(self):

        self.numberOfGammaSpin.valueChanged.connect(self.update_tables)
        self.numberOfAlphaSpin.valueChanged.connect(self.update_tables)
        self.numberofTightnessSpin.valueChanged.connect(self.update_tables)

    def setupComponents(self):
        self.gammaTable = QTableWidget(1, 1)
        self.alphaTable = QTableWidget(1, 1)
        self.tightnessFactorTable = QTableWidget(1, 1)

    def setupButtons(self):
        self.loadingTimeLabel = QLabel("Loading Time")
        self.loadingTimeEdit = QLineEdit()

        self.changeoverTimeLabel = QLabel("Changeover Time")
        self.changeoverTimeEdit = QLineEdit()

        self.makespanFactorLabel = QLabel("Makespan Factor")
        self.makespanFactorEdit = QLineEdit()

        self.transferTimeLabel = QLabel("Truck Transfer Time")
        self.transferTimeEdit = QLineEdit()

        self.inboundArrivalTimeLabel = QLabel("Inbound Arrival Time")
        self.inboundArrivalTimeEdit = QLineEdit()

        self.outboundArrivalTimeLabel = QLabel("Outbound Arrival Time")
        self.outboundArrivalTimeEdit = QLineEdit()

        self.goodTransferTimeLabel = QLabel("Good Transfer Time")
        self.goodTransferTimeEdit = QLineEdit()

        self.doneButton = QPushButton('Done')
        self.doneButton.clicked.connect(self.save_data)

        self.numberOfGammaLabel = QLabel("Number of gamma values")
        self.numberOfGammaSpin = QSpinBox()
        self.numberOfGammaSpin.setMinimum(1)

        self.numberOfAlphaLabel = QLabel("Number of alpha values")
        self.numberOfAlphaSpin = QSpinBox()
        self.numberOfAlphaSpin.setMinimum(1)

        self.numberofTightnessLabel = QLabel("Number of tightness factors")
        self.numberofTightnessSpin = QSpinBox()
        self.numberofTightnessSpin.setMinimum(1)

    def setup_layout(self):

        self.dataSetForm = QFormLayout()
        self.vTableLayout = QVBoxLayout()
        self.mainLayout = QHBoxLayout()
        
        self.dataSetForm.addRow(self.loadingTimeLabel, self.loadingTimeEdit)
        self.dataSetForm.addRow(self.changeoverTimeLabel, self.changeoverTimeEdit)
        self.dataSetForm.addRow(self.makespanFactorLabel, self.makespanFactorEdit)
        self.dataSetForm.addRow(self.transferTimeLabel, self.transferTimeEdit)
        self.dataSetForm.addRow(self.inboundArrivalTimeLabel, self.inboundArrivalTimeEdit)
        self.dataSetForm.addRow(self.outboundArrivalTimeLabel, self.outboundArrivalTimeEdit)
        self.dataSetForm.addRow(self.goodTransferTimeLabel, self.goodTransferTimeEdit)
        self.dataSetForm.addRow(self.numberOfGammaLabel, self.numberOfGammaSpin)
        self.dataSetForm.addRow(self.numberOfAlphaLabel, self.numberOfAlphaSpin)
        self.dataSetForm.addRow(self.numberofTightnessLabel, self.numberofTightnessSpin)
        self.dataSetForm.addRow(self.doneButton)

        self.vTableLayout.addWidget(self.gammaTable)
        self.vTableLayout.addWidget(self.alphaTable)
        self.vTableLayout.addWidget(self.tightnessFactorTable)

        self.mainLayout.addLayout(self.dataSetForm)
        self.mainLayout.addLayout(self.vTableLayout)
        
        self.setLayout(self.mainLayout)

    def update_tables(self):

        self.gammaTable.setColumnCount(self.numberOfGammaSpin.value())
        self.alphaTable.setColumnCount(self.numberOfAlphaSpin.value())
        self.tightnessFactorTable.setColumnCount(self.numberofTightnessSpin.value())

    def save_data(self):

        self.data.changeover_time = float(self.changeoverTimeEdit.text())
        self.data.loading_time = float(self.loadingTimeEdit.text())
        self.data.makespan_factor = float(self.makespanFactorEdit.text())
        self.data.transfer_time = float(self.transferTimeEdit.text())
        self.data.good_transfer_time = float(self.goodTransferTimeEdit.text())
        self.data.inbound_arrival_time = float(self.inboundArrivalTimeEdit.text())
        self.data.outbound_arrival_time = float(self.outboundArrivalTimeEdit.text())
        
        alpha = []
        gamma = []
        tightness = []
        
        for value in range(self.numberOfAlphaSpin.value()):
            data = self.alphaTable.item(0,value)
            if data:
                alpha.append(float(data.text()))

        for value in range(self.numberOfGammaSpin.value()):
            data = self.gammaTable.item(0, value)
            if data:
                gamma.append(float(data.text()))

        for value in range(self.numberofTightnessSpin.value()):
            data = self.tightnessFactorTable.item(0, value)
            if data:
                tightness.append(float(data.text()))

        self.data.alpha_values = alpha
        self.data.gamma_values = gamma
        self.data.tightness_factors = tightness

        self.data.create_data_set()
        self.close()

    def load_data(self):

        self.loadingTimeEdit.setText(str(self.data.loading_time))
        self.changeoverTimeEdit.setText(str(self.data.changeover_time))
        self.makespanFactorEdit.setText(str(self.data.makespan_factor))
        self.transferTimeEdit.setText(str(self.data.transfer_time))
        self.goodTransferTimeEdit.setText(str(self.data.good_transfer_time))
        self.inboundArrivalTimeEdit.setText(str(self.data.inbound_arrival_time))
        self.outboundArrivalTimeEdit.setText(str(self.data.outbound_arrival_time))

        self.numberOfGammaSpin.setValue(len(self.data.gamma_values))
        self.numberOfAlphaSpin.setValue(len(self.data.alpha_values))
        self.numberofTightnessSpin.setValue(len(self.data.tightness_factors))
        
        self.update_tables()

        for i in range(self.numberOfGammaSpin.value()):
            new_item = QTableWidgetItem()
            new_item.setText(str(self.data.gamma_values[i]))
            self.gammaTable.setItem(0, i, new_item)

        for i in range(self.numberOfAlphaSpin.value()):
            new_item = QTableWidgetItem()
            new_item.setText(str(self.data.alpha_values[i]))
            self.alphaTable.setItem(0, i, new_item)

        for i in range(self.numberofTightnessSpin.value()):
            new_item = QTableWidgetItem()
            new_item.setText(str(self.data.tightness_factors[i]))
            self.tightnessFactorTable.setItem(0, i, new_item)
