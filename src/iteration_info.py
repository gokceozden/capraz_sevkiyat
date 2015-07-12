__author__ = 'mustafa'

from PySide.QtGui import *

class IterationInfo(QMessageBox):
    def __init__(self, truck):
        QMessageBox.__init__(self)