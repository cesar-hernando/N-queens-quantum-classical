# In this script, the N queens problem is solved using the QUBO formalism and a hybrid D-Wave's solver
# In V2, the matrix is passed through numpy arrays instead of a dictionary

from QUBO_queens_matrix import Q_matrix
from draw_queens_module import draw_queens
from N_queens_v4_all_sols import N_queens
import dimod
from dwave.system import LeapHybridSampler
import numpy as np
import dimod.binary_quadratic_model
import pandas as pd
import time

start_chrono = time.time()
n_queens = 130
print(f'Chessboard size = {n_queens}x{n_queens}')
qubo = Q_matrix(n_queens)
problem = dimod.BinaryQuadraticModel(qubo.get_Q_matrix(),offset=2*n_queens,vartype=dimod.Vartype.BINARY)
sampler = LeapHybridSampler()
result = sampler.sample(problem)
end_chrono = time.time()
sol_chain = list(result.record[0][0])
print(f"Number of queens placed = {sum(sol_chain)}")
nq = N_queens()
sol_vector = nq.transform_chain_to_tuple(sol_chain)
#print('Solution: ', sol_vector)
energy = result.record[0][1]
print('Energy = ', energy)
validity = nq.check(sol_vector)
print('Validity of the solution found: ', validity)
print(f"Execution time: {end_chrono-start_chrono} s")
