import random
from BaseCA import TorroidalCA

class SpectorMachine(TorroidalCA):
    def __init__(self, numcells):
        super(SpectorMachine,self).__init__(numcells)
        #This rule only shifts living cells to the left and leaves the rest alone
        self.rulesTable = ['C','C','L','L','C','C','L','L']
    def updateOrder(self):
        """Updates cells in pseudorandom fixed-interval order,
           guarantees every cell gets updated for prime numcells"""
        stepnum = random.randint(0,self.numcells-1)
        for i in range(self.numcells):
            yield stepnum**i % self.numcells
    def step(self):
    	#For now, just update one cell per step
        iterator = self.updateOrder()
        for col in iterator:
            ruleToUse = self.getRuleForCell(col)
            if ruleToUse.upper() == 'L':
                self.swapCells (self.wrapCell(col-1),self.wrapCell(col))
            elif ruleToUse.upper() == 'R':
                self.swapCells (self.wrapCell(col),self.wrapCell(col+1))
                    #if ruletouse == 'c', do absolutely nothing!
    def swapCells(self,cellA, cellB):
    	oldA = self.isAlive(cellA)
    	self.setState(cellA, self.isAlive(cellB))
    	self.setState(cellB, oldA)
