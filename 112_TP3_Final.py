#################################
# 15-112 Term Project TP3
# Name: Wenqi Deng
# Andrew ID: wenqid

# Citations:
# Images: 
# https://www.aigei.com/game2d/character/ 
# (including characters, enemies, decorations, path, background)
# Icons: 
# https://game-icons.net/ (including pause, play, settings)
# getCell, getCellBound functions: 
# https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
#################################

import math, copy, random, time
from cmu_112_graphics import *
# definition of classes into this file:
from class_definition import *

#################################
# App functions
#################################

def appStarted(app):
    # some default/unchanged variables
    app.margin = 25
    app.cellSize = 50
    app.toolSize = 50 # for buttons like pause, settings
    app.barSize = 100 # for select/delete towers
    app.rows = (app.height-2*app.margin-app.toolSize-app.barSize)//app.cellSize
    app.cols = (app.width-2*app.margin)//app.cellSize
    app.disallowColor = 'red' 
    app.allowColor = 'gainsboro'
    app.pathColor = 'dark orange'
    app.decorationColor = 'yellow'
    app.enemy1 = [app.loadImage('slime1.png'), app.loadImage('slime2.png'),
                    app.loadImage('slime3.png'), app.loadImage('slime4.png')]
    app.enemy2 = [app.loadImage('zombie1.png'), app.loadImage('zombie2.png'),
                    app.loadImage('zombie3.png'), app.loadImage('zombie4.png')]
    app.enemy3 = [app.loadImage('rock giant1.png'), 
                    app.loadImage('rock giant2.png'),
                    app.loadImage('rock giant3.png'), 
                    app.loadImage('rock giant4.png')]
    app.character1 = [app.scaleImage(app.loadImage('Charmander1.png'), 5/4), 
                        app.scaleImage(app.loadImage('Charmander2.png'), 5/4), 
                        app.scaleImage(app.loadImage('Charmander3.png'), 5/4), 
                        app.scaleImage(app.loadImage('Charmander4.png'), 5/4)]
    app.character2 = [app.scaleImage(app.loadImage('Bulbasaur1.png'), 5/4), 
                        app.scaleImage(app.loadImage('Bulbasaur2.png'), 5/4), 
                        app.scaleImage(app.loadImage('Bulbasaur3.png'), 5/4), 
                        app.scaleImage(app.loadImage('Bulbasaur4.png'), 5/4)]
    app.character3 = [app.scaleImage(app.loadImage('Squirtle1.png'), 5/4), 
                        app.scaleImage(app.loadImage('Squirtle2.png'), 5/4), 
                        app.scaleImage(app.loadImage('Squirtle3.png'), 5/4), 
                        app.scaleImage(app.loadImage('Squirtle4.png'), 5/4)]
    app.characterSelect = [app.scaleImage(app.loadImage('Charmander.png'), 4/3),
                        app.scaleImage(app.loadImage('Bulbasaur.png'), 4/3),
                        app.scaleImage(app.loadImage('Squirtle.png'), 4/3)]
    app.pathImage = app.scaleImage(app.loadImage('path unit.png'), 5/8)
    app.bgImage = app.scaleImage(app.loadImage('background.png'), 5/7)
    app.decorationImage = [app.loadImage('decoration1.png'), 
                            app.loadImage('decoration2.png'),
                            app.loadImage('decoration3.png')]
    app.pauseImage = app.scaleImage(app.loadImage('pause.png'), 5/29)
    app.settingImage = app.scaleImage(app.loadImage('setting.png'), 5/29)
    app.playImage = app.scaleImage(app.loadImage('play.png'), 5/28)
    app.characters = [character1, character2, character3]
    app.enemies = [enemy1, enemy2, enemy3]
    initialize(app)

