import pygame, random, sys
from pygame.locals import *

if len(sys.argv) == 2:
    numcells = int(sys.argv[1])
else:
    numcells = 40

def main():
    G_Screen = pygame.display.set_mode((400,400))
    G_Screen.fill([0xff,0xff,0xff])
    cwidth = G_Screen.get_width()/numcells
    cheight = G_Screen.get_height()
    board = WolframArray(numcells)
    display = CADisplay(G_Screen, board)
    execSpeed = 100
    while 1:
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
        display.update()

class CADisplay:
    def __init__(self, screen, board):
        self.screen = screen
        self.screen.fill([0,0,0])
        self.board = board
        cwidth = screen.get_width()/board.numcells
        cheight = screen.get_height()/board.numcells
        self.histlen = screen.get_height()/cheight
        self.rects = []
        #History rects
        for i in range(self.histlen):
            self.rects.append(pygame.Rect(0, cheight*i, screen.get_width(), cheight))
        #Current cell rects
        self.cellRects = []
        for col in range(numcells):
            self.cellRects.append(pygame.Rect(col*cwidth, screen.get_height()-cheight, cwidth, cheight))
    def update(self):
        for i in range(self.histlen-1):
            self.screen.blit(self.screen, self.rects[i], self.rects[i+1])
        self.screen.fill([0,0,0], self.rects[-1])
        for col in range(numcells):
            alive = self.board.isAlive(col)
            pygame.draw.rect(self.screen, (0, 0xff*alive, 0), self.cellRects[col])
        self.board.step()
        pygame.display.flip()
        pygame.time.wait(100)

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
