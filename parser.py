#!/usr/bin/python
import numpy as np
from Polygon import Polygon
from geometry import rand_angle

"""

parser.py - defines functions to read and write relevant data


author: Lexi Signoriello
date: 1/22/16



"""


def read_poly_indices(file):
	# indices = np.loadtxt(file, dtype=int)
	indices = []
	f = open(file)
	for line in f:
		poly_indices = []
		linesplit = line.strip().split("\t")
		for i in linesplit:
			poly_indices.append(int(i))
		indices.append(poly_indices)
	f.close()
	return indices


def build_polygons(cell_indices, A0):
	polys = []
	for i,indices in enumerate(cell_indices):
		theta = rand_angle()
		poly = Polygon(i, indices, A0, theta)
		polys.append(poly)
	return polys


def read_vertices(file):
	vertices = np.loadtxt(file)
	return vertices

def write_vertices(vertices, file):
	np.savetxt(file, vertices)
	return

# i1 i2
# indices for edge from v1 to v2
def read_edges(file):
	edges = np.loadtxt(file).astype(int)
	return edges









