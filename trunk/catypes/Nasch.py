import random
from BaseCA import BaseCA, TorroidalCA

class Nasch(TorroidalCA):
    def __init__(self, numcells):
        super(Nasch, self).__init__(numcells)
        self.validRules = ['L','N']
        self.highestState = 10 #Applies to 'N' cells only
        self.randomization = 0.5
        self.randomRule()
    def drawCell (self, col):
        if self.ruleStr[col] == 'N': #unlike wolfram/spector, we always want to draw every node cell
            return True
        return self.cells[col] != 0
    def incCell(self, col, amt=1):
        self.setState(col, self.getState(col)+amt)
    def decCell(self, col, amt=1):
        self.setState(col, self.getState(col)-amt)
    def emitMessageFrom(self, col):
        self.decCell(col)   # Take a message from col
        self.incCell(col+1) # and move it to the right
    def updateOrder(self):
        #NOTE: order is reversed to prevent avalanche effect.
        #If you want non-sequential order you'll have to change the step
        #method so that cells don't emit messages during the same generation
        #they receive them.
        return xrange(self.numcells-1,-1,-1)
    def step(self):
        willEmit = {} # {column number:True|False}
        # Iterate through cells and randomly select nodes to emit
        for col in range(self.numcells):
            #Cell must have messages in its queue
            if self.ruleStr[col] == 'N' and self.cells[col] > 0:
                willEmit[col] = bool(random.random() < self.randomization)
        for col in self.updateOrder():
            # A node emits when:
            #       1) it was selected in last step,
            #       2) it's loaded*, 
            #       3) and its neighbor is accepting^
            # A link emits when:
            #       1) it's loaded*,
            #       2) and its neighbor is accepting^
            # * cell has message(s) in queue
            # ^ cell has space in queue for more messages
            emittingNode = willEmit.get(col,False) and \
                           self.getState(col+1) < self.highestState
            emittingLink = self.ruleStr[col] == 'L' and self.getState(col) > 0
            if emittingNode or emittingLink:
                self.emitMessageFrom(col)
    def maxPacketsForCell(self,col):
        typeOfNode = self.ruleStr[self.wrapCell(col)]
        packetLimit = { 'L' : 1, 'N' : self.highestState}[typeOfNode]
        return packetLimit
    def randomize(self):
        self.randomizePercent(10) #10% of packet capacity
    def randomizePercent(self, percentDistribution):
        packetCapacity = 0
        # calculate packet capacity, and reset grid while we're at it.
        for col in range (self.numcells):
            self.cells[col] = 0
            typeOfNode = self.ruleStr[col]
            packetCapacity += { 'L' : 1, 'N' : self.highestState}[typeOfNode]
        # we'll have this number of packets propagate through the system
        numPackets = percentDistribution/100.0*packetCapacity 
        curPackets = 1
        cellToFill = 0
        while curPackets < numPackets:
            cellToFill = random.randint (0,self.numcells-1)
            if self.getState (cellToFill) < self.maxPacketsForCell (cellToFill):
                self.cells[cellToFill] +=1
                curPackets +=1
    def shapeToDraw(self, cell):
        return {'N' : 'circle', 'L' : 'square' } [self.ruleStr[cell]]
    def randomRule(self):
        self.ruleStr = ""
        for i in range (self.numcells):
            self.ruleStr += {0 : 'N', 1 : 'L'}[random.randint(0,1)]
    def setRule(self,rule):
        if isinstance(rule, int):
            # Int -> rule string (array of '1' and '0' characters)
            self.rulesTable = [str(int((rule&1<<(7-i))>0)) for i in range(8)]
        elif isinstance(rule, str):
            if len(rule) != len(self.rulesTable):
                # Pyconsole echos return values :)
                return "ERROR: requires %d character string." % len(self.rulesTable)
            self.rulesTable = list(rule)
