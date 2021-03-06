# Prueba #
##########

from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from scipy.special import gamma, j1, jv
from scipy.misc import factorial
from scipy.integrate import quad, simps

# parametros
N = 2
L = 3
Jmax = 4

f1 = 1.0
f2 = 0.2#0.1
wl = 532e-9
z0 = f2
fFR = 1.6
a = 5.e-2
b = 1000*a
k = 2*np.pi / wl
j = np.array([-1,0])#np.array([-1,0])
m = L*(1 + j*N)
print (m)
#m = 1
rmax = a*f2/f1

NN = 64/4
x = np.linspace(-2*rmax/1,2*rmax/1,NN)
#x = np.linspace(-5,5,NN)
X,Y = np.meshgrid(x,x)
R = np.sqrt(X**2+Y**2)
T = np.arctan2(Y,X)

def integrand(rho,m,r):
    alpha = 0.5*1j*k * (m/(L*fFR) + z0/f2**2 - 1/f1 - 1/f2)
    return j1(k*a/f1 * rho) * np.exp(-alpha * rho**2) * jv(m, k*r/f2 * rho)

def integrand_gauss(rho,m,r):
    w0 = a/10. 
    #z0 = f2 - m*f2**2 / (L * fFR) 
    alpha = 0.5*1j*k * (m/(L*fFR) + z0/f2**2 - 1/f2) + 1/w0**2
    return 1j * np.exp(-alpha * rho**2) * jv(m, k*r/f2 * rho) * rho
    

def do_image(m):
    #rho = np.linspace(0,10*a,1000000)
    rho = np.linspace(0,10*a,1000000)
    R_unique = list(set(R.flatten()))
    u_m = np.zeros((NN,NN)) + 1j*np.zeros((NN,NN))

    arg = np.pi * m / (L*N)
    K1 = (np.exp(-1j*arg) * np.sinc(arg)
          * (k*a/f2) * (1j**(3*abs(m)-2))
          * np.exp(1j*k*(f2+z0))
          * np.exp(1j*m*T))

    id = 0
    for r in R_unique:
        I2 = np.trapz(integrand_gauss(rho, m, r), x = rho)
        indices = np.where(R == r)
        u_m[indices] = I2
        print (id)
        id+=1

    return K1 * u_m

U_RT = 0 #U(r,theta)
for i in m:
    U_RT += do_image(i)

plt.imshow(abs(U_RT)**2, norm = colors.LogNorm())
plt.colorbar()
#plt.savefig("int_bessel.png")
plt.savefig("int_gauss_N%d_L%d.png"%(N,L))
plt.show()

#integral from 0 to inf of (J1(2pi*a*rho / lamb*f1) * exp(-alpha*rho**2) * Jm(k*rho*r/f2)) drho
