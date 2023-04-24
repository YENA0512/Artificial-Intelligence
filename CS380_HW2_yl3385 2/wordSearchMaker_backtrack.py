# ===============================================================================
#  Word Search Constructor
# ===============================================================================
import sys
import random
from copy import deepcopy

# ============================================================================
# get_arg() returns command line arguments.
# ============================================================================


def get_arg(index, default=None):
    '''Returns the command-line argument, or the default if not provided'''
    return sys.argv[index] if len(sys.argv) > index else default


# --------------------------------------------------------------------------------

class Grid:

    # ----------------------------------------------------------------------------
    # Grid:
    # A NUM_ROWS x NUM_COLS grid of characters
    # ----------------------------------------------------------------------------

    def __init__(self, nRows, nCols):
        self.NUM_ROWS = nRows
        self.NUM_COLS = nCols
        self.grid = [[" " for cols in range(nCols)] for rows in range(nRows)]

    def __getitem__(self, index):
        return self.grid[index]

    def __str__(self):
        # ========================================================================
        # Prints Puzzle
        # ========================================================================

        out = "+" + "---+"*self.NUM_ROWS + "\n"
        for i in range(self.NUM_ROWS):
            for j in range(self.NUM_COLS):
                out += "| " + self.grid[i][j] + " "
            out += "|" + "\n"
            out += "+" + "---+"*self.NUM_COLS + "\n"
        return out


# --------------------------------------------------------------------------------

class State:

    def __init__(self, grid, words):

        self.Grid = grid
        self.Words = words

    def __str__(self):
        return '\n\nGrid: \n\n' + self.Grid.__str__() + "\n\nWords: \n\n" + str(self.Words) + "\n\n"

# --------------------------------------------------------------------------------


class Rule:

    def __init__(self, word, row, col, dh, dv):
        self.word = word
        self.row = row
        self.col = col
        self.dh = dh
        self.dv = dv

    def __str__(self):

        return "Place the word "+"'" + self.word + "'"+" in the grid starting at position " + "("+str(self.row) + "," + str(self.col) + ")" + " and proceeding in the direction" + " ["+str(self.dh) + "," + str(self.dv) + "]."

    def applyRule(self, state):
        print(self.__str__())
        newState = deepcopy(state)
        newState.Words.remove(self.word)
        for i in range(len(self.word)):
            character = self.word[i]
            new_pos_x = self.col + i*self.dh
            new_pos_y = self.row + i*self.dv

            newState.Grid[new_pos_y][new_pos_x] = character

        return newState

    def precondition(self, state):

        x_pos = self.col
        y_pos = self.row

        x_end = x_pos + len(self.word)*self.dh
        y_end = y_pos + len(self.word)*self.dv

        # check if new position is outside the grid

        if x_end < 0 or x_end >= state.Grid.NUM_COLS:
            return False
        if y_end < 0 or y_end >= state.Grid.NUM_ROWS:
            return False

        for i in range(len(self.word)):
            character = self.word[i]

            new_pos_x = x_pos + i*self.dh
            new_pos_y = y_pos + i*self.dv

            char_at_new_pos = state.Grid[new_pos_y][new_pos_x]
            if char_at_new_pos != ' ':
                return False
            else:
                continue
        # if all position empty
        return True

# --------------------------------------------------------------------------------


def goal(state):
    if state.Words == []:
        return True
    else:
        return False


def allCandidates(word, state):
    allvalidrules = []
    for i in range(0, state.Grid.NUM_ROWS):
        for j in range(0, state.Grid.NUM_COLS):
            directions = [(0, 1), (1, 0), (1, 1), (1, -1),
                          (-1, 0), (0, -1), (-1, -1), (-1, 1)]
            for direction in directions:
                rule = Rule(word, i, j, direction[0], direction[1])
                if(rule.precondition(state)):
                    allvalidrules.append(rule)
    return allvalidrules


# def failyWidly(state):
#   while(1):
#       if goal(state):
#           break
#       else:
#           for i in range(0,len(state.Words)-1):
#               curlist = allCandidates(state.Words[i],state)
#               if(len(curlist) > 0):
#                   for rule in curlist:
#                       rule = random.choice(curlist)
#                       print(rule)
#                       state = rule.applyRule(state)
#                       print(state)
#                       break
#           break
#   print(state)

theWords = []

depth = 10

Failure = 0
def backTrack(stateLists):
    global backTracking
    global Failure
    state = stateLists[0]
    if goal(state):
        return None
    curlist = allCandidates(state.Words[0], state)

    for i in range(1, len(stateLists)):
        if state == stateLists[i]:
            Failure = Failure + 1
            print('FAILED-1')
            return 'FAILED-1'

    if len(curlist) == 0:
        Failure = Failure + 1
        print('FAILED-2')
        return 'FAILED-2'

    elif(len(theWords) < len(stateLists)):
        Failure = Failure + 1
        print('FAILED-3')
        return 'FAILED-3'
    elif curlist == None or len(curlist) == 0:
        Failure = Failure + 1
        print('FAILED-4')
        return 'FAILED-4'

    else:
        for r in curlist:
            newState = r.applyRule(state)
            newStateList = [newState] + stateLists
            backTracking = backTracking + 1
            path = backTrack(newStateList)
            if path and len(path) > 0 and path[0] != "F" and path != None:
                if verbosecheck == "verbose":
                    return path + [r] + [newState]
                else:
                    return [newState]

            elif path == None:
                if verbosecheck == "verbose":
                    return [r] + [newState]
                else:
                    return [newState]
        #return path + [newState]
    Failure = Failure + 1
    print('FAILED-5') 
    return 'FAILED-5'


# --------------------------------------------------------------------------------
#  MAIN PROGRAM
# --------------------------------------------------------------------------------
theWords = []

if __name__ == '__main__':

    # ============================================================================
    # Read input from command line:
    #   python3 <this program>.py  NUM_ROWS NUM_COLS filename
    # where NUM_ROWS and NUM_COLS give the size of the grid to be filled,
    # and filename is a file of words to place in the grid, one word per line.
    # ============================================================================
    # Sample:
    #   python3 <this program>.py  12 12 wordfile1.txt
    # where wordfile1.txt contains these words on separate lines:
    #   ADMISSIBLE AGENT BACKTRACK CANNIBAL   DEADEND  GLOBAL   GRAPHSEARCH
    #   HEURISTIC  LISP  LOCAL     MISSIONARY OPTIMUM  RATIONAL SEARCH  SYMMETRY
    # ============================================================================

    NUM_ROWS = int(get_arg(1))
    NUM_COLS = int(get_arg(2))
    filename = get_arg(3)
    verbosecheck = get_arg(4)
    backTracking = 0
    Failure = 0
    Go = False
    with open(filename, 'r') as infile:
        theWords = [line.strip() for line in infile]

    # ============================================================================
    # Demonstration code for the Grid class:
    # Shows grid initialization, printing, and assignment to grid cells.
    # ============================================================================
    grid = Grid(NUM_ROWS, NUM_COLS)
    state = State(grid, theWords)
    # print(grid)

    stateLists = [state]
    # print(state)
    path = backTrack(stateLists)
    for p in path.__reversed__():
        print(p.__str__())

    print("backTracking number : " , backTracking)
    print("Failures : " , Failure)

 
