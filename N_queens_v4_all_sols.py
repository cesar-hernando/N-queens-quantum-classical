# Solution to the 8-queen problem (V4: Replacing the recursive function for the while loop implementation)

# The queens' positions are parametrised by an 8-tuple, where the index represents the chessboard column
# and the corresponding component value indicates the row. Thus, the 8-tuple can be viewed as a permutation
# of 8 elements. However, the diagonal restrictions in the chessboard lead to restrictions in the permutations
# space.

# The problem has been generalised to the arrangement of N queens on an NxN chessboard.

# In this script, all the possible solutions are found

import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
from scipy.optimize import curve_fit

# Function to adjust the graph
def exponential(x, a, b, c):
    return a + b*np.exp(c*x)

# This class has the method of checking the validity of a queens configuration in a chessboard. It checks
# whether any of queens is threatend by other queen. It also has the method of arranging N queens in an NxN
# chessboard from scratch.

class N_queens:
    def __init__(self):
        ...

    def check(self, positions):
        # Initialisation of the sets that contain the information about the diagonals and rows availability
        sum = set()
        difference = set()
        row = set()

        # All the columns are iterated over to check if they fulfil the restrictions
        for i in range(len(positions)):
            if positions[i] in row:                 # Is there another queen in that row?
                return False
            elif (positions[i] + i) in sum:         # Is there another queen in that negative-slope diagonal?
                return False
            elif (i - positions[i]) in difference:  # Is there another queen in that positive-slope diagonal?
                return False
            else:                                   # If it's a safe position, the respective restrictions are added
                row.add(positions[i])               
                sum.add(positions[i] + i)
                difference.add(i - positions[i])
        return True                                 # If any queen is threatened, the method returns True
                                                    # It returns False otherwise 
    
    # The algorithm does 1 + 3 + 6 + 9 + ... + 21 = 1 + 3*(1 + 2 + .. + 7) = 1 + 3*(8-1)*(8/2) = 85 iterations
    # at most approximately in order to check if a certain 8-queen configuration is valid.
    # Hence, the number of iterations scales quadratically with the number of queens (or rows/columns).

    def transform_matrix_to_tuple(self, matrix):
        nrows = matrix.shape[0]
        vector = []
        for i in range(nrows):
            a = False
            for j in range(nrows):
                if matrix[j,i] == 1:
                    vector.append(j)
                    a = True
            if not(a):
                vector.append(-1)
        return vector
    
    def transform_chain_to_tuple(self, chain):
        numel = len(chain)
        N = round(math.sqrt(numel))
        vector = []
        for i in range(numel):
            if chain[i] == 1:
                vector.append(i % N)
        return vector

    def arrange(self, n_rows):

        # Initialise the solutions list
        solutions = []
        
        # Initialise the positions list
        positions = []

        # Initialise the sets cointaining the row and diagonals availability
        row = {x for x in range(n_rows)}
        sum = {x for x in range(2*n_rows - 1)}
        difference = {x for x in range(-n_rows + 1, n_rows)}
        
        # Initialise different variables that monitor the arrangement of the queens
        iterations = 0
        end = False
        # i represents the column where the queen is placed, whereas j runs over the available rows
        # j_list keeps track of the rows tried out for each column
        i = 0
        j = 0
        j_list = [0 for _ in range(n_rows)]

        # A maximum number of iterations is set (it is not essential and it could be replace by a while True:, 
        # although it may be used as a way of limiting the execution time)
        iterations_limit = 10**10
        
        while iterations < iterations_limit and (not end):

            # When all the queens are arranged, we look up for other solutions changing the last column, 
            # and if it is not possible, the previous one, until all the possible solutions have been 
            # checked out
            if i == n_rows:
                solution = tuple(positions)
                solutions.append(solution)
                # The last queen arranged is removed 
                aux = positions[-1]
                del positions[-1]
                # The last restrictions imposed are lifted
                row.add(aux)
                sum.add(i-1+aux)
                difference.add(i-1-aux)
                # Another row will be tried out in the previous column
                i -= 1
                # The next row available will be the one selected
                j = j_list[i]+1

            # For each column, the rows that fulfil the row and diagonal restrictions are filtered
            rows_available = [x for x in row if (x+i in sum) and (i-x in difference)]
            # This list has to be sorted for the algorithm coherence
            rows_available.sort()
            
            # If there are rows available in the column and not all the rows have been tried out,
            # the queen is placed
            if j < len(rows_available):
                aux = rows_available[j]
                # The queen is placed and the corresponding restrictions are taken into account
                positions.append(aux)
                row.discard(aux)
                sum.discard(i+aux)
                difference.discard(i-aux)
                # The index of the chosen row in the available rows list is stored
                j_list[i] = j
                # In the next iteration a queen may be placed in the next column
                i += 1
                # The row chosen will be be first one from the available rows list
                j = 0

            else:           # If there no more available rows to try out in the column
                if i > 0:   # and the column is not the 0-th one

                    # The last queen arranged is removed 
                    aux = positions[-1]
                    del positions[-1]
                    # The last restrictions imposed are lifted
                    row.add(aux)
                    sum.add(i-1+aux)
                    difference.add(i-1-aux)
                    # Another row will be tried out in the previous column
                    i -= 1
                    # The next row available will be the one selected
                    j = j_list[i] + 1
                    
                else:           # If all the possibilities have been checked out and there are no positions left
                                # to place the 0-th queen          
                    
                    # The loop ends without success
                    print(f"There are no more valid configurations of {n_rows} queens in a {n_rows}x{n_rows} chessboard")
                    end = True
            
            # The number of iterations is tracked
            iterations += 1

        # The method returns the success and end boolean variables as well as the number of iterations needed
        return solutions, end, iterations

    def analysis(self, max_num_queens):
        times = []
        nsols = []
        num_queens = range(4, max_num_queens+1)
        for num in num_queens:
            start_time = time.time()
            solutions, end, iterations = self.arrange(num)
            end_time = time.time()
            if end:
                times.append(end_time - start_time)
                nsols.append(len(solutions))
            else:
                times.append(f'> {end_time - start_time}')
                nsols.append(f'> {len(solutions)}')

        df = pd.DataFrame(list(zip(num_queens, times, nsols)), columns=["Number of queens", "Arrangement time", "Number of solutions"])
        path = f'C:/Users/a929493/OneDrive - Eviden/Documentos/N_queens/tablas_csv_all_sols/{max_num_queens}_queens_max.csv'
        df.to_csv(path)
        print("csv file created correctly")
    
    def plot_and_fit_graph(self, max_num_queens):
        path = f'C:/Users/a929493/OneDrive - Eviden/Documentos/N_queens/tablas_csv_all_sols/{max_num_queens}_queens_max.csv'
        df = pd.read_csv(path, index_col=0)
        num_queens = df["Number of queens"]
        times = df["Arrangement time"]
        #p_opt, p_cov = curve_fit(exponential, np.array(num_queens), np.array(times))
        #a_opt, b_opt, c_opt = p_opt
        #x_fit = np.array([i * 0.1 for i in range((max_num_queens + 1)*10 + 1)])
        #y_fit = exponential(x_fit, a_opt, b_opt, c_opt)
        plt.plot(num_queens, times, '.--', label='Experimental data')
        #plt.plot(x_fit, y_fit, label = f'Exponential fit: $T = {a_opt:.2f} + {b_opt:.2e} x 2^{{{c_opt:.2f}N}}$')
        plt.xlabel('Number of queens/rows/columns')
        plt.ylabel('Arrangement time (s)')
        plt.title('Time performance analysis of the N queen arrangement algorithm')
        #plt.legend()
        plt.show()

        nsols = df["Number of solutions"]
        plt.plot(num_queens, nsols, '.--', label='Experimental data') 
        plt.xlabel('Number of queens/rows/columns')
        plt.ylabel('Number of solutions')
        plt.title('Analysis of the number of solutions of the queens problem')
        #plt.legend()
        plt.show()  
        


