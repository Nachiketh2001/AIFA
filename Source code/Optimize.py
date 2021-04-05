import numpy as np
# This file minimises the total time taken by that vehicle which has the longest journey time

def check_time(time_occupied, t_initial, t_final):
    station_free_at = t_initial
    t = t_initial
    while t < t_final:
        if not time_occupied[t]:
            t = t + 1
        else:
            while True:
                if time_occupied[t]:
                    t = t + 1
                else:
                    break

            time_occupied, station_free_at = check_time(time_occupied, t, t + t_final - t_initial)
            return time_occupied, station_free_at
    else:
        t = t_initial
        while t < t_final:
            time_occupied[t] = True
            t = t + 1
        return time_occupied, station_free_at


def optimize(n, time, required_time_start, required_time_middle, begin_time_middle, station_node):

    i1 = 0
    while i1 < n:
        if station_node[i1][0] is not None and len(station_node[i1][0]) > 1:
            row = station_node[i1][0]

            priority_order = []
            max_priority_vehicle = 0
            vehicle_available = {}
            for i2 in row:
                vehicle_available[i2] = True

            i2 = 0
            while i2 < len(row):
                i3 = 0
                while i3 < len(row):
                    if vehicle_available.get(i3):
                        max_priority_vehicle = row[i3]
                        break
                    i3 = i3 + 1

                i3 = 0
                while i3 < len(row):
                    if vehicle_available.get(i3) and time[row[i3]] > time[max_priority_vehicle]:
                        max_priority_vehicle = row[i3]
                    i3 = i3 + 1

                vehicle_available[max_priority_vehicle] = False
                priority_order = priority_order + [max_priority_vehicle]
                i2 = i2 + 1

            add_time = 0
            for i2 in priority_order:
                time[i2] = time[i2] + add_time
                add_time = add_time + required_time_start[i2]

        if station_node[i1][1] is not None and len(station_node[i1][0]) > 1:
            row = station_node[i1][1]

            priority_order = []
            max_priority_vehicle = 0
            vehicle_available = {}
            for i2 in row:
                vehicle_available[i2] = True

            i2 = 0
            while i2 < len(row):
                i3 = 0
                while i3 < len(row):
                    if vehicle_available.get(row[i3]):
                        max_priority_vehicle = row[i3]
                        break
                    i3 = i3 + 1

                i3 = 0
                while i3 < len(row):
                    if vehicle_available.get(row[i3]) and time[row[i3]] > time[max_priority_vehicle]:
                        max_priority_vehicle = row[i3]
                    i3 = i3 + 1

                vehicle_available[max_priority_vehicle] = False
                priority_order = priority_order + [max_priority_vehicle]
                i2 = i2 + 1

            # Assuming energy given per unit time at any station is not greater than 10 times
            # of the energy lost per unit time during travelling(thinking practically)
            t = 0
            t_max = 10*3600*(time[priority_order[0]])
            time_occupied = np.zeros(t_max, dtype=int)
            while t < t_max:
                time_occupied[t] = False
                t = t + 1

            i2 = 0
            while i2 < len(row):
                t_initial = begin_time_middle[row[i2]]
                t_final = begin_time_middle[row[i2]] + required_time_middle[row[i2]]
                time_occupied, t_initial_new = check_time(time_occupied, t_initial, t_final)
                time[row[i2]] = time[row[i2]] + t_initial_new - t_initial
                i2 = i2 + 1
        i1 = i1 + 1
    return time
