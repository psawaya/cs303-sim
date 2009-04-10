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
import pyconsole
import pygame
from pygame.locals import *
from math import log

import catypes
from display import CADisplay

## Global constants ##
SCREENW = 600 # Screen Width
SCREENH = 600 # Screen Height

def main(numcells=31, catype=catypes.BaseCA, fancy=True):
    G_Screen = pygame.display.set_mode((SCREENW,SCREENH))
    board = catype(numcells)
    D_Screen = pygame.Surface((SCREENW, SCREENH))
    display = CADisplay(D_Screen, board, fancy=fancy)
    C_Screen = pygame.Surface((SCREENW, SCREENH/4))
    console = pyconsole.Console(C_Screen,
                                (0,0,SCREENW, SCREENH/4),
                                functions={"+":board.setAlive,
                                           "-":board.setDead,
                                           "print":board.toString,
                                           "rand":board.randomize,
                                           "clear":board.clear,
                                           "setrule":board.setRule,
                                           "setspectorstr":board.setRule,
                                           "stop":display.stop,
                                           "start":display.run,
                                           "step":display.step,
                                           "quit":sys.exit},
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
                # 3 sets the sim speed to /fast/ 
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

if __name__ == "__main__":
    #TODO: Better cli argument handling
    args = {'numcells':31, \
            'catype':catypes.Wolfram, \
            'fancy':True}
    for i in sys.argv:
        x = i.split("=")
        if x[0] == '?' or len(sys.argv) == 1:
            print "Usage: python ca.py [ca=MachineName] [n=Num. Cells] \
                   [fancy=True|False]"
        elif x[0] == 'n':
            args['numcells'] = int(x[1])
        elif x[0] == 'ca':
            try:
                args['catype'] = getattr(catypes, x[1])
            except AttributeError:
                print "%s is not a valid CA Type." % x[1],
                print "use one of: %s" % ', '.join(catypes.availCAs)
        elif x[0] == 'fancy' and x[1] in ("True","False"):
            args['fancy'] = eval(x[1])
    main(**args)
