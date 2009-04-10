import random
from BaseCA import BaseCA

class Wolfram(BaseCA):
    def __init__(self, numcells):
        super(Wolfram, self).__init__(numcells)
        #The famed rule 30
        self.setRule(30)
    def wrapCell(self, col):
        return col % self.numcells
    def step(self):
    	#For now, just update one cell per step
        tmp = []
        for col in self.updateOrder():
            ruleToUseIdx = (not self.cellAt(col-1))*4 + \
                            (not self.cellAt(col))*2 + (not self.cellAt(col+1))
            ruleToUse = self.rulesTable[ruleToUseIdx]
            if ruleToUse == '1':
                tmp.append(1)
            elif ruleToUse == '0':
                tmp.append(0)
        self.cells = tmp
    def setRule(self,rule):
        if isinstance(rule, int):
            # Int -> rule string (array of '1' and '0' characters)
            self.rulesTable = [str(int((rule&1<<(7-i))>0)) for i in range(8)]
        elif isinstance(rule, str):
            if len(rule) != len(self.rulesTable):
                # Pyconsole echos return values :)
                return "ERROR: requires %d character string." % len(self.rulesTable)
            self.rulesTable = list(rule)
