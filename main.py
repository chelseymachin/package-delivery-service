# Written by Chelsey Machin, WGU Student ID: 001221846
# For C950: Data Structures & Algorithms II

import Distances
import Packages
import Addresses
import datetime
from tabulate import tabulate
import Utilities

# empty lists where packages will be loaded eventually
truck_one = []
truck_two = []
truck_three = []

# to keep track of total accrued travel mileage
totalMileage = 0

# to keep track of individual trucks' mileage
truck_one_mileage = 0
truck_two_mileage = 0
truck_three_mileage = 0

# pre-formatted leave times for delivery trucks
first_truck_leaves = datetime.datetime.strptime('8:00:00', '%H:%M:%S').time()
second_truck_leaves = datetime.datetime.strptime('9:10:00', '%H:%M:%S').time()
third_truck_leaves = datetime.datetime.strptime('11:00:00', '%H:%M:%S').time()

# loading all package data from CSVs in data directory
Packages.load_package_data('./data/packages.csv')
Distances.load_distances_data('./data/distances.csv')
Addresses.load_address_data('./data/addresses.csv')


# this function is a greedy algorithm that iterates through
# all packages in the hash table and prioritizes based on a few factors:
# complexity of O(n)
def get_truck_load_lists():
    for i in range(40):
        selectedPackage = Packages.packages_table.lookup(i + 1)

        # 1. If the package has any special notes, those are used to determine
        # the best fitting truck.  The package is then appended to the truck and
        # the package's loaded status becomes true

        if 'Can only be on truck 2' in selectedPackage.special_notes or 'Delayed on flight' in selectedPackage.special_notes:
            truck_two.append(selectedPackage.package_id)
            selectedPackage.loaded = True
            continue
        elif 'Must be delivered with' in selectedPackage.special_notes or '9:00 AM' in selectedPackage.delivery_deadline:
            truck_one.append(selectedPackage.package_id)
            selectedPackage.loaded = True
            continue

    # 2. The first package on the first truck is looked up and the
    # get_nearest_neighbors function generates a list of nearest packages
    # based on address.  If the package is already "loaded", the next
    # package is visited. The unloaded packages from this list are
    # added in until the truck length reaches 16.

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

    # 3. The first package on the second truck is handled in the same
    # way as the first!

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

    # 4. Finally, each package is iterated through again to see if
    # there's any outliers that are still not loaded, these are then
    # loaded onto truck 3

    for i in range(40):
        selectedPackage = Packages.packages_table.lookup(i + 1)
        if selectedPackage.loaded:
            continue
        else:
            truck_three.append(selectedPackage.package_id)
            selectedPackage.loaded = True


# iterates through all packages in table, getting a list of distances
# from each package in the table to the input address, then the list is
# sorted using the utilities sort_function as a key to return the first
# package ID in the list (the nearest neighbor package)
# complexity of O(n)
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


# looks up status of all packages at the input time
# iterates through all packages in table, compares input time to
# time of delivery and time package was loaded to create an output table
# of the status of all 40 packages at that time
# complexity of O(n)
def package_status_lookup_by_time(input_time):
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


# looks up status of single package by input id
# iterates through all packages in table, if the input ID matches one,
# it gets pulled and the final status data for it is output as tabulated data
# complexity of O(n)
def package_status_lookup_by_id(input_id):
    package_lookup_results = []
    for i in range(40):
        selectedPackage = Packages.packages_table.lookup(i + 1)
        if input_id == selectedPackage.package_id:
            package_lookup_results.append([
                f"{selectedPackage.package_id}",
                f"{selectedPackage.address}",
                f"{selectedPackage.time_left_hub}",
                f"{selectedPackage.time_of_delivery}"
            ])
    print(tabulate(package_lookup_results, headers=[
        "Package ID",
        "Address",
        "Time Left Hub",
        "Time of Delivery"
    ]))


