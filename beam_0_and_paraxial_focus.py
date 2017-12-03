import OpticalSystem as os
import NewBundle as Bundle
import plotting as plo


#rays
n = 5
rmax = 5 #ray parameters see genpolar and Newbundle modules for further details.
m = 4
initial_z = 0
direction = [0.0,0.0,1]
x1=0 # adjust the values of the offset to see different plots.
y1=0

rays = Bundle.bundle(n  ,rmax , m, initial_z, direction,x1,y1)
#surface elements
n1 = 1
n2 = 1.5168
#swap the argument of elements 1 to change the system of refractive elements.
convex_surface = [[100,0.02,n1,n2,50]] # must be used with 'use' set to no.
convexside_parameters = [[100,0.02,n1,n2,50],[105,0.00,n2,n1,50]]# curved side of planoconvex first
planoside_parameters = [[100,0.00,n1,n2,50],[105,-0.02,n2,n1,50]]# flat side of planoconvex first
bi_con_para = [[100,0.02,1,1.5168,50],[105,-0.02,1.5168,1,50]]# unoptimsed bi-convex lens
elements1 = os.elements(convexside_parameters) 

# system
System1 = os.System(elements1,use = 'yes') #set use to no for a diverging lens.
z0 = System1.paraxial_focus()
System1.propagate_ray(rays)
System1.Beam_plots(rays) # plots the x and y coordiates of the rays at z =0 and at the paraxial focus.
