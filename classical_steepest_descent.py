# In this script, the N queens problem is solved using the QUBO formalism and a classical D-Wave's solver

from N_queens.QUBO_queens_matrix import Q_matrix
from N_queens.draw_queens_module import draw_queens
from N_queens.N_queens_v4_all_sols import N_queens
import dimod
from dwave.samplers import SteepestDescentSolver
import numpy as np
import dimod.binary_quadratic_model
import pandas as pd
import time

start_chrono = time.time()
n_queens = 12
print(f'Chessboard size = {n_queens}x{n_queens}')
qubo = Q_matrix(n_queens)
Q_mat = qubo.get_Q_matrix()
J = qubo.np_matrix_to_dic_off_diag(Q_mat)
h = qubo.np_matrix_to_dic_diag(Q_mat)
problem = dimod.BinaryQuadraticModel(h,J,2*n_queens,dimod.BINARY)
solver = SteepestDescentSolver()
result = solver.sample(problem,num_reads=100)
#print(result)
zero_energy_solutions = result.filter(lambda sample: sample.energy == 0)
print(zero_energy_solutions)
#print(zero_energy_solutions)
end_chrono = time.time()
nsols = 3
nq = N_queens()
sol_chain = list(zero_energy_solutions._record[0][0])
queens_placed = sum(sol_chain)
print(f"Number of queens placed = {queens_placed}")
sol_vector = nq.transform_chain_to_tuple(sol_chain)
print('Solution: ', sol_vector)
energy = zero_energy_solutions.record[0][1]
print('Energy = ', energy)
validity = nq.check(sol_vector) and queens_placed == n_queens
print('Validity of the solution found: ', validity)
'''
for i in range(nsols):
    sol_chain = list(zero_energy_solutions._record[i][0])
    queens_placed = sum(sol_chain)
    print(f"Number of queens placed = {queens_placed}")
    sol_vector = nq.transform_chain_to_tuple(sol_chain)
    print('Solution: ', sol_vector)
    energy = zero_energy_solutions.record[i][1]
    print('Energy = ', energy)
    validity = nq.check(sol_vector) and queens_placed == n_queens
    print('Validity of the solution found: ', validity)
'''
print(f"Execution time: {end_chrono-start_chrono} s")