import OpticalSystem as os
#import NewBundle as Bundle
#import matplotlib.pyplot as plt

#This script is used for the optimisation of a biconvex lens.

x= 198.452700178 -102.5 # sets focus to the paraxial focus of the planoconvex lens for comparison of the rms.
c0 = 0.02 # curvature of 1st refractive surface element
c1 = -0.02 # curvature of 2nd refractive surface element
# They are intial guesses and varied to minimise the rms.
z0 = 100 #z0 and z1 are the intercepts of the refractive surfaces with the z axis.
z1 = 105
rmax = 5 # radius of beam of rays
focus_point = 198.452700178 -102.5 # sets focus to the paraxial focus of the planoconvex lens for comparison of the rms.
# Note it can be set to other values.

optimised_rms = os.Lens_Optimization(c0,c1,z0,z1,rmax,focus_point)

print optimised_rms
