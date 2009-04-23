import pygame
from pygame.locals import *

bgcolor = [0x00, 0x00, 0x00] # Background
bocolor = [0x10, 0x10, 0x10] # Border
fgcolor = [0x00, 0xff, 0x00] # Foreground

#TODO:
#  Allow other types of displays, eg. 2D

class CADisplay:
    def __init__(self, screen, board, fancy=True):
        self.screen = screen
        self.board = board
        cwidth = (screen.get_width()/board.numcells) - 1 # -1 gives space for border
        self.cellOffset = 0    #The leftmost cell to actually display (allows for larger board sizes
                               #than will fit on the screen)
        self.dispNum = board.numcells
        if cwidth < 2:
            cwidth = 2
            self.cellOffset = (board.numcells - (screen.get_width()/cwidth+1))/2
            self.dispNum = board.numcells - (2*self.cellOffset)
            if (self.cellOffset + self.dispNum) > board.numcells:
                self.dispNum = board.numcells
        cheight = cwidth
        self.histlen = screen.get_height()/cheight

        #Not all grid sizes will fit the screen perfectly, so center the array
        if self.cellOffset > 0:
            # Push half of the disp off the left side of the screen
            offset = -1 * (self.cellOffset * (cwidth+1))
        else:
            # Push everything a few pixels to the right
            offset = (screen.get_width()%(cwidth+1))/2

        #Fancy mode makes the history fade out
        if fancy:
            geomP = 255/self.histlen if self.histlen < 255 else 1
            self.screen.set_alpha(255 - geomP)
        self.screen.fill(bgcolor)

        #History rects, Rectangles defining each row on the screen
        self.histrects = []
        for i in range(self.histlen):
            self.histrects.append(pygame.Rect(0, i*cheight+i, screen.get_width(), cheight+1))

        #Current cell rects
        self.cellRects = []
        for col in range(board.numcells):
            self.cellRects.append(pygame.Rect(offset + col*cwidth+col, screen.get_height()-cheight, cwidth, cheight))

        self.running = True

    def run(self):
        """Run the simulation"""
        self.running = True
    def stop(self):
        """Stop the simulation"""
        self.running = False
    def update(self):
        """Step the display, only if the simulation is running"""
        if not self.running:
            return
        self.step()
    def step(self):
        """Advance the simulation and display by one timestep"""
        if self.running:
            for i in range(self.histlen-1):
                self.screen.fill(bgcolor, self.histrects[i])
                self.screen.blit(self.screen, self.histrects[i], self.histrects[i+1])
        #Clear the bottom row for new data
        self.screen.fill(bgcolor, self.histrects[-1])
        #Copy new data into the display
        for col in range(self.dispNum):
            actualPos = self.cellOffset + col
            #hack to display nasch automata correctly
            shouldDraw = self.board.drawCell(actualPos)
            if shouldDraw:
                shapeToDraw = self.board.shapeToDraw (col)
                if shapeToDraw == 'square':
                    pygame.draw.rect(self.screen, fgcolor, self.cellRects[actualPos])
                elif shapeToDraw == 'circle':
                    newFgColor = []
                    #TODO: make this more logical, so that color shades apply to non-circles
                    for fgComponent in fgcolor:
                        adjustedVal = fgComponent*self.board.getState (col) / self.board.highestState
                        """ Don't want to become too dark... """
                        newFgColor.append (min (adjustedVal + 0.2 * fgComponent,255))
                    cellRect = self.cellRects[actualPos]
                    pygame.draw.circle (self.screen, newFgColor, cellRect.center, cellRect[3]/2)
        #Step the simulation
        self.board.step()
