import numpy as np
import Route_Finding_Algorithm

# Getting inputs

n = int(input("Enter number of cities: "))
e = np.array(input("Enter distance between cities: ").split(), float)
e = e.reshape(n, n)

k = int(input("Enter number of electric vehicles: "))

# s_node-source node   d_node-destination node   b-battery charge status initially
# c-charging rate   d-discharging rate   m-maximum battery capacity   s-average travelling speed

s_node = np.array(input("Enter source node: ").split(), int)
d_node = np.array(input("Enter destination node: ").split(), int)

initial_battery = np.array(input("Enter initial battery charge status: ").split(), float)
# unit: kW hr
charging = np.array(input("Enter charging rate: ").split(), float)
# unit: kW
discharging = np.array(input("Enter discharging rate: ").split(), float)
# unit: kW
maximum_battery = np.array(input("Enter maximum battery capacity: ").split(), float)
# unit: kW hr
speed = np.array(input("Enter average travelling speed: ").split(), float)
# unit: km/hr

# Applying Route_Finding_Algorithm

time = Route_Finding_Algorithm.find_route(n, e, k, s_node, d_node, initial_battery, charging, discharging, maximum_battery, speed)
print(time)
