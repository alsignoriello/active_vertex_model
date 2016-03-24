#!/usr/bin/python
import numpy as np
from Polygon import Polygon
from geometry import periodic_diff, euclidean_distance

""" 

energy.py - contains components to compute the potential energy
in the current configuration of vertex model 


author: Lexi Signoriello
date: 1/20/16



"""


def get_energy(vertices, polys, edges, parameters):
	# get necessary parameters 
	lx = parameters['lx']
	ly = parameters['ly']
	L = np.array([lx,ly])
	ka = parameters['ka']
	Lambda = parameters['Lambda']
	gamma = parameters['gamma']

	e1 = E_elasticity(vertices, polys, ka, L)
	e2 = E_adhesion(vertices, edges, Lambda, L)
	# take into account double counting edges
	e2 = e2 / 4.
	
	e3 = E_contraction(vertices, polys, gamma, L)

	return (e1 + e2 + e3)



def E_elasticity(vertices, polys, ka, L):
	e = 0.
	for poly in polys:
		a = poly.get_area(vertices, L)
		A0 = poly.A0
		e += (ka / 2.) * (a - A0)**2
	return e



def E_adhesion(vertices, edges, Lambda , L):
	e = 0.
	for edge in edges:
		i1 = edge[0]
		i2 = edge[1]
		v1 = vertices[i1]
		vertex2 = vertices[i2]
		v2 = v1 + periodic_diff(vertex2, v1, L)
		dist = euclidean_distance(v1[0], v1[1], v2[0], v2[1])
		e += Lambda * dist
	return e


def E_contraction(vertices, polys, gamma, L):
	e = 0.
	for poly in polys:
		p = poly.get_perim(vertices, L)
		e += ((gamma / 2.) * (p**2))
	return e


