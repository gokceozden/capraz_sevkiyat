__author__ = 'mustafa'

from PySide.QtGui import *

class DoorInfo(QMessageBox):
      def __init__(self, door):
        QMessageBox.__init__(self)
        sequence_text = 'Sequence: '
        for sequence in door.sequence:
            sequence_text += str(sequence.truck_name) + '. '

        self.setText(sequence_text)