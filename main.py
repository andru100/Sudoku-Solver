from utils import *
import sys
sys.setrecursionlimit(5000)

#from utils import *

#zip boxes and gtidvalues and replace empty boxes with all poss vaalues 123456789
test = grid_values(gridvar)

print (test)

#create copy for constarin prop test

test1 = test

# use the copied display fun to display dict as board

display(test)

# run eliminate all values from peer boxes if its the only one in a box eg len of boxval ==1
eliminatedver = eliminate(test)

display(eliminatedver)

#run lastone where the number only appears once in possible values of it unit eg row column or 3x3

lastonever = lastone(eliminatedver)

display(lastonever)

# run a loop of eliminate and last one checking that boxes are being solved or quit with stalled = true
propagation = reducepzl(test1)

print ('im getting smart i propogated')

display(propagation)

# declare harder suduko grid data
grid2 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
#zip boxes and gtidvalues and replace empty boxes with all poss vaalues 123456789
hrdrpzl = grid_values(grid2)

#run propagation of eliminate and search reducepzl on harder sudoku.

propagation2 = reducepzl(hrdrpzl)

display(propagation2)

print ('damn thats harder')

hrdpzl2 = grid_values(grid2)
display(search(hrdpzl2))