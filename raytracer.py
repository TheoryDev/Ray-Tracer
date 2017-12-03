import numpy as np
import scipy as sp
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


__doc__ = """
This module simulates a raytracer.
It creates: ray objects, optical surface elements and Output planes.
In addition, it contains methods to calculate where the rays intercept the Optical elements and outputplane.
Then methods to determine the effect at the interface.
Then the propagate_ray method propogates the rays through optical elements to the output plane.
"""
class Ray:

        """The Ray class initializes ray objects.
		   It takes 3 parameters: self, initial_position and initial_direction.
		   It then contains methods p() and k() to return the last
		   position and direction.
		   The append method, appends the new positions and directions to their respective lists.
		   The vectrices() method returns the list of positions.
		"""

	def __init__(self, initial_position = [], initial_direction = [] ):
	    """ Initializes ray object instances. The parameters
	       initial_position and initial_direction are 3 dimensional vectors in
	       cartesian coordinates.
	    """

	    if len(initial_position) and len(initial_direction) == 3:
	           if initial_direction[2] > 0: # rays must propagate in the positive z direction.


          		a = np.array(initial_direction, dtype = np.float)
          		a = a/np.linalg.norm(a)
          		self.__positions = [np.array(initial_position , dtype = np.float)]
          		self.__direction = [a]
          		self.terminate = False
	           else:
	               raise  Exception("rays must propagate in the positive z direction!")

            else:
                raise Exception("rays must have 3 directions (Length %d provided)" % len(initial_position))

	def p(self):
            """This methods reutrns the last position of the ray"""
            return self.__positions[-1]

	def k(self):
            """This methods reuturns the last direction of the ray"""
            return self.__direction[-1]

	def append(self , new_point , new_direction ):
	    """ This method appends the new position and direction of the ray to their respective lists"""

            self.__positions.append(new_point)
            self.__direction.append(new_direction/np.linalg.norm(new_direction))

	def vertices(self):
            """ This method returns a list of all of the positions a ray has been at as it propagates"""
            return np.copy(self.__positions)


class OpticalElement:
	#"""hello"""
	def propagate_ray(self , ray):
		""" propagate a ray through the optical element"""
		raise NotImplementedError()


class SphericalRefraction(OpticalElement):
	""" This class creates spherical refraction surface elements.
	   It contains a intilization, intercept,refraction and propagate ray methods.
	"""
	def __init__(self,z0, curvature, n1 = 1 , n2 = 1.5 , aperture = 10):
	        """ The initilization parameters are z0,curvature, n1,n2 and aperture
	    z0 is where the SpherialRefraction element intercepts the z axis.
	    n1 is the refractive index on the first side of the surface while 2 is the refractive index on the second side.
	    The aperture radius is the limit of how far the surface extends from the z a"""
		self.__z0 = z0
		self.__curvature = curvature
		self.__n1 = n1
		self.__n2 = n2
		self.__aperture = aperture


	def intercept(self , ray):
		""" Intercept calcualtes the position at which the ray intercepts the surface element.
		    There are three types of surface element: convex,concave and plane.
		    This method differentiates between the three cases and returns the appropriate intercept position.
		"""

		if self.__curvature != 0 :

			self.__radius = 1/self.__curvature
			self.__origin = np.array([0, 0, self.__z0 + self.__radius], dtype='float')
			self.__r = np.subtract(ray.p(),self.__origin)
			r_dot_k = np.dot(self.__r, ray.k() )
			k_dot_k = np.dot(self.__r,self.__r)
			discriminant = (r_dot_k*r_dot_k - (k_dot_k -self.__radius*self.__radius))


			if discriminant < 0: # The will be no physical solution so no intercept.
				print "no intercepts"
				
				return None


			d = np.sqrt(discriminant)


			L1 = - r_dot_k + d
			L2 = - r_dot_k - d



			if self.__curvature > 0: # Convex surface
				a = min(L1,L2)
				if a > 0: # prevents ray going backwards
				    return np.add(a*ray.k(),ray.p())
                                else:
                                    return None

			elif self.__curvature < 0 : # Concave surface
			        b = max(L1,L2)
			        if b > 0: #prevents ray going backwards
				    return np.add(b*ray.k(),ray.p())
                                else:
                                    return None

                else:  #Plane surface
                        L3 = (self.__z0 - ray.p()[2])/(ray.k()[2])

                        return  np.add(L3*ray.k(),ray.p())


	def refraction(self,ray,incident,normal,n1,n2): # put in sin02>n1/n2 test it later
            """The refraction method calculates the new direction of an incident ray
                when it is refracted at the boudary between two different mediums.
                It takes parameters: self, input ray, incident direction, normal, n1, n2.
            """


	    cosine_incidence = -np.dot(normal,ray.k())
	    sine_incidence = np.sqrt(1 - cosine_incidence * cosine_incidence )


	    n = float(self.__n1)/float(self.__n2)


	    if sine_incidence >  1/n :
     		     print "total internal reflection"

     		     return None

	    else: # This uses Snells law in 3D to caculate the new ray direction.

		square_sine_refractive = n * n * (1 - cosine_incidence * cosine_incidence)
		direction = n * ray.k() + (n*cosine_incidence - np.sqrt(1- square_sine_refractive ))*normal
		return direction #error cases



        def propagate_ray(self,ray):
                """The propagate_ray method calculates the intercept of an incident ray
                   with a refractive surface. It then determines the normal to the surface.
                   If the interception with the surface is not valid the ray is terminated , otherwise it calls the refraction method.
                   Then it uses the ray object's append method to update the ray with a new position
                   and direction.
                """
		if ray.terminate == False:

		    intercept = self.intercept(ray)
		    if intercept is None:
		      ray.terminate = True # terminates ray
		    else:

          		n1 = self.__n1
          		n2 = self.__n2

          		if self.__curvature != 0:
              		        if self.__curvature > 0:
             			#calculate intercept position
                          		gradient =  intercept - self.__origin

                                elif self.__curvature < 0:
                                    gradient = -intercept + self.__origin
                                normal = gradient/np.linalg.norm(gradient) # normal to surface
                        else:
                                normal = np.array([0,0,-1])

          		limit = self.__aperture # radius curvature of surface in x-y plane

          		if  (intercept[0])*(intercept[0]) + (intercept[1])* (intercept[1]) > limit*limit :
         			print "no intercept"
         			ray.terminate = True
         			 # Need to stop it from going past without touching it and hitting the output plane.



          		else:
         			direction = self.refraction(ray,ray.k(), normal, n1 ,n2)
         			if direction is None:
     			            ray.terminate = True
     			        else:
         			    ray.append( intercept , direction )

