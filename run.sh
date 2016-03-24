#!/usr/bin/bash

vertex_file=$1
edge_file=$2
poly_file=$3


# Relaxation (steepest descent)
# python relax.py $vertex_file $edge_file $poly_file 
# python plot.py $vertex_file $edge_file $poly_file 


# Molecular Dynamics
python MD.py $vertex_file $edge_file $poly_file 

# later, will add division simulations..
# python divide.py $vertex_file $edge_file $poly_file 

