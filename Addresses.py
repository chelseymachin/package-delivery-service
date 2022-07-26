import csv


# function that allows loading of address data from a designated csv file
# data from the CSV import is input into a 2D array
# runtime complexity is O(n)
def load_address_data(file):
    with open(file, mode='r') as address_file:
        address_data = csv.reader(address_file, delimiter=',')

        for address in address_data:
            address_list.append(address)


# function that allows for input of an address in string format
# then iterates through each item in the address_list data
# to determine a matching address string
# returns the index number of the address in the list
# runtime complexity is O(n)
def address_lookup(address_string):
    for i in range(len(address_list)):
        if address_list[i][2] == address_string:
            return i


# array data structure of addresses to store and export
# space complexity is O(1) as it's linear
address_list = []
