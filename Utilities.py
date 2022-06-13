import datetime


def get_delivery_time(time_left_hub, distance_from_hub):
    time_taken = distance_from_hub / 18
    datetime_delivered = datetime.datetime.combine(datetime.date.today(), time_left_hub) + datetime.timedelta(
        hours=time_taken)
    return datetime_delivered.time()


def sort_function(item):
    return item[1]


def time_transformer(string):
    time_string_formatted = string + ':00'
    return datetime.datetime.strptime(time_string_formatted, '%H:%M:%S').time()
