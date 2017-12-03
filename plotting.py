import numpy as np
import scipy as sp
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def plotxz(z,x):
        "Produces a plot of the z and x coordinates on the path that a ray has travelled"
	plt.figure('x vs z')
	plt.plot(z,x,'b-')
	plt.title('ray trace')
	plt.xlabel('z/mm')
	plt.ylabel('x/mm')


def plotyz(z,y):
        "Produces a plot of the z and y coordinates on the path that a ray has travelled"
	plt.figure('z vs y')
	plt.plot(z,y,'b-')
	plt.title('ray trace')
	plt.xlabel('z/mm')
	plt.ylabel('y/mm')

def plotxy(x,y):
    "Produces a plot of the x and y coordinates on the path that a ray has travelled"
    plt.figure('x vs y')
    plt.plot(x,y,'ro')
    plt.title('ray trace')
    plt.axis("equal")
    plt.xlabel('x/mm')
    plt.ylabel('y/mm')


def plot3d(list_of_rays,x,y,z):
    "Produces a 3 dimesional plot of the coordinaate on the path that a ray has travelled"
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.set_title('ray trace')
    ax.set_xlabel('x/mm')
    ax.set_ylabel('y/mm')
    ax.set_zlabel('z/mm')

    for i in list_of_rays:


        coord = i.vertices()
        for j in coord:
            x = [j[0] for j in coord]
            y = [j[1] for j in coord]
            z = [j[2] for j in coord]
        ax.plot(x,y,z)


def plot_rms(RMS,axes):
        """ Produces a plot of the beam diameter against rms.
        The input parameter RMS is a list where each element is itself a list
        that contains a beam diameter value and the corresponding rms value.
        """
        for i in RMS:
            D = [i[0] for i in RMS]
            rms = [i[1] for i in RMS]
	axes.plot(D,rms,'r-',label='rms')
	plt.title('Beam diameter vs rms')
	#plt.axis("equal")
	plt.xlabel('Beam diameter/mm')
	plt.ylabel(' root mean square/mm ')
	#plt.show()

def plot_diffraction(RMS,wavelength,axes,z0=200):
        """ Produces a plot of the beam diameter against diffraction scale.
        The input parameter RMS is a list where each element is itself a list
        that contains a beam diameter value and the corresponding rms value.The rms value is not used
        to calculate the diffraction. The RMS parameter is used again to simplify using this method in
        combination with the plot_rms method."""
        focal = z0 - 102.5
        for i in RMS:
            D = [i[0] for i in RMS]
            DiffractionScale = [((wavelength*focal)/(i[0])) for i in RMS]
	axes.plot(D,DiffractionScale,'b-',label ='Diffraction scale')
	plt.title('Beam diameter vs Diffraction scale')
	#plt.axis("equal")
	plt.xlabel('Beam diameter/mm')
	plt.ylabel('Diffractionscale/mm')