def initialize(app):
    # initialize variables that will be used/changed in the game
    app.waitForStart = True
    app.showInstruction = False
    app.showSetting = False
    app.pause = False
    app.gameOver = False
    app.deleteMode = False
    app.existRows = [ ]
    app.existCols = [ ]
    app.board = [ ]
    for i in range(app.rows):
        app.board.append(copy.copy([app.disallowColor]*app.cols))
    app.enemiesOnGraph = [ ]
    app.towerOnGraph = [ ]
    app.path = [ ]
    app.pixelPath = [ ]
    app.decorationList = [ ]
    app.point = 0
    app.timerDelay = 125
    app.totalWave = 10
    app.waveRemain = app.totalWave
    app.furthestPlace = None
    app.furthest = [ ]
    app.direction = None
    app.selectedChar = None
    app.selectPlace = (-1, -1)
    app.lastTime = time.time()
    app.pointTime = time.time()
    app.pauseTime = None
    app.pointPauseTime = None
    app.message = 'Welcome to the game :)'
    character1.availableNum = 3
    character2.availableNum = 3
    character3.availableNum = 3
    generateMap(app)

def generateMap(app):
    numOfTurns = random.randint(1, 3)
    entryRow = random.randint(1, app.rows-2)
    app.existRows.append(entryRow)
    prevRow = entryRow
    prevCol = 0
    for turn in range(numOfTurns):
        prevCol = generateTurnCol(app, prevRow, prevCol)
        if turn < numOfTurns-1:
            prevRow = generateTurnRow(app, prevRow, prevCol)
        else:
            generateLastTurn(app, prevRow, prevCol)
    # modify the board so players can place tower next to the path
    # (but not on the path, so change the path to path color)
    for (row, col) in app.path:
        for drow in range(-1, 2):
            for dcol in range(-1, 2):
                if 0 <= row+drow < app.rows and 0 <= col+dcol < app.cols:
                    app.board[row+drow][col+dcol] = app.allowColor
    for (row, col) in app.path:
        app.board[row][col] = app.pathColor
        (x0, y0, x1, y1) = getCellBounds(app, row, col)
        app.pixelPath.append([(x0+x1)/2, (y0+y1)/2])
    chooseDecoration(app)

def generateTurnCol(app, prevRow, prevCol):
    turnCol = random.randint(1, app.cols-2)
    while (turnCol in app.existCols or turnCol+1 in app.existCols 
            or turnCol-1 in app.existCols):
            turnCol = random.randint(1, app.cols-2)
    turn = (prevRow, turnCol)
    if prevCol < turnCol:
        for col in range(prevCol, turnCol):
            app.path.append((prevRow, col))
    else:
        for col in range(prevCol, turnCol, -1):
            app.path.append((prevRow, col))
    app.existCols.append(turnCol)
    return turnCol

def generateTurnRow(app, prevRow, prevCol):
    turnRow = random.randint(1, app.rows-2)
    while (turnRow in app.existRows or turnRow+1 in app.existRows 
            or turnRow-1 in app.existRows):
            turnRow = random.randint(1, app.rows-2)
    turn = (turnRow, prevCol)
    if prevRow < turnRow:
        for row in range(prevRow, turnRow):
            app.path.append((row, prevCol))
    else:
        for row in range(prevRow, turnRow, -1):
            app.path.append((row, prevCol))
    app.existRows.append(turnRow)
    return turnRow

def generateLastTurn(app, prevRow, prevCol):
    exitRow = random.randint(1, app.rows-2)
    while (exitRow in app.existRows or exitRow+1 in app.existRows 
            or exitRow-1 in app.existRows):
        exitRow = random.randint(1, app.rows-2)
    turn = (exitRow, prevCol)
    if prevRow < exitRow:
        for row in range(prevRow, exitRow):
            app.path.append((row, prevCol))
    else:
        for row in range(prevRow, exitRow, -1):
            app.path.append((row, prevCol))
    for col in range(prevCol, app.cols):
        app.path.append((exitRow, col))

def chooseDecoration(app):
    num = random.randint(5, 10)
    for i in range(num):
        image = random.choice(app.decorationImage)
        (row, col) = (random.randint(1, app.rows-2), 
                        random.randint(1, app.cols-2))
        while app.board[row][col] != app.disallowColor:
            (row, col) = (random.randint(1, app.rows-2), 
                            random.randint(1, app.cols-2))
        app.board[row][col] = app.decorationColor
        app.decorationList.append((row, col, image))

