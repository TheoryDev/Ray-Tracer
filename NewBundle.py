import numpy as np
import genpolar as gen
import raytracer as rt
#

""" This module is used to create a list of ray objects.
    It uses the rtuniform method in the genpolar module to
    create the intial x and y coordinates.The coordinates are then used
    in the creation of a list of instances of the Ray class from the ray tracer module.
"""

X,Y,Z= [],[],[]


def bundle( n=5 ,rmax=5  ,m=4  ,initial_z=0 ,direction=[0,0,1] ,x1=0,y1=0 ):
    """ The bundle function takes 5 parameters.
        The parameters n ,rmax and m are used when calling rtuniform.
        (see it's docstring for further information)
        The intial_z parmeter determines where the bundle of rays
        starts at on the z axis.
        The initial direction parameter determines the initial direction
        of the bundle of rays.
        The parameters x1,y1 allow the x and y coordinates to be offset.
        Note bundle of rays is returned as list_of_rays.
    """

    list_of_rays = []



    for r ,t in gen.rtuniform(n,rmax,m):
            ith_ray = rt.Ray([(r * np.cos(t)+x1),(r * np.sin(t)+y1),initial_z] , direction)
            # Creates a ray instance for each pair of r, theta coordinates.
            # The rays are then appended to a list.
            list_of_rays.append(ith_ray)
    return list_of_rays
# The list_of_rays is then used in the ray tracer model
