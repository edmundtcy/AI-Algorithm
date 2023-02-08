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
            return ''.join(self.board) == ''.join(other.board)
        return False

    def __hash__(self):
        return hash(''.join(self.board))

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


def A_search(ini, goal, h_func):
    global goal_state
    goal_state = goal

    openSet = [ini]
    gScore = {ini:0}
    fScore = {ini:0}
    cameFrom = {ini:None}

    while len(openSet) > 0:
        m = None
        for i in openSet:
            if m==None:
                m = fScore[i]
                current = i
            elif fScore[i] < m:
                m = fScore[i]
                current = i #select the lowest f score as current
        
        if current == goal_state:
            return path_find(cameFrom, current)

        openSet.remove(current) #remove it from openSet as it is exported

        for neighbor in current.neighbors(): #expand
            new_gScore = gScore[current] + 1 #increase the g score associated with the current set
            if (not( exist(gScore.keys(),neighbor) )) or (new_gScore < gScore[neighbor]): 
                # if the new node from expand is not in the g score dict or the new g score is still lower than all the expanded node
                cameFrom[neighbor] = current # for path checking
                gScore[neighbor] = new_gScore #neightbor g score
                fScore[neighbor] = new_gScore + h_func(neighbor) #neightbor f score
                if (not( exist(openSet,neighbor) )):
                    openSet.append(neighbor) #Add the expanded node to the openset

    return None


def path_find(set, state):

    path = [state.dir]
    s = state

    while s.dir != None:
        try:
            s = set[s]
            path.append(s.dir)
            #print_array(s.board)
            #i+=1
        except Exception as e:
            print(e)
            break
    return list(reversed(path))[1:]


############# heuristics ################


def h_misplace(A):
    global goal_state
    sum = 0
    for i in range(9):
        if A.board[i] != goal_state.board[i]:
            if A.board[i] != '0':
                sum+=1
    return sum


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
    start = ['7','2','4','5','0','6','8','3','1']
    end = ['0','1','2','3','4','5','6','7','8']
    Goal = BoardState(end)
    Ini = BoardState(start)
    
    #1b part1
    print("A*Search - Misplacement:")
    print_result(A_search(Ini, Goal, h_misplace))


main("input.txt")