
# create str of row and col labels
rows = 'ABCDEFGHI'
cols = '123456789'

# values string wit each board val or '.' for empty

#gridvalues
gridvar = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'

# create helper function that takes (a,b) and does
# for loop for a in b the adds the letters in a list

def cross (a,b) :

    return [x+z for x in a for z in b]


# create a list with all box numbers in grid

boxes = cross(rows, cols)
print (boxes)

# create list with row names a1.a2.a3.a4 etc
# doing cross inside list comp creates lists inside list

row_units = [cross(x, cols) for x in rows]

print (row_units)

# make list with column names a1,b1,c1,d1 eth
# notice the use of for loop on cross order

column_units = [cross(rows, a) for a in cols]

print (column_units)

# create boxes of 3x3 a1,a2,a3,b1,b2.b3
# note is you do for loops through tuple of strings
# each string is the loop iterable and is passed  whole to cross
#so iteration 1 is 'abc' not a so u can chop and create boxes

square_units = [cross(a,b) for a in ('ABC', 'DEF', 'GHI') for b in ('123', '456', '789')]
print (square_units)

# create a list with combo of all possible rows cols boxes
# to be used to find out what numbers are in a boxes peers
# note when u add lists it takes the lists inside the lists and puts them next to eachorher rather than lists in lists in lists lol
unit_list = row_units  + column_units  + square_units

print ("\n" "\n")
print (unit_list)

#create a dictionary where each box is the key and value is
# a list of 3 lists which contain its peer, so its row, clumn and 3x3 box
# uses generator like list comp with a list comp inside! looks like tuple complol then turned to dict
# so {a1 : [[a1,a2,a3,a4 etc], [a1,b1,b3,b4 etc], [a1,a2,a3,b1,b2,b3,c1,c2,c3,etc]}

units = dict((s, [u for u in unit_list if s in u]) for s in boxes)

#peers takes units dict with list of lists and makes set { of all the lists added together and
#puts it in a dictionary. basically removes the separation of lists so it can be searched easily.

peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

print ('units list is:' )
print( units )
print ('peers list is:')
print (peers)
checkdicttype = [type(i) for i in peers.values()]
print (checkdicttype)



# copied code func that displays dict as board