def generateEnemies(app):
    # increase the probability of generating suggested enemies according to 
    # location/existing tower type
    suggestion = suggestEnemies(app)
    enemiesChoice = app.enemies + suggestion
    if app.waveRemain > 0:
        difficulty = 3*(app.totalWave-app.waveRemain+1)
        curDifficulty = 0
        app.message = f'Wave No.{app.totalWave-app.waveRemain+1} is coming!!!'
        while curDifficulty <= difficulty:
            # generate a wave with a difficulty no less than the wave difficulty
            enm = random.choice(enemiesChoice)()
            (row, col) = app.path[0]
            (x0, y0, x1, y1) = getCellBounds(app, row, col)
            x = random.randint(0, 4)*10
            app.enemiesOnGraph.append([enm.name, enm.moveSpeed, x, (y0+y1)/2, 
                                        enm.health, -1])
            curDifficulty += enm.difficulty
        app.waveRemain -= 1

def suggestEnemies(app):
    # suggest enemies that players may find difficult to defeat and increase
    # the probability of generating them
    suggestion = [ ]
    minOnGraph = 3
    for character in app.characters:
        if character.availableNum < minOnGraph:
            suggestion = [character(app).enemy]
            minOnGraph = character.availableNum
        elif character.availableNum == minOnGraph and minOnGraph != 3:
            suggestion.append(character(app).enemy)
    for enm in app.enemies:
        if enm().name in app.furthest:
            suggestion += [enm]
    return suggestion

def selectCharacter(app, x, y):
    # check whether players select a tower to place it on graph
    boxSize = 150
    y0 = app.height-app.margin/1.5-app.barSize
    y1 = app.height-app.margin/1.5
    if y0 < y < y1:
        for i in range(5):
            x0 = app.margin+boxSize*(i)
            x1 = app.margin+boxSize*(i+1)-app.margin
            if x0 < x < x1:
                if i < 3:
                    if app.point >= app.characters[i](app).requiredPoint:
                        app.selectedChar = app.characters[i]
                        app.message = 'Select an available place!'
                    else:
                        app.message = 'Your points are not enough'
                elif app.towerOnGraph != [ ]:
                    app.deleteMode = True
                    app.message = 'Select a Pokemon on graph first!'
                else:
                    app.message = 'There is no Pokemon on graph!'

def moveEnemies(app):
    # check what is next step in path
    # determine the direction of enemy move
    # modify pixel location according to the direction/moving speed of enemy
    for i in range(len(app.enemiesOnGraph)):
        x0 = app.enemiesOnGraph[i][2]
        y0 = app.enemiesOnGraph[i][3]
        ind = app.enemiesOnGraph[i][-1]
        if checkDirection(app, x0, y0, ind) != None:
            (drow, dcol) = checkDirection(app, x0, y0, ind)
        else:
            app.gameOver = True
            app.message = 'You LOSE!'
            return
        moveSpeed = app.enemiesOnGraph[i][1]
        app.enemiesOnGraph[i][2] += dcol*moveSpeed
        app.enemiesOnGraph[i][3] += drow*moveSpeed
        if [app.enemiesOnGraph[i][2],app.enemiesOnGraph[i][3]] in app.pixelPath:
            app.enemiesOnGraph[i][-1] += 1

def checkDirection(app, x, y, index):
    # check the direction of an enemy's next move
    if index+1 < len(app.path):
        if x == app.pixelPath[index+1][0]:
            dcol = 0
        elif x < app.pixelPath[index+1][0]:
            dcol = 1
        elif x > app.pixelPath[index+1][0]:
            dcol = -1
        if y == app.pixelPath[index+1][1]:
            drow = 0
        elif y < app.pixelPath[index+1][1]:
            drow = 1
        elif y > app.pixelPath[index+1][1]:
            drow = -1
        return (drow, dcol)
    else:
        return None

def placeCharacter(app, character):
    # for players to place the selected characters on the graph
    (row, col) = app.selectPlace
    char = character(app)
    if character.availableNum > 0:
        app.towerOnGraph.append([character, row, col, app.direction])
        app.board[row][col] = app.disallowColor
        character.availableNum -= 1
        app.point -= char.requiredPoint
        app.message = 'Succeed!'
    else:
        app.message = 'You got all three of this Pokemon on graph!'
    app.selectPlace = (-1, -1)
    app.direction = None

