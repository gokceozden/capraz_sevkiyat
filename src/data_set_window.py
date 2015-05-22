__author__ = 'robotes'

from PySide.QtGui import *

from src.solver import Solver

class DataSetWindow(QWidget):
    """
    Data set window widget
    """
    def __init__(self, model = Solver()):
        QWidget.__init__(self)
        self.model = model
        self.setWindowTitle('Data Set Window')
        
        self.setupComponents()

        self.setupButtons()
        self.setupComponents()
        self.setupConnections()
        self.setupLayout()

        self.loadData()


    def setupConnections(self):

        self.numberOfGammaSpin.valueChanged.connect(self.updateTables)
        self.numberOfAlphaSpin.valueChanged.connect(self.updateTables)

        
    def setupComponents(self):
        self.gammaTable = QTableWidget(1,1)
        self.alphaTable = QTableWidget(1,1)


    def setupButtons(self):
        self.loadingTimeLabel = QLabel("Loading Time")
        self.loadingTimeEdit = QLineEdit()

        self.changeoverTimeLabel = QLabel("Changeover Time")
        self.changeoverTimeEdit = QLineEdit()

        self.makespanFactorLabel = QLabel("Makespan Factor")
        self.makespanFactorEdit = QLineEdit()

        self.doneButton = QPushButton('Done')
        self.doneButton.clicked.connect(self.saveData)


        self.numberOfGammaLabel = QLabel("Number of gamma values")
        self.numberOfGammaSpin = QSpinBox()
        self.numberOfGammaSpin.setMinimum(1)

        self.numberOfAlphaLabel = QLabel("Number of alpha values")
        self.numberOfAlphaSpin = QSpinBox()
        self.numberOfAlphaSpin.setMinimum(1)
        
    def setupLayout(self):

        self.dataSetForm = QFormLayout()
        self.vTableLayout = QVBoxLayout()
        self.mainLayout = QHBoxLayout()
        
        self.dataSetForm.addRow(self.loadingTimeLabel, self.loadingTimeEdit)
        self.dataSetForm.addRow(self.changeoverTimeLabel, self.changeoverTimeEdit)
        self.dataSetForm.addRow(self.makespanFactorLabel, self.makespanFactorEdit)
        self.dataSetForm.addRow(self.numberOfGammaLabel, self.numberOfGammaSpin)
        self.dataSetForm.addRow(self.numberOfAlphaLabel, self.numberOfAlphaSpin)
        self.dataSetForm.addRow(self.doneButton)

        self.vTableLayout.addWidget(self.gammaTable)
        self.vTableLayout.addWidget(self.alphaTable)

        self.mainLayout.addLayout(self.dataSetForm)
        self.mainLayout.addLayout(self.vTableLayout)
        
        self.setLayout(self.mainLayout)
        

    def updateTables(self):

        self.gammaTable.setColumnCount(self.numberOfGammaSpin.value())
        self.alphaTable.setColumnCount(self.numberOfAlphaSpin.value())


        
        
    def saveData(self):

        self.model.changeover_time = float(self.changeoverTimeEdit.text())
        self.model.loading_time = float(self.loadingTimeEdit.text())
        self.model.makespan_factor = float(self.makespanFactorEdit.text())
        
        alpha = []
        gamma = []
        
        for value in range(self.numberOfAlphaSpin.value()):
            data = self.alphaTable.item(0,value)
            if data:
                alpha.append(float(data.text()))

        for value in range(self.numberOfGammaSpin.value()):
            data = self.gammaTable.item(0,value)
            if data:
                gamma.append(float(data.text()))

        self.model.alpha = alpha
        self.model.gamma = gamma



    def loadData(self):

        self.loadingTimeEdit.setText(str(self.model.loading_time))
        self.changeoverTimeEdit.setText(str(self.model.changeover_time))
        self.makespanFactorEdit.setText(str(self.model.makespan_factor))

        self.numberOfGammaSpin.setValue(len(self.model.gamma))
        self.numberOfAlphaSpin.setValue(len(self.model.alpha))

        self.updateTables()

        for i in range(self.numberOfGammaSpin.value()):
            new_item = QTableWidgetItem()
            new_item.setText(str(self.model.gamma[i]))
            self.gammaTable.setItem(0,i,new_item)

        for i in range(self.numberOfAlphaSpin.value()):
            new_item = QTableWidgetItem()
            new_item.setText(str(self.model.alpha[i]))
            self.alphaTable.setItem(0,i,new_item)

        