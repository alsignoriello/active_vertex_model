#!/usr/bin/python
import sys
from parameters import get_parameters
from steepest_descent import steepest_descent
from parser import *

"""

Relaxes current network using a steepest descent method 


"""

# command line arguments for data files
vertex_file = sys.argv[1]
edge_file = sys.argv[2]
poly_file = sys.argv[3]


# Parameters
lx = 9 * (2 / (3 * (3**0.5)))**0.5
ly = 4 * (2 / (3**0.5))**0.5
ka = 1.
A0 = 1. # current preferred area for polygon
gamma = 0.04 * ka * A0 # hexagonal network
# gamma = 0.1 * ka * A0 # soft network
Lambda = 0.12 * ka * (A0**(3/2)) # hexagonal network
# Lambda = -0.85 * ka * A0**(3/2) # soft network
lmin = 0.2
delta_t = 0.05
eta = 1.


# get parameter dictionary
parameters = get_parameters(lx, ly, ka, gamma, Lambda, eta, lmin, delta_t)

# get vertices
vertices = read_vertices(vertex_file)

# get edges
edges = read_edges(edge_file)

# get polygons
poly_indices = read_poly_indices(poly_file)
polys = build_polygons(poly_indices, A0)

steepest_descent(vertices, edges, polys, parameters)





