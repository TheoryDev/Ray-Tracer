import raytracer as rt
import plotting as plo
import NewBundle as Bundle

#This script produces reflects a beam of rays.
#rays
x1=0 #offset of beam or ray positions
y1=0
rays = Bundle.bundle(n=5 , rmax=5  , m=4, initial_z = 0, direction = [0.1,0.0,1],x1=0,y1=0)

#surface
z0=100
curvature = -0.02 # change to 0.02 to see convex reflective surface, set to 0.0 to see the plane reflective surface
aperture = 50
surface =rt.SphericalReflection(z0,curvature,aperture)

#Output
Output = rt.OutputPlane()

x,y,z = [],[],[]
for ray in rays:
    surface.propagate_ray(ray)
    Output.propagate_ray(ray)

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
