# Analysis of the time performance of the simulated annealing approach to the N queens problem

import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np

def quad(x, a, b, c):
    return a+b*x+c*x*x

def exponential(x, a, b, c):
    return a + b*np.exp(c*x)

def lineal(x, a, b):
    return a+b*x

def pol_4(x, a, b):
    return a + b*x**4

# Sim annealing
max_queens = 244
step = 20
path = f'C:/Users/a929493/OneDrive - Eviden/Documentos/N queens/N_queens_QUBO/Simulated_Annealing/{max_queens}_queens_sim_ann_step_{step}.csv'
df = pd.read_csv(path, index_col=0)
num_queens = np.array(df["Number of queens"][:-1])
times = np.array(df["Arrangement time"][:-1])
energies = np.array(df["Energy"][:-1])

# Filtro los puntos de energia 0 y 2
indices_0 = np.isin(energies, 0)
num_queens_0 = num_queens[indices_0]
times_0 = times[indices_0]
indices_2 = np.isin(energies, 2)
num_queens_2 = num_queens[indices_2]
times_2 = times[indices_2]

# Hybrid
#Declaracion
#Declaracion
n_queens_h = np.array([4,20, 24, 44, 64, 70, 100, 124, 148, 200,224,244])
energies_h = np.array([0,0,0,0,0,0,0,0,2,2,0,0])
times_h = np.array([0.5*(5.9+9.8), 7.5, 9.77, 16.86, 0.5*(23.87+21.34), 23.55, 36.1, 79.86, 182.83, 0.5*(528.81+810.69),901.79,1185.44])

#Filtrado
indices_h_0 = np.isin(energies_h, 0)
n_queens_h_0 = n_queens_h[indices_h_0]
times_h_0 = times_h[indices_h_0]
indices_h_2 = np.isin(energies_h, 2)
n_queens_h_2 = n_queens_h[indices_h_2]
times_h_2 = times_h[indices_h_2]

'''
l_num_queens = np.log(num_queens)
l_times = np.log(times)
p_opt, p_cov = curve_fit(lineal, l_num_queens, l_times)
a_opt, b_opt= p_opt
x_fit = np.log(np.array([i * 0.1 for i in range(40,(max_queens + 1)*10 + 1)]))
y_fit = lineal(x_fit, a_opt, b_opt)
plt.plot(l_num_queens, l_times, '.--', label='Experimental data')
plt.plot(x_fit, y_fit, label = f'Linear fit: $logT = {a_opt:.3f} + {b_opt:.3f}logN $')
plt.xlabel('Number of queens/rows/columns')
plt.ylabel('Arrangement time (s)')
plt.title('Time performance analysis of Simulated Annealing')
plt.legend()
plt.show()
'''

p_opt, p_cov = curve_fit(pol_4, num_queens, times)
a_opt, b_opt= p_opt
x_fit = np.array([i * 0.1 for i in range(30,(max_queens + 1)*10 + 1)])
y_fit = pol_4(x_fit, a_opt, b_opt)
#plt.plot(num_queens, times, '.--', label='Experimental data')
#plt.plot(x_fit, y_fit,'-k', label = f'Curve fit: $T = {a_opt:.2f} + {b_opt:.2e}N^4 $')
plt.plot(num_queens_0, times_0, 'sb')
plt.plot(num_queens_2, times_2, '^b')
plt.plot(num_queens, times, '--b', label='Simulated Annealing')
plt.plot(n_queens_h_0, times_h_0, 'sr')
plt.plot(n_queens_h_2, times_h_2, '^r')
plt.plot(n_queens_h, times_h, '--r', label='Hybrid Method')
plt.xlabel('Number of rows/columns of the chessboard')
plt.ylabel('Arrangement time (s)')
#plt.title('Time performance analysis of Simulated Annealing')
plt.legend()
plt.show()

    