class SphericalReflection(SphericalRefraction):
    """ This class creates spherical reflection elements.
        It contains a intilization, intercept,refraction and propagate ray methods.
    """
    def __init__(self,z0=100, curvature=0.02, aperture = 50):
	        """ The initilization parameters are z0,curvature, and aperture
	    z0 is where the SpherialReflection element intercepts the z axis.
	    The aperture radius is the limit of how far the surface extends from the z a"""
		self.__z0 = z0
		self.__curvature = curvature
		self.__aperture = aperture


    def intercept(self , ray):
		""" Intercept calcualtes the position at which the ray intercepts the surface element.
		    There are three types of surface element: convex,concave and plane.
		    This method differentiates between the three cases and returns the appropriate intercept position.
		"""

		if self.__curvature != 0 :

			self.__radius = 1/self.__curvature
			self.__origin = np.array([0, 0, self.__z0 + self.__radius], dtype='float')
			self.__r = np.subtract(ray.p(),self.__origin)
			r_dot_k = np.dot(self.__r, ray.k() )
			k_dot_k = np.dot(self.__r,self.__r)
			discriminant = (r_dot_k*r_dot_k - (k_dot_k -self.__radius*self.__radius))


			if discriminant < 0: # The will be no physical solution so no intercept.
				print "no intercepts"
				#ray.terminate = True
				return None


			d = np.sqrt(discriminant)


			L1 = - r_dot_k + d
			L2 = - r_dot_k - d



			if self.__curvature > 0: # Convex surface
				a = min(L1,L2)
				if a > 0: # prevents ray going backwards
				    return np.add(a*ray.k(),ray.p())
                                else:
                                    return None

			elif self.__curvature < 0 : # Concave surface
			        b = max(L1,L2)
			        if b > 0: #prevents ray going backwards
				    return np.add(b*ray.k(),ray.p())
                                else:
                                    return None

                else:  #Plane surface
                        L3 = (self.__z0 - ray.p()[2])/(ray.k()[2])

                        return  np.add(L3*ray.k(),ray.p())



    def reflection(self,ray,incident,normal):
        """ This method takes an ray object, incident direction and normal to the surface as parameters.
            It returns the direction at which the ray is relfected.
        """
        new_direction= incident - 2*np.dot(incident,normal)*normal
        return new_direction


    def propagate_ray(self,ray):
                """The propagate_ray method calculates the intercept of an incident ray
                   with a reflective surface. It then determines the normal to the surface.
                   If the interception with the surface is not valid the ray is terminated , otherwise it calls the reflection method.
                   Then it uses the ray object's append method to update the ray with a new position
                   and direction.
                """
		if ray.terminate == False:

		    intercept = self.intercept(ray)
		    if intercept is None:
		      ray.terminate = True # terminates ray
		    else:

          		if self.__curvature != 0:
              		        if self.__curvature > 0:
             			#calculate intercept position
                          		gradient =  intercept - self.__origin

                                elif self.__curvature < 0:
                                    gradient = -intercept + self.__origin
                                normal = gradient/np.linalg.norm(gradient) # normal to surface
                        else:
                                normal = np.array([0,0,-1])

          		limit = self.__aperture # radius curvature of surface in x-y plane

          		if  (intercept[0])*(intercept[0]) + (intercept[1])* (intercept[1]) > limit*limit :
         			print "no intercept"
         			ray.terminate = True
         			 # Need to stop it from going past without touching it and hitting the output plane.



          		else:
         			direction = self.reflection(ray,ray.k(), normal)
         			if direction is None:
     			            ray.terminate = True
     			        else:
         			    ray.append( intercept , direction )



class OutputPlane(OpticalElement):
        """ This class creates an output plane.
            It has an initilization and a propagate_ray method.

            """

	def __init__(self, z0 = 250):
	        """ The initilization takes two parameters: self and z0.
	            z0 determines the position of the output plane.
	            It can be set manually or set using the paraxial focus method.
	            This is needed when calculating the rms of the focus.
	        """
		self.__z0 = z0

	def propagate_ray(self,ray):
	        """ The propagate_ray method calculates where the ray
	            meets the output plane. It takes two parameters: self and ray.
	            The ray's p and k methods are called to obtain the ray's
	            position and direction. Then the intercept with the output
	            plane is determined and appended to the ray's using it's append method.
	        """
	        if ray.terminate == False:
	            p = ray.p()
	            k = ray.k()
	            if np.linalg.norm(k) == 0:
	                return None
	            elif k[2]<0: #reflection
	                 L = -(self.__z0-p[2])/(k[2])
	                 a = L*k + p
	                 ray.append(a , k)

	            else: # refraction
	                L = (self.__z0-p[2])/(k[2])
	                a = L*k + p
	                ray.append(a , k)
