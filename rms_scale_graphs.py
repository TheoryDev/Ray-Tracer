import OpticalSystem as os
import NewBundle as Bundle
import plotting as plo

#surfaces elements
n1 = 1
n2 = 1.5168
convex_surface = [[100,0.02,n1,n2,50]] # must be used with 'use' set to no.
convexside_parameters = [[100,0.02,n1,n2,50],[105,0.00,n2,n1,50]]# curved side of planoconvex first
planoside_parameters = [[100,0.00,n1,n2,50],[105,-0.02,n2,n1,50]]# flat side of planoconvex first
bi_con_para = [[100,0.02,1,1.5168,50],[105,-0.02,1.5168,1,50]]# unoptimsed bi-convex lens
elements1 = os.elements(convexside_parameters)

#System
System1 = os.System(elements1)
z0 = System1.paraxial_focus()
RMS=System1.get_data_RMS(rmax=6,step=0.05) # RMS is a list of rms values and beam diameters.
ax=plo.plt.subplot(111)
plo.plot_rms(RMS,ax)
plo.plot_diffraction(RMS,588E-6,ax,z0)
plo.plt.ylabel('/mm')
plo.plt.title('')
ax.legend()
plo.plt.show()
# plots a graph of the rms and diffraction scale against beam diameter.
