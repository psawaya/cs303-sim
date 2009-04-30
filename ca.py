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

#add start/stop collecting data commands, for n generations, spit results out into file

import sys
import pyconsole
import pygame
import traceback
from pygame.locals import *
from math import log
from threading import Thread, Event

import catypes
from display import CADisplay

class CAEnvironment(object):
    def __init__(self, numcells=31, catype=catypes.BaseCA, fancy=True,
                        (screenW, screenH)=(600,600)):
        ## Initialize pygame display
        self.G_Screen = pygame.display.set_mode((screenW,screenH))
        ## Create cellular automata
        self.board = catype(numcells)
        ## Create a surface to draw the CA on, and the display object
        self.D_Screen = pygame.Surface((screenW, screenH))
        self.display = CADisplay(self.D_Screen, self.board, fancy=fancy)
        ## Create a surface to draw the console on and the console object
        self.C_Screen = pygame.Surface((screenW, screenH/4))
        
        defaultFuncs = {"+":self.board.setAlive,
                                               "-":self.board.setDead,
                                               "print":self.board.toString,
                                               "rand":self.board.randomize,
                                               "clear":self.board.clear,
                                               "setrule":self.board.setRule,
                                               "setspectorstr":self.board.setRule,
                                               "setdelay":self.setdelay,
                                               "stop":self.display.stop,
                                               "start":self.display.run,
                                               "step":self.display.step,
                                               "quit":self.quit}
        
        consoleFuncs = defaultFuncs
        consoleFuncs.update (self.board.returnSpecificFunctions())
        
        self.console = pyconsole.Console(self.C_Screen,
                                    (0,0,screenW, screenH/4), self.sched,
                                    functions=consoleFuncs,
                                    key_calls={"d":self.quit})
        ## Number of milliseconds to wait between generations
        self.delay = 100
        ## Queue for tasks added by event loop
        self.tasks = []

        self.doneflag = Event()
       ## Start the event loop
        self.e = Thread(target=self.main, args=[self.doneflag])
        self.e.start()
        self.eventLoop(self.doneflag)

    def drawConsole(self):
        self.console.draw()
        if self.console.active:
            self.G_Screen.blit(self.C_Screen, (0,0))
        #pygame.display.update(self.console.rect)
        pygame.display.flip()

    def setdelay(self, n):
        self.delay = n

    def quit(self):
        self.doneflag.set()
        try:
            self.e.join()
        except RuntimeError, e:
            print e
        try:
            sys.exit()
        except SystemExit:
            # Keep quiet on exit
            pass

    def sched(self, method, args=[]):
        self.tasks.append((method, args))

    def pop_external_tasks(self):
        """Thread safe method to execute externally
           added tasks
        """
        try:
            while self.tasks:
                func, args = self.tasks.pop()
                func(*args)
        except:
            self.error("Exception in interpreted command")

    def error(self, m="Exception raised"):
        print m
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60

    def main(self, doneflag):
        try:
            while not doneflag.isSet():
                ## Update the simulation
                self.display.update()
                ## Blit the simulation surface to the root surface
                self.G_Screen.blit(self.D_Screen,(0,0))
                ## Wait until next timestep
                doneflag.wait(float(self.delay)/1000)
        except:
            self.error("Exception in main loop")
            self.sched(quit)

    def eventLoop(self, doneflag):
        try:
            while not doneflag.isSet():
                self.pop_external_tasks()
                self.handleInput()
                self.drawConsole()
                doneflag.wait(0.016)
                #pygame.time.wait(16)
        except:
            self.error("Exception in event loop")
            self.quit()

    def handleInput(self):
        """Runs in its own thread"""
        self.console.process_input()
        #Handle Events
        for event in pygame.event.get():
            #Keypresses
            if event.type == KEYDOWN:
                # q quits
                if event.key == K_q:
                    self.sched(pygame.event.post, \
                                    [pygame.event.Event(QUIT)])
                # w toggles the console
                elif event.key == K_w:
                    self.sched(self.console.set_active)
                # r randomizes the display
                elif event.key == K_r:
                    self.sched(self.board.randomize)
                # s steps the simulator
                elif event.key == K_s:
                    self.sched(self.display.step)
                # 1 sets the sim speed to slow
                elif event.key == K_1:
                    self.sched(self.setdelay, [200])
                # 2 sets the sim speed to medium 
                elif event.key == K_2:
                    self.sched(self.setdelay, [100])
                # 3 sets the sim speed to /fast/ 
                elif event.key == K_3:
                    self.sched(self.setdelay, [10])
            elif event.type == QUIT:
                self.sched(self.quit)

if __name__ == "__main__":
    #TODO: Better cli argument handling
    args = {'numcells':31, \
            'catype':catypes.Wolfram, \
            'fancy':True}
    for i in sys.argv:
        x = i.split("=")
        if x[0] == '?' or len(sys.argv) == 1:
            print "Usage: python ca.py [ca=MachineName] [n=Num. Cells] [fancy=True|False]"
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
    CAEnvironment(**args)
