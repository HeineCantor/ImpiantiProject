import matplotlib.pyplot as plt
import numpy as np

x = np.arange(0, 8000000, 100)

MTTFa = 500 * 3600
MTTFb = 9000 * 3600
MTTFc = 10000 * 3600

# y = -np.e**(-x/100)+2*np.e**(-x/200)
# z = np.e**(-x/100)-8*np.e**(-7/800*x)+24*np.e**(-3/400 * x)-32*np.e**(-x/160)+16*np.e**(-x/200)

# y = 1-(1-np.e**(-4*x/2880000))**(8)    # Rsys1 <<-----
# z = (1-(1-np.e**(-x/2880000))**2)**(4)

# y = -2*np.e**(-3*x)+3*np.e**(-2*x)
# z = 3*np.e**(-2*x)+np.e**(-3*x)-3*np.e**(-4*x)-3*np.e**(-5*x)+np.e**(-6*x)+3*np.e**(-7*x)-np.e**(-9*x)

# y = 1 - (1-np.e**(-(x/(500*3600)+x/(9000*3600))))*(1-np.e**(-(x/(500*3600)+x/(10000*3600))))
# z = (1-(1-np.e**(-x/(9000*3600)))*(1-np.e**(-x/(10000*3600))))*np.e**(-x/(500*3600))

# y = (1-(1-np.e**(-x/MTTFb))*(1-np.e**(-x/MTTFa)))*np.e**(-x/MTTFa)
# z = np.e**(-x/MTTFa)

# y = (1-(1-np.e**(-x/MTTFb))*(1-np.e**(-x/MTTFa)))*np.e**(-(x/MTTFa+x/MTTFb))
# z = np.e**(-(x/MTTFa+x/MTTFb))

y = 1-(1-np.e**(-(x/MTTFa+x/MTTFb)))*(1-np.e**(-x/MTTFa))
z = np.e**(-x/MTTFa)

plt.plot(x, y, label="Rsys1(t)")
plt.plot(x, z, label="Rsys2(t)")

plt.legend()
plt.xlabel("time (s)")

plt.grid()
plt.show()