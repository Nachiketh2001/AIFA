import numpy as np


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

    for j in range(0, n):
        column.append(None)

    for i in range(0, n):
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
    time = np.zeros(k)
    time_without_charge = np.zeros(k)
    print(heuristic)

    i1 = 0
    while i1 < k:
        time_without_charge[i1] = heuristic[s_node[i1]][d_node[i1]] / speed[i1]
        i1 = i1 + 1

    # A dictionary 'battery_level' is defined to store the battery_level at any time
    battery_level = {}
    # A dictionary required charge is defined to tell what charge is required by a vehicle in it's complete travel
    required_charge = {}
    # A dictionary 'station_busy_at' is defined to tell when will the next station be free
    station_busy_at = []
    for j in range(0, n):
        station_busy_at[j] = 0

    i1 = 0
    while i1 < k:
        required_charge[i1] = heuristic[s_node[i1]][d_node[i1]] / discharging[i1]
        battery_level[i1] = initial_battery[i1]
        middle_node = intermediate_node[s_node[i1]][d_node[i1]]

        if required_charge[i1] < battery_level[i1]:

            if maximum_battery[i1] == battery_level[i1]:
                time[i1] = heuristic[s_node[i1]][d_node[i1]] / speed[i1]

            elif maximum_battery[i1] > battery_level[i1]:
                starting_time = (required_charge[i1] - battery_level[i1]) / charging[s_node[i1]]
                station_busy_at[s_node[i1]] = station_busy_at[s_node[i1]] + [0, starting_time]
                time[i1] = heuristic[s_node[i1]][d_node[i1]] / speed[i1] + starting_time

        elif required_charge[i1] > maximum_battery[i1]:

            if maximum_battery[i1] == battery_level[i1] and middle_node is not None:
                battery_level[i1] -= heuristic[s_node[i1]][middle_node] / discharging[i1]
                required_charge[i1] -= heuristic[s_node[i1]][middle_node] / discharging[i1]

                initial_time = heuristic[s_node[i1]][middle_node] / speed[i1]
                final_time = initial_time+(required_charge[i1] - battery_level[i1]) / charging[middle_node]
                station_busy_at[middle_node] = station_busy_at[middle_node] + [initial_time, final_time]
                time[i1] = heuristic[s_node[i1]][d_node[i1]] / speed[i1] + final_time - initial_time

            # When the maximum battery is lesser than required charge and there is no middle node, journey is impossible
            elif maximum_battery[i1] == battery_level[i1] and middle_node is None:
                time[i1] = None

            elif maximum_battery[i1] > battery_level[i1] and middle_node is None:
                time[i1] = None

            elif maximum_battery[i1] > battery_level[i1] and middle_node is not None:

                starting_time = (maximum_battery[i1] - battery_level[i1]) / charging[s_node[i1]]
                station_busy_at[s_node[i1]] = station_busy_at[s_node[i1]] + [0, starting_time]

                battery_level[i1] -= heuristic[s_node[i1]][middle_node] / discharging[i1]
                required_charge[i1] -= heuristic[s_node[i1]][middle_node] / discharging[i1]

                initial_time = heuristic[s_node[i1]][middle_node] / speed[i1] + starting_time
                final_time = initial_time + (required_charge[i1] - battery_level[i1]) / charging[middle_node]
                station_busy_at[middle_node] = station_busy_at[middle_node] + [initial_time, final_time]
                time[i1] = heuristic[s_node[i1]][d_node[i1]] / speed[i1] + starting_time + final_time - initial_time

        i1 = i1 + 1

    print(time)
    return 0
