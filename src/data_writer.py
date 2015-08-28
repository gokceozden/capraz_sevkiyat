__author__ = 'mustafa'

from data_store import DataStore
from jinja2 import Template

def gams_writer(file_name, data = DataStore()):
    f = open('gams_template.txt')
    src = Template(f.read())
    d = {'number_of_inbound': data.number_of_inbound_trucks,
         'number_of_outbound': data.number_of_outbound_trucks,
         'number_of_compound': data.number_of_compound_trucks,
         'number_of_receiving_doors': data.number_of_receiving_doors,
         'number_of_shipping_doors': data.number_of_shipping_doors}
    result = src.render(d)
    s = open(file_name, 'w')
    s.write(result)
    s.close()

