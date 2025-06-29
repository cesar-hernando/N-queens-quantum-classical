# In this script, the N queens problem is solved using the QUBO formalism and a classical D-Wave's solver

from QUBO_queens_matrix_v2 import Q_matrix
from draw_queens_module import draw_queens
from N_queens_v4_all_sols import N_queens
import dimod
from dwave.samplers import SimulatedAnnealingSampler
import numpy as np
import dimod.binary_quadratic_model
import pandas as pd
import time

times = []
solution_found = []
energies = []
max_num_queens = 244
step = 20
n_reads = 1
num_queens_list = range(244, max_num_queens+1, step)
for n_queens in num_queens_list:
    start_chrono = time.time()
    qubo = Q_matrix(n_queens)
    problem = dimod.BinaryQuadraticModel(qubo.get_Q_matrix(),offset=2*n_queens,vartype=dimod.Vartype.BINARY)
    solver = SimulatedAnnealingSampler()
    result = solver.sample(problem,num_reads=n_reads)
    #print(result)
    zero_energy_solutions = result.filter(lambda sample: sample.energy == 0)
    end_chrono = time.time()
    #print(zero_energy_solutions)
    if len(zero_energy_solutions) > 0:
        solution_found.append(True)
    else:
        solution_found.append(False)

    energy = result.record[0][1]
    #energies.append(energy)
    #times.append(end_chrono-start_chrono)
    print(f'Best energy of N = {n_queens}: {energy}')
    print(f"Time: {end_chrono-start_chrono}")

#df = pd.DataFrame(list(zip(num_queens_list, times, energies, solution_found)), columns=["Number of queens", "Arrangement time", "Energy", "Validity"])
#path = f'C:/Users/a929493/OneDrive - Eviden/Documentos/N queens/N_queens_QUBO/Simulated_annealing/{max_num_queens}_queens_sim_ann_step_{step}_{n_reads}_reads.csv'
#df.to_csv(path)

    # Comprobar la validez de las soluciones con el algoritmo de comprobación clásico
    nq= N_queens()
    sol_chain = list(result._record[0][0])
    queens_placed = sum(sol_chain)
    print(f"Number of queens placed = {queens_placed}")
    sol_vector = nq.transform_chain_to_tuple(sol_chain)
    validity = nq.check(sol_vector) and queens_placed == n_queens
    #print('Solution: ', sol_vector)
    #energy = zero_energy_solutions.record[0][1]
    #print('Energy = ', energy)
    print('Validity: ',validity)
    #print(f"Execution time: {end_chrono-start_chrono} s")
