# Analysis of the time performance of hybrid method to solve N queens problem

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

#Declaracion
n_queens = np.array([4,20, 24, 44, 64, 70, 100, 124, 148, 200])
energies = np.array([0,0,0,0,0,0,0,0,2,2])
times = np.array([0.5*(5.9+9.8), 7.5, 9.77, 16.86, 0.5*(23.87+21.34), 23.55, 36.1, 79.86, 182.83, 0.5*(528.81+810.69)])

#Filtrado
indices_0 = np.isin(energies, 0)
n_queens_0 = n_queens[indices_0]
times_0 = times[indices_0]
indices_2 = np.isin(energies, 2)
n_queens_2 = n_queens[indices_2]
times_2 = times[indices_2]

#plot
plt.plot(n_queens_0, times_0, 'sb', label='E = 0 solution')
plt.plot(n_queens_2, times_2, 'sr', label='E = 2 solution')
plt.xlabel('Number of rows/columns of the chessboard')
plt.ylabel('Arrangement time (s)')
plt.title('Time performance analysis of the Hybrid Method')
plt.legend()
plt.show()
