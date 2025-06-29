# In this module, the QUBO matrix for the N_queens problem is created
# In this version, I create matrices of type int8 to optimize use of memory
import numpy as np

class Q_matrix:
    def __init__(self, N):
        self.N = N

    def get_Q_matrix(self):
        N = self.N
        # Initialisation of the N^2xN^2 Q matrix
        Q = np.zeros((N*N,N*N),dtype=np.int8)
        # Sum of the different terms
        Q += np.kron(np.eye(N,dtype=np.int8), np.ones((N,N),dtype=np.int8))      # Q_0a  Q_0 -> no queens in the same row
        Q -= 2*np.eye(N*N,dtype=np.int8)                          # Q_0b
        Q += np.kron(np.ones((N,N),dtype=np.int8), np.eye(N,dtype=np.int8))      # Q_1a  Q_1 -> no queens in the same column
        Q -= 2*np.eye(N*N,dtype=np.int8)                          # Q_1b
        Q += self.get_Q_diag('Q_2a')                # Q_2a
        Q -= np.eye(N*N,dtype=np.int8)                            # Q_2b
        Q += self.get_Q_diag('Q_3a')                # Q_3a
        Q -= np.eye(N*N,dtype=np.int8)                            # Q_3b
        # Return the final matrix
        return Q
    
    def get_Q_diag(self, mode):
        N = self.N
        # Concatenation of the NxN blocks
        # Firstly, the concatenation is performed horizontally, and then the row is appended to the above matrix
        # The variable aux stores each of the rows of block matrices
        # For each mode (term of Q), A is slightly different
        for i in range(N):
            aux_matrix = self.A(i,0, mode)         
            for j in range(1,N):
                aux_matrix = np.block([aux_matrix, self.A(i, j, mode)])
            
            if i == 0:
                Q_2a = aux_matrix
            else:
                Q_2a = np.block([[Q_2a],[aux_matrix]])

        return Q_2a

    def A(self, i, j, mode):
        # For each mode, the 1s are placed in different position, where a condition is satisfied
        # The conditions for each mode only differ in a sign
        if mode == 'Q_2a':
            sign = 1
        else:
            sign = -1

        N = self.N
        A = np.zeros((N,N),dtype=np.int8)
        for k in range(N):
            for l in range(N):
                if k-l == sign*(j-i):
                    A[k,l] = 1
        
        return A
    
    def np_matrix_to_dic_off_diag(self, Q):
        matrix_dic = {}
        n_rows = Q.shape[0]
        for i in range(n_rows):
            for j in range(i+1,n_rows):
                matrix_dic[(i,j)] = Q[i,j]
                matrix_dic[(j,i)] = Q[j,i]
        return matrix_dic
    
    def np_matrix_to_dic_diag(self, Q):
        matrix_dic = {}
        n_rows = Q.shape[0]
        for i in range(n_rows):
            matrix_dic[i] = Q[i,i]
        return matrix_dic
    