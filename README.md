AI610005
Assignment-1
Route_Finding_Algorithm

The assignment is to solve an electric vehicle problem by finding the best posssible route to optimisethe time taken by the electric vehicles which are travelling across cities. I have approached the assignment by incorporating heuristic and optimal algorithm into a single file called Route_Finding_algorithm in the following way:

1) The heuristic matrix which gives the minimum distance between any two nodes is used to find the total time taken by a vehicle.
2) The minimum distance between any two nodes which are not directly connected is through an intermediate node which connects both of them and minimises the distances between them.
3) Any vehicle when not fully charged, only gets sufficient charge which is necessary for it to reach the destination node.
4) The output time is given None for all those vehicles which are incapable to hold sufficient charge to reach the nearest node, hence journey is impossible.

Please refer to the report file and source code in the main for more details on the algorithm.

Nachiketh B M
19ME30028
