#!/usr/bin/python
import numpy as np 
from Polygon import Polygon
from geometry import periodic_diff
from energy import *
import copy


""" 

transition.py - implements T1 transition for short bond lengths

author: Lexi Signoriello
date: 2/12/16

4 polys involved in transition are 1-4 counter-clockwise order

Cells defined such that:
Cell 0: i4, i1, i2, i5
Cell 1: i3, i1, i4
Cell 2: i6, i2, i1, i3
Cell 3: i5, i2, i6


Edges defined such that:
Edge 0: i1 - i2
Edge 1: i1 - i3
Edge 2: i1 - i4
Edge 3: i2 - i1
Edge 4: i2 - i5
Edge 5: i2 - i6
Edge 6: i3 - i1 # reverse edges
Edge 7: i4 - i1
Edge 8: i5 - i2 
Edge 9: i6 - i2


"""



def get_6_indices(polys, i1, i2, poly_ids):
	polys_copy = []
	for i in poly_ids:
		poly = copy.deepcopy(polys[i])
		polys_copy.append(poly)

	# define polys
	poly_0 = polys_copy[0]
	poly_1 = polys_copy[1]
	poly_2 = polys_copy[2]
	poly_3 = polys_copy[3]

	# Find indices wrt Cell 1
	pos = int(np.where(poly_1.indices == i1)[0])
	# i3: poly 1 before i1
	if pos == 0:
		i_left = len(poly_1.indices) - 1
	else:
		i_left = pos - 1
	i3 = poly_1.indices[i_left]
	# i4: poly 1 after i1
	if pos == len(poly_1.indices) - 1:
		i_right = 0
	else:
		i_right = pos + 1
	i4 = poly_1.indices[i_right]
	# i5: poly 3 before i2
	pos = int(np.where(poly_3.indices == i2)[0])
	if pos == 0:
		i_left = len(poly_3.indices) - 1
	else: 
		i_left = pos - 1
	i5 = poly_3.indices[i_left]
	# i6: poly 3 after i2
	if pos == len(poly_3.indices) - 1:
		i_right = 0
	else:
		i_right = pos + 1
	i6 = poly_3.indices[i_right]

	indices = [i1,i2,i3,i4,i5,i6]

	return indices



# get polys and edges associated with short bond length
def T1_0(polys, i1, i2, poly_ids, indices):
	polys_0 = []

	for i in poly_ids:
		# copy poly so it can be manipulated without changing
		# current configuation
		poly = copy.deepcopy(polys[i])
		polys_0.append(poly)

	# define polys
	poly_0 = polys_0[0]
	poly_1 = polys_0[1]
	poly_2 = polys_0[2]
	poly_3 = polys_0[3]

	i1 = indices[0]
	i2 = indices[1]
	i3 = indices[2]
	i4 = indices[3]
	i5 = indices[4]
	i6 = indices[5]

	edges_0 = np.zeros((10,2))
	# Edge 0: i1 - i2
	edges_0[0,0] = i1
	edges_0[0,1] = i2

	# Edge 1: i1 - i3
	edges_0[1,0] = i1
	edges_0[1,1] = i3

	# Edge 2: i1 - i4
	edges_0[2,0] = i1
	edges_0[2,1] = i4

	# Edge 3: i2 - i1
	edges_0[3,0] = i2
	edges_0[3,1] = i1

	# Edge 4: i2 - i5
	edges_0[4,0] = i2
	edges_0[4,1] = i5

	# Edge 5: i2 - i6
	edges_0[5,0] = i2
	edges_0[5,1] = i6

	# Edge 6: i3 - i1 # reverse edges
	edges_0[6,0] = i3
	edges_0[6,1] = i1

	# Edge 7: i4 - i1
	edges_0[7,0] = i4
	edges_0[7,1] = i1

	# Edge 8: i5 - i2 
	edges_0[8,0] = i5
	edges_0[8,1] = i2

	# Edge 9: i6 - i2
	edges_0[9,0] = i6
	edges_0[9,1] = i2

	return polys_0, edges_0

