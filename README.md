# Vertex Model

The vertex model uses polygons, composed of vertices and edges, to illustrate the mechanics in formation of polygon sheets. This model has successfully been applied to fly wings and eyes in 2D.  

Simulations compute the energy and forces in the system using the following equations:

E = 0.5 &Sigma;<sub>&alpha;</sub> K<sub>&alpha;</sub> (A<sub> &alpha; </sub> - A<sub>&alpha;</sub>)<sup>2</sup> + &Sigma;<sub> i,j </sub> &Lambda;<sub>i,j</sub> l<sub> i,j</sub>	+ 0.5 &Sigma;<sub> &alpha; </sub> &Gamma;<sub>&alpha;</sub> P<sub>&alpha;</sub><sup>2</sup>

where A is the area and P is the perimeter. 

&#8407;F<sub>i</sub> = - &#8407;&nabla; <sub>i</sub>E<sub>i</sub>


The terms represent cell elasticity, line tension and contraction, respectively. 

<img src="https://github.com/alsignoriello/vertex_model/blob/master/images/vertex_model_description.png">


Farhadifar, R., Röper, J.-C., Aigouy, B., Eaton, S. & Jülicher, F. The Influence of Cell Mechanics, Cell-Cell Interactions, and Proliferation on Epithelial Packing. Current Biology 17, 2095–2104 (2007).


# Parameters


|Parameter | Definition | Range |
|----------|------------|-------|
| lx | length of box x-axis | positive float |
| ly | length of box y-axis | positive float |
| k<sub>A</sub> | elasticity | |
| &Lambda; | line tension | | 
| &Gamma; | contraction| |
| l<sub>min</sub> | minimum bond length | positive float |
| &Delta; t| time step | small positive float | 

# Input

vertices.txt (x,y) coordinates for every vertex in network

edges.txt (index1, index2) indices for every edge between two vertices in the network

cells.txt (index0, index1, ... indexN) indices in counter-clockwise order that form every cell in the network, a cell is defined as a polygon, does not assume number of sides


# Notes

- Periodic boundary conditions




