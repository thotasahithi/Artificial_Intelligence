#import copy
import random
import sys
from queue import PriorityQueue

class GamePriorityQueue(PriorityQueue):
        def put(self, tuple):
            newtuple = tuple[0] * -1, tuple[1]
            PriorityQueue.put(self, newtuple)
        def get(self):
            tuple = PriorityQueue.get(self)
            newtuple = tuple[0] * -1, tuple[1]
            return newtuple

# all the eight directions with their corresponding values
class Direction:
    North = 8
    South = 2
    East = 6
    West = 4
    North_East = 9
    South_East = 3
    North_West = 7
    South_West = 1

# game state with required declarations
class GameState:
    def __init__(self):
        self.dungeonLayout = []             # List to store dungeon layout
        self.actManPos = None               # Act-Man's current position
        self.monsterPositions = []          # Monster positions
        self.score = 50                     # Player's score
        self.bulletFired = False            # Flag to check if bullet is already fired
        self.validActions = []              #List to store valid actions.
        self.noOfMonsters = 0
        
def get_copy(self) :
    s2 = GameState()
    s2.dungeonLayout = list( self.dungeonLayout )
    s2.actManPos = tuple( self.actManPos )
    s2.monsterPositions = list( self.monsterPositions )
    s2.score = self.score
    
    return s2

# reading the input file and the respective positions of act man, monsters and corpses
def readInputFile(filename):
    gameState = GameState()
    with open(filename, 'r') as inputFile:
        numRows, numCols = map(int, inputFile.readline().split())
        for row, line in enumerate(inputFile):
            if line.strip():
                gameState.dungeonLayout.append(line.strip())
                for col, char in enumerate(line.strip()):
                    if char == '#':
                        continue
                    elif char == ' ':
                        continue
                    elif char == 'A':
                        gameState.actManPos = (row, col)
                    elif char in ['D', 'G']:
                        gameState.noOfMonsters += 1
                        gameState.monsterPositions.append((row, col))
                    elif char == '@':
                        gameState.monsterPositions.append((row, col))
    return gameState    
 
# writing the output into a file
def writeOutputFile(filename, gameState):
    with open(filename, 'w') as outputFile:
        outputFile.write(''.join(map(str, gameState.validActions))  + '\n')
        outputFile.write(str(gameState.score) + '\n')
        for row in gameState.dungeonLayout:
            outputFile.write(row + '\n')


# this function generates a randon direction among all the eight directions to move the actman except its initial position.
def getRandomDirection():
    while(True):
        randomNum = random.randint(1, 8)
        if randomNum == 5:
            continue
        else:
            return randomNum    

# function to generate a random direction to fire 
def getRandomFiringDirection():
    # returns a random direction among the four main directions
    cardinalDirections = [
        ((-1, 0), "North"),
        ((1, 0), "South"),
        ((0, 1), "East"),
        ((0, -1), "West")
    ]
    # Randomly select a direction
    direction, direction_name = random.choice(cardinalDirections)
    # returns the coordinates oof the direction and the direction name
    return direction, direction_name        

# function to move the act man to a new cell
def moveActMan(gameState, newRow, newCol, action):
    # if the new cell contains any monster then the score should change to zero and the game should end
    if gameState.dungeonLayout[newRow][newCol] in ['D', 'G']:
        # make the score zero
        gameState.score = 0
        # empty the cell of act man and mark it 'X'
        gameState.dungeonLayout[gameState.actManPos[0]] = gameState.dungeonLayout[gameState.actManPos[0]][:gameState.actManPos[1]] + ' ' + gameState.dungeonLayout[gameState.actManPos[0]][gameState.actManPos[1]+1:] 
        gameState.dungeonLayout[newRow] = gameState.dungeonLayout[newRow][:newCol] + 'X' + gameState.dungeonLayout[newRow][newCol+1:] 
        # change the act man position to none.
        gameState.actManPos = None 
        return 
    # else change the act man position to the new cells and reduce the score by 1 and place the movement into the valid actions.
    gameState.dungeonLayout[gameState.actManPos[0]] = gameState.dungeonLayout[gameState.actManPos[0]][:gameState.actManPos[1]] + ' ' + gameState.dungeonLayout[gameState.actManPos[0]][gameState.actManPos[1]+1:] 
    gameState.actManPos = (newRow, newCol)
    gameState.dungeonLayout[newRow] = gameState.dungeonLayout[newRow][:newCol] + 'A' + gameState.dungeonLayout[newRow][newCol+1:] 
    # Decrease score for moving
    gameState.score -= 1 
    # Record the valid action
    gameState.validActions.append(action)

