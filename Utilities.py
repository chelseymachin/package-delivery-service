import datetime


# takes in time left hub and the distance from hub to return the datetime
# object of the time the package would be delivered
# runtime complexity is O(1)
def get_delivery_time(time_left_hub, distance_from_hub):
    time_taken = distance_from_hub / 18
    datetime_delivered = datetime.datetime.combine(datetime.date.today(), time_left_hub) + datetime.timedelta(
        hours=time_taken)
    return datetime_delivered.time()


# takes in the item and just returns the first in the list
# sort function as utility for list sorting for distances
# runtime complexity is O(1)
def sort_function(item):
    return item[1]


# takes in a string and transforms it to a correctly formatted datetime
# object
# runtime complexity is O(1)
def time_transformer(string):
    time_string_formatted = string + ':00'
    return datetime.datetime.strptime(time_string_formatted, '%H:%M:%S').time()
