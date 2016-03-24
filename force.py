#!/usr/bin/python
import numpy as np
from geometry import *
from math import pi
import matplotlib.pyplot as plt

"""

force.py - computes forces in the current configuration
of the vertex model


author: Lexi Signoriello
date: 1/20/16

"""


def get_forces(vertices, polys, edges, parameters):
	# get necessary parameters 
	lx = parameters['lx']
	ly = parameters['ly']
	L = np.array([lx,ly])
	ka = parameters['ka']
	Lambda = parameters['Lambda']
	gamma = parameters['gamma']
	eta = parameters['eta']


	f1 = F_elasticity(vertices, polys, ka, L)
	f2 = F_adhesion(vertices, edges, Lambda, L)
	f3 = F_contraction(vertices, polys, gamma, L)
	f4 = F_motility(vertices, polys, eta)

	return -(f1 + f2 + f3 + f4)


def move_vertices(vertices, forces, parameters):
	delta_t = parameters['delta_t']
	lx = parameters['lx']
	ly = parameters['ly']

	vertices = vertices + delta_t * forces

	# wrap around periodic boundaries
	for i,(x,y) in enumerate(vertices):
		if x < 0:
			# wrap around to right
			vertices[i,0] = x + lx

		if x > lx:
			# wrap around to left
			vertices[i,0] = x - lx

		if y < 0:
			# wrap around to top
			vertices[i,1] = y + ly

		if y > ly:
			# wrap around to bottom
			vertices[i,1] = y - ly

		return vertices 



def get_clockwise(index, indices, vertices, L):
	
	# get position of vertex in list
	pos = [i for i,x in enumerate(indices) if x == index]
	pos = pos[0]

	# clockwise is position to right
	# wrap around to 0 if at end of the list
	if pos == len(indices) - 1:
		pos = 0
	else:
		pos += 1

	# compute vertex wrt periodic boundaries
	v0 = vertices[index]
	v = vertices[indices[pos]]
	vc = v0 + periodic_diff(v, v0, L)

	return vc 



def get_counter_clockwise(index, indices, vertices, L):
		
	# get position of vertex in list
	pos = [i for i,x in enumerate(indices) if x == index]
	pos = pos[0]
	
	# clockwise is position to left
	# wrap around to end of list if first value
	if pos == 0:
		pos = len(indices) - 1
	else:
		pos -= 1

	v0 = vertices[index]
	v = vertices[indices[pos]]
	vcc = v0 + periodic_diff(v, v0, L)

	return vcc


# Force on vertex due to elasticity
def F_elasticity(vertices, polys, ka,  L):
	n_vertices = len(vertices)

	# evert vertex has an associated force
	forces = np.zeros((n_vertices, 2))

	# iterate over vertices and get force
	for i,vertex in enumerate(vertices):

		# find polys with this vertex
		for poly in polys:

			# if this vertex is in current poly
			# compute force contributed from this poly
			if i in poly.indices:

				# get clockwise vector
				vc = get_clockwise(i, poly.indices, vertices, L)

				# get counter-clockwise vector
				vcc = get_counter_clockwise(i, poly.indices, vertices, L)

				# get the difference vector
				diff = vc - vcc

				# compute perpendicular vector
				# assure correct direction (pointing towards vertex)
				perp_matrix = np.zeros((2,2))
				perp_matrix[0,1] = 1.
				perp_matrix[1,0] = -1.

				f = -0.5 * np.dot(perp_matrix, diff)

				# force contributed from this poly stored in f
				coeff = ka * (poly.A0 - poly.get_area(vertices, L))

				forces[i,:] += coeff * f


	return forces



def F_contraction(vertices, polys, gamma, L):

	# every vertex has an associated force
	n_vertices = len(vertices)
	forces = np.zeros((n_vertices, 2))

	for i,vertex in enumerate(vertices):

		# find polys with this vertex
		for poly in polys:

			if i in poly.indices:

				# get clockwise vector
				vc = get_clockwise(i, poly.indices, vertices, L)
				uvc = unit_vector(vertex, vc)
	
				# get counter-clockwise vector
				vcc = get_counter_clockwise(i, poly.indices, vertices, L)
				uvcc = unit_vector(vcc, vertex)

				# get perimeter for this poly
				p = poly.get_perim(vertices, L)

				forces[i,:] += (gamma * p) * (uvc - uvcc)

	return forces

def F_adhesion(vertices, edges, Lambda, L):

	# every vertex has an associated force
	n_vertices = len(vertices)
	forces = np.zeros((n_vertices, 2))

	for edge in edges:
		i1 = edge[0]
		i2 = edge[1]
		v1 = vertices[i1]
		vertex2 = vertices[i2]
		v2 = v1 + periodic_diff(vertex2, v1, L)
		uv = unit_vector(v1, v2)
		forces[i1,:] += Lambda * uv

	return forces

# Force to move vertices of polys in particular direction
def F_motility(vertices, polys, eta):


	n_vertices = len(vertices)
	forces = np.zeros((n_vertices, 2))

	# find neighbors for every poly
	# defined as any two polys that share a vertex
	avg_angles = np.zeros((len(polys), 2))
	neighbor_count = np.ones(len(polys))

	for i,poly in enumerate(polys):
		avg_angles[i, :] += angle_2_vector(poly.theta)
		for j,poly2 in enumerate(polys):
			if i != j:
				a = poly.indices
				b = poly2.indices
				if any(k in a for k in b) == True:
					avg_angles[i, :] += angle_2_vector(poly2.theta)
					neighbor_count[i] += 1

	for i,poly in enumerate(polys):
		# noise variable
		nx = np.random.uniform(-pi,pi)
		ny = np.random.uniform(-pi,pi)
		n = np.array([nx,ny])
	
		# average all of the unit vectors for angles 
		avg = (avg_angles[i,:] / neighbor_count[i])
	
		# add this force direction for every vertex in current poly
		for index in poly.indices:
			forces[index, :] += avg + (eta * n)
	
		# theta = avg + eta * noise
		poly.theta = vector_2_angle(avg[0] + eta * n[0], avg[1] + eta * n[1])
	return forces













# visualization for average vector

# plt.plot([0, avg_angles[i,0]],[0,avg_angles[i,1]], color="k")

# v = angle_2_vector(poly2.theta)
# plt.plot([0,v[0]],[0,v[1]],color="k")
# print avg_angles[i,:] / neighbor_count[i]
# print magnitude(avg_angles[i,:] / neighbor_count

# v_avg = avg_angles[i,:] / neighbor_count[i]
# print magnitude(v_avg)
# print vector_2_angle(v_avg[0], v_avg[1])
# plt.plot([0,v_avg[0]],[0,v_avg[1]],color="m")
# v_avg_unit = unit_vector(v_avg, np.array([0,0]))
# plt.plot([0,v_avg_unit[0]],[0,v_avg_unit[1]],color="g")
# plt.plot([0,v_avg[0]],[0,v_avg[1]],color="m")
# plt.show()
# eetat()


