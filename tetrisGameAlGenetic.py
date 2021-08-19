import pygame
import random
import time
import copy
import numpy as np
import _thread as thread

colors = [
    (255, 255, 255),    # White           
    (0, 255, 255),      # Cyan
    (0, 0, 255),        # Blue
    (255, 165, 0),      # Orange       
    (128, 0, 128),      # Purple
    (255, 255, 0),      # Yellow
    (255, 0, 0),        # Red
    (0, 128, 0),        # Green
]

spawnPoints = [
    [3, -1],
    [3, -1],
    [2, -1],
    [3, -1],
    [3, -1],
    [3, -1],
    [2, -1],
]

moveCombinations = [
    ['L', 'LL', 'LLL', 'R', 'RR', 'RRR', 'rL', 'rLL', 'rLLL', 'rLLLL', 'rR', 'rRR', 'rRRR', 'rRRRR', 'rRRRRR', 'r'],
    ['L', 'LL', 'LLL', 'R', 'RR', 'RRR', 'RRRR', 'rL', 'rLL', 'rLLL', 'rR', 'rRR', 'rRRR', 'rRRRR', 'rrLrr', 'rrLL', 'rrLLL', 'rrLLLL', 'rrR', 'rrRR', 'rrRRR', 'rrRRRR', 'rrrL', 'rrrLL', 'rrrLLL', 'rrrR', 'rrrRR', 'rrrRRR', 'rrrRRRR', 'rrrRRRRR', 'r', 'rr', 'rrr'],
    ['L', 'LL', 'LLL', 'R', 'RR', 'RRR', 'RRRR', 'rL', 'rLL', 'rLLL', 'rR', 'rRR', 'rRRR', 'rRRRR', 'rRRRRR', 'rrL', 'rrLL', 'rrLLL', 'rrLLLL', 'rrR', 'rrRR', 'rrRRR', 'rrRRRR', 'rrrL', 'rrrLL', 'rrrLLL', 'rrrR', 'rrrRR', 'rrrRRR', 'rrrRRRR', 'r', 'rr', 'rrr'],
    ['L', 'LL', 'LLL', 'R', 'RR', 'RRR', 'RRRR', 'rL', 'rLL', 'rLLL', 'rR', 'rRR', 'rRRR', 'rRRRR', 'rrL', 'rrLL', 'rrLLL', 'rrR', 'rrRR', 'rrRRR', 'rrRRRR', 'rrRRRRR', 'rrrL', 'rrrLL', 'rrrLLL', 'rrrLLLL', 'rrrR', 'rrrRR', 'rrrRRR', 'rrrRRRR', 'r', 'rr', 'rrr'],
    ['L', 'LL', 'LLL', 'LLLL', 'R', 'RR', 'RRR', 'RRRR'],
    ['L', 'LL', 'LLL', 'R', 'RR', 'RRR', 'RRRR', 'rL', 'rLL', 'rLLL', 'rLLLL', 'rR', 'rRR', 'rRRR', 'rRRRR', 'r'],
    ['L', 'LL', 'LLL', 'R', 'RR', 'RRR', 'RRRR', 'rL', 'rLL', 'rLLL', 'rR', 'rRR', 'rRRR', 'rRRRR', 'rRRRRR', 'r']
]

class Figure:

    xPos = 0
    yPos = 0

    # 0  1  2  3
    # 4  5  6  7
    # 8  9  10 11
    # 12 13 14 15

    figures = [
        [[4, 5, 6, 7], [1, 5, 9, 13]],                                      # I
        [[4, 5, 6, 10], [0, 4, 5, 6], [1, 2, 5, 9], [1, 5, 9, 8]],          # J
        [[5, 6, 7, 9], [1, 2, 6, 10], [2, 6, 10, 11], [3, 5, 6, 7]],        # L
        [[4, 5, 6, 9], [1, 4, 5, 6], [1, 4, 5, 9], [1, 5, 6, 9]],           # T
        [[5, 6, 9, 10]],                                                    # O
        [[4, 5, 9, 10], [2, 6, 5, 9]],                                      # Z
        [[6, 7, 9, 10], [1, 5, 6, 10]]                                      # S
    ]


    def __init__ (self, figureNum):

            self.xPos = spawnPoints[figureNum][0]
            self.yPos = spawnPoints[figureNum][1]
            self.shape = figureNum
            self.color = figureNum + 1
            self.rotation = 0

    def shapeData(self):
            return self.figures[self.shape][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.shape])


