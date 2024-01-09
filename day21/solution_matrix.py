from functools import cache
import numpy as np
import scipy.sparse as sp
import cProfile

class Garden:
    def __init__(self, grid):
        self.grid = grid
        self.h = len(self.grid)
        self.w = len(self.grid[0])
        self.s = self.get_starting_square()

    def get_starting_square(self):
        for r in range(self.h):
            if 'S' in self.grid[r]:
                return r, self.grid[r].index('S')

    @cache
    def get_accessible_neighbors(self, row, col):
        adj = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = dr + row, dc + col
            if 0 <= nr < self.h and 0 <= nc < self.w:
                if self.grid[nr][nc] == '#':
                    continue
                else:
                    adj.append((nr, nc))
        return adj

    def initialize_matrix(self):
        n = self.h * self.w
        adj = np.zeros((n, n), dtype=bool)
        for r in range(self.h):
            for c in range(self.w):
                for edge in self.get_accessible_neighbors(r, c):
                    adj[r * self.w + c][edge[0] * self.w + edge[1]] = True
        return adj

    def get_positions_after_n_moves(self, n):
        sq_r, sq_c = self.get_starting_square()
        sq = sq_r * self.w + sq_c
        adj = self.initialize_matrix()
        sparse_matrix = sp.csr_matrix(adj)
        matrix_pow = sparse_matrix ** (n)
        dense_matrix_pow = matrix_pow.toarray()
        return np.count_nonzero(dense_matrix_pow[sq])
    
def main_part_one():
    with open('day21/input.txt', 'r') as file:
        lines = file.read().splitlines()
    g = Garden(lines)
    return g.get_positions_after_n_moves(64)

if __name__ == '__main__':
    #cProfile.run('print(main_part_one())')
    print(main_part_one())

"""
    I tried taking a matrix eponentiation approach to count the nonzero indices
    and finding a cycle however hashing the 17161x17161 matrix is quite slow (I
    tried to use the a tuple of the indices of nonzero elements for my key)
    and I didn't realize the prompt mentioned the map repeats infinitely.
    So this solution is a dead end, but I'd like to revisit the concept of
    hashing sparse matrices later on as well as run benchmarks on the same
    computations between sparse and dense matrices. Mathematically, dense 
    matrices store 8 bytes per entry while sparse matrices store 12 bytes per
    entry, so there is a theoretical 67% sparsity threshold below which sparse
    matrices should be more memory and compute efficient, without considering 
    for interpreter/translation overhead.

    def find_cycle(self, n):
        sq_r, sq_c = self.get_starting_square()
        sq = sq_r * self.w + sq_c
        adj = self.initialize_matrix()
        sparse_end_matrix = sparse_adj_matrix = sp.csr_matrix(adj)
        seen = {}
        step = 1
        while True:
            step += 1
            sparse_end_matrix = sparse_end_matrix.astype(bool).dot(sparse_adj_matrix)
            rows, cols = sparse_end_matrix.nonzero()
            non_zeros = 0
            #non_zeros = tuple((row, col) for row, col in zip(rows, cols))
            print(step)
            if non_zeros in seen:
                print(step)
                cycle = step - seen[non_zeros]
                break
            else:
                #seen[non_zeros] = step
                pass
        steps_left = (n - seen[non_zeros]) % cycle
        matrix_pow = sparse_adj_matrix ** (steps_left)
        dense_matrix_pow = matrix_pow.toarray()
        return np.count_nonzero(dense_matrix_pow[sq])
        """