# get polys and edges associated with 
def T1_left(polys, i1, i2, poly_ids, indices):

	# Cells
	polys_l = []
	# ids in correct order already
	for i in poly_ids:
		poly = copy.deepcopy(polys[i])
		polys_l.append(poly)

	# define polys
	poly_0 = polys_l[0]
	poly_1 = polys_l[1]
	poly_2 = polys_l[2]
	poly_3 = polys_l[3]

	# define indices
	i1 = indices[0]
	i2 = indices[1]
	i3 = indices[2]
	i4 = indices[3]
	i5 = indices[4]
	i6 = indices[5]

	# Cell 0: remove i2
	pos = int(np.where(poly_0.indices == i2)[0])
	indices = np.delete(poly_0.indices, pos)
	polys_l[0].indices = indices


	# Cell 1: insert i2 before i1 
	pos = int(np.where(poly_1.indices == i1)[0])
	left_indices = poly_1.indices[:pos]
	right_indices = poly_1.indices[pos:]
	indices = np.concatenate((left_indices, [i2], right_indices))
	polys_l[1].indices = indices

	# Cell 2: remove i1
	pos = int(np.where(poly_2.indices == i1)[0])
	indices = np.delete(poly_2.indices, pos)
	polys_l[2].indices = indices

	# Cell 3: insert i1 before i2
	pos = int(np.where(poly_3.indices == i2)[0])
	left_indices = poly_3.indices[:pos]
	right_indices = poly_3.indices[pos:]
	indices = np.concatenate((left_indices, [i1], right_indices))
	polys_l[3].indices = indices


	# Edges
	edges_l = np.zeros((10,2))
	# Edge 0: i1 - i2
	edges_l[0,0] = i1
	edges_l[0,1] = i2

	# Edge 1: i2 - i3
	edges_l[1,0] = i2
	edges_l[1,1] = i3

	# Edge 2: i1 - i4
	edges_l[2,0] = i1
	edges_l[2,1] = i4

	# Edge 3: i2 - i1
	edges_l[3,0] = i2
	edges_l[3,1] = i1

	# Edge 4: i1 - i5
	edges_l[4,0] = i1
	edges_l[4,1] = i5

	# Edge 5: i2 - i6
	edges_l[5,0] = i2
	edges_l[5,1] = i6

	# Edge 6: i3 - i2 # reverse edges
	edges_l[6,0] = i3
	edges_l[6,1] = i2

	# Edge 7: i4 - i1
	edges_l[7,0] = i4
	edges_l[7,1] = i1

	# Edge 8: i5 - i1 
	edges_l[8,0] = i5
	edges_l[8,1] = i1

	# Edge 9: i6 - i2
	edges_l[9,0] = i6
	edges_l[9,1] = i2


	return polys_l, edges_l

def T1_right(polys, i1, i2, poly_ids, indices):

	polys_r = []
	for i in poly_ids:
		poly = copy.deepcopy(polys[i])
		polys_r.append(poly)

	# define polys
	poly_0 = polys_r[0]
	poly_1 = polys_r[1]
	poly_2 = polys_r[2]
	poly_3 = polys_r[3]

	# define indices
	i1 = indices[0]
	i2 = indices[1]
	i3 = indices[2]
	i4 = indices[3]
	i5 = indices[4]
	i6 = indices[5]

	# Cell 0: remove i1
	pos = int(np.where(poly_0.indices == i1)[0])
	indices = np.delete(poly_0.indices, pos)
	polys_r[0].indices = indices


	# Cell 1: insert i2 after i1
	pos = int(np.where(poly_1.indices == i1)[0])
	left_indices = poly_1.indices[:pos+1]
	right_indices = poly_1.indices[pos+1:]
	indices = np.concatenate((left_indices, [i2], right_indices))
	polys_r[1].indices = indices

	# Cell 2: remove i2
	pos = int(np.where(poly_2.indices == i2)[0])
	indices = np.delete(poly_2.indices, pos)
	polys_r[2].indices = indices

	# Cell 3: insert i1 after i2
	pos = int(np.where(poly_3.indices == i2)[0])
	left_indices = poly_3.indices[:pos+1]
	right_indices = poly_3.indices[pos+1:]
	indices = np.concatenate((left_indices, [i1], right_indices))
	polys_r[3].indices = indices 

	# # Edges
	edges_r = np.zeros((10,2))
	# Edge 0: i1 - i2
	edges_r[0,0] = i1
	edges_r[0,1] = i2

	# Edge 1: i1 - i3
	edges_r[1,0] = i1
	edges_r[1,1] = i3

	# Edge 2: i1 - i6
	edges_r[2,0] = i1
	edges_r[2,1] = i6

	# Edge 3: i2 - i1
	edges_r[3,0] = i2
	edges_r[3,1] = i1

	# Edge 4: i2 - i5
	edges_r[4,0] = i2
	edges_r[4,1] = i5

	# Edge 5: i2 - i4
	edges_r[5,0] = i2
	edges_r[5,1] = i4

	# Edge 6: i3 - i1 # reverse edges
	edges_r[6,0] = i3
	edges_r[6,1] = i1

	# Edge 7: i4 - i2
	edges_r[7,0] = i4
	edges_r[7,1] = i2

	# Edge 8: i5 - i2 
	edges_r[8,0] = i5
	edges_r[8,1] = i2

	# Edge 9: i6 - i1
	edges_r[9,0] = i6
	edges_r[9,1] = i1


	return polys_r, edges_r