def characterAttack(app):
    # check whether the towers can attack and do the attacking
    for tower in app.towerOnGraph:
        row = tower[1]
        col = tower[2]
        direction = tower[3]
        char = tower[0](app)
        char.attack(app, row, col, direction)

def deleteCharacter(app, row, col):
    # for player to select a tower to delete
    for towerLst in app.towerOnGraph:
        if towerLst[1] == row and towerLst[2] == col:
            app.board[row][col] = app.allowColor
            towerLst[0].availableNum += 1
            app.point += (towerLst[0](app).requiredPoint-5)
            app.towerOnGraph.remove(towerLst)
            app.message = 'Deleted!'
            app.deleteMode = False
            return
    app.message = 'There is no Pokemon Here, plz try elsewhere'

def removeDefeatedEnemy(app):
    # remove enemies with health smaller or equal to 0
    # check whether the furthest place an enemy can reach is updated
    # (suggest this enemy is stronger)
    for enemyList in app.enemiesOnGraph:
        if app.furthestPlace == None or enemyList[-1] > app.furthestPlace:
            app.furthestPlace = enemyList[-1]
            app.furthest.append(enemyList[0])
        if enemyList[-2] <= 0:
            for enm in app.enemies:
                if enm().name == enemyList[0]:
                    app.point += enm().pointReward
            app.enemiesOnGraph.remove(enemyList)

def checkGameEnd(app):
    # if all the 10 waves of enemies are defeated
    # player wins
    if app.enemiesOnGraph == [ ] and app.waveRemain == 0:
        app.gameOver = True
        app.message = 'You WIN!'

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

def mousePressed(app, event):
    buttonWidth= 300
    buttonHeight = 50
    buttonX0 = (app.width-buttonWidth)/2
    instrButtonY0 = app.height/3+7*app.margin
    startButtonY0 = app.height/3+11*app.margin
    if app.waitForStart:
        # check whether the players click the instruction/start buttons
        if (buttonX0 <= event.x <= buttonX0+buttonWidth and 
            instrButtonY0 <= event.y <= instrButtonY0+buttonHeight):
            app.showInstruction = True
        elif (buttonX0 <= event.x <= buttonX0+buttonWidth and 
            startButtonY0 <= event.y <= startButtonY0+buttonHeight):
            app.waitForStart = False
            app.lastTime = time.time()
            app.pointTime = time.time()
    else:
        # check whether the players click the pause/setting buttons
        pauseX = app.width-2*app.margin-app.cellSize
        settingX = app.width-app.margin
        if (pauseX-app.cellSize < event.x < pauseX and 
            app.margin < event.y < app.margin+app.cellSize):
            if app.pause:
                app.pause = False
                app.lastTime = time.time()-app.pauseTime
                app.pointTime = time.time()-app.pointPauseTime
                app.pauseTime = None
                app.pointPauseTime = None
            else:
                app.pauseTime = time.time()-app.lastTime
                app.pointPauseTime = time.time()-app.pointTime
                app.pause = True
        elif (settingX-app.cellSize < event.x < settingX and 
            app.margin < event.y < app.margin+app.cellSize):
            app.pauseTime = time.time()-app.lastTime
            app.pointPauseTime = time.time()-app.pointTime
            app.showSetting = True
            app.pause = True
        if app.showSetting:
            # check the selected speed level of players
            for i in range(5):
                x = app.width/2-5*app.cellSize-2*app.margin
                dx = 2*app.cellSize+app.margin
                if (x+i*dx < event.x < x+i*dx+2*app.cellSize and 
                    app.height/2-2*app.cellSize < event.y < app.height/2):
                    app.timerDelay = 50*(4-i)+25
            doneX = app.width/2-app.margin-2*app.cellSize
            doneY = app.height-app.barSize-7*app.margin
            if (doneX < event.x < doneX+4*app.cellSize+2*app.margin and 
                doneY < event.y < doneY+2*app.margin):
                app.lastTime = time.time()-app.pauseTime
                app.pointTime = time.time()-app.pointPauseTime
                app.pause = False
                app.showSetting = False
        if not app.pause:
            (row, col) = getCell(app, event.x, event.y)
            if 0 <= row < app.rows and 0 <= col < app.cols:
                if app.selectedChar != None:
                    if app.board[row][col] == app.allowColor:
                        app.selectPlace = (row, col)
                        app.message = 'Select a direction the character face!'
                    else:
                        app.message = 'Cannot place here!'
                if app.deleteMode:
                    deleteCharacter(app, row, col)
            else:
                app.message = 'Plz click on board!'
            selectCharacter(app, event.x, event.y)
        if app.gameOver:
            if (buttonX0 <= event.x <= buttonX0+buttonWidth and 
                startButtonY0 <= event.y <= startButtonY0+buttonHeight):
                initialize(app)

