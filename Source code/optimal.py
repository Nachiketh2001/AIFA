import numpy as np


def calculate_distance(n, e, k, s_node, d_node):

    relation = []
    i1 = 0
    while(i1<n):
        relation_temp = []
        i2 = 0
        while(i2<n):
            if e[i1][i2]!=0:
                relation_temp = relation_temp + [i2]
            i2 = i2 + 1
        relation = relation + relation_temp
        i1 = i1 + 1
    i2 = 0
    i1 = 0


    return 0


def calculate_time(time, n, e, k, s_node, d_node, speed):


    return 0


def optimal(n, e, k, s_node, d_node, b, c, d, m, s):

    e = np.array(e, float)
    s_node = np.array(s_node, int)
    d_node = np.array(d_node, int)
    initial_battery = np.array(b, float)
    charging = np.array(c, float)
    discharging = np.array(d, float)
    maximum_battery = np.array(m, float)
    speed = np.array(s, float)

    distance = calculate_distance(n, e, k, s_node, d_node)
    time = calculate_time(time, n, e, k, s_node, d_node, speed)


    return 0