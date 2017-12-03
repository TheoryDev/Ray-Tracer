import numpy as np

""" This module is used to create the initial x and y coordinates
    of each ray in a beam of rays. It contains two methods rtpairs and rt uniform.
    rtpairs creates rings of points.
    rtuniform calls rtpairs and creates a uniform disc of points.
    """

def rtpairs(R=[],T=[]):
    """ rtpairs takes two parmeters: R and N
        R is a list of radii.
        N is a list that specifies how many pairs of coordinates
        evenly spaced from 0 to 2pi, should be created for each radius.

    """
    for i in range(len(R)):
	angles = np.linspace(0.0 , 2 * np.pi , int(T[i]) , endpoint = False)
        for j in range(int(T[i])):
            r = R[i]
            t = angles[j]

            yield r , t

def rtuniform(n = 0, rmax = 0 , m = 6):
    """ rtuniform creates specific R and N parameters for rtpairs.
        The parameters are created such that when rtpairs is called
        a uniform disc of points is created.
        These points are then used as the initial x and y positions of rays.
        """
    R = [i*float(rmax)/n for i in range(int(n+1))]

    N = [m * i for i in range(int(n+1))]
    N[0] = 1
    return rtpairs(R,N)