def keyPressed(app, event):
    if (event.key == 'r'):
        initialize(app)
    elif app.gameOver:
        return
    if app.waitForStart:
        if (event.key == 'Up'):
            if app.totalWave < 20:
                app.totalWave += 1
                app.waveRemain = app.totalWave
        elif (event.key == 'Down'):
            if app.totalWave > 5:
                app.totalWave -= 1
                app.waveRemain = app.totalWave
    else:
        if app.selectedChar != None:
            if (event.key == 'Up'):
                app.direction = (-1, 0)
                app.message = 'Press Enter after seleting direction!'
            elif (event.key == 'Down'):
                app.direction = (+1, 0)
                app.message = 'Press Enter after seleting direction!'
            elif (event.key == 'Left'):
                app.direction = (0, -1)
                app.message = 'Press Enter after seleting direction!'
            elif (event.key == 'Right'):
                app.direction = (0, +1)
                app.message = 'Press Enter after seleting direction!'
            elif (event.key == 'Enter'):
                if app.selectPlace != (-1, -1):
                    if app.direction != None:
                        placeCharacter(app, app.selectedChar)
                        app.selectedChar = None
                    else:
                        app.message = 'Select a direction first!'
                else:
                    app.message = 'Select a place first!'

def timerFired(app):
    if app.pause or app.waitForStart or app.gameOver:
        return
    else:
        characterAttack(app)
        moveEnemies(app)
        checkGameEnd(app)
        removeDefeatedEnemy(app)
    if int(time.time()-app.lastTime) == 15:
        # generate a group of enemies after 15 secs 
        generateEnemies(app)
        app.lastTime = time.time()
    if int(time.time()-app.pointTime) == 1:
        app.point += 1
        app.pointTime = time.time()

#################################
# Draw functions
#################################

def drawStartPage(app, canvas):
    drawTitle(app, canvas)
    drawButtons(app, canvas)

def drawTitle(app, canvas):
    canvas.create_text(app.width/2, app.height/3, text = 'Pokemon Defense', 
                        font = 'Courier 50')
    canvas.create_text(app.width/2, app.height/3+2.5*app.margin, 
                        text = 'Select number of waves with arrow keys', 
                        font = 'Courier 23 italic')
    canvas.create_text(app.width/2, app.height/3+5*app.margin, 
                        text = f'Current: {app.totalWave}', 
                        font = 'Courier 25 italic bold')
    canvas.create_text(app.width/2, app.height/3+3.5*app.margin, 
                        text = 'Up = +1, Down = -1', 
                        font = 'Courier 23 italic')  

def drawInstruction(app, canvas):
    rule = '''
    Rules:

    1. Each wave of enemies is generated per 15 sec. 
       Defeat them with ur Pokemon before they reach the end of the path!
    2. Difficulty increases as number of waves increases.
    3. Purchase Pokemon on the bar under board with ur points!
       You have 3 types of Pokemon and 3 available Pokemon for each type.
    4. Different Pokemon have different required points and attacking ways

    You have:
    '''
    canvas.create_text(app.width/2, (app.height-app.barSize)/2, anchor = 's', 
                        text = rule, font = 'Courier 20')
    for i in range(3):
        char = app.characters[i](app)
        canvas.create_text((i+1)*app.width/4, app.height/2-app.cellSize, 
                            font = 'Courier 17 bold', text = f'{char.name}:')
        canvas.create_text((i+1)*app.width/4, (app.height-app.cellSize)/2, 
                            font = 'Courier 13', anchor = 's', 
                            text = f'Point: {char.requiredPoint}')
        canvas.create_image((i+1)*app.width/4, app.height/2, 
                        image = ImageTk.PhotoImage(app.characterSelect[i]))
        canvas.create_text((i+1)*app.width/4, app.height/2+app.cellSize, 
                            font = 'Courier 13 underline', anchor = 'n', 
                            text = char.attackWay)
    
    buttonWidth= 300
    buttonHeight = 50
    canvas.create_rectangle((app.width-buttonWidth)/2, 
                            app.height/3+11*app.margin, 
                            (app.width+buttonWidth)/2,
                            app.height/3+11*app.margin+buttonHeight, width = 3)
    canvas.create_text(app.width/2, app.height/3+11*app.margin+buttonHeight/2, 
                        text = 'Ready To Start?', font = 'Courier 25')


