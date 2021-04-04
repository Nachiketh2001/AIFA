import numpy as np
import Optimize

def calculate_distance(heuristic, row, col):
    n = heuristic.shape[0]
    node_tested = {}
    node_sum = {}

    i1 = 0
    while i1 < n:

        min_value = None
        min_index = None
        i2 = 0
        while i2 < n:
            if min_value is None and node_tested.get(i2) is None:
                min_value = heuristic[i2][col]
                min_index = i2
                break
            i2 = i2 + 1

        i2 = 0
        while i2 < n:
            if heuristic[i2][col] < min_value and not heuristic[i2][col] == 0 and node_tested.get(i2) is None:
                min_value = heuristic[i2][col]
                min_index = i2
            i2 = i2 + 1

        if not heuristic[row][min_index] == 0:
            node_tested[min_index] = True
            node_sum[min_index] = [min_value + heuristic[row][min_index]]
        else:
            node_tested[min_index] = False
        i1 = i1 + 1

    min_value = node_sum.get(0)
    min_index = 0

    i1 = 0
    while i1 < n:
        if min_value is None and node_sum.get(i1) is not None:
            min_value = node_sum.get(i1)
            min_index = i1
            break
        i1 = i1 + 1

    i1 = 0
    while i1 < n:
        if node_sum.get(i1) is not None:
            if node_sum.get(i1) < min_value:
                min_value = node_sum.get(i1)
                min_index = i1
        i1 = i1 + 1

    return min_value, min_index


def calculate_heuristic(n, e):
    heuristic = np.zeros((n, n))
    # Every row of a heuristic matrix describes the closest route distance from node i(row number) to all other nodes

    intermediate_node = []
    column = []

    for i1 in range(0, n):
        column.append(None)

    for i2 in range(0, n):
        intermediate_node.append(column)
    # Lists the intermediate nodes through which a vehicle passes while travelling from source node to destination node

    i1 = 0
    while i1 < n:
        i2 = 0
        while i2 < n:
            if e[i1][i2] != 0:
                heuristic[i1][i2] = e[i1][i2]
            i2 = i2 + 1
        i1 = i1 + 1

    i1 = 0
    while i1 < n:
        i2 = 0
        while i2 < n:
            if heuristic[i1][i2] == 0 and not i1 == i2:
                min_value, min_index = calculate_distance(heuristic, i1, i2)
                heuristic[i1][i2] = min_value
                intermediate_node[i1][i2] = min_index
            i2 = i2 + 1
        i1 = i1 + 1

    return heuristic, intermediate_node


def find_route(n, e, k, s_node, d_node, initial_battery, charging, discharging, maximum_battery, speed):

    heuristic, intermediate_node = calculate_heuristic(n, e)
    print(heuristic)

    time = np.zeros(k)
    battery_level = {}  # battery_level is defined to store the battery_level of all vehicle at any time
    required_charge = {}  # required charge stores what charge is required by a vehicle in it's complete travel
    required_time_start = {}
    required_time_middle = {}
    begin_time_middle = {}

    i1 = 0
    while i1 < k:
        required_charge[i1] = heuristic[s_node[i1]][d_node[i1]] / discharging[i1]
        battery_level[i1] = initial_battery[i1]
        middle_node = intermediate_node[s_node[i1]][d_node[i1]]

        if required_charge[i1] < maximum_battery[i1]:

            if maximum_battery[i1] == battery_level[i1]:
                required_time_start[i1] = 0
                required_time_middle[i1] = 0
                begin_time_middle[i1] = 0
                time[i1] = heuristic[s_node[i1]][d_node[i1]] / speed[i1]

            elif maximum_battery[i1] > battery_level[i1]:
                starting_time = (required_charge[i1] - battery_level[i1]) / charging[s_node[i1]]

                required_time_start[i1] = starting_time
                required_time_middle[i1] = 0
                begin_time_middle[i1] = 0
                time[i1] = heuristic[s_node[i1]][d_node[i1]] / speed[i1] + starting_time

        elif required_charge[i1] > maximum_battery[i1]:

            if maximum_battery[i1] == battery_level[i1] and middle_node is not None:
                battery_level[i1] -= heuristic[s_node[i1]][middle_node] / discharging[i1]
                required_charge[i1] -= heuristic[s_node[i1]][middle_node] / discharging[i1]
                initial_time = heuristic[s_node[i1]][middle_node] / speed[i1]
                final_time = initial_time+(required_charge[i1] - battery_level[i1]) / charging[middle_node]

                required_time_start[i1] = 0
                required_time_middle[i1] = final_time - initial_time
                begin_time_middle[i1] = initial_time
                time[i1] = heuristic[s_node[i1]][d_node[i1]] / speed[i1] + final_time - initial_time

            # When the maximum battery is lesser than required charge and there is no middle node, journey is impossible
            elif maximum_battery[i1] == battery_level[i1] and middle_node is None:
                time[i1] = None

            elif maximum_battery[i1] > battery_level[i1] and middle_node is None:
                time[i1] = None

            elif maximum_battery[i1] > battery_level[i1] and middle_node is not None:

                starting_time = (maximum_battery[i1] - battery_level[i1]) / charging[s_node[i1]]
                battery_level[i1] -= heuristic[s_node[i1]][middle_node] / discharging[i1]
                required_charge[i1] -= heuristic[s_node[i1]][middle_node] / discharging[i1]
                initial_time = heuristic[s_node[i1]][middle_node] / speed[i1] + starting_time
                final_time = initial_time + (required_charge[i1] - battery_level[i1]) / charging[middle_node]

                required_time_start[i1] = starting_time
                required_time_middle[i1] = final_time - initial_time
                begin_time_middle[i1] = initial_time
                time[i1] = heuristic[s_node[i1]][d_node[i1]] / speed[i1] + starting_time + final_time - initial_time

        i1 = i1 + 1

    station_node = []  # station_node lists all the vehicles starting from or passing through a particular node

    for i1 in range(0, n):
        node_at_start = []
        node_at_middle = []
        for i2 in range(0, k):
            if s_node[i2] == i1:
                node_at_start = node_at_start + [i2]
        for i3 in range(0, n):
            if intermediate_node[i1][i3] is not None:
                for i4 in range(0, k):
                    if i1 == s_node[i4] and i3 == d_node[i4]:
                        node_at_middle = node_at_middle + [i4]
        if len(node_at_start) == 0:
            node_at_start = None
        if len(node_at_middle) == 0:
            node_at_middle = None
        station_node = station_node + [[node_at_start, node_at_middle]]

    time = Optimize.optimize(n, time, required_time_start, required_time_middle, begin_time_middle, station_node)

    return time
