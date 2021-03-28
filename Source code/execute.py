# Getting inputs

n = int(input("Enter number of cities(a positive integer): "))
e = input("Enter distance between cities(a 2D list with single space as a separator): ")

k = int(input("Enter number of electric vehicles: "))

# s_node-source node   d_node-destination node   b-battery charge status initially
# c-charging rate   d-discharging rate   m-maximum battery capacity   s-average travelling speed

s_node = input("Enter source node: ")
d_node = input("Enter destination node: ")
b = input("Enter initial battery charge status: ")
c = input("Enter charging rate: ")
d = input("Enter discharging rate: ")
m = input("Enter maximum battery capacity: ")
s = input("Enter average travelling speed: ")

# Applying optimal algorithm

optimal(n, e, k, s_node, d_node, b, c, d, m, s)