# function that designates truck delivery start
# truck list and leave time are input
# all the packages in the truck have their loaded status set to True
# all the packages in the truck have the input leave time set as their
# time_left_hub data
# complexity of O(n)

def leave_hub(truck_list, truck_leave_time):
    for package_id in truck_list:
        selectedPackage = Packages.packages_table.lookup(package_id)
        selectedPackage.loaded = True
        selectedPackage.time_left_hub = truck_leave_time


# function that delivers all packages in an input truck list
# uses leave_hub to update status on all packages in list
# first package to be delivered is determined by using
# get_nearest_undelivered_package, which returns the closest package
# to the hub from the truck_list; this package is set as the current_package
# its distance from the hub is added to the mileage counter
# complexity of O(n)

def deliver_packages(truck_list, truck_leave_time):
    leave_hub(truck_list, truck_leave_time)
    first_package_id = int(Packages.get_nearest_undelivered_package(Addresses.address_list[0][2], truck_list))
    current_package = Packages.packages_table.lookup(first_package_id)
    mileage_counter = 0
    first_package_miles = Distances.distance_lookup(Addresses.address_list[0][2], current_package.address)
    mileage_counter += first_package_miles

    # The delivered package is removed from list and the same sequence as
    # above continues as long as truck list has more than 1 package in
    # it. If there's no nearest neighbor packages left, but the truck still
    # has undelivered packages, the nearest_neighbor is just set to the first
    # remaining package in truck

    while len(truck_list) > 1:
        Packages.deliver_package(current_package.package_id, mileage_counter)
        truck_list.remove(current_package.package_id)

        if Packages.get_nearest_undelivered_package(current_package.address, truck_list) is None and len(
                truck_list) > 0:
            nearest_neighbor = truck_list[0]

        else:
            nearest_neighbor = Packages.get_nearest_undelivered_package(current_package.address, truck_list)
        next_package = Packages.packages_table.lookup(nearest_neighbor)
        miles_to_add = Distances.distance_lookup(current_package.address, next_package.address)
        mileage_counter += miles_to_add
        current_package = next_package

    # once length is just one package left in truck, that package is
    # delivered and removed from list
    if len(truck_list) == 1:
        Packages.deliver_package(truck_list[0], mileage_counter)
        truck_list.remove(truck_list[0])

    # final mileage count for truck is returned
    return mileage_counter


# load trucks
get_truck_load_lists()
# add mileage from first truck to total Mileage
truck_one_mileage = deliver_packages(truck_one, first_truck_leaves)
totalMileage += truck_one_mileage
print(f"Truck one mileage is: {truck_one_mileage}")
# add mileage from second truck to total Mileage
truck_two_mileage = deliver_packages(truck_two, second_truck_leaves)
totalMileage += truck_two_mileage
print(f"Truck two mileage is: {truck_two_mileage}")
# add mileage from third truck to total Mileage
truck_three_mileage = deliver_packages(truck_three, third_truck_leaves)
totalMileage += truck_three_mileage
print(f"Truck three mileage is: {truck_three_mileage}")

# confirmation of all packages delivered under mileage
print(f"All packages delivered with a total mileage of: {totalMileage}")

selection = 0
# user input screen loop
# user can enter 1 to enter a time to see all package statuses then
# user can enter 2 to enter an ID and see an individual packages final
# data
while selection != 3:
    print("Welcome to the delivery service package lookup system! \n"
          "You can make a choice from the options below. \n"
          "1 --> Get package updates by time \n "
          "2 --> Get package update by ID \n "
          "3 --> Quit \n"
          )
    selection = int(input("Enter a number from above: "))
    if selection == 1:
        selected_time = Utilities.time_transformer(
            input("Please enter a time in the format "
                  "HH:MM (24 hour): "))
        package_status_lookup_by_time(selected_time)
        continue
    elif selection == 2:
        selected_id = int(input("Please enter a package ID number: "))
        package_status_lookup_by_id(selected_id)
        continue

print("Goodbye!")
