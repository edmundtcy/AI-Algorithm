from copy import deepcopy
############# Classes ################


class Coord():
    def __init__(self, i):
        self.x = i//3
        self.y = i%3

    def __eq__(self, other):
        return (self.x==other.x) and (self.y==other.y)

    def __hash__(self):
        return hash((x,y))

    def __sub__(self, other):
        return abs(self.x-other.x) + abs(self.y-other.y)

    def CopyAndMove(self, x, y):
        new = deepcopy(self)
        new.x += x
        new.y += y
        return new

    def Valid(self):
        return (self.x in [0,1,2]) and (self.y in [0,1,2])

    def Index(self):
        return self.x*3 + self.y


class BoardState():
    def __init__(self, board, dir = None):
        self.board = board
        self.dir = dir
        self.FindEmpty()

    def __eq__(self, other):
        if isinstance(other, BoardState):
            return self.board == other.board
        return False

    def __hash__(self):
        return hash(self.board)

    def FindEmpty(self):
        i = self.board.index('0')
        self.empty = Coord(i)


    def CopyTo(self, new_coord, dir):
        new_board = deepcopy(self.board)
        new_board[self.empty.Index()] = new_board[new_coord.Index()]
        new_board[new_coord.Index()] = '0'

        new = BoardState(new_board, dir)
        return new

    def neighbors(self):
        listn = []

        new = self.empty.CopyAndMove(1, 0)
        if new.Valid():
            listn.append(self.CopyTo(new, "down"))

        new = self.empty.CopyAndMove(-1, 0)
        if new.Valid():
            listn.append(self.CopyTo(new, "up"))

        new = self.empty.CopyAndMove(0, 1)
        if new.Valid():
            listn.append(self.CopyTo(new, "right"))
            
        new = self.empty.CopyAndMove(0, -1)
        if new.Valid():
            listn.append(self.CopyTo(new, "left"))

        return listn

    def Print(self):
        for r in [0,1,2]:
            for c in [0,1,2]:
                print(self.board[r*3+c], end=' ')
            print()
        print()
        return


def exist(set, state):
    for _state in set:
        if _state == state:
            return True
    return False


############# Algorithm ################


def itr_deep_search(ini, goal, max):
    global max_count, goal_state
    global SearchSet, path
    global SearchedNodes

    ini_state = ini
    goal_state = goal
    max_count = max

    SearchedNodes = 0
    SearchSet=[]
    path = []
    
    #depth = 26
    #while (SearchedNodes<max_count) and (depth < 27):
    depth = 0
    while (SearchedNodes<max_count):
        SearchedNodes = 0
        SearchSet=[]
        (found, stop) = DFS(ini_state, depth)
        if found:
            return list(reversed(path))[1:]
        if stop:
            break
        depth += 1
    
    print("Exceed limit\n")
    return None


def DFS(state, depth):
    global max_count, goal_state
    global SearchSet, path
    global SearchedNodes

    #print_array(state.board)
    
    
    #if visited stop
    if exist(SearchSet,state):
        return (False,False)

    SearchSet.append(state)

    if depth == 0:
        if state == goal_state:
            path.append(state.dir)
            return (True,False)

    else:
        SearchedNodes += 1
        if (SearchedNodes >= max_count):
            return (False, True)

        for neighbor in state.neighbors():
            (found, stop) = DFS(neighbor, depth-1)
            if found:
                path.append(state.dir)
                return (True, False)
            if stop:
                return (False, True)

    SearchSet.remove(state)
    return (False, False)


############# Main ################


def read_state(file):
    input_file = open(file,"r")
    output = []
    for i in range (3):
        for j in input_file.readline().strip().split():
            output.append(j)
    return output


def print_result(result):
    if result == None:
            print("Solution not found.")
    else:
        for move in result:
            print(move)
        print("Total moves:", len(result))


def main(file):
    Goal = BoardState(read_state("goal.txt"))
    Ini = BoardState(read_state(file))
    
    #1a.
    print("ItrDeepingSearch:")
    print_result(itr_deep_search(Ini, Goal, 1000000))


main("input.txt")