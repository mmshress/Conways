import sys, pygame, time, copy
import Tkinter
import tkMessageBox
pygame.init()

displayWidth = 1000
displayHeight = 1000
cellWidth = 20
cellHeight = 20
margin = 5
cells = []

screen = pygame.display.set_mode((displayWidth, displayHeight))

def drawFinalPopup():
    root = Tkinter.Tk()
    root.withdraw()
    tkMessageBox.showinfo("Done!", "Final state reached!")
    sys.exit()

def drawGrid(cells, screen):
        column = 0
        row = 0
        for i in range(0, displayWidth, (cellWidth + margin)):
            for j in range(0, displayHeight, (cellHeight + margin)):
                if cells[column][row] == 1: cellColor = pygame.Color("white") #alive cells are white
                if cells[column][row] == 0: cellColor = pygame.Color("black") #dead cells are black
                currentCell = pygame.Rect((i, j), (cellWidth, cellHeight))
                pygame.draw.rect(screen, cellColor, currentCell)
                row += 1
            row = 0
            column += 1

def getAliveNeighbors(cells, column, row):
    if((row == len(cells) - 1)):
        if(column == len(cells) - 1):
            return cells[column - 1][row] + cells[column][row - 1] + cells[column - 1][row - 1]
        elif(column == 0):
            return cells[column + 1][row] + cells[column][row - 1] + cells[column + 1][row - 1]
        else:
            return cells[column + 1][row] + cells[column][row - 1] + cells[column - 1][row] + cells[column - 1][row - 1] + cells[column + 1][row - 1]
    elif((column == len(cells) - 1)):
        if(row == 0):
            return cells[column - 1][row] + cells[column][row + 1] + cells[column - 1][row - 1]
        else:
            return cells[column - 1][row] + cells[column][row + 1] + cells[column][row - 1] + cells[column - 1][row - 1] + cells[column - 1][row + 1]
    elif((column == 0)):
        if(row == 0):
            return cells[column + 1][row] + cells[column][row + 1] + cells[column + 1][row + 1]
        else:
            return cells[column + 1][row] + cells[column][row + 1] + cells[column][row - 1] + cells[column + 1][row + 1] + cells[column + 1][row - 1]
    elif((row == 0)):
        return cells[column + 1][row] + cells[column - 1][row] + cells[column][row + 1] + cells[column + 1][row + 1] + cells[column - 1][row + 1]
    else:
        return (cells[column + 1][row] + cells[column - 1][row] + cells[column][row + 1] + cells[column][row - 1] + cells[column - 1][row - 1] + cells[column - 1][row + 1]
        + cells[column + 1][row - 1] + cells[column + 1][row + 1])

def updateCells(cells):
    newCells = copy.deepcopy(cells) #copy the list to a new object, newCells = cells still points to the same object
    for i in range(0, len(cells)):
        for j in range(0, len(cells[0])):
            adjacentLives = getAliveNeighbors(cells, i, j)
            if(cells[i][j] == 1):
                if adjacentLives == 2 or adjacentLives == 3:
                    # print("Cell {0}, {1} is living on".format(i, j))
                    newCells[i][j] = 1
                elif adjacentLives < 2 or adjacentLives > 3:
                    # print("Cell {0}, {1} is dying".format(i, j))
                    newCells[i][j] = 0
            else:
                if adjacentLives == 3:
                    # print("Cell {0}, {1} came to life".format(i, j))
                    newCells[i][j] = 1
    # print("Generation complete")
    return newCells, (newCells == cells)


#initialize cells
cells = []
for i in range((displayWidth / (cellWidth + margin))):
    cells.append([])
    for j in range((displayHeight / (cellHeight + margin))):
        cells[i].append(0)


conwaysFlag = False
conwaysDone = False
while True:
    if(conwaysFlag and not(conwaysDone)):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN: #press Enter to interrupt/reset
                conwaysFlag = False
                #reinit cells
                cells = []
                for i in range((displayWidth / (cellWidth + margin))):
                    cells.append([])
                    for j in range((displayHeight / (cellHeight + margin))):
                        cells[i].append(0)
                continue
        screen.fill(pygame.Color("blue"))
        time.sleep(.4)
        cells, conwaysDone = updateCells(cells) #conwaysDone flag to check if no change btn. generations
        drawGrid(cells, screen)
        pygame.display.flip()
    elif(conwaysDone):
        drawFinalPopup()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN: #press Enter to interrupt/reset
                conwaysFlag = False
        screen.fill(pygame.Color("blue"))
        time.sleep(.4)
        drawGrid(cells, screen)
        pygame.display.flip()
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                column = x / (cellWidth + margin)
                row = y / (cellWidth + margin)
                if cells[column][row] == 0:
                    cells[column][row] = 1
                elif cells[column][row] == 1:
                    cells[column][row] = 0
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                conwaysFlag = True
        screen.fill(pygame.Color("blue"))
        drawGrid(cells, screen)
        pygame.display.flip()
