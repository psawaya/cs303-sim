#     CS303 Cellular Automata Simulator
#     Copyright (C) 2009 Hampshire College CS303
#     
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#     
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#     
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import random
import pyconsole
import pygame
from pygame.locals import *

#TODO: Better cli argument handling
if len(sys.argv) == 2:
    numcells = int(sys.argv[1])
else:
    numcells = 40

## Global constants ##
bgcolor = [0x00, 0x00, 0x00] # Background
bocolor = [0x10, 0x10, 0x10] # Border
fgcolor = [0x00, 0xff, 0x00] # Foreground
SCREENW = 600 # Screen Width
SCREENH = 600 # Screen Height

def main():
    G_Screen = pygame.display.set_mode((SCREENW,SCREENH))
    G_Screen.fill(bgcolor)
    board = WolframArray(numcells)
    D_Screen = pygame.Surface((SCREENW, SCREENH))
    display = CADisplay(D_Screen, board, fancy=True)
    C_Screen = pygame.Surface((SCREENW, SCREENH/2))
    console = pyconsole.Console(C_Screen,
                                (0,0,SCREENW, SCREENH/2),
                                functions={"+":board.setAlive,
                                           "-":board.setDead,
                                           "print":board.toString,
                                           "rand":board.randomize,
                                           "setspectorstr":board.setRule,
                                           "stop":display.stop,
                                           "start":display.run,
                                           "step":display.step},
                                key_calls={"d":sys.exit})
    delay = 100 #milliseconds
    while 1:
        console.process_input()
        #Handle Events
        for event in pygame.event.get():
            #Keypresses
            if event.type == KEYDOWN:
                # q quits
                if event.key == K_q:
                    pygame.event.post(pygame.event.Event(QUIT))
                # w toggles the console
                elif event.key == K_w:
                    console.set_active()
                # r randomizes the display
                elif event.key == K_r:
                    board.randomize()
                # s steps the simulator
                elif event.key == K_s:
                    display.step()
                # 1 sets the sim speed to slow
                elif event.key == K_1:
                    delay = 200
                # 2 sets the sim speed to medium 
                elif event.key == K_2:
                    delay = 100
                # 1 sets the sim speed to /fast/ 
                elif event.key == K_3:
                    delay = 10
            elif event.type == QUIT:
                sys.exit()
        #Draw the console to its buffer
        console.draw()
        #Update the simulation
        display.update()
        #blit the simulation surface to the root surface
        G_Screen.blit(D_Screen,(0,0))
        #blit the console surface to the root surface if it's active
        if console.active:
            G_Screen.blit(C_Screen, (0,0))
        #Display the screen
        pygame.display.flip()
        #Wait until next timestep
        pygame.time.wait(delay)

class CADisplay:
    def __init__(self, screen, board, fancy=True):
        self.screen = screen
        self.board = board
        #Fancy mode makes the history fade out
        self.fancy = fancy
        if self.fancy:
            self.screen.set_alpha(210)
        self.screen.fill(bgcolor)
        cwidth = screen.get_width()/board.numcells
        cheight = screen.get_height()/board.numcells
        self.histlen = screen.get_height()/cheight
        #History rects, Rectangles defining each row on the screen
        self.histrects = []
        for i in range(self.histlen):
            self.histrects.append(pygame.Rect(0, cheight*i, screen.get_width(), cheight))
        #Current cell rects
        self.cellRects = []
        for col in range(numcells):
            self.cellRects.append(pygame.Rect(col*cwidth, screen.get_height()-cheight, cwidth, cheight))
        self.running = True
    def run(self):
        """Run the simulation"""
        self.running = True
    def stop(self):
        """Stop the simulation"""
        self.running = False
    def update(self):
        if not self.running:
            return
        self.step()
    def step(self):
        """Advance the simulation and display by one timestep"""
        for i in range(self.histlen-1):
            self.screen.fill(bgcolor, self.histrects[i])
            self.screen.blit(self.screen, self.histrects[i], self.histrects[i+1])
            #Double blit necessary for fancy screen!
            if self.fancy:
                self.screen.blit(self.screen, self.histrects[i], self.histrects[i+1])
        #Step the simulation
        self.board.step()
        #Clear the bottom row for new data
        self.screen.fill(bgcolor, self.histrects[-1])
        #Copy new data into the display
        for col in range(numcells):
            alive = self.board.isAlive(col)
            if alive:
                pygame.draw.rect(self.screen, fgcolor, self.cellRects[col])
            pygame.draw.rect(self.screen, bocolor, self.cellRects[col], 1)

class WolframArray:
    def __init__(self, numcells):
        self.numcells = numcells
        self.cells = [0]*self.numcells
        
        #This rule only shifts living cells to the left and leaves the rest alone
        self.rulesTable = ['C','C','L','L','C','C','L','L']
    def toString(self):
        return ''.join(str(i) for i in self.cells)
    def neighborCount(self, row):
        return sum(self.getNeighbors(row))
    def getNeighbors(self, col):
        neighbors = [self.cellAt(col-1), self.cellAt(col+1)]
        return neighbors
    def cellAt(self, col):
        # % numcells for torroidal display:
        return self.cells[col % self.numcells]
    def wrapCell(self, col):
        return col % self.numcells
    def setAlive(self, col):
        """Turn the specified cell on"""
        self.cells[self.wrapCell(col)] = 1
    def setDead(self, col):
        """Turn the specified cell on"""
        self.cells[self.wrapCell(col)] = 0
    def isAlive(self, col):
        return bool(self.cells[col])
    def setState (self, col, state):
    	self.cells[col] = state
    def randomize(self):
        """Randomize the display"""
        for r in range(numcells):
            self.cells[r] = random.randint(0,1)
    def swapCells (self,cellA, cellB):
    	oldA = self.isAlive (cellA)
    	self.setState(cellA, self.isAlive (cellB))
    	self.setState (cellB, oldA)
    def step(self):
    	#For now, just update one cell per step
    	col = random.randint (0,self.numcells-1)
    	ruleToUseIdx = self.cellAt (col-1) + self.cellAt(col) * 2 + self.cellAt(col+1) * 4
    	ruleToUse = self.rulesTable[ruleToUseIdx]
    	if ruleToUse.upper() == 'L':
    		self.swapCells (self.wrapCell(col-1),self.wrapCell(col))
    	elif ruleToUse.upper() == 'R':
    		self.swapCells (self.wrapCell(col),self.wrapCell(col+1))
		#if ruletouse == 'c', do absolutely nothing!
    def setRule(self,ruleStr):
    	if len(ruleStr) != 8:
            # Pyconsole echos return values :)
            return "ERROR: requires 8 character string."
    	for idx in range (len(ruleStr)):
            self.rulesTable[idx] = ruleStr[idx]   


if __name__ == "__main__":
    main()
