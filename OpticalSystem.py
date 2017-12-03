import numpy as np
import scipy as sp
import genpolar as gen
import matplotlib.pyplot as plt
import raytracer as rt
import plotting as plo
from mpl_toolkits.mplot3d import Axes3D
import NewBundle as Bundle
import scipy.optimize as spo


""" This module is used to create optical systems. The elements class is used to create
    a list of spherical refraction elements. The System class takes an elements object
    an creates a system object. The systems class has methods to propagate rays.
    Finally, the module has other methods outside of the classes to calculate rms and
    for lens optimisation.
"""

class elements:
    """ The elements class takes a list of spherical refraction surface elements parameters and
        produces a list of spherical refraction surface elements. This elements oject is then used to
        produce a system.
    """
    def __init__(self,para = []):
        " para is a list where each element is a list of parameters for a particular surface element "
        self.__para = para

    def append(self):
        """ Takes each set of spherical refraction surface element parameters
        and creates a list of the corresponding surface elements """
        para = self.__para
        list_of_elements = []

        for i in para:
            ith_element = rt.SphericalRefraction(i[0],i[1],i[2],i[3],i[4])
            list_of_elements.append(ith_element)
        return list_of_elements

class System(elements,rt.OutputPlane):
    """ The System class inherits the elements and Outputplane classes.
    It creates a system of refractive surface elements and an output plane at which the process stops.
    It contains methods to calculate the paraxial focus,propagate a list of rays, plot graphs and calulate rms data.

    """

    def __init__(self,elements,z_choice = 250.0 , use='yes'):
        """ Initializes instances of the System class, an elements class object is a parameter.
        If the use parameter = 'yes' the paraxial_focus method is used to position the outputplane.
        If use = 'no' then the outputplane position is set to z_choice.
        """
        self.__elements = elements
        self.__list_of_elements = elements.append()
        self.__z_choice = z_choice #, dtype= np.float
        self.__use = use


    def paraxial_focus(self):
           """ The paraxial_focus method calculates where the paraxial
               focus of a surface element is.It then returns a z0 value
               at which the output plane can be positioned.
               The exceptions prevent the use of the paraxial focus when the system is not converging

           """
           elements = self.__list_of_elements
           test_ray = rt.Ray([0.1,0,0],[0,0,1])
           for i in elements:
               i.propagate_ray(test_ray)

           if self.__use == 'yes' and len(elements) == 1:
                last = elements[-1]
                last_n1 = last._SphericalRefraction__n1
                last_n2 = last._SphericalRefraction__n2
                last_curvature = last._SphericalRefraction__curvature 
                #print last_n1,last_n2,last_curvature
    	        if last_curvature > 0 and last_n1 > last_n2:
    	           raise Exception("cannot calculate paraxial focus for divering lens, set, use='no' ")
    	        else:        
    	            if last_curvature < 0 and last_n2 > last_n1:
    	               raise Exception("cannot calculate paraxial focus for divering lens, set, use='no' ")
    	            else:
    	                if last_curvature != 0:
    	                   direction = test_ray.k()
    	                   position = test_ray.p()

	                   L = -position[0]/direction[0]

    	                   if L > 0:

        	               paraxial_position = position[2] + L * direction[2]
        	               return paraxial_position
        	        else:
           	            raise Exception("cannot calculate paraxial focus for plane refractive surface ,set, use='no' ")   
	   elif self.__use == 'yes' and len(elements) > 1:
	      
    	                   direction = test_ray.k()
    	                   position = test_ray.p()

	                   L = -position[0]/direction[0]

    	                   if L > 0:

        	               paraxial_position = position[2] + L * direction[2]
        	               return paraxial_position
	       
	   
	   elif  self.__use == 'no':
	           return self.__z_choice
	           

    def propagate_ray(self,rays):
            """ The method takes a Systems class instance and a list of rays as arguements.
            It then propagates the rays through the spherical refraction elements.
            Next the paraxial focus is estimated and the Outputplane is positioned at this point.
            """

            elements = self.__list_of_elements

            for elem in elements:
                for ray in rays:
                    elem.propagate_ray(ray)

            z0 = self.paraxial_focus()
            OutputPlane = rt.OutputPlane(z0)

            for ray in rays:
                OutputPlane.propagate_ray(ray)
            return rays

    def plot(self,rays):
        """ The method takes a Systems class instance and a list of rays as arguements.
            The vertices method of each ray in the list of ray objects is then called to obtain a list of coordinates.
            Then for loops are used to produces plots of the list of coordinates of each ray.
            This allows for a visualisation of each ray's propagation through the system.
        """

        for ray in rays:

            coord = ray.vertices()
            for j in coord:
                x = [j[0] for j in coord]
                y = [j[1] for j in coord]
                z = [j[2] for j in coord]

                plo.plotyz(z,y)
                plo.plotxz(z,x)
        plo.plot3d(rays,x,y,z)
        plo.plt.show()

    def Beam_plots(self,rays):
        """ The method takes a Systems class instance and a list of rays as arguements.
            This method produces plots of the x and y coordinates of each ray in a list of rays.
            This is done at the z = 0 plane and the plane of the paraxial focus.
        """
        coord_initial=[]
        coord_final=[]
        for ray in rays:
            coord_initial.append( ray.vertices()[0])
            coord_final.append( ray.p())

        for i in coord_initial:
            x1=i[0]
            y1=i[1]
            plo.plt.subplot(1,2,1)
            plt.plot(x1, y1, 'bo')
            plt.title('Beam profile at z = 0 ')
            plt.xlabel('x/mm')
            plt.ylabel('y/mm')
        plt.axis("equal")

        for i in coord_final:
            x2=i[0]
            y2=i[1]
            plo.plt.subplot(1,2,2)
            plt.plot(x2, y2, 'bo')
            plt.title('Beam profile at z = paraxial focus ')
            plt.xlabel('x/mm')
            plt.ylabel('y/mm')
        plt.axis("equal")

        plt.show()



    def get_data_RMS(self,rmin = 1,rmax =5,step = 0.5):
        """ The method requires a Systems class instance and parameters for the range and step size to produce
            an arange of beam radius values. It retruns a list where each element is itself a list
            that contains a beam diameter value and the corresponding rms value
        ."""
        RMS =[]
        list_of_radii = np.arange(rmin,rmax,step)
        for i in list_of_radii:
            rays = Bundle.bundle(n =10 ,rmax=i , m = 6, initial_z = 0, direction=[0,0,1])
            rays = self.propagate_ray(rays)
            RMS.append([2*i,root_mean_square(rays)]) # factor of 2 is because D=2r
        return RMS