class Tetris:

    state = "start"
    level = 1
    score = 0
    xPos = 325
    yPos = 60
    zoom = 34

    figure = None
    holdFigure = None
    nextFigure = None

    canHold = True

    field = []
    height = 24
    width = 10

    figuresBag = [0, 1, 2, 3, 4, 5, 6]
    nextFigurePosition = 0

    parameters = []
    
    def __init__ (self, parameters):

        self.field = []
        for _ in range (self.height):
            newLine = []
            for _ in range (self.width):
                newLine.append(0)
            self.field.append(newLine)

        self.parameters = parameters



    def generateFigure(self):

        if self.field[1][4] != 0 or self.field[1][5] != 0 or self.field[1][6] or self.field[1][7] or self.field[0][4] or self.field[0][5] or self.field[0][6] or self.field[0][7]:
            self.endGame = True
            return
        
        self.figure = Figure(self.figuresBag[self.nextFigurePosition])
        self.nextFigurePosition += 1

        if self.nextFigurePosition >= 7:
            random.shuffle(self.figuresBag)
            self.nextFigurePosition = 0

        self.nextFigure = Figure(self.figuresBag[self.nextFigurePosition])


    def collision(self, figure, testFigureCheck):
        collision = False

        for rowNumbers in range (4):
            for column in range (4):
                if 4 * rowNumbers + column in figure.shapeData():
                    if (rowNumbers + figure.yPos < 0 or column + figure.xPos < 0) and not testFigureCheck:
                        collision = True
                        return collision
                    if (rowNumbers + figure.yPos > self.height - 1 or column + figure.xPos > self.width - 1 or column + figure.xPos < 0 or self.field[rowNumbers + figure.yPos][column + figure.xPos] > 0):
                        if testFigureCheck and rowNumbers + figure.yPos < 0:
                            continue
                        else:
                            collision = True

        return collision


    def placePiece (self):

        for rowNumbers in range (4):
            for column in range (4):
                if 4 * rowNumbers + column in self.figure.shapeData() and rowNumbers + self.figure.yPos > -1 and column + self.figure.xPos > -1:
                    self.field[rowNumbers + self.figure.yPos][column + self.figure.xPos] = self.figure.color


        self.checkLines(self.field)
        self.canHold = True
        self.generateFigure()

        if self.collision(self.figure, False):
            self.state = "gameover"
            self.endGame = True

    
    def checkLines (self, field):
        fullLines = 0

        for lineCounter in range (1, self.height):
            empty = 0
            for j in range (self.width):
                if self.field[lineCounter][j] == 0:
                    empty += 1
                    break
            
            if empty == 0:
                fullLines += 1
                for i in range (lineCounter, 1, -1):
                    for j in range (self.width):
                        self.field[i][j] = self.field[i - 1][j]

        tetrises = fullLines // 4
        rem = fullLines % 4

        lines3 = rem // 3
        rem = rem % 3

        lines2 = rem // 2
        rem = rem % 2

        self.score += tetrises * 800 + lines3 * 500 + lines2 * 300 + rem * 100

        return fullLines


    def moveDown (self):

        self.figure.yPos += 1
        if self.collision(self.figure, False):
            self.figure.yPos -= 1
            self.placePiece()

    def moveSide (self, xSpaces):

        oldXPos = self.figure.xPos
        self.figure.xPos += xSpaces
        if self.collision(self.figure, False):
            self.figure.xPos = oldXPos

    def moveBottom (self):

        while not self.collision(self.figure, False):
            self.figure.yPos += 1
        self.figure.yPos -= 1
        self.placePiece()

    def rotate (self):

        oldRot = self.figure.rotation
        self.figure.rotate()
        if self.collision(self.figure, False):
            self.figure.rotation = oldRot

    def hold (self):

        if self.canHold:
            if self.holdFigure is None:
                self.holdFigure = Figure(self.figure.shape)
                self.generateFigure()
            else:
                tempFigure = Figure(self.figure.shape)
                self.figure = Figure(self.holdFigure.shape)
                self.holdFigure = Figure(tempFigure.shape)

        self.canHold = False

    #Parameters!

    def findHeights(self, fieldTest):
        
        heights = []
        for j in range(0, len(fieldTest[0])):
            for i in range(0, len(fieldTest)):
                if fieldTest[i][j] != 0:
                    heights.append(len(fieldTest) - i)
                    break
                if i == len(fieldTest) - 1:
                    heights.append(0)

        return heights

    def calcHeight (self, fieldTest, heights):

        totalHeight = 0
        maxHeight = -1
        numOfPits = 0
        
        for height in heights:
            totalHeight += height
            if height > maxHeight:
                maxHeight = height
            if height == 0:
                numOfPits += 1
                    
        return totalHeight, maxHeight, numOfPits

    def numOfHoles (self, fieldTest, heights):

        holes = 0
        columnsWithAHole = 0

        for j in range(0, len(fieldTest[0])):
            holesInColumn = 0
            for k in range(len(fieldTest) - heights[j], len(fieldTest)):
                if fieldTest[k][j] == 0:
                    holes += 1
                    holesInColumn += 1
            if holesInColumn > 0:
                columnsWithAHole += 1
        
        return holes, columnsWithAHole

    def calcBumpiness(self, heights):
        
        bumpiness = 0
        
        for i in range(len(heights) - 1):
            bumpiness += abs(heights[i] - heights[i+1])

        return bumpiness    

    def numOfRightLineBlocks(self, fieldTest, heights):
        
        counter = 0
        j = len(fieldTest[0]) - 1
        for i in range(len(fieldTest) - heights[-1], len(fieldTest)):
            if fieldTest[i][j] != 0:
                counter += 1

        return counter

    def calcDeepestWell(self, fieldTest, heights):

        wells = []
        for i in range(len(heights)):
            if i == 0:
                well = heights[1] - heights[0]
                if well <= 0:
                    well = 0
                wells.append(well)       
            elif i == len(heights) - 1:
                well = heights[-2] - heights[-1]
                if well <= 0:
                    well = 0
                wells.append(well)
            else:
                well1 = heights[i - 1] - heights[i]
                well2 = heights[i + 1] - heights[i]
                if well1 <= 0:
                    well1 = 0
                if well2 <= 0:
                    well2 = 0
                if well1 >= well2:
                    well = well1
                else:
                    well = well2

                wells.append(well)

        return max(wells)

    def calcLinesCleared(self, fieldTest):

        fullLines = 0

        for lineCounter in range (1, self.height):
            empty = 0
            for j in range (self.width):
                if fieldTest[lineCounter][j] == 0:
                    empty += 1
                    break
            
            if empty == 0:
                fullLines += 1

        tetrises = fullLines // 4
        rem = fullLines % 4

        lines3 = rem // 3
        rem = rem % 3

        lines2 = rem // 2
        rem = rem % 2

        return tetrises, lines3 + lines2 + rem

    #Evaluation functions!

    def findTestField (self, currMoves, figure):

        testFigure = Figure(figure.shape)
        fieldTest = copy.deepcopy(self.field)
        fieldTestCheck = copy.deepcopy(self.field)

        for move in currMoves:
            if move == 'L':
                testFigure.xPos -= 1
            elif move == 'R':
                testFigure.xPos += 1
            elif move == 'r':
                testFigure.rotate()
            else:
                print("Error: move not recognized!")

        while not self.collision(testFigure, True):
            testFigure.yPos += 1
        testFigure.yPos -= 1

        for rowNumbers in range (4):
            for column in range (4):
                if 4 * rowNumbers + column in testFigure.shapeData() and rowNumbers + testFigure.yPos > -1 and column + testFigure.xPos > -1:
                    fieldTest[rowNumbers + testFigure.yPos][column + testFigure.xPos] = testFigure.color
        
        if fieldTest == fieldTestCheck:
            return fieldTest, False
        return fieldTest, True


    def calcPositionValue (self, currMoves, figure):

        fieldTest, successValue = self.findTestField(currMoves, figure)    
        heights = self.findHeights(fieldTest)
        totalHeight, maxHeight, numOfPits = self.calcHeight(fieldTest, heights)
        holes, columnsWithAHoles = self.numOfHoles(fieldTest, heights)
        tetrises, threeOrLessLines = self.calcLinesCleared(fieldTest)

        if successValue:
            finalValue = self.parameters[0] * maxHeight + self.parameters[1] * totalHeight + self.parameters[2] * holes + self.parameters[3] * columnsWithAHoles + self.parameters[4] * self.calcBumpiness(heights) + self.parameters[5] * self.numOfRightLineBlocks(fieldTest, heights) + self.parameters[6] * numOfPits + self.parameters[7] * self.calcDeepestWell(fieldTest, heights) + self.parameters[8] * tetrises + self.parameters[9] * threeOrLessLines
        else:
            finalValue = float('-inf')
        return finalValue

    def simulateAllPositions(self, figure):

        bestValue = float('-inf')
        bestMoves = []

        for moves in moveCombinations[figure.shape]:
            currValue = self.calcPositionValue(moves, figure)
            if currValue > bestValue:
                bestValue = currValue
                bestMoves = moves

        return bestValue, bestMoves

