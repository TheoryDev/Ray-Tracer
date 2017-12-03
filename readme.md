# In this project I simulated a laser beam interacting with different lenses/mirrors to study refraction, reflection and diffraction.
There is also optimisation to find the optimal biconvex lens

`The Scripts are best run in the terminal using Python 2. When running the 3d plots make sure that the plot is displayed outside of the terminal so that you can change the orientation.`

## Modules used to model physics:
* raytracer.py
* plotting.py
* NewBundle.py
* genpolar.py
* OpticalSystem.py

## Scripts:
* beam_0_and_paraxial_focus.py
* Standard lens.py
* rms_scale_graphs.py
* Optimization.py
* Reflection.py

Description of modules used to model the physics.

### `raytracer.py:`

This module simulates a raytracer.
It creates: ray objects, refractive optical surface elements and Output planes.
In addition, it contains methods to calculate where the rays intercept the Optical elements and outputplane.
Then methods to determine the effect at the interface.
Then the propagate_ray method propogates the rays through optical elements to the output plane.

### `OpticalSystem.py:`

This module is used to create optical systems. The elements class is used to create
a list of spherical refraction elements. The System class takes an elements object
an creates a system object. The systems class has methods to propagate rays.
Finally, the module has other methods outside of the classes to calculate rms and
for lens optimisation.

### `Genpolar.py:`

This module is used to create the initial x and y coordinates
of each ray in a beam of rays. It contains two methods rtpairs and rt uniform.
rtpairs creates rings of points.
rtuniform calls rtpairs and creates a uniform disc of points.

### `NewBundle.py:`

This module is used to create a list of ray objects.
It uses the rtuniform method in the genpolar module to
create the intial x and y coordinates.The coordinates are then used
in the creation of a list of instances of the Ray class from the ray tracer module.
x1 and y1 are used to offset the disc of x and y positions.

### `plotting.py:`

This module contains various plotting functions that are used by the OpticalSystem graphs to produce plots.
The methods are called from outside of the module in practice.

Description of scripts:

### `standard lens.py:`

This script is used to model different lens. A list of rays is created that is an approximation
to a beam of rays. Alternatively ray objects can be created and then a list of them made
to propagate them through the system. The list can contain one or many rays.
Examples of all 3 cases are shown. Then a list of refractive surface elements is created using
a list where each element is a list of surface element parameters. There are several examples to use an
example change the argument of elements1 to the list of parameters for the desired setup. An example is convexside_parameters.
The script then creates a System class element using the elements instance as a parmeter.
In additon to this the Systems class automatically places the output plane at the paraxial focus of the system.
However,this is not always desired the parameter use allows the user to decided wether or not to use the paraxial focus.
If they set use='yes' it is used if they set use='no' it is not used and the parameter z_choice also the outputplane
positon to be manually set.
Finally the script produces plots detailing the propagation of the rays and calculates the root mean square
and its associated error.

<p align="center"> 
 <img src="/images/standard.png" height= "400" width="400"> <img src="/images/stanZvY.png" height= "400" width="400">
 </p>

### `beam_0_and_paraxial_focus.py:`

This script is used to create a beam of rays that are then propagated through a system of spherical refracting elements.
The system class object has a Beam_plots method that is called to produced plots of the x and y coordinates of the rays
at z=0 and at the paraxial focus.

<p align="center"> 
 <img src="/images/paraxial.png" height= "400" width="600"> 
 </p>


### `rms_scale_graphs.py:`

This script is used to produce a plot of the rms and diffraction scale against beam diameter.
This is done for a System of refractive optical surface elements.
The get_data_rms method creates a list of rms values and beam diamters for the specified system.
Then the plot_rms and plot_diffraction methods are used with axes and subplots to create a graph
witht the rms and diffraction scale against beam diameter.

<p align="center"> 
 <img src="/images/rms.png" height= "400" width="400"> 
 </p>

### `Optimisation.py:`

This script is used to optimse a biconvex focal lens.
The optimisation varies the curvature of the two spherical refraction
surfaces to minmise the rms value returned. It calls the lens optimisation function
from the OpticalSystem module. The focus of the biconvex lens is set to that of the paraxial
focus of the planoconvex lens when light is incident on the curved size. This is so that comparison
of the rms values will make sense.

### `Reflection.py`

This script is used to create relective optical surface elements. 
A beam of rays was created and reflected off of the surface. 
The reflection class was developed in a late stage in the project and so it is not integrated
with the OpticalSystem class due to time constraints. The example below is the paths of a bundle of rays reflected by a concave mirror, on the left is a plot with a side ways view and on the right is a 3d plot. We can see that the rays which hit the mirror head on are dispersed in different directions.

<p align="center"> 
 <img src="/images/mirror.png" height= "400" width="400"> <img src="/images/mirror3d.png" height= "400" width="400">
 </p>
