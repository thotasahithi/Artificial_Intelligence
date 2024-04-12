import random
import sys

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
        # storing the dungeon layout
        self.dungeonLayout = []    
        # storing the actman position         
        self.actManPos = None 
        # storing the monster positions              
        self.monsterPositions = []   
        # to store the score value of the act man     
        self.score = 50 
        # for storing the bullet status                    
        self.bulletFired = False      
        # to store the valid actions      
        self.validActions = []
# this function generates a randon direction among all the eight directions to move the actman
def getRandomDirection():
    # returns a random number except 5 between 1 to 8
    while(True):
        randomNum = random.randint(1, 8)
        if randomNum == 5:
            continue
        else:
            return randomNum
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
                    elif char in ['D', 'G', '@']:
                        gameState.monsterPositions.append((row, col))
    return gameState

# function to move the act man to a new cell
def moveActMan(gameState, newRow, newCol, action):
    # if the new cell contains any monster then the score should change to zero and the game should end
    if gameState.dungeonLayout[newRow][newCol] in ['D', 'G']:
        gameState.score = 0
        gameState.dungeonLayout[gameState.actManPos[0]] = gameState.dungeonLayout[gameState.actManPos[0]][:gameState.actManPos[1]] + ' ' + gameState.dungeonLayout[gameState.actManPos[0]][gameState.actManPos[1]+1:] # Erase previous position
        gameState.dungeonLayout[newRow] = gameState.dungeonLayout[newRow][:newCol] + 'X' + gameState.dungeonLayout[newRow][newCol+1:] # Update new position
        gameState.actManPos = None 
        return 
    # else change the act man position to the new cells and reduce the score by 1 and place the movement into the valid actions.
    gameState.dungeonLayout[gameState.actManPos[0]] = gameState.dungeonLayout[gameState.actManPos[0]][:gameState.actManPos[1]] + ' ' + gameState.dungeonLayout[gameState.actManPos[0]][gameState.actManPos[1]+1:] # Erase previous position
    gameState.actManPos = (newRow, newCol)
    gameState.dungeonLayout[newRow] = gameState.dungeonLayout[newRow][:newCol] + 'A' + gameState.dungeonLayout[newRow][newCol+1:] # Update new position
    gameState.score -= 1 
    gameState.validActions.append(action)

# function to generate a random dorection to fire 
def getRandomFiringDirection():
    # returns a random direction among the four main directions
    cardinalDirections = [
        [-1, 0, "N"],
        [1, 0, "S"],
        [0, 1, "E"],
        [0, -1, "W"]
    ]
    direction = random.choice(cardinalDirections)
    return direction
# function that performs firing
def fireMagicBullet(gameState, direction):
    # as the bullet should be fired only once if the bullet is fired once then firing should not be performed.
    if gameState.bulletFired:
        return
    # if the firing is not performed previously then the firing will be done in any of the random direction. 
    # when fired the monster in that direction dies until the bullet hits the wall.
    newRow = gameState.actManPos[0] + direction[0]
    newCol = gameState.actManPos[1] + direction[1]

    while (True):
        if ((0 > newRow or newRow >= len(gameState.dungeonLayout)) or (0 > newCol or newCol >= len(gameState.dungeonLayout[0])) or (gameState.dungeonLayout[newRow][newCol] == '#')):
            break

        targetPos = (newRow, newCol)
        # if the target position contains a monster then the score must be increased by 5 for every monster death
        # and change the monster to a corpses if dead
        if targetPos in gameState.monsterPositions:
            
            gameState.monsterPositions.remove(targetPos)
            gameState.score += 5
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
        for act in [[0, 1, 3], [0, -1, 7], [1, 0, 5], [-1, 0, 1], [1, 1, 4], [-1, 1, 2], [1, -1, 6], [-1, -1, 8]]:
            newRow, newCol = monsterPos[0] + act[0], monsterPos[1] + act[1]
            if (0 <= newRow < len(gameState.dungeonLayout) and
                0 <= newCol < len(gameState.dungeonLayout[0]) and
                gameState.dungeonLayout[newRow][newCol] != '#'):
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
                gameState.dungeonLayout[new_pos[0]] = gameState.dungeonLayout[new_pos[0]][:new_pos[1]] + '@' + gameState.dungeonLayout[new_pos[0]][new_pos[1]+1:]
                gameState.score += 10
            elif gameState.dungeonLayout[new_pos[0]][new_pos[1]] in ['@']:
                gameState.dungeonLayout[new_pos[0]] = gameState.dungeonLayout[new_pos[0]][:new_pos[1]] + '@' + gameState.dungeonLayout[new_pos[0]][new_pos[1]+1:]
                gameState.score += 5
            elif gameState.dungeonLayout[new_pos[0]][new_pos[1]] in ['A']:
                gameState.dungeonLayout[new_pos[0]] = gameState.dungeonLayout[new_pos[0]][:new_pos[1]] + 'X' + gameState.dungeonLayout[new_pos[0]][new_pos[1]+1:]
                gameState.actManPos = None 
                gameState.score = 0
                return
        else:
        # if the new cell is empty then the monster moves to that cell.
            new_placements.append(new_pos)
            gameState.dungeonLayout[new_pos[0]] = gameState.dungeonLayout[new_pos[0]][:new_pos[1]] + monst + gameState.dungeonLayout[new_pos[0]][new_pos[1]+1:]

    new_placements.pop(0)
    gameState.monsterPositions = new_placements
# writing the output into a file
def writeOutputFile(filename, gameState):
    with open(filename, 'w') as outputFile:
        outputFile.write(''.join(map(str, gameState.validActions))  + '\n')
        outputFile.write(str(gameState.score) + '\n')
        for row in gameState.dungeonLayout:
            outputFile.write(row + '\n')
# monster check 
def is_monster_present(layout, monst):
    for line in layout:
        if monst in line:
            return True
    return False

# main function
def main():
    if len(sys.argv) != 3:
        print("Usage:", sys.argv[0], "<input_file> <output_file>")
        sys.exit(1)
    gameState = readInputFile(sys.argv[1])
    while True:
        direction = getRandomDirection()
        dx, dy = 0, 0
        direction_changes = {
            Direction.North: (-1, 0),
            Direction.South: (1, 0),
            Direction.East: (0, 1),
            Direction.West: (0, -1),
            Direction.North_East: (-1, 1),
            Direction.South_East: (1, 1),
            Direction.North_West: (-1, -1),
            Direction.South_West: (1, -1)
        }
        dx, dy = direction_changes[direction]

        newRow = gameState.actManPos[0] + dx
        newCol = gameState.actManPos[1] + dy
        # the programs rum if the newrow and newcol is in the range of length of dungeon layout.
        if (0 > newRow >= len(gameState.dungeonLayout) or 0 > newCol >= len(gameState.dungeonLayout[0])):
            continue
        
        if gameState.bulletFired == False and (random.randint(1, 10) < 4):
            fireMagicBullet(gameState, getRandomFiringDirection())
            moveMonsters(gameState)
        
        elif gameState.dungeonLayout[newRow][newCol] != '#':
            moveActMan(gameState, newRow, newCol, direction)
            if gameState.actManPos is not None:
                moveMonsters(gameState)

        if gameState.actManPos is None:
            break

        if not is_monster_present(gameState.dungeonLayout, 'D') and not is_monster_present(gameState.dungeonLayout, 'G'):
            break 
        if gameState.score <= 0:
            break 
    writeOutputFile(sys.argv[2], gameState)

if __name__ == "__main__":
    main()