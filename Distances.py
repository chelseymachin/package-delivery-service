import csv
from Addresses import address_lookup


def distance_lookup(address_1, address_2):
    address_1_index = address_lookup(address_1)
    address_2_index = address_lookup(address_2)
    if address_2_index > address_1_index:
        temp_index = address_1_index
        address_1_index = address_2_index
        address_2_index = temp_index
    return float(distance_list[address_1_index][address_2_index])


def load_distances_data(file):
    with open(file) as distances_file:
        distances_data = csv.reader(distances_file, delimiter=',')

        for distance in distances_data:
            distance_list.append(distance)


distance_list = []