#Helper

def printField(field):
    matrix = np.matrix(field)
    print(matrix)
    print()

#Game

def playTetris(parameters):

    score = 0

    pygame.init()

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (128, 128, 128)

    size = (1000, 1000)
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Tetris")

    endGame = False
    clock = pygame.time.Clock()
    fps = 30
    game = Tetris(parameters)
    counter = 0

    pressDown = False

    random.shuffle(game.figuresBag)

    while game.state != "gameover":

        if game.score >= 999999:
            game.state = "gameover"
            return game.score

        if game.figure is None:
            game.generateFigure()

        counter += 1
        if counter > 100000:
            counter = 0

        if counter % (fps // game.level // 2) == 0 or pressDown:
            if game.state == "start":
                game.moveDown()

        bestMoves = []
        if game.holdFigure is None:
            bestValueCurrent, bestMovesCurrent = game.simulateAllPositions(game.figure)
            bestValueNext, bestMovesNext = game.simulateAllPositions(game.nextFigure)

            if bestValueNext >= bestValueCurrent:
                game.hold()
                bestMoves = bestMovesNext
            else:
                bestMoves = bestMovesCurrent
        else:
            bestValueCurrent, bestMovesCurrent = game.simulateAllPositions(game.figure)
            bestValueHeld, bestMovesHeld = game.simulateAllPositions(game.holdFigure)

            if bestValueHeld >= bestValueCurrent:
                game.hold()
                bestMoves = bestMovesHeld
            else:
                bestMoves = bestMovesCurrent

        rotCounter = 0
        for move in bestMoves:
            if move == 'R':
                game.moveSide(1)
            elif move == 'L':
                game.moveSide(-1)     
            elif move == 'r':
                if rotCounter == 0:
                    rotCounter = 1
                    game.moveDown()
                game.rotate()
            else:
                print(move)
                print("Error: move not recognized!")
        game.moveBottom()

        
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                endGame = True
                game.state = "gameover"
            """ if event.type == pygame.KEYDOWN and game.state != "gameover":
                if event.key == pygame.K_UP:
                    game.rotate()
                if event.key == pygame.K_DOWN:
                    pressDown = True
                if event.key == pygame.K_LEFT:
                    game.moveSide(-1)
                if event.key == pygame.K_RIGHT:
                    game.moveSide(1)
                if event.key == pygame.K_SPACE:
                    game.moveBottom()
                if event.key == pygame.K_h:
                    game.hold()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return score

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    pressDown = False """

        screen.fill(WHITE)

        for i in range (game.height):
            for j in range (game.width):
                pygame.draw.rect(screen, GRAY, [game.xPos + game.zoom * j, game.yPos + game.zoom * i, game.zoom, game.zoom], 1)
                if game.field[i][j] > 0:
                    pygame.draw.rect(screen, colors[game.field[i][j]], [game.xPos + game.zoom * j + 1, game.yPos + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])

        if game.figure is not None:
            for i in range(4):
                for j in range(4):
                    p = 4 * i + j
                    if p in game.figure.shapeData():
                        pygame.draw.rect(screen, colors[game.figure.color], [game.xPos + game.zoom * (j + game.figure.xPos) + 1, game.yPos + game.zoom * (i + game.figure.yPos) + 1, game.zoom - 2, game.zoom - 2])

        for i in range (4):
            for j in range (4):
                pygame.draw.rect(screen, GRAY, [100 + game.zoom * j, 100 + game.zoom * i, game.zoom, game.zoom], 1)
                p = 4 * i + j
                if game.holdFigure is not None and p in game.holdFigure.shapeData():
                    pygame.draw.rect(screen, colors[game.holdFigure.color], [100 + game.zoom * j + 1, 100 + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])

        for i in range (4):
            for j in range (4):
                pygame.draw.rect(screen, GRAY, [760 + game.zoom * j, 100 + game.zoom * i, game.zoom, game.zoom], 1)
                p = 4 * i + j
                if game.nextFigure is not None and p in game.nextFigure.shapeData():
                    pygame.draw.rect(screen, colors[game.nextFigure.color], [760 + game.zoom * j + 1, 100 + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])


        fontCalibri = pygame.font.SysFont('Calibri', 50, True, False)
        textScore = fontCalibri.render("Score: " + str(game.score), True, BLACK)
        textGameOver = fontCalibri.render("Game Over", True, BLACK)
        textHeld = fontCalibri.render("Held", True, BLACK)
        textNext = fontCalibri.render("Next", True, BLACK)


        screen.blit(textScore, [400, 0])
        screen.blit(textHeld, [115, 250])
        screen.blit(textNext, [780, 250])
        if game.state == "gameover":
            screen.blit(textGameOver, [375, 900])

        pygame.display.flip()
        score = game.score
        clock.tick(fps)

    pygame.quit()
    return score

#parameters = holes, pillars, height, bumpiness, rightLineBlocks, openHoles, rowTrans, columnTrans, threeOrLess, TETRIS
#maxHeight, totalHeight, holes, columnsWithAHoles, Bumpiness, numOfRightLineBlocks, numOfPits, DeepestWell, tetrises, threeOrLessLines
parameters = [-4.559007630929106, -1.5595837011458946, -2.2505933871251207, -4.5628332872062485, -0.11242003274736323, 0.8487740555609218, -2.580379762741857, -3.5604646679756122, 4.539226493838742, 0.9277233544208183]
print(playTetris(parameters))
#print(playTetris(parameters))



