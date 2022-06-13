import csv
from HashTable import HashTable
from Distances import distance_lookup
import Utilities


class Package:
    def __init__(self, package_id, address, city, state, zip, delivery_deadline, mass, special_notes):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.delivery_deadline = delivery_deadline
        self.mass = mass
        self.special_notes = special_notes
        self.time_of_delivery = ''
        self.time_left_hub = ''
        self.delivered = False
        self.loaded = False

    def __str__(self):
        return f"{self.package_id}, {self.address}, {self.city}, {self.state}, {self.zip}, {self.delivery_deadline}, {self.mass}, {self.special_notes}, Time of Delivery: {self.time_of_delivery}, Time Left Hub: {self.time_left_hub}, Delivered: {self.delivered}, Loaded: {self.loaded}"


def load_package_data(file):
    with open(file) as packages_file:
        package_data = csv.reader(packages_file, delimiter=',')

        for package in package_data:
            package_id = int(package[0])
            address = package[1]
            city = package[2]
            state = package[3]
            zip = package[4]
            delivery_deadline = package[5]
            mass = package[6]
            special_notes = package[7]

            package = Package(package_id, address, city, state, zip, delivery_deadline, mass, special_notes)
            packages_table.insert(package_id, package)


def get_nearest_undelivered_package(address, truck_list):
    distances = list()
    for package_id in truck_list:
        selectedPackage = packages_table.lookup(package_id)
        if address == selectedPackage.address or selectedPackage.delivered:
            continue
        else:
            distance = distance_lookup(address, selectedPackage.address)
            distances.append([selectedPackage.package_id, distance])
    distances.sort(key=Utilities.sort_function)
    if len(distances) == 0:
        return None
    else:
        return distances[0][0]


def deliver_package(package_id, mileage_count):
    selectedPackage = packages_table.lookup(package_id)
    selectedPackage.time_of_delivery = Utilities.get_delivery_time(selectedPackage.time_left_hub, mileage_count)
    selectedPackage.delivered = True


packages_table = HashTable()