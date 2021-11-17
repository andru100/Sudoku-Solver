
# create string of row and column labels
rows = 'ABCDEFGHI'
cols = '123456789'

# A list of gridvalues where a "." represents an empty box that needs to be solved
gridvar = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'

# create helper function that uses rows and colums and creates grid box names. eg A1 A2 A3
def cross (a,b) :

    return [x+z for x in a for z in b]


# USe the helper function to create a list with all box numbers in grid
boxes = cross(rows, cols)

# create list with row names a1.a2.a3.a4 etc
row_units = [cross(x, cols) for x in rows]

# Create a list with column names a1,b1,c1,d1 etc
column_units = [cross(rows, a) for a in cols]

# create boxes of 3x3 eg. a1,a2,a3,b1,b2.b3
square_units = [cross(a,b) for a in ('ABC', 'DEF', 'GHI') for b in ('123', '456', '789')]

# create a list with combo of all possible rows cols and boxes
unit_list = row_units  + column_units  + square_units

#create a dictionary where each box is the key and value is
# a list of 3 lists which contain its peers. eg. its row, column and 3x3 box
units = dict((s, [u for u in unit_list if s in u]) for s in boxes)

#peers takes units dict and makes set, removes the separation of lists so it can be searched easily.
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

# func that displays the soduko board
def display(values1):
    width = 1+max(len(values1[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values1[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

#Convert grid string into {<box>: <value>} dict and replace the empty value "." with all possible values '123456789'
def grid_values(grid):
    values = []

    for i in grid:

        if i == '.':

            values.append('123456789')

        else:

            values.append(i)

    return dict(zip(boxes, values))

#Strategy1 eliminate 
# If a box has a single value and has been solved. Remove it from possible values f its peers
def eliminate(dictpuzzle) :

    # Find the key of all boxes with a solved value/ single value
    solvedvalues =[box for box in dictpuzzle.keys() if len(dictpuzzle[box]) == 1]

    # Loop through solved value keys,
    for boxkey in solvedvalues :

        #Take the value from the key
        foundvalue= dictpuzzle[boxkey]

        # find all the peers of the solved value
        for peerbxkey in peers[boxkey]:

            # Find andremove the found value
            dictpuzzle[peerbxkey] = dictpuzzle[peerbxkey].replace(foundvalue, '')

    #return the updated grid
    return dictpuzzle

#Strategy 2 finds if a possible value isnt present in any of its peers possible values. In that case it must be the answer.
def lastone (dictpzl) :

    for unitlists in unit_list :

        for digit in '123456789' :
            truecount = [subunit for subunit in unitlists if digit in dictpzl[subunit] ]

            #If value isnt found in any of peers possible values, make it that boxes answer/value
            if len(truecount) == 1 :

                dictpzl[truecount[0]] = digit



    return dictpzl

# Strategy 3 CONSTRAINT PROPAGATION
# create func that recursively uses eliminate and onlychoice funcs to narrow possibilities
def reducepzl (pzl):
    #Check if recursion has run out of moves
    stalled = False
    while stalled == False :
        #Track how many boxes have been solved - if number stops increasing, we know there isnt any moves left, so its stalled
        solvedb4 = [box for box in pzl.keys() if len(pzl[box]) == 1]

        #Recursively run eliminate and only option (constraint propagation)
        round1 = eliminate(pzl)
        round2 = lastone(pzl)

        # track how many boxes have been solved
        solvedafter = [box for box in pzl.keys() if len(pzl[box]) == 1]

        #compare to see if recursive loop is no longer solving anymore boxes
        stalled = solvedb4 == solvedafter

        #Check if puzzle solved
        if len([box for box in pzl.keys() if len(pzl[box]) == 0]):
            return False

    return pzl

# Use depth first search and propagation, create a search tree and solve the sudoku
def search(pzl):
    # First, reduce the puzzle using the previous function
    propagation3 = reducepzl(pzl)

    # if reducepzl returns false because using the guessed number leaves it with no options in another square return false
    if propagation3 is False:
        return False
    # write a generator comprehension that creates a boolean list
    # to check if length of all values in boxes = 1 eg all solved. then return the sudoku
    elif all(len(propagation3[s]) == 1 for s in propagation3):
        return propagation3

    # if not solved. Choose one of the unfilled squares with the fewest possibilities and guess if its correct
    else:
        n, s = min((len(propagation3[s]), s) for s in propagation3.keys() if len(propagation3[s]) > 1)

        # Loop through the values of the box selected with least amount of possible values to be used to guess
        for value in propagation3[s] :
            #copy the sudoku passed back to search to try another combo tree keeping propagation 3 intact for future loops
            newsoduko = propagation3.copy()
            #subset suduko box to selected box with min values and replace them with 1 value/guess selected by for loop
            newsoduko[s] = value
            #recurse and run search again on suduko trying to guess other value
            attempt = search(newsoduko)
            #if attempt is truthy then return attempt this only happens when answer is found all other options return false
            #if guess failed and returned false then return to loop and guess the next number in possible values
            if attempt:
                return attempt