def Lens_trial(c,z0,z1,rmax,z0_out):
    """ This method produces a function that returns an rms value.
        The rms value will be minimised using an numerical optimisation function.
        c is a list with the curvatures of the two refractive surface elements.
        z0 is the intecept of the first spherical refraction surface with the z axis
        while z1 is the intercept for the second surface. rmax is the beam radius.
        z0_out is the position of the output plane.
            """
    test_rays = Bundle.bundle(n=5 , rmax=5  , m=4, initial_z = 0, direction = [0,0,1])
    Surface1 = rt.SphericalRefraction(100,c[0],1,1.5168,50)
    Surface2 = rt.SphericalRefraction(155,c[1],1.5168,1,50)
    Output = rt.OutputPlane(z0_out)
    for ray in test_rays:
        Surface1.propagate_ray(ray)
        Surface2.propagate_ray(ray)
        Output.propagate_ray(ray)
    rms = root_mean_square(test_rays)
    return rms

def Lens_Optimization(c0,c1,z0,z1,rmax,focus_point):
    """ This function optimises the Lens_trial method by varying the curvatures to minimse the rms returned.
        z0 is the intecept of the first spherical refraction surface with the z axis
        while z1 is the intercept for the second surface. rmax is the beam radius. They are all held
        constant.
        The parameters c0 and c1 are the respective curvatures of the first and second refractive surface elements.
        c0 and c1 are used to set the boundaries for the optimisation.
        focus_point simply determines how far the output plane is from the midpoint of the lens.
        The method then returns a minimised rms values and the corresponding curvatures.
    """
    if focus_point < 0:
        raise Exception("rays must be focused at a position to the right of the lens")
    else:
        z0_out = 0.5*(z0 +z1) + focus_point
        bound = ((0.,1./(rmax +1)),(-1./(rmax +1),0.))
        opt= spo.minimize(Lens_trial,[c0,c1], args=(z0,z1,rmax,z0_out),bounds=bound)
        return opt

def root_mean_square_error(rays):
    """ The method determines the rms of the x and y positions of the rays in a list of rays
        at the output plane. It takes a list of rays and uses the ray class object's p() method
        to return the coordinates at the output plane.
        It then calculates the rms sample standard deviation and the associated percentage error.
    """
    x,y = [],[]
    distances = []
    deviations =[]
    for ray in rays:
        if ray.terminate == False:
            x,y = ray.p()[0],ray.p()[1]
            distance = x * x + y * y
            distances.append(distance)
    dev = np.mean(distance)
    rms = np.sqrt(np.mean(distances))
    for ray in rays:
        if ray.terminate == False:
            x,y = ray.p()[0],ray.p()[1]
            distance = x * x + y * y
            error_d = np.sqrt(distance)-np.sqrt(dev)
            deviations.append(error_d*error_d)


    rms_error = np.sqrt(np.mean(deviations))/len(rays)

    return rms,rms_error



def root_mean_square(rays):
    """ The method determines the rms of the x and y positions of the rays in a list of rays
        at the output plane. It takes a list of rays and uses the ray class object's p() method
        to return the coordinates at the output plane.
    """
    x,y = [],[]
    distances = []
    deviations =[]
    for ray in rays:
        if ray.terminate == False:
            x,y = ray.p()[0],ray.p()[1]
            distance = x * x + y * y
            distances.append(distance)

    rms = np.sqrt(np.mean(distances))
    return rms