# Creation of an object of the class N_queen
n_queens_problem = N_queens()
print("\nWelcome to the N-queens problem")
# Select either the arrange or check mode
mode = 'imported'  
print(f"Mode = {mode}")         
num_queens = 12

if mode == 'check':
    # In this section, the validity of different queens configurations can be checked
    configuration_1 = [14, 12, 10, 13, 5, 3, 1, 11, 2, 6, 9, 0, 8, 4, 7]
    print(f"\nThe {len(configuration_1)}-queen configuration is: {n_queens_problem.check(configuration_1)}")

elif mode == 'arrange':
    start_chrono = time.time()
    solutions, end, iterations = n_queens_problem.arrange(num_queens)
    end_chrono = time.time()
    print(f'\nN = {num_queens}')
    print(f'End of the arrangement algorithm: {end}')
    print(f'Number of iterations completed: {iterations}')
    print(f'Arrangement time: {end_chrono - start_chrono}')
    print(f'The number of solutions for {num_queens} queens is: {len(solutions)}')
    a = input('Do you want to see all the possible solutions (y/n): ')
    if a.lower() == 'y':
        print("The possible solutions are: ")
        for solution in solutions:
            print(solution)
    print('\n')

elif mode == 'analysis':
    n_queens_problem.analysis(num_queens)

elif mode == 'plot':
    n_queens_problem.plot_and_fit_graph(num_queens)