def drawButtons(app, canvas):
    buttonWidth= 300
    buttonHeight = 50
    canvas.create_rectangle((app.width-buttonWidth)/2, 
                            app.height/3+7*app.margin, 
                            (app.width+buttonWidth)/2,
                            app.height/3+7*app.margin+buttonHeight, width = 3)
    canvas.create_text(app.width/2, app.height/3+7*app.margin+buttonHeight/2, 
                        text = 'Instruction', font = 'Courier 25')
    canvas.create_rectangle((app.width-buttonWidth)/2, 
                            app.height/3+11*app.margin, 
                            (app.width+buttonWidth)/2,
                            app.height/3+11*app.margin+buttonHeight, width = 3)
    canvas.create_text(app.width/2, app.height/3+11*app.margin+buttonHeight/2, 
                        text = 'Start!', font = 'Courier 25')

def drawGamePage(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'grey')
    drawBackground(app, canvas)
    drawPath(app, canvas)
    drawDecoration(app, canvas)
    drawIconsAndText(app, canvas)
    drawSelectBar(app, canvas)
    if app.selectedChar != None:
        drawAuxiliaryLines(app, canvas)
        if app.selectPlace != (-1, -1):
            drawPlaceCharacter(app, canvas)
    drawEnemy(app, canvas)
    drawCharacter(app, canvas)

def drawBackground(app, canvas):
    for row in range(app.rows):
        for col in range(app.cols):
            (x0, y0, x1, y1) = getCellBounds(app, row, col)
            canvas.create_image((x0+x1)/2, (y0+y1)/2, 
                                image = ImageTk.PhotoImage(app.bgImage))

def drawPath(app, canvas):
    for (row, col) in app.path:
        (x0, y0, x1, y1) = getCellBounds(app, row, col)
        canvas.create_image((x0+x1)/2, (y0+y1)/2, 
                            image = ImageTk.PhotoImage(app.pathImage))

def drawDecoration(app, canvas):
    for (row, col, image) in app.decorationList:
        (x0, y0, x1, y1) = getCellBounds(app, row, col)
        canvas.create_image((x0+x1)/2, (y0+y1)/2, 
                            image = ImageTk.PhotoImage(image))

def drawIconsAndText(app, canvas):
    x0 = app.width-app.margin-app.cellSize/2
    y0 = app.margin/2+app.cellSize/2
    x1 = app.width-2*app.margin-3*app.cellSize/2
    canvas.create_image(x0, y0, image = ImageTk.PhotoImage(app.settingImage))
    if app.pause:
        image = app.playImage
    else:
        image = app.pauseImage
    canvas.create_image(x1, y0, image = ImageTk.PhotoImage(image))
    canvas.create_rectangle(3*app.cellSize, y0-app.cellSize/2, 
                            x1-3*app.cellSize, y0+app.cellSize/2, 
                            fill = 'black')
    canvas.create_text(x1/2, y0, fill = 'white', text = app.message, 
                        font = 'Courier 20')