def display(values1):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1+max(len(values1[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values1[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return


def grid_values(grid):
    """Convert grid string into {<box>: <value>} dict with '123456789' value for empties.

    Args:
        grid: Sudoku grid in string form, 81 characters long
    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'
        - values: Value in corresponding box, e.g. '8', or '123456789' if it is empty.
    """


    # take the grid values variable and replace replace the no value .'s  with '123456789' so u can do elimination of if the number is in one of its peers and remove
    # create new list with a for loop appending '.' then zip it to boxes and create dict so box is value and key is box number
    # cant be run on existing iterable so make new one which is why u declare empto list and run the for loopp to ther

    values = []

    for i in grid:

        if i == '.':

            values.append('123456789')

        else:

            values.append(i)

    return dict(zip(boxes, values))

#STRATEGY1 eliminate all single vals that appear in its peers
# look at a boxes peers and remove all 1 digit boxes from current
# boxes poss answers
def eliminate(dictpuzzle) :

    # create a new list by for loop thru the dict key n and subset each box to discover value len
    #if the value is 1 digit return key to new solved value list. so creating list of alll boxes wit 1 anser
    #use the iterated box/key to pull the value eg dictpuzzle[key]
    solvedvalues =[box for box in dictpuzzle.keys() if len(dictpuzzle[box]) == 1]
    #print('solvedvalue wit keys  is')
    #print (solvedvalues)

    # for loop thru solved value keys,

    for boxkey in solvedvalues :

        #create var with boxkeys value on each iteration of the for loop.
        foundvalue= dictpuzzle[boxkey]

        # find all the peers to boxkey by for loop thru peers using boxkey to locate the one where boxkey is the key and peers are the value
        for peerbxkey in peers[boxkey]:

            # go to each box which is its peer in the main puzzle and find and replace the exracted foundvalue
            # var with '' blank
            dictpuzzle[peerbxkey] = dictpuzzle[peerbxkey].replace(foundvalue, '')

    #return edited dictpuzzle remember to indent with beggining for loop to return once all iters are done
    return dictpuzzle

##strategy 2 only choice searches the values in each unit to see if the possible
#answer only appears once because then it has to be in the box. f it finds one with len=1 the it deletes over
#possible answers from that box and replaces with the found number that has to be there
def lastone (dictpzl) :

    for unitlists in unit_list :

        for digit in '123456789' :



            # create a list that does for loop through subunits so a1a2a3b1b2b3 3x3
            #then yeilds it if the digit iterrable is in the box values of the subunits being iterd through
            truecount = [subunit for subunit in unitlists if digit in dictpzl[subunit] ]

            #within the same loop and once all poss boxes in that unit have been checked
            #say if the count ==1 its unique and replace that boxkey taken from
            #truecount[0] and use it to replace value in main dictpzl

            if len(truecount) == 1 :

                dictpzl[truecount[0]] = digit



    return dictpzl

# CONSTRAINT PROPAGATION
# create func that uses eliminate and onlychoice in funcs a loop to narrow possibilities



def reducepzl (pzl):
    #declare stalled var for boolean true false to be used later
    stalled = False
    #while loop to check if stalled is true and stop program.. so while not false
    #meaning whats returned isnt stalled or false it carrys on loopin
    while stalled == False :
    # track how many boxes have been solved
        solvedb4 = [box for box in pzl.keys() if len(pzl[box]) == 1]

    #run eliminate and only option over and over which is constraint propagation
    #more options and narrows it down with each iter in while loops


        round1 = eliminate(pzl)

        round2 = lastone(pzl)

        # track how many boxes have been solved
        solvedafter = [box for box in pzl.keys() if len(pzl[box]) == 1]

        #compare to see if its stop solving boxes and change stalled var the while loop depends on to true
        stalled = solvedb4 == solvedafter

        #run for loop through pzl keys and check if after eliminate and reduce len of values in box is zero
        #important later because if guessing numbers in depth first search theyll come times when its removed
        #from peers and leaves no poss answer
        if len([box for box in pzl.keys() if len(pzl[box]) == 0]):
            return False

    return pzl

# depth first search

def search(pzl):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    propagation3 = reducepzl(pzl)

    # if reducepzl returns false because using the guessed number leaves it with no options in another square return false
    if propagation3 is False:
        print('its false')
        return False
    # write a generator comprehension that creates a boolean list using a for loop of the pzl keys
    # to check if all values of boxes length = 1 eg solved the return that recursion of th pzl
    elif all(len(propagation3[s]) == 1 for s in propagation3):
        print('its solved')
        return propagation3

    # if not solved or false failed Choose one of the unfilled squares with the fewest possibilities must be > 1
    else:
        n, s = min((len(propagation3[s]), s) for s in propagation3.keys() if len(propagation3[s]) > 1)

        print(min((len(propagation3[s]), s) for s in propagation3.keys() if len(propagation3[s]) > 1))


        # run a for loop through the values of box selected with min characters to be used to guess
        for value in propagation3[s] :
            #copy the sudoku passed back to search to try another combo tree keeping propagation 3 intact for future loops
            newsoduko = propagation3.copy()
            #subset suduko box to selected box with min values and replace them with 1 value selected by for loop
            newsoduko[s] = value
            #recurse and run search again on suduko trying to guess other value
            #so start at top of func run reduzepzl check if caused to fail check is all =1 else pick another box and guess
            #then if fails go back to original for loop value and guess next number in sequence try again tree of guesses
            attempt = search(newsoduko)
            #if attempt is truthy eg has value and error further up in search or reducepzl hasnt returned a false
            #then return attempt this only happens when answer found all other options return false
            #if guess failed and returned false then return to for loop and gues next number in value
            if attempt:
                print('truthy')
                return attempt