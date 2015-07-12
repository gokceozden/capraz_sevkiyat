__author__ = 'mustafa'

from PySide.QtGui import *

class TruckInfo(QMessageBox):
    def __init__(self, truck):
        QMessageBox.__init__(self)
        self.setWindowTitle(truck.truck_name)
        name_text = "Truck Name: %s \n" %(truck.truck_name)
        state_text = "Truck State: %s\n" %(truck.state_list[truck.current_state])
        next_time = "Time for next state %d\n" %(truck.finish_time)


        if truck.truck_type ==  'inbound':
            door_name = 'Receive door %s\n' %(truck.receiving_door_name)
            good_text = ''
            for goods in truck.coming_goods:
                good_text += 'Type: %s, ' %str(goods.type)
                good_text += 'Amount: %d\n' % goods.amount

        if truck.truck_type ==  'outbound':
            door_name = 'Shippping door: %s\n' %(truck.shipping_door_name)
            good_text = ''
            for goods in truck.going_goods:
                good_text += 'Type: %s, ' %str(goods.type)
                good_text += 'Amount: %d\n' % goods.amount

        if truck.truck_type ==  'compound':
            door_name = 'Receive door %s\n' %(truck.receiving_door_name)
            door_name += 'Shippping door: %s\n' %(truck.shipping_door_name)
            good_text = 'coming goods:\n'
            for goods in truck.coming_goods:
                good_text += 'Type: %s, ' %str(goods.type)
                good_text += 'Amount: %d\n' % goods.amount
            good_text += 'leaving goods:\n'
            for goods in truck.going_goods:
                good_text += 'Type: %s, ' %str(goods.type)
                good_text += 'Amount: %d\n' % goods.amount



        self.setText(name_text + state_text + next_time + door_name + good_text)