def drawSelectBar(app, canvas):
    boxSize = 150
    y0 = app.height-app.margin/1.5-app.barSize
    y1 = app.height-app.margin/1.5
    for i in range(4):
        x0 = app.margin+boxSize*(i)
        x1 = app.margin+boxSize*(i+1)-app.margin
        canvas.create_rectangle(x0, y0, x1, y1, outline = 'white', 
                                fill = 'azure4')
        if i+1 < 4:
            char = app.characters[i](app)
            canvas.create_text((x0+x1)/2, y0+5, font = 'Courier 13', 
                            anchor = 'n', text = f'Point: {char.requiredPoint}')
            canvas.create_image((x0+x1)/2, (y0+y1)/2, 
                            image = ImageTk.PhotoImage(app.characterSelect[i]))
            if app.characters[i].availableNum == 0:
                canvas.create_line(x0, y0, x1, y1, fill = 'black', width = 2)
                canvas.create_line(x0, y1, x1, y0, fill = 'black', width = 2)
        else:
            canvas.create_text((x0+x1)/2, (y0+y1)/2, font = 'Courier 20', 
                                text = 'DEL')
    x2 = app.width-app.margin-boxSize
    x3 = app.width-app.margin
    canvas.create_rectangle(x2, y0, x3, y1, outline = 'white', fill = 'azure4')
    canvas.create_text((x2+x3)/2, y0+10, font = 'Courier 15', anchor = 'n',
                        text = 'Current Point:')
    canvas.create_text((x2+x3)/2, (y0+y1)/2, font = 'Courier 20', 
                        text = str(app.point))

def drawEnemy(app, canvas):
    for enemyList in app.enemiesOnGraph:
        if enemyList[0] == 'Slime':
            imageLst = app.enemy1
            fullHealth = enemy1().health
        elif enemyList[0] == 'Zombie':
            imageLst = app.enemy2
            fullHealth = enemy2().health
        else:
            imageLst = app.enemy3
            fullHealth = enemy3().health
        x0 = enemyList[2]
        y0 = enemyList[3]
        i = enemyList[-1]
        if checkDirection(app, x0, y0, i) != None:
            (drow, dcol) = checkDirection(app, x0, y0, i)
        else:
            return
        if (drow, dcol) == (0, -1):
            image = imageLst[1]
        elif (drow, dcol) == (1, 0):
            image = imageLst[2]
        elif (drow, dcol) == (-1, 0):
            image = imageLst[3]
        else:
            image = imageLst[0]
        healthPercent = enemyList[-2]/fullHealth
        canvas.create_image(enemyList[2], enemyList[3]-5, 
                            image = ImageTk.PhotoImage(image))
        canvas.create_rectangle(enemyList[2]-app.cellSize/2, 
                                enemyList[3]-app.cellSize+10,
                                enemyList[2]+app.cellSize/2, 
                                enemyList[3]-app.cellSize+15, fill = '')
        canvas.create_rectangle(enemyList[2]-app.cellSize/2, 
                                enemyList[3]-app.cellSize+10,
                                enemyList[2]+(healthPercent-0.5)*app.cellSize, 
                                enemyList[3]-app.cellSize+15, fill = 'black')

