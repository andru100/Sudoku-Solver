from utils import *
import sys
sys.setrecursionlimit(5000)

#Here I solve a simple sudoku without depth first search

#zip boxes and grid values then replace empty boxes with all possible values 123456789
test = grid_values(gridvar)

# Recursively run funcs eliminate and last one, checking that boxes are being solved or quit
propagation = reducepzl(test)

print('Here a simple sudoku is solved without depth first search. \n')

display(propagation)

# declare harder suduko grid data and repeat process except this time implement the DFS search function in utils.py 
grid2 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'

hrdrpzl = grid_values(grid2)

propagation2 = reducepzl(hrdrpzl)

#Display the results of the harder sudoku using previous solution without depth first search
print('\nHere we can see that depth first search is needed as the board is not solved: \n')
display(propagation2)

print('\nHere we can see depth first search has solved the puzzle:\n')
hrdpzl2 = grid_values(grid2)

display(search(hrdpzl2))