import csv


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


def load_package_data(file, hashtable):
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
            hashtable.insert(package_id, package)




