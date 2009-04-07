import pygame, random, sys
from pygame.locals import *

if len(sys.argv) == 2:
    numcells = int(sys.argv[1])
else:
    numcells = 31

def main():
    G_Screen = pygame.display.set_mode((310,50))
    G_Screen.fill([0xff,0xff,0xff])
    cwidth = G_Screen.get_width()/numcells
    cheight = G_Screen.get_height()
    cellRects = []
    for col in range(numcells):
        cellRects.append(pygame.Rect(col*cwidth, 0, cwidth, cheight))
    board = WolframArray(numcells)
    board.setAlive(1)
    board.setAlive(2)
    board.setAlive(3)
    execSpeed = 100
    while 1:
        G_Screen.fill([0,0,0])
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_q:
                    pygame.event.post(pygame.event.Event(QUIT))
                elif event.key == K_r:
                    board.randomize()
                elif event.key == K_1:
                    execSpeed = 10
                elif event.key == K_2:
                    execSpeed = 100
                elif event.key == K_3:
                    execSpeed = 200
            elif event.type == QUIT:
                sys.exit()
        for col in range(numcells):
            alive = board.isAlive(col)
            pygame.draw.rect(G_Screen, (0, 0xff*alive, 0), cellRects[col])
        board.step()
        pygame.display.flip()
        pygame.time.wait(execSpeed)

class WolframArray:
    def __init__(self, numcells):
        self.numcells = numcells
        self.cells = [0]*self.numcells
    def neighborCount(self, row):
        return sum(self.getNeighbors(row))
    def getNeighbors(self, col):
        neighbors = [self.cellAt(col-1), self.cellAt(col+1)]
        return neighbors
    def cellAt(self, col):
        if col < 0:
            col = self.numcells-1
        elif col >= self.numcells:
            col = 0
        return self.cells[col]
    def setAlive(self, col):
        self.cells[col] = 1
    def setDead(self, col):
        self.cells[col] = 0
    def isAlive(self, col):
        return bool(self.cells[col])
    def randomize(self):
        for r in range(numcells):
            self.cells[r] = random.randint(0,1)
    def step(self):
        pass
        #ctemp = self.cells.copy()
        #for c in range(numcells):
        #    n = self.neighborCount(c)
            # Rules go here
            #if self.isAlive(c):
                #if n < 2 or n > 3:
                    #ctemp[c] = 0
            #else:
                #if n == 3:
                    #ctemp[c] = 1
        #    self.cells = ctemp


if __name__ == "__main__":
    main()
