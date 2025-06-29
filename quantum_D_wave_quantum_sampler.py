

from QUBO_queens_matrix import Q_matrix
from draw_queens_module import draw_queens
from N_queens_v4_all_sols import N_queens
import dimod
from dwave.system import DWaveSampler
from dwave.system import EmbeddingComposite
import numpy as np
import dimod.binary_quadratic_model
import pandas as pd


n_queens = 7
qubo = Q_matrix(n_queens)
Q_mat = qubo.get_Q_matrix()
problem = dimod.BinaryQuadraticModel(Q_mat,offset=2*n_queens,vartype=dimod.Vartype.BINARY)
sampler = EmbeddingComposite(DWaveSampler())
nreads = 100
result = sampler.sample(problem, num_reads=nreads)
# Filter the solutions with energy less or equal to 4
print(result)
zero_energy_solutions = result.filter(lambda sample: sample.energy == 0)
#print(result.first.energy)
for solution in zero_energy_solutions:
    chain = [solution[square] for square in solution]
    draw_queens(chain)
    vector = N_queens().transform_chain_to_tuple(chain)
    if len(vector) >= n_queens:
        sol_validity = N_queens().check(vector)
    else:
        sol_validity = False
    print(f"Validity of the solution: {sol_validity}")



#df = pd.DataFrame(zero_energy_solutions, columns=[f"col {col}" for col in range(n_queens**2)] + ['Energy', 'Num_oc'])
df = pd.DataFrame(zero_energy_solutions)
path = f'C:/Users/a929493\OneDrive - Eviden/Documentos/N_queens_QUBO/{n_queens}_queens_{nreads}_reads.csv'
df.to_csv(path)
