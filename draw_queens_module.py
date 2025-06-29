# In this script, a chessboard is drew and N queens are placed according to the positions
# indicated by an NxN vector.

import math

def draw_queens(vector):
    N2 = len(vector)
    N = round(math.sqrt(N2))
    print("\n")
    j = 0
    for i in range(N2):
        if j == N-1:
            j = 0
            if vector[i]:
                print('1',end='\n')
            else:
                print('0',end='\n')
            if i != N2-1:
                print("-" * 4*N)
        else:
            j += 1
            if vector[i] :
                print('1', end=' | ')
            else:
                print('0', end=' | ')
    print("\n")         
            