def drawPlaceCharacter(app, canvas):
    direction = [(0,1), (0,-1), (1,0), (-1,0)]
    if app.direction != None:
        if app.selectedChar == character1:
            image = app.character1[direction.index(app.direction)]
        elif app.selectedChar == character2:
            image = app.character2[direction.index(app.direction)]
        elif app.selectedChar == character3:
            image = app.character3[direction.index(app.direction)]
        (dirx, diry) = app.direction
        (towerRow, towerCol) = app.selectPlace
        (x0, y0, x1, y1) = getCellBounds(app, towerRow, towerCol)
        canvas.create_image((x0+x1)/2, (y0+y1)/2, 
                            image = ImageTk.PhotoImage(image))
        if diry == 0:
            attackRow = (len(app.selectedChar(app).attackRange[0])-1)*dirx
            attackCol = len(app.selectedChar(app).attackRange)-1
            rowMin = min(towerRow, towerRow+attackRow)
            rowMax = max(towerRow, towerRow+attackRow)
            colMin = min(towerCol-attackCol//2, towerCol+attackCol//2)
            colMax = max(towerCol-attackCol//2, towerCol+attackCol//2)
        else:
            attackRow = len(app.selectedChar(app).attackRange)-1
            attackCol = (len(app.selectedChar(app).attackRange[0])-1)*diry
            colMin = min(towerCol, towerCol+attackCol)
            colMax = max(towerCol, towerCol+attackCol)
            rowMin = min(towerRow-attackRow//2, towerRow+attackRow//2)
            rowMax = max(towerRow-attackRow//2, towerRow+attackRow//2)
        for row in range(rowMin, rowMax+1):
            for col in range(colMin, colMax+1):
                (x0, y0, x1, y1) = getCellBounds(app, row, col)
                canvas.create_rectangle(x0, y0, x1, y1, fill = '', width = 2,
                                        outline = 'green')

def drawCharacter(app, canvas):
    direction = [(0,1), (0,-1), (1,0), (-1,0)]
    for charList in app.towerOnGraph:
        if charList[0] == character1:
            image = app.character1[direction.index(charList[-1])]
        elif charList[0] == character2:
            image = app.character2[direction.index(charList[-1])]
        elif charList[0] == character3:
            image = app.character3[direction.index(charList[-1])]
        (x0, y0, x1, y1) = getCellBounds(app, charList[1], charList[2])
        canvas.create_image((x0+x1)/2, (y0+y1)/2, 
                            image = ImageTk.PhotoImage(image))

def drawSettingPage(app, canvas):
    canvas.create_rectangle(app.margin/2, app.toolSize-app.margin/2, 
                            app.width-app.margin/2, 
                            app.height-app.barSize+app.margin, fill = 'ivory4')
    canvas.create_text(app.width/2, app.toolSize+3*app.margin, 
                    text = 'Choose the speed level of gameplay (Default: 3)', 
                    fill = 'white', font = 'Courier 25', anchor = 'n')
    for i in range(5):
        if 50*(4-i)+25 == app.timerDelay:
            color = 'LightSteelBlue4'
        else:
            color = 'white'
        x = app.width/2-5*app.cellSize-2*app.margin
        canvas.create_rectangle(x+2*i*app.cellSize+i*app.margin, 
                                app.height/2-2*app.cellSize, 
                                x+2*(i+1)*app.cellSize+i*app.margin, 
                                app.height/2, fill = color, width = 3)
        canvas.create_text(x+(2*i+1)*app.cellSize+i*app.margin, 
                            app.height/2-app.cellSize, text = str(i+1),
                            font = 'Courier 20', fill = 'black')

    canvas.create_rectangle(app.width/2-app.margin-2*app.cellSize, 
                            app.height-app.barSize-7*app.margin, 
                            app.width/2+app.margin+2*app.cellSize, 
                            app.height-app.barSize-5*app.margin, 
                            width = 3, fill = 'white')
    canvas.create_text(app.width/2, app.height-app.barSize-6*app.margin, 
                        text = 'Done!', fill = 'black', font = 'Courier 25')

def drawAuxiliaryLines(app, canvas):
    # show after player select a character (tower)
    for row in range(app.rows):
        for col in range(app.cols):
            (x0, y0, x1, y1) = getCellBounds(app, row, col)
            canvas.create_rectangle(x0, y0, x1, y1, fill = '', 
                                    outline = app.board[row][col])
            if (app.board[row][col] != app.allowColor):
                canvas.create_line(x0, y0, x1, y1, fill = app.board[row][col])
                canvas.create_line(x0+app.cellSize, y0, x1-app.cellSize, y1, 
                                    fill = app.board[row][col])
                # create a cross on the cell indicating that players cannot 
                # place tower on it

def drawEndPage(app, canvas):
    canvas.create_text(app.width/2, app.height/2, text = app.message, 
                        font = 'Courier 50')
    buttonWidth= 300
    buttonHeight = 50
    canvas.create_rectangle((app.width-buttonWidth)/2, 
                            app.height/3+11*app.margin, 
                            (app.width+buttonWidth)/2,
                            app.height/3+11*app.margin+buttonHeight, width = 3)
    canvas.create_text(app.width/2, app.height/3+11*app.margin+buttonHeight/2, 
                        text = 'Restart?', font = 'Courier 25')

def redrawAll(app, canvas):
    if app.waitForStart:
        if not app.showInstruction:
            drawStartPage(app, canvas)
        else:
            drawInstruction(app, canvas)
    elif not app.gameOver:
        drawGamePage(app, canvas)
        if app.showSetting:
            drawSettingPage(app, canvas)
    else:
        drawEndPage(app, canvas)

def main():
    runApp(width = 1000, height = 750)

if __name__ == '__main__':
    main()