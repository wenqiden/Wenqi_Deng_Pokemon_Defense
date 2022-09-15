import math

#################################
# Classes
#################################

# define enemies/towers classes used in the game

# three types of enemies players need to defeat
class enemy1(object):
    def __init__(self):
        self.name = 'Slime'
        self.health = 200
        self.moveSpeed = 5
        self.difficulty = 1
        self.pointReward = 5
class enemy2(object):
    def __init__(self):
        self.name = 'Zombie'
        self.health = 110
        self.moveSpeed = 10
        self.difficulty = 2
        self.pointReward = 10
class enemy3(object):
    def __init__(self):
        self.name = 'Rock Giant'
        self.health = 475
        self.moveSpeed = 2.5
        self.difficulty = 3
        self.pointReward = 15

# one of available characters (towers) players can choose
class character1(object):
    availableNum = 3
    def __init__(self, app):
        self.name = 'Charmander'
        self.requiredPoint = 12
        self.attackRange = [[  True,  True,  True,  True ]]
        self.damage = 7
        self.enemy = enemy2
        self.attackWay = '   Attack the closest\nenemy in attacking range'

    def attack(self, app, towerRow, towerCol, direction):
        (dirx, diry) = direction
        if diry == 0:
            attackRow = (len(self.attackRange[0])-1)*dirx
            attackCol = len(self.attackRange)-1
            rowMin = min(towerRow, towerRow+attackRow)
            rowMax = max(towerRow, towerRow+attackRow)
            colMin = min(towerCol-attackCol//2, towerCol+attackCol//2)
            colMax = max(towerCol-attackCol//2, towerCol+attackCol//2)
        else:
            attackRow = len(self.attackRange)-1
            attackCol = (len(self.attackRange[0])-1)*diry
            colMin = min(towerCol, towerCol+attackCol)
            colMax = max(towerCol, towerCol+attackCol)
            rowMin = min(towerRow-attackRow//2, towerRow+attackRow//2)
            rowMax = max(towerRow-attackRow//2, towerRow+attackRow//2)
        closest = None
        closeDis = app.width
        (x0, y0, x1, y1) = getCellBounds(app, towerRow, towerCol)
        for i in range(len(app.enemiesOnGraph)):
            (row, col) = getCell(app, app.enemiesOnGraph[i][2], 
                                    app.enemiesOnGraph[i][3])
            if (rowMin <= row <= rowMax) and (colMin <= col <= colMax):
                if (distance(x0, app.enemiesOnGraph[i][2], y0, 
                        app.enemiesOnGraph[i][3]) <= closeDis):
                    closeDis = distance(x0, app.enemiesOnGraph[i][2], y0, 
                                        app.enemiesOnGraph[i][3])
                    closest = i
        if closest != None:
            app.enemiesOnGraph[closest][-2] -= self.damage

class character2(object):
    availableNum = 3
    def __init__(self, app):
        self.name = 'Bulbasaur'
        self.requiredPoint = 25
        self.attackRange = [[  True,  True,  True ],
                            [  True,  True,  True ],
                            [  True,  True,  True ]]
        self.damage = 5
        self.enemy = enemy1
        self.attackWay = 'Attack enemies simultaneously\n    in attacking range'

    def attack(self, app, towerRow, towerCol, direction):
        (dirx, diry) = direction
        if diry == 0:
            attackRow = (len(self.attackRange[0])-1)*dirx
            attackCol = len(self.attackRange)-1
            rowMin = min(towerRow, towerRow+attackRow)
            rowMax = max(towerRow, towerRow+attackRow)
            colMin = min(towerCol-attackCol//2, towerCol+attackCol//2)
            colMax = max(towerCol-attackCol//2, towerCol+attackCol//2)
        else:
            attackRow = len(self.attackRange)-1
            attackCol = (len(self.attackRange[0])-1)*diry
            colMin = min(towerCol, towerCol+attackCol)
            colMax = max(towerCol, towerCol+attackCol)
            rowMin = min(towerRow-attackRow//2, towerRow+attackRow//2)
            rowMax = max(towerRow-attackRow//2, towerRow+attackRow//2)
        for i in range(len(app.enemiesOnGraph)):
            (row, col) = getCell(app, app.enemiesOnGraph[i][2], 
                                    app.enemiesOnGraph[i][3])
            if (rowMin <= row <= rowMax) and (colMin <= col <= colMax):
                app.enemiesOnGraph[i][-2] -= self.damage

class character3(object):
    availableNum = 3
    def __init__(self, app):
        self.name = 'Squirtle'
        self.requiredPoint = 35
        self.attackRange = [[  True,  True],
                            [  True,  True],
                            [  True,  True],
                            [  True,  True],
                            [  True,  True]]
        self.damage = 10
        self.enemy = enemy3
        self.attackWay = '   Attack the furthest\nenemies in attacking range'
        
    def attack(self, app, towerRow, towerCol, direction):
        # it will attack the enemy furthest from it in its attacking range
        (dirx, diry) = direction
        if diry == 0:
            attackRow = (len(self.attackRange[0])-1)*dirx
            attackCol = len(self.attackRange)-1
            rowMin = min(towerRow, towerRow+attackRow)
            rowMax = max(towerRow, towerRow+attackRow)
            colMin = min(towerCol-attackCol//2, towerCol+attackCol//2)
            colMax = max(towerCol-attackCol//2, towerCol+attackCol//2)
        else:
            attackRow = len(self.attackRange)-1
            attackCol = (len(self.attackRange[0])-1)*diry
            colMin = min(towerCol, towerCol+attackCol)
            colMax = max(towerCol, towerCol+attackCol)
            rowMin = min(towerRow-attackRow//2, towerRow+attackRow//2)
            rowMax = max(towerRow-attackRow//2, towerRow+attackRow//2)
        furthest = None
        furthestDis = 0
        (x0, y0, x1, y1) = getCellBounds(app, towerRow, towerCol)
        for i in range(len(app.enemiesOnGraph)):
            (row, col) = getCell(app, app.enemiesOnGraph[i][2], 
                                    app.enemiesOnGraph[i][3])
            if (rowMin <= row <= rowMax) and (colMin <= col <= colMax):
                if (distance(x0, app.enemiesOnGraph[i][2], y0, 
                        app.enemiesOnGraph[i][3]) > furthestDis):
                    furthestDis = distance(x0, app.enemiesOnGraph[i][2], y0, 
                                        app.enemiesOnGraph[i][3])
                    furthest = i
        if furthest != None:
            app.enemiesOnGraph[furthest][-2] -= self.damage

# getCell and getCellBounds from course website
def getCell(app, x, y):
    row = int((y-app.margin-app.toolSize) / app.cellSize)
    col = int((x-app.margin) / app.cellSize)
    return (row, col)

def getCellBounds(app, row, col):
    x0 = app.margin + col * app.cellSize
    x1 = app.margin + (col+1) * app.cellSize
    y0 = app.margin + app.toolSize + row * app.cellSize
    y1 = app.margin + app.toolSize + (row+1) * app.cellSize
    return (x0, y0, x1, y1)

# determine distance between 2 points
def distance(x0, x1, y0, y1):
    return math.sqrt((x0-x1)**2+(y0-y1)**2)
