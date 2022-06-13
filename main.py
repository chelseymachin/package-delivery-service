import Distances
import Packages
import Addresses
import datetime
from tabulate import tabulate
import Utilities

truck_one = []
truck_two = []
truck_three = []

first_truck_leaves = datetime.datetime.strptime('8:00:00', '%H:%M:%S').time()
second_truck_leaves = datetime.datetime.strptime('9:10:00', '%H:%M:%S').time()
third_truck_leaves = datetime.datetime.strptime('11:00:00', '%H:%M:%S').time()

Packages.load_package_data('./data/packages.csv')
Distances.load_distances_data('./data/distances.csv')
Addresses.load_address_data('./data/addresses.csv')


def get_truck_load_lists():
    for i in range(40):
        selectedPackage = Packages.packages_table.lookup(i + 1)

        if 'Can only be on truck 2' in selectedPackage.special_notes or 'Delayed on flight' in selectedPackage.special_notes:
            truck_two.append(selectedPackage.package_id)
            selectedPackage.loaded = True
            continue
        elif 'Must be delivered with' in selectedPackage.special_notes or '9:00 AM' in selectedPackage.delivery_deadline:
            truck_one.append(selectedPackage.package_id)
            selectedPackage.loaded = True
            continue

    first_package_truck_one = Packages.packages_table.lookup(truck_one[0])
    nearest_list_truck_one = get_nearest_neighbors(first_package_truck_one.address)

    for package in nearest_list_truck_one:
        selectedPackage = Packages.packages_table.lookup(package[0])
        if selectedPackage.loaded:
            continue
        else:
            while len(truck_one) < 16:
                truck_one.append(selectedPackage.package_id)
                selectedPackage.loaded = True
                break

    first_package_truck_two = Packages.packages_table.lookup(truck_two[0])
    nearest_list_truck_two = get_nearest_neighbors(first_package_truck_two.address)

    for package in nearest_list_truck_two:
        selectedPackage = Packages.packages_table.lookup(package[0])
        if selectedPackage.loaded:
            continue
        else:
            while len(truck_two) < 16:
                truck_two.append(selectedPackage.package_id)
                selectedPackage.loaded = True
                break

    for i in range(40):
        selectedPackage = Packages.packages_table.lookup(i + 1)
        if selectedPackage.loaded:
            continue
        else:
            truck_three.append(selectedPackage.package_id)


def get_nearest_neighbors(address):
    distances = list()
    for i in range(40):
        selectedPackage = Packages.packages_table.lookup(i + 1)
        if address == selectedPackage.address:
            continue
        else:
            distance = Distances.distance_lookup(address, selectedPackage.address)
            distances.append((selectedPackage.package_id, distance))
    distances.sort(key=Utilities.sort_function)
    return distances


def package_status_lookup(input_time):
    package_lookup_results = []
    for i in range(40):
        selectedPackage = Packages.packages_table.lookup(i + 1)
        if input_time < selectedPackage.time_of_delivery and input_time < selectedPackage.time_left_hub:
            package_lookup_results.append([f"{selectedPackage.package_id}", "Hasn't left hub yet"])
        elif selectedPackage.time_of_delivery > input_time > selectedPackage.time_left_hub:
            package_lookup_results.append(
                [f"{selectedPackage.package_id}", f"Left hub at {selectedPackage.time_left_hub}, not yet delivered"])
        elif input_time > selectedPackage.time_of_delivery and input_time > selectedPackage.time_left_hub:
            package_lookup_results.append(
                [f"{selectedPackage.package_id}", f"Delivered at {selectedPackage.time_of_delivery}"])
    print(tabulate(package_lookup_results, headers=["Package ID", "Current Status"]))


def leave_hub(truck_list, truck_leave_time):
    for package_id in truck_list:
        selectedPackage = Packages.packages_table.lookup(package_id)
        selectedPackage.loaded = True
        selectedPackage.time_left_hub = truck_leave_time


def deliver_packages(truck_list, truck_leave_time):
    leave_hub(truck_list, truck_leave_time)
    first_package_id = int(Packages.get_nearest_undelivered_package(Addresses.address_list[0][2], truck_list))
    current_package = Packages.packages_table.lookup(first_package_id)
    mileage_counter = 0
    first_package_miles = Distances.distance_lookup(Addresses.address_list[0][2], current_package.address)
    mileage_counter += first_package_miles

    while len(truck_list) > 1:
        Packages.deliver_package(current_package.package_id, mileage_counter)
        truck_list.remove(current_package.package_id)

        if Packages.get_nearest_undelivered_package(current_package.address, truck_list) is None and len(truck_list) > 0:
            nearest_neighbor = truck_list[0]

        else:
            nearest_neighbor = Packages.get_nearest_undelivered_package(current_package.address, truck_list)
        next_package = Packages.packages_table.lookup(nearest_neighbor)
        miles_to_add = Distances.distance_lookup(current_package.address, next_package.address)
        mileage_counter += miles_to_add
        current_package = next_package

    if len(truck_list) == 1:
        Packages.deliver_package(truck_list[0], mileage_counter)
        truck_list.remove(truck_list[0])

    return mileage_counter


get_truck_load_lists()
print(deliver_packages(truck_one, first_truck_leaves))
print(deliver_packages(truck_two, second_truck_leaves))
print(deliver_packages(truck_three, third_truck_leaves))
selected_time = Utilities.time_transformer(
    input("Welcome to the delivery service package lookup system!  Please enter a time in the format "
          "HH:MM (24 hour): "))

package_status_lookup(selected_time)
