import OpticalSystem as os
import NewBundle as Bundle
import raytracer as rt
#rays
n = 5
rmax = 5 # Parameters of the beam of rays see genpolar and NewBundle modules.
m = 4
initial_z = 0 # Where the rays start on the z-axis
direction = [0.0,0.0,1.] # Initial direction
x1=0 # adjust the values of the offsets to see different plots.
y1=0
rays = Bundle.bundle( n  ,rmax , m, initial_z, direction,x1,y1 )
# can also manually make ray objects then make a list of them. This list can contain one ray.
#surface elements
n1 = 1.
n2 = 1.5168
# See spherical refraction class for description of the intialization parameters
# swap the arguement of elements1 to these lists to model the corresponding system of refractive surfaces.
convex_surface = [[100,0.02,n1,n2,50]]
concave_surface = [[100,-0.02,n1,n2,50]]
plane_surface = [[100,0.0,n1,n2,50]]
convexside_parameters = [[100,0.02,n1,n2,50],[105,0.00,n2,n1,50]] #curved side of planoconvex first
planoside_parameters = [[100,0.00,n1,n2,50],[105,-0.02,n2,n1,50]] #flat side of planoconvex first
bi_con_para = [[100,0.02,1,1.5168,50],[105,-0.02,1.5168,1,50]]# unoptimsed bi-convex lens

elements1 = os.elements(convexside_parameters)

#System
System1 = os.System(elements1,z_choice=198.452700178,use = 'yes')
z0 = System1.paraxial_focus()
System1.propagate_ray(rays)
System1.plot(rays) # plots graphs

rms_and_error= os.root_mean_square_error(rays) # prints (rms,rms_error)
print rms_and_error
