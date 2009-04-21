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
    def step(self):
    	#For now, just update one cell per step
        tmp = []
        """ Nodes decide to emit packets randomly, iterate through cells and decide which ones will first """
        willEmit = {}
        for col in range(self.numcells):
        	#cells with state 0 have nothing to emit
        	if self.ruleStr[col] == 'N' and self.cells[col] > 0:
        		willEmit[col] = bool(random.random() < self.randomization)
        for col in self.updateOrder():
        	leftCell = self.wrapCell(col-1)
        	leftCellWillEmit = self.getState(col-1) > 0 and (self.ruleStr[leftCell] == 'L' or willEmit[leftCell])
        	if self.ruleStr[col] == 'N':
        		if self.getState(col) < self.highestState and leftCellWillEmit:
        			tmp.append (self.getState(col) + 1) #get packet from neighbor to left
        			continue
        		if self.getState(col) > 0: #Are there packets in my queue? Have I decided to emit?
					if self.maxPacketsForCell (col+1) and willEmit[col]: #if so, release one
						tmp.append (self.getState(col)-1)
					else: #otherwise, stay the same
						tmp.append (self.getState(col))
			else:
				tmp.append (0) #waiting for packets...
        	else:
				if self.getState (col) == 0: #link cell, currently empty
					if leftCellWillEmit:
						tmp.append (1)
					else:
						tmp.append (0)
				else: #link cell, currently full
					if self.getState (col+1) < self.maxPacketsForCell (col+1):
						tmp.append(0)
					else:
						tmp.append(1)
        self.cells = tmp
    def maxPacketsForCell(self,col):
    	typeOfNode = self.ruleStr[self.wrapCell(col)]
    	packetLimit = { 'L' : 1, 'N' : self.highestState}[typeOfNode]
    	return packetLimit
    def randomize(self):
    	self.randomizePercent(10) #10% of packet capacity
    def randomizePercent(self, percentDistribution):
		packetCapacity = 0
		""" calculate packet capacity, and reset grid while we're at it. """
		for col in range (self.numcells):
			self.cells[col] = 0
			typeOfNode = self.ruleStr[col]
			packetCapacity += { 'L' : 1, 'N' : self.highestState}[typeOfNode]
		""" we'll have this number of packets propagate through the system """
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
    def getState(self, col):
    	return self.cells[self.wrapCell (col)]
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
