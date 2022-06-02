import Distances
import Packages
import Addresses
from HashTable import HashTable
import datetime

packages_table = HashTable()
address_list = []
distance_list = []

truck_one = []
truck_two = []
truck_three = []

first_truck_leaves = datetime.datetime.strptime('8:00:00', '%H:%M:%S').time()
second_truck_leaves = datetime.datetime.strptime('9:10:00', '%H:%M:%S').time()
third_truck_leaves = datetime.datetime.strptime('11:00:00', '%H:%M:%S').time()

total_mileage_truck_one = 0
total_mileage_truck_two = 0
total_mileage_truck_three = 0

Packages.load_package_data('./data/packages.csv', packages_table)
Distances.load_distances_data('./data/distances.csv', distance_list)
Addresses.load_address_data('./data/addresses.csv', address_list)


def get_truck_load_lists():
    for i in range(40):
        selectedPackage = packages_table.lookup(i + 1)

        if 'Can only be on truck 2' in selectedPackage.special_notes or 'Delayed on flight' in selectedPackage.special_notes:
            truck_two.append(selectedPackage.package_id)
            selectedPackage.loaded = True
            continue
        elif 'Must be delivered with' in selectedPackage.special_notes or '9:00 AM' in selectedPackage.delivery_deadline:
            truck_one.append(selectedPackage.package_id)
            selectedPackage.loaded = True
            continue

    first_package_truck_one = packages_table.lookup(truck_one[0])
    nearest_list_truck_one = get_nearest_neighbors(first_package_truck_one.address)

    for package in nearest_list_truck_one:
        selectedPackage = packages_table.lookup(package[0])
        if selectedPackage.loaded:
            continue
        else:
            while len(truck_one) < 16:
                truck_one.append(selectedPackage.package_id)
                selectedPackage.loaded = True
                break

    first_package_truck_two = packages_table.lookup(truck_two[0])
    nearest_list_truck_two = get_nearest_neighbors(first_package_truck_two.address)

    for package in nearest_list_truck_two:
        selectedPackage = packages_table.lookup(package[0])
        if selectedPackage.loaded:
            continue
        else:
            while len(truck_two) < 16:
                truck_two.append(selectedPackage.package_id)
                selectedPackage.loaded = True
                break

    for i in range(40):
        selectedPackage = packages_table.lookup(i + 1)
        if selectedPackage.loaded:
            continue
        else:
            truck_three.append(selectedPackage.package_id)


def distance_lookup(address_1, address_2):
    address_1_index = Addresses.address_lookup(address_1, address_list)
    address_2_index = Addresses.address_lookup(address_2, address_list)
    if address_2_index > address_1_index:
        temp_index = address_1_index
        address_1_index = address_2_index
        address_2_index = temp_index
    return float(distance_list[address_1_index][address_2_index])


def minimum_distance_from_address_truck(address, truck_list):
    min_distance = 0
    if not len(truck_list) == 0:
        for package in truck_list:
            selectedPackage = packages_table.lookup(package)
            calculated_distance = distance_lookup(address, selectedPackage.address)
            if min_distance == 0:
                min_distance = calculated_distance
            elif calculated_distance < min_distance:
                min_distance = calculated_distance

    return min_distance


def minimum_distance_from_address(address):
    min_distance = 0
    selected_id = 0
    for entry in address_list:
        calculated_distance = distance_lookup(address, entry[2])
        if min_distance == 0:
            min_distance = calculated_distance
        elif calculated_distance < min_distance:
            min_distance = calculated_distance
            selected_id = entry[0]

    return [min_distance, selected_id]


def get_nearest_neighbors(address):
    distances = list()
    for i in range(40):
        selectedPackage = packages_table.lookup(i + 1)
        if address == selectedPackage.address:
            continue
        else:
            distance = distance_lookup(address, selectedPackage.address)
            distances.append((selectedPackage.package_id, distance))
    distances.sort(key=sort_function)
    return distances


def get_nearest_undelivered_package(address, truck_list):
    distances = list()
    for package_id in truck_list:
        selectedPackage = packages_table.lookup(package_id)
        if address == selectedPackage.address or selectedPackage.delivered == True:
            continue
        else:
            distance = distance_lookup(address, selectedPackage.address)
            distances.append([selectedPackage.package_id, distance])
    distances.sort(key=sort_function)
    if len(distances) == 0:
        return None
    else:
        return distances[0][0]


def sort_function(item):
    return item[1]


def deliver_package(package_id, mileage_count):
    selectedPackage = packages_table.lookup(package_id)
    selectedPackage.time_of_delivery = get_delivery_time(selectedPackage.time_left_hub, mileage_count)
    selectedPackage.delivered = True


def leave_hub(truck_list, truck_leave_time):
    for package_id in truck_list:
        selectedPackage = packages_table.lookup(package_id)
        selectedPackage.time_left_hub = truck_leave_time


def get_delivery_time(time_left_hub, distance_from_hub):
    time_taken = distance_from_hub / 18
    datetime_delivered = datetime.datetime.combine(datetime.date.today(), time_left_hub) + datetime.timedelta(
        hours=time_taken)
    return datetime_delivered.time()


def deliver_packages(truck_list, truck_leave_time):
    leave_hub(truck_list, truck_leave_time)
    first_package_id = int(get_nearest_undelivered_package(address_list[0][2], truck_list))
    current_package = packages_table.lookup(first_package_id)
    mileage_counter = 0
    first_package_miles = distance_lookup(address_list[0][2], current_package.address)
    mileage_counter += first_package_miles

    while len(truck_list) > 1:
        deliver_package(current_package.package_id, mileage_counter)
        truck_list.remove(current_package.package_id)

        if get_nearest_undelivered_package(current_package.address, truck_list) is None and len(truck_list) > 0:
            nearest_neighbor = truck_list[0]

        else:
            nearest_neighbor = get_nearest_undelivered_package(current_package.address, truck_list)
        next_package = packages_table.lookup(nearest_neighbor)
        miles_to_add = distance_lookup(current_package.address, next_package.address)
        mileage_counter += miles_to_add
        current_package = next_package

    if len(truck_list) == 1:
        deliver_package(truck_list[0], mileage_counter)
        truck_list.remove(truck_list[0])

    return mileage_counter


get_truck_load_lists()
print(truck_one)
print(truck_two)
print(truck_three)
print(deliver_packages(truck_one, first_truck_leaves))
print(deliver_packages(truck_two, second_truck_leaves))
print(deliver_packages(truck_three, third_truck_leaves))
