#!/usr/bin/python
import numpy as np
from energy import get_energy
from force import get_forces, move_vertices
from transition import T1_transition


def steepest_descent(vertices, edges, polys, parameters):

	epsilon = 10**-6
	delta_t = parameters['delta_t']
	t = 0.

	count = 0
	forces = 10**6
	while np.sum(forces**2)**(0.5) > epsilon:

		# get energy for network
		energy = get_energy(vertices, polys, edges, parameters)
		# print energy		
		
		# get forces for network
		forces = get_forces(vertices, polys, edges, parameters)
		print np.sum(forces**2)**(0.5)

	
		# move vertices
		vertices = move_vertices(vertices, forces, parameters)

		# check for T1 transitions
		cells, edges = T1_transition(vertices, polys, edges, parameters)

		# add routine to write vertices, energy, forces at every time step
		# can be used for plotting routines later...
	
		t += delta_t


	return 

































# def steepest_descent(network, vertices, cells, edges, delta_t, epsilon, folder):

# 	# keep track of time steps
# 	time = []
# 	t = 0

# 	# keep track of energy
# 	energy = []

# 	# for T1 transition
# 	min_dist = 0.2

# 	L = network.L

# 	# while forces are greater than epsilon
# 	forces = epsilon**0.5
# 	count = 0

# 	# generate random angle vectors
# 	for cell in cells:
# 		cell.theta = rand_angle()
	

# 	os.mkdir("noise/hex/%s" % folder)
# 	# f = open("energy/energy.txt", "w+")

# 	while count < 50:
# 	# while np.sum(forces**2)**(0.5) > epsilon:

# 		# plot_network(vertices, cells, L, "motility/%d.jpg" % count)

# 		# if count % 200 == 0:
# 		# 	for cell in cells:
# 		# 		cell.theta = rand_angle()

# 		# # write cell vertices for MSD

# 		os.chdir("noise/hex/%s" % folder)
# 		np.savetxt("%d.txt" % count, vertices)
# 		os.chdir("..")
# 		os.chdir("..")
# 		os.chdir("..")

# 		# get energy for network
# 		energy = network.get_energy(vertices, cells, edges)

# 		# get forces for network
# 		forces = network.get_forces(vertices, cells, edges)
	
# 		# move vertices with forces
# 		vertices = network.move_vertices(forces, vertices)


# 		ka = network.parameters['ka']
# 		A0 = 1.
# 		print t, energy / (24.*ka*(A0**2)), np.sum(forces**2)**(0.5)
# 		# norm_energy = np.array(energy / (24.*ka*(A0**2)))
# 		# f.write("%f\n" % norm_energy)


# 		# new time step
# 		t += delta_t

# 		# # check for T1 transitions
# 		cells, edges = T1_transition(network, vertices, cells, edges, min_dist)
# 		count += 1

# 	# f.close()
# 	return vertices