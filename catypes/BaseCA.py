import random

class BaseCA(object):
    def __init__(self, numcells):
        self.numcells = numcells
        self.cells = [0]*self.numcells
        self.validRules = ['0','1'] # Always put Null/Zero state first!
        self.rulesTable = ['0','0','0','0','0','0','0','0']
        self.highestState = 1
    def returnSpecificFunctions(self):
    	return {} #nothing specific about a general class!
    def toString(self):
        return ''.join(str(int(i)) for i in self.cells)
    def shapeToDraw(self, cell):
    	return 'square'
    def clear(self):
        self.cells = [0]*self.numcells
    def cellAt(self, col):
        if col >= self.numcells or col < 0:
            return 0
        return self.cells[col]
    def getState (self, col):
    	return isAlive(col)
    def setState (self, col, state):
    	self.cells[col] = state
    def setAlive(self, col):
        """Turn the specified cell(s) on"""
        if isinstance(col, list):
            for i in col:
                self._on(i)
        else:
            self._on(col)
    def setDead(self, col):
        """Turn the specified cell(s) on"""
        if isinstance(col, list):
            for i in col:
                self._off(i)
        else:
            self._off(col)
    def _on(self, c):
        self.cells[c] = 1
    def _off(self, c):
        self.cells[c] = 0
    def isAlive(self, col):
        return bool(self.cells[col])
    def drawCell(self,col):
    	return self.isAlive(col)
    def randomize(self):
        """Randomize the display"""
        for r in range(self.numcells):
            self.cells[r] = random.randint(0,1)
    def updateOrder(self):
        for i in range(self.numcells):
            yield i
    def getRuleForCell(self, col):
        """Returns the rule which corresponds to the cell at col"""
        ruleToUseIdx = (not self.cellAt(col-1))*4 + \
                       (not self.cellAt(col))*2 + \
                       (not self.cellAt(col+1))
        return self.rulesTable[ruleToUseIdx]
    def step(self):
        pass
    def setRule(self,rule):
        if len(rule) != len(self.rulesTable):
            # Pyconsole echos return values :)
            return "ERROR: requires %d character string." % len(self.rulesTable)
        self.rulesTable = list(rule)

class TorroidalCA(BaseCA):
    def wrapCell(self, col):
        # % numcells for torroidal display:
        return col % self.numcells
    def cellAt(self, col):
        return self.cells[self.wrapCell(col)]
    def getState(self, col):
        return self.cells[self.wrapCell(col)]
    def setState(self, col, state):
        self.cells[self.wrapCell(col)] = state
