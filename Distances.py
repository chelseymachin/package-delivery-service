import csv
from Addresses import address_lookup


# function takes in two address strings
# and returns the distance between them based on both addresses
# position within the distance_list multidimensional array
# returns distance in miles as a float
# complexity of O(1)
def distance_lookup(address_1, address_2):
    address_1_index = address_lookup(address_1)
    address_2_index = address_lookup(address_2)
    if address_2_index > address_1_index:
        temp_index = address_1_index
        address_1_index = address_2_index
        address_2_index = temp_index
    return float(distance_list[address_1_index][address_2_index])


# function that allows loading of distance data from a designated csv file
# data from the CSV import is input into a 2D array
def load_distances_data(file):
    with open(file) as distances_file:
        distances_data = csv.reader(distances_file, delimiter=',')

        for distance in distances_data:
            distance_list.append(distance)


# array data structure of distances to store and export
distance_list = []
