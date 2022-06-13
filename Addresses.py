import csv


def load_address_data(file):
    with open(file, mode='r') as address_file:
        address_data = csv.reader(address_file, delimiter=',')

        for address in address_data:
            address_list.append(address)


def address_lookup(address_string):
    for i in range(len(address_list)):
        if address_list[i][2] == address_string:
            return i


address_list = []
