import random
from BaseCA import BaseCA, TorroidalCA

class Nasch(TorroidalCA):
    def __init__(self, numcells):
        super(Nasch, self).__init__(numcells)
        self.validRules = ['L','N']
        self.highestState = 3 #Applies to 'N' cells only
        self.randomization = 0.5
        self.randomRule()
        self.asyncUpdate = True
        self.countingFlux = False
        self.fluxCount = 0
        self.fluxValue = 0 #the flux value as it changes
        self.doingReport = False
    def returnSpecificFunctions(self):
    	return {'randompercent' : self.randomizePercent,
    	'setrandomization' : self.setRandomization, 
    	'setnodedistpercent' : self.setNodeDist,
    	 'setasync' : self.setAsync,
    	 'beginfluxcount' : self.beginFluxCount,
    	 'genreport' : self.beginReport}
    def beginReport(self, param, start, end, step, filename):
    	self.doingReport = True
    	self.reportParamType = param
    	self.reportParam = start
    	self.reportParamStart = start
    	self.reportParamEnd = end
    	self.reportParamStep = step
    	self.reportFilename = filename
    	self.setParam (param, start)
    	reportFile = open (filename + '.csv', 'w')
    	reportFile.write ('') #clear the report file first
    	reportFile.close()
    	self.beginFluxCount (200) 
    def setParam(self,param, value):
        #for now, random packet density percent is only param
        self.randomizePercent (value)
    def beginFluxCount(self, generations):
    	try:
	    	self.fluxCell = self.ruleStr.index ('L') #which cell we're using to calc flux
        except ValueError:
        	return "ERROR: There are no link cells." #TODO: find out why this won't appear on the console
    	self.countingFlux = True
    	self.fluxCount = 0 #count the number of generations we sampled
    	self.fluxValue = 0	    	
    	self.fluxCellLast = self.getState (self.fluxCell)
    	print "flux cell is of type: " + str (self.ruleStr[self.fluxCell])
    	self.fluxGenerations = generations
    def setAsync(self,setTo):
    	self.asyncUpdate = (setTo == 'on')
    def setNodeDist(self,nodeDistPercent):
		newRules = ['L'] * self.numcells
		numberNodeCells = int (nodeDistPercent / 100.0 * self.numcells)
		for i in range (numberNodeCells):
			newRules[i] = 'N'
		random.shuffle (newRules)
		self.ruleStr = newRules
        #Make sure that our new rules and old states are consistent
		for i in range (self.numcells):
			self.cells[i] = min (self.maxPacketsForCell(i), self.cells[i])
    def setRandomization(self,randomization):
    	self.randomization = randomization
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
        if self.asyncUpdate:
			update = range(self.numcells-1,-1,-1)
#			random.shuffle (update)
			return update
        else:
            return xrange(self.numcells-1,-1,-1)
    def step(self):
        willEmit = {} # {column number:True|False}
        # Iterate through cells and randomly select nodes to emit
        for col in range(self.numcells):
            #Cell must have messages in its queue
            if self.ruleStr[col] == 'N' and self.cells[col] > 0:
                willEmit[col] = bool(random.random() < self.randomization)
        updateCols = self.updateOrder()
        for col in updateCols:
            # A node emits when:
            #       1) it was selected in last step,
            #       2) it's loaded*, 
            #       3) and its neighbor is accepting^
            # A link emits when:
            #       1) it's loaded*,
            #       2) and its neighbor is accepting^
            # * cell has message(s) in queue
            # ^ cell has space in queue for more messages
            #Not going to emit if neighbor isn't accepting
            if self.getState(col+1) == self.maxPacketsForCell (col+1):
                continue
            emittingNode = willEmit.get(col,False) 
            emittingLink = self.ruleStr[col] == 'L' and self.getState(col) > 0
            if emittingNode or emittingLink:
                self.emitMessageFrom(col)
                """ Even with async updating, we can't allow a packet to skip multiple cells in one
	            generation, since that could throw off our flux calculation. """
                if self.asyncUpdate: updateCols.remove (self.wrapCell(col+1))
        if self.countingFlux:
            if self.fluxCount == self.fluxGenerations:
                print "fluxValue: " + str (self.fluxValue)
                if self.doingReport:
                    if self.reportParam > self.reportParamEnd:
                        self.doingReport = False
                    else:
                        reportFile = open (self.reportFilename + '.csv', 'a')
                        reportFile.write (str(self.reportParam) + '\t' + str(self.fluxValue) + '\n')
                        reportFile.close()
                        self.reportParam += self.reportParamStep
                        self.setParam (self.reportParamType, self.reportParam)                        
                        self.beginFluxCount (200)
                        print "wrote to file!"
                else:
                    self.countingFlux = False
            else:
				if self.fluxCellLast != self.getState (self.fluxCell):
					self.fluxValue += (1.0/self.fluxGenerations)
				self.fluxCellLast = self.getState (self.fluxCell)
#				self.fluxValue += (1.0/self.fluxGenerations) * (self.cells[self.fluxCell] > 0)
#				print "Adding: " + str((1.0/self.fluxGenerations) * (self.cells[self.fluxCell] > 0))
				self.fluxCount += 1
    def doCount(self): #for debugging
    	count = 0
    	highState = 0
    	for i in range (self.numcells):
    	    count += self.cells[i]
    	    highState = [highState,self.cells[i]][self.cells[i]>highState]
    	print "count states: "  + str(count)
    	print "highest state: " + str(highState)
    def getPacketCapacity(self):
		count = 0
		for col in range (self.numcells):
			count += self.maxPacketsForCell(col)
		return count
    def maxPacketsForCell(self,col):
        typeOfNode = self.ruleStr[self.wrapCell(col)]
        packetLimit = { 'L' : 1, 'N' : self.highestState}[typeOfNode]
        return packetLimit
	def randomize(self):
		self.randomizePercent(10) #10% of packet capacity
    def randomizePercent(self, percentDistribution):
        newCells = [0] * self.numcells
        # we'll have this number of packets propagate through the system
        numPackets = percentDistribution/100.0*self.getPacketCapacity()
        curPackets = 0
        cellToFill = 0
        while curPackets < numPackets:
		    cellToFill = random.randint (0,self.numcells-1)
		    newCellState = newCells[self.wrapCell(cellToFill)]
		    if newCellState < self.maxPacketsForCell (cellToFill):
			    newCells[cellToFill] +=1
			    curPackets +=1
        self.cells = newCells
    def getState(self, cell):
    	return self.cells[self.wrapCell(cell)]
    def shapeToDraw(self, cell):
        return {'N' : 'circle', 'L' : 'square' } [self.ruleStr[cell]]
    def randomRule(self):
		self.ruleStr = []
		for i in range (self.numcells):
			self.ruleStr.append ({0 : 'N', 1 : 'L'}[random.randint(0,1)])
    def setRule(self,rule):
        if isinstance(rule, int):
            # Int -> rule string (array of '1' and '0' characters)
            self.rulesTable = [str(int((rule&1<<(7-i))>0)) for i in range(8)]
        elif isinstance(rule, str):
            if len(rule) != len(self.rulesTable):
                # Pyconsole echos return values :)
                return "ERROR: requires %d character string." % len(self.rulesTable)
            self.rulesTable = list(rule)