# function that performs firing
def fireMagicBullet(gameState, direction):
    # as the bullet should be fired only once if the bullet is fired once then firing should not be performed.
    if gameState.bulletFired:
        return
    # if the firing is not performed previously then the firing will be done in any of the random direction. 
    # when fired the monster in that direction dies until the bullet hits the wall.
    newRow = gameState.actManPos[0] + direction[0]
    newCol = gameState.actManPos[1] + direction[1]

    # Move target position in the chosen direction until hitting a wall or reaching the edge of the dungeon
    while (True):
        if ((0 > newRow or newRow >= len(gameState.dungeonLayout)) or (0 > newCol or newCol >= len(gameState.dungeonLayout[0])) or (gameState.dungeonLayout[newRow][newCol] == '#')):
            break

        targetPos = (newRow, newCol)
        # if the target position contains a monster then the score must be increased by 5 for every monster death
        # and change the monster to a corpses if dead
        if targetPos in gameState.monsterPositions and gameState.dungeonLayout[newRow][newCol] != '@':
            # when the monster dies increment the score by 5
            gameState.score += 5
            gameState.noOfMonsters -= 1
            # change the cells to '@' as corpses
            gameState.dungeonLayout[targetPos[0]] = gameState.dungeonLayout[targetPos[0]][:targetPos[1]] + '@' + gameState.dungeonLayout[targetPos[0]][targetPos[1]+1:]
        
        newRow = newRow + direction[0]
        newCol = newCol + direction[1]
    # when bullet is fired the score must be reduced by 20 and add the bullet fired direction to valid actions.
    gameState.score -= 20
    gameState.bulletFired = True
    gameState.validActions.append(direction[2])

#functions to move monsters
def moveMonsters(gameState):
    monsterPositions = []
    new_placements = []
    new_placements.append(gameState.actManPos)

    for monsterPos in gameState.monsterPositions:
        # if there are not monster alive then we will continue the loop
        if (gameState.dungeonLayout[monsterPos[0]][monsterPos[1]] == '@'):
            new_placements.append((monsterPos[0], monsterPos[1]))
            continue
        # else calculate the distances from act man to the monster. based on the distance will move the monster to the cell
        # to which the distance is minimum. if the multiple cells are same far from the act man then the demon moves in clock wise direction
        # and the ogre moves in counter clockwise direction.
        distances = []
        for act in [[1, -1, 1], [1, 0, 2], [1, 1, 3], [0, -1, 4], [0, 1, 6], [-1, -1, 7], [-1, 0, 8], [-1, 1, 9]]:
            newRow, newCol = monsterPos[0] + act[0], monsterPos[1] + act[1]
            # Check if the target cell is within the bounds of the dungeon and not a wall
            if (0 <= newRow < len(gameState.dungeonLayout) and
                0 <= newCol < len(gameState.dungeonLayout[0]) and
                gameState.dungeonLayout[newRow][newCol] != '#'):
                # Calculate distance to Act-Man from all the empty cells in eight directions
                dx = gameState.actManPos[0] - newRow
                dy = gameState.actManPos[1] - newCol
                distance = (dx * dx) + (dy * dy)
                distances.append((distance, act[2], (newRow, newCol)))
        # sort the distances array based on distances.
        distances.sort(key=lambda b : b[0])
        monst = gameState.dungeonLayout[monsterPos[0]][monsterPos[1]]

        min_value = float('inf')
        matching_record = None
        sort_pref = [8,9,6,3,2,1,4,7] if (monst == 'G') else [8,7,4,1,2,3,6,9]
        # based on the demon preference and ogre preference move the monsters
        
        for pref in sort_pref:
            record = next((item for item in distances if item[1] == pref), None)
            if record and record[0] < min_value:
                min_value = record[0]
                matching_record = record
        (dist, dir, (newRow, newCol)) = matching_record
        monsterPositions.append([(monsterPos[0], monsterPos[1]), (newRow, newCol), monst])
    # during this monster movements if the monster moves to a cell which has monster in it, then both the monsters dies the score increments by 10
    # if the monster moves to a cell which has corpses in it, then the monster dies and the score increments by 5
    # if monster moves to a cell which had act man in it then the act man dies and game ends.
    for position in monsterPositions:
        prev_pos, new_pos, monst = position
        if prev_pos not in new_placements:
            gameState.dungeonLayout[prev_pos[0]] = gameState.dungeonLayout[prev_pos[0]][:prev_pos[1]] + ' ' + gameState.dungeonLayout[prev_pos[0]][prev_pos[1]+1:]
        if new_pos in new_placements:
            if gameState.dungeonLayout[new_pos[0]][new_pos[1]] in ['D', 'G']:
                # If both monsters moves to the same cell, then the two dies. Changes the cell to '@'
                gameState.dungeonLayout[new_pos[0]] = gameState.dungeonLayout[new_pos[0]][:new_pos[1]] + '@' + gameState.dungeonLayout[new_pos[0]][new_pos[1]+1:]
                # increment the score by 10 as both the monster dies[5 points for each monster death]
                gameState.score += 10
                gameState.noOfMonsters -= 2
            elif gameState.dungeonLayout[new_pos[0]][new_pos[1]] in ['@']:
                # if monster moves to a cell which has corpses in it then the monster dies. Change the cell to '@'
                gameState.dungeonLayout[new_pos[0]] = gameState.dungeonLayout[new_pos[0]][:new_pos[1]] + '@' + gameState.dungeonLayout[new_pos[0]][new_pos[1]+1:]
                # increment the score by 5
                gameState.score += 5
                gameState.noOfMonsters -= 1
            elif gameState.dungeonLayout[new_pos[0]][new_pos[1]] in ['A']:
                # Game ends because Act-Man encounters a monster
                gameState.dungeonLayout[new_pos[0]] = gameState.dungeonLayout[new_pos[0]][:new_pos[1]] + 'X' + gameState.dungeonLayout[new_pos[0]][new_pos[1]+1:]
                # Update Act-Man's position to none as it is dead.
                gameState.actManPos = None 
                # change the score to zero
                gameState.score = 0
                return
        else:
            # if the new cell is empty then the monster moves to that cell.
            new_placements.append(new_pos)
            gameState.dungeonLayout[new_pos[0]] = gameState.dungeonLayout[new_pos[0]][:new_pos[1]] + monst + gameState.dungeonLayout[new_pos[0]][new_pos[1]+1:]

    new_placements.pop(0)
    gameState.monsterPositions = new_placements


