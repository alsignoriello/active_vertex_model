#!/usr/bin/python

"""

Builds a parameter dictionary 

"""

def get_parameters(lx, ly, ka, gamma, Lambda, eta, lmin, delta_t):

	parameters = {}
	
	# Side length of box in x direction
	parameters['lx'] = lx

	# Side length of box in y directions
	parameters['ly'] = ly

	# ka - elastic area coefficient
	parameters['ka'] = ka

	# gamma - actin myosin contraction coefficient
	parameters['gamma'] = gamma

	# lambda - line tension coefficient
	parameters['Lambda'] = Lambda 

	# eta - noise scaling coefficient
	parameters['eta'] = eta

	# lmin - minimum bond length between two vertices
	parameters['lmin'] = lmin

	# delta t - time step
	parameters['delta_t'] = delta_t


	return parameters