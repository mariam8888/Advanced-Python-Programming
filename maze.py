import random
from pyamaze import maze, agent, COLOR

#Dictionary for directions
direction = {'forward': 'N', 'left': 'W', 'back': 'S', 'right': 'E'}

#Function for clockwise rotation
def RCW():
    global direction
    k = list(direction.keys())
    v = list(direction.values())
    v_rotated = [v[-1]] + v[:-1]
    direction = dict(zip(k, v_rotated))

#function for counter-clockwise rotation
def RCCW():
    global direction
    k = list(direction.keys())
    v = list(direction.values())
    v_rotated = v[1:] + [v[0]]
    direction = dict(zip(k, v_rotated))


def moveForward(cell):
    if direction['forward'] == 'E':
        return (cell[0], cell[1] + 1), 'E'
    if direction['forward'] == 'W':
        return (cell[0], cell[1] - 1), 'W'
    if direction['forward'] == 'N':
        return (cell[0] - 1, cell[1]), 'N'
    if direction['forward'] == 'S':
        return (cell[0] + 1, cell[1]), 'S'


def traverse(m):
    global direction

    currCell = (m.rows, m.cols)
    path = ''
    while True:

        if currCell == (1, 1):
            break
        if m.maze_map[currCell][direction['left']] == 0:
            if m.maze_map[currCell][direction['forward']] == 0:
                RCW()
            else:
                currCell, d = moveForward(currCell)
                path += d
        else:
            RCCW()
            currCell, d = moveForward(currCell)
            path += d
    path2 = path
    while 'EW' in path2 or 'WE' in path2 or 'NS' in path2 or 'SN' in path2:
        path2 = path2.replace('EW', '')
        path2 = path2.replace('WE', '')
        path2 = path2.replace('NS', '')
        path2 = path2.replace('SN', '')
    return path, path2

#To create a maze of different size each time
x = random.randint(3, 10)
y = random.randint(3, 10)
myMaze = maze(x, y)
myMaze.CreateMaze()

#agent
b = agent(myMaze, shape='arrow', color=COLOR.yellow)


path, path2 = traverse(myMaze)
myMaze.tracePath({b: path2})

print(path)
myMaze.run()