# goal state function to check all the valid cases of the victory
def goal(gameState, max_moves=7):
    # length of the valid actions is greater than 7 and the act man is alive with score not equal to zero it is a victory.
    if gameState.actManPos is None:
        return False
    # if the act man score is not zero and there are no demons.
    elif gameState.score != 0 and not any(char in ['D', 'G'] for row in gameState.dungeonLayout for char in row):
        return True

# function to check the valid moves.
def getValidActions(state: GameState):
    # check for all valid actions
    validActions = []
    antManPos = state.actManPos
    # if act man position is alive then check for a valid move and move the act man.
    # valid moves:
    # the newrow and newcolumn are in range of 0 and length od dungeon layout
    # new cell must be empty
    # also check for firing the bullet
    
    if (antManPos != None):
        if not state.bulletFired:
            for action in [[-1, 0, 'N'], [0, 1, 'E'], [0, -1, 'W'], [1, 0, 'S']]:
                validActions.append([action[0], action[1], action[2], True])
        #dir = [[1, -1, Direction.South_West], [1, 0, Direction.South], [1, 1, Direction.South_East], [0, -1, Direction.West], [0, 1, Direction.East], [-1, -1, Direction.North_West], [-1, 0, Direction.North], [-1, 1, Direction.North_East]]
        # The act man prefers to move in this order "north, northeast, east, southeast, south, southwest, west, northwest"
        dir = [[-1, 0, Direction.North], [-1, 1, Direction.North_East],[0, 1, Direction.East],[1, 1, Direction.South_East],[1, 0, Direction.South],[1, -1, Direction.South_West],[0, -1, Direction.West],[-1, -1, Direction.North_West]]
        #dir.reverse()
        for action in dir:
            newRow = antManPos[0] + action[0]
            newCol = antManPos[1] + action[1]
            direction = action[2]
            if (0 > newRow >= len(state.dungeonLayout) or 0 > newCol >= len(state.dungeonLayout[0])):
                continue
            if not (state.dungeonLayout[newRow][newCol] in ['D', 'G', '@', '#']):
                validActions.append([newRow, newCol, direction, False])
    return validActions

def TransitionFunction(s, p):
    # for all the actions in p perform the specified operations and retun the state.
    for action in p:
        if (action[3] == True):
            fireMagicBullet(s, [action[0], action[1], action[2]])
        else:
            moveActMan(s, action[0], action[1], action[2])
        moveMonsters(s)
    return s
# heuristic function which return the heuristic value
def h(s: GameState):
    return s.noOfMonsters * 10
# cost functions which return the cost value[Score]
def cost(s: GameState):
    return s.score

# BFS 
def Astar(s0):
    # initialize the frontier and enqueu the empty sequence into the frontier. The frontier is the priority  queue
    frontier = GamePriorityQueue()
    frontier.put((0, []))
    # while the frontier is not empty dequeue the sequence of actions and get the new state
    while frontier:
        action = frontier.get()
        current_actions = action[1]
        new_state = TransitionFunction(get_copy(s0), current_actions)
        # after performing the transformation functions
        # if the new state achieves the goal return the new state.
        if (goal(new_state)):
            return new_state
        # for all valid actions perform the transition function and append it to the frontier.
        for action in getValidActions(new_state):
            new_actions = current_actions[:]
            new_actions.append(action)
            sx = TransitionFunction(get_copy(s0), new_actions)
            frontier.put((cost(sx) + h(sx), new_actions))
    return s0
    

def main():
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 3:
        print("Usage:", sys.argv[0], "<input_file> <output_file>")
        sys.exit(1)
    # Read input file from the command line interface.
    gameState = readInputFile(sys.argv[1])
    # call the BFS
    result = Astar(gameState)

    # Write output file
    writeOutputFile(sys.argv[2], result)

if __name__ == "__main__":
    main()
