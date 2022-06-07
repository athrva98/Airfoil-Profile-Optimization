# Airfoil-Profile-Optimization
This repository contains code adapted from my Bachelor's Thesis. The goal was to use Meta-Heuristic Optimization techniques to Generate high performance airfoil profiles for Vertical Axis Wind Turbines.

# I continue to update the code here, with newer Optimization algorithms and more support. Feel free to contribute to this repository.

# Working

1. This codebase uses the Xfoil solver to get the performance parameters of the generated airfoil. The average cl/cd ratio is then calculated and used as a cost function.
2. I use NURBS splines to generate the airfoil profile. You will find the parameters used for optimization in the ```Main_file_to_run.py``` file.
3. You can set specific Mach Number and Reynolds number for your application in the ```Xfoil_runner.py``` file. 

# Some problems

Xfoil sometimes fails to converge on some of the generated airfoil, in such cases, no mechnism is implemented to recognize this and close the xfoil instance.
Basically, the software freezes and has to be manually interrupted.