# # find 4 polys involved with 2 vertices
# Labeled polys 0-3 in counter-clockwise order
# Cell 0 and Cell 3 are neighbors
def get_4_polys(polys, i1, i2):

	poly_ids = np.zeros(4).astype(int)
	poly_ids.fill(-1) # catch errors later

	for poly in polys:
		# Cell 0 or Cell 2
		# Current neighboring polys
		# Cell 1 should have i1 before i2 in counter-clockwise orde
		if i1 in poly.indices and i2 in poly.indices:
			pos1 = np.where(poly.indices == i1)
			pos2 = np.where(poly.indices == i2)

			if pos1 == len(poly.indices) - 1:
				pos1 = -1
			if pos2 == len(poly.indices) - 1:
				pos2 = -1

			# if Cell 1: i1 is before i2
			if pos1 < pos2:
				poly_ids[0] = poly.id
			# if Cell 3: i2 is before i1
			if pos2 < pos1:
				poly_ids[2] = poly.id
		
		# Cell 3
		if i2 in poly.indices and i1 not in poly.indices:
			poly_ids[3] = poly.id
		# Cell 1
		if i1 in poly.indices and i2 not in poly.indices:
			poly_ids[1] = poly.id

	return poly_ids
	


def T1_transition(vertices, polys, edges, parameters):
	

	lx = parameters['lx']
	ly = parameters['ly']
	L = np.array([lx,ly])
	lmin = parameters['lmin']

	reverse = []

	for edge in edges:
		i1 = edge[0]
		i2 = edge[1]

		v1 = vertices[i1]
		vertex2 = vertices[i2]
		v2 = v1 + periodic_diff(vertex2, v1, L)

		dist = euclidean_distance(v1[0], v1[1], v2[0], v2[1])

		if dist < lmin and (i1,i2) not in reverse:
			print "T1", i1, i2, dist
			poly_ids = get_4_polys(polys, i1, i2)
			if -1 in poly_ids:
				pass
			else:
				# find minimum configuration
				reverse.append((i2,i1))

				# 6 indices for vertices involved in transition
				indices = get_6_indices(polys, i1, i2, poly_ids)

				# original configuration
				polys_0, edges_0 = T1_0(polys, i1, i2, poly_ids, indices)
				E0 = get_energy(vertices, polys_0, edges_0, parameters)

				# left T1 transition 
				polys_l, edges_l = T1_left(polys, i1, i2, poly_ids, indices)
				E_left = get_energy(vertices, polys_l, edges_l, parameters)

				# # right T1 transition
				polys_r, edges_r = T1_right(polys, i1, i2, poly_ids, indices)
				E_right = get_energy(vertices, polys_r, edges_r, parameters)


				# get minimum
				min_energy = np.min((E0, E_left, E_right))
				min_i = np.argmin((E0, E_left, E_right))
				print min_i

				# # do nothing - same configuration
				if min_i == 0:
					pass

				if min_i == 1:
					set_T1_left(polys, polys_l, poly_ids, edges, indices)

				if min_i == 2:
					set_T1_right(polys, polys_r, poly_ids, edges, indices)

	return polys, edges


def set_T1_left(polys, polys_l, poly_ids, edges, indices):
	# set new poly indices
	for i,poly in enumerate(polys_l):
		polys[poly_ids[i]].indices = poly.indices

	# set new edges
	i1 = indices[0]
	i2 = indices[1]
	i3 = indices[2]
	i5 = indices[4]
	for i,edge in enumerate(edges):

		# i1 - i3 becomes i2 - i3
		if edge[0] == i1 and edge[1] == i3:
			edges[i][0] = i2
	
		# i2 - i5 becomes i1 - i5
		if edge[0] == i2 and edge[1] == i5:
			edges[i][0] = i1

		# i3 - i1 becomes i3 - i2
		if edge[0] == i3 and edge[1] == i1:
			edges[i][1] = i2

		# i5 - i2 becomes i5 - i1
		if edge[0] == i5 and edge[1] == i2:
			edges[i][1] = i1
	
	return 


def set_T1_right(polys, polys_r, poly_ids, edges, indices):

	# set new poly indices
	for i,poly in enumerate(polys_r):
		polys[poly_ids[i]].indices = poly.indices
	

	# set new edges
	i1 = indices[0]
	i2 = indices[1]
	i4 = indices[3]
	i6 = indices[5]

	for i,edge in enumerate(edges):

		# i1 - i4 becomes i2 - i4
		if edge[0] == i1 and edge[1] == i4:
			edges[i][0] = i2

		# i2 - i6 becomes i1 - i6
		if edge[0] == i2 and edge[1] == i6:
			edges[i][0] = i1

		# i4 - i1 becomes i4 - i2
		if edge[0] == i4 and edge[1] == i1:
			edges[i][1] = i2

		# i6 - i2 becomes i6 - i1
		if edge[0] == i6 and edge[1] == i2:
			edges[i][1] = i1

	return 




def T2_transition(network, vertices, polys, edges, min_area):
	pass



















