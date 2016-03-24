import matplotlib.pyplot as plt
import sys
from parser import *
from geometry import periodic_diff

"""

plot.py - plots the network for vertex model


author: Lexi Signoriello
date: 1/19/16

[vertices] [edges]

options:
	vertices

	line color

	color by number of neighbors
	color by area


"""


def plot_network(vertices, polys, L, file):
	plt.cla()
	fig = plt.figure()
	ax = fig.add_subplot(1,1,1)
	for x,y in vertices:
		ax.scatter(x, y, c="m", marker=".", s=100)

	for poly in polys:
		indices = poly.indices
		for i,index in enumerate(indices):
			x1,y1 = vertices[index]
			if i == len(indices) - 1:
				x2,y2 = vertices[indices[0]]
			else:
				x2,y2 = vertices[indices[i+1]]

			v1 = np.array((x1,y1))
			v2 = np.array((x2,y2))
			v2 = v1 + periodic_diff(v2, v1, L)
			x2,y2 = v2
			ax.plot([x1,x2], [y1,y2], c="c")

			v2 = np.array((x2,y2))
			v1 = v2 + periodic_diff(v1, v2, L)
			x1,y1 = v1
			ax.plot([x1,x2], [y1,y2], c="c")


		# # plot centers
		# x,y = poly.get_center(vertices, L)
		# plt.scatter(x,y,color="m", marker="*")

	# remove axis ticks
	ax.axes.get_xaxis().set_ticks([])
	ax.axes.get_yaxis().set_ticks([])

	ax.axis([0,L[0],0,L[1]])
	plt.savefig(file)
	plt.close(fig)
	return

def plot_edges(vertices, edges, L):
	plt.cla()
	for vertex in vertices:
		x = vertex[0]
		y = vertex[1]
		plt.scatter(x, y, c="c")

	for edge in edges:
		i1 = edge[0]
		i2 = edge[1]
		x1,y1 = vertices[i1]
		x2,y2 = vertices[i2]
		v1 = np.array((x1,y1))
		v2 = np.array((x2,y2))
		v2 = v1 + periodic_diff(v2, v1, L)
		x2,y2 = v2
		plt.plot([x1,x2],[y1,y2],c="k")

	plt.axis([0,L[0],0,L[1]])
	plt.show()
	return




vertex_file = sys.argv[1]
edge_file = sys.argv[2]
poly_file = sys.argv[3]

lx = 9 * (2 / (3 * (3**0.5)))**0.5
ly = 4 * (2 / (3**0.5))**0.5
A0 = 1.
L = np.array([lx,ly])


# get vertices
vertices = read_vertices(vertex_file)

# get edges
edges = read_edges(edge_file)

# get polygons
poly_indices = read_poly_indices(poly_file)
polys = build_polygons(poly_indices, A0)

file = "test.jpg"
plot_network(vertices, polys, L, file)
