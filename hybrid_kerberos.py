# In this script, the N queens problem is solved using the QUBO formalism and a hybrid D-Wave's solver
# In V2, the matrix is passed through numpy arrays instead of a dictionary

from QUBO_queens_matrix import Q_matrix
from draw_queens_module import draw_queens
from N_queens_v4_all_sols import N_queens
import dimod
import hybrid
import numpy as np
import dimod.binary_quadratic_model
import pandas as pd
import time

start_chrono = time.time()
n_queens = 60
n_reads = 10
print(f'Chessboard size = {n_queens}x{n_queens}')
qubo = Q_matrix(n_queens)
Q_mat = qubo.get_Q_matrix()
end_chrono_matrix = time.time()
problem = dimod.BinaryQuadraticModel(Q_mat,offset=2*n_queens,vartype=dimod.Vartype.BINARY)
result = hybrid.KerberosSampler().sample(problem,num_reads=n_reads)
end_chrono = time.time()
print(result)
sol_chain = list(result.record[0][0])
print(f"Number of queens placed = {sum(sol_chain)}")
nq = N_queens()
sol_vector = nq.transform_chain_to_tuple(sol_chain)
#print('Solution: ', sol_vector)
energy = result.record[0][1]
print('Energy = ', energy)
print(f"Execution time: {end_chrono-start_chrono} s")
print(f"Matrix construction time: {end_chrono_matrix-start_chrono} s")