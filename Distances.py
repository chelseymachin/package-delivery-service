import csv


def load_distances_data(file, distance_list):
    with open(file) as distances_file:
        distances_data = csv.reader(distances_file, delimiter=',')

        for distance in distances_data:
            distance_list.append(distance)
