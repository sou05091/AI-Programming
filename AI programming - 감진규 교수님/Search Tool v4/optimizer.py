from setup import Setup

class HillClibming:
    def __init__(self):
        Setup.__init__(self)
        self._pType = 0
        self._limitStock = 0
        self._numExp = 0
        self._numRestart = 0
        
    def run(self):
        pass
    
    def displaySetting(self):
        if self._pType == 1:
            print()
            print("Mutant step size is:",self._delta)
            
    def displayNumExp(self):
        print()
        print("Number of experiments: ", self._numExp)
    
    def setVariables(self, parameters):
        Setup.setVariables(self, parameters)
        self._pType = parameters['pType']
        self._limitStock = parameters['limitStuck']
        self._numExp = parameters['numExp']
        self._numRestart = parameters['numRestart']
    
    def getNumExp(self):
        return self._numExp
    
    def randomRestart(self, p):
        self.run(p)
        bestSolution = p.getSolution()
        bestMinimum = p.getValue()
        numEval = p.getNumEval()
        for i in range(1, self._numRestart):
            self.run(p)
            newSolution = p.getSolution()
            newMinimum = p.getValue()
            numEval += p.getNumEval()
            if newMinimum < bestMinimum:
                bestMinimum = newMinimum
                bestSolution = newSolution
        p.storeResult(bestSolution, bestMinimum)
                             
class SteepestAscent(HillClibming):
    def run(self, p):
        current = p.randomInit() # 'current' is a list of values
        valueC = p.evaluate(current)
        while True:
            neighbors = p.mutants(current)
            successor, valueS = self.bestOf(neighbors, p)
            if valueS >= valueC:
                break
            else:
                current = successor
                valueC = valueS
        #return current, valueC
        p.storeResult(current, valueC)

    def bestOf(self, neighbors, p):
        best = neighbors[0]  # 'best' is a value list
        bestValue = p.evaluate(best)
        for i in range(1, len(neighbors)):
            newValue = p.evaluate(neighbors[i])
            if newValue < bestValue:
                best = neighbors[i]
                bestValue = newValue
        return best, bestValue
        
    def displaySetting(self):
        print()
        print("Search algorithm: Steepest-Ascent Hill Climbing")
        HillClibming.displaySetting(self)
        
class FirstChoice(HillClibming):
    def run(self,p):
        current = p.randomInit()   # 'current' is a list of values
        valueC = p.evaluate(current)
        i = 0
        while i < self._limitStock:
            successor = p.randomMutant(current)
            valueS = p.evaluate(successor)
            if valueS < valueC:
                current = successor
                valueC = valueS
                i = 0              # Reset stuck counter
            else:
                i += 1
        #return current, valueC
        p.storeResult(current, valueC)

    
    def displaySetting(self):
        print()
        print("Search algorithm: First-Choice Hill Climbing")
        HillClibming.displaySetting(self)
        print("Max evaluations".format(self._limitStock))
    
class GradientDescent(HillClibming):
    def run(self, p):
        current = p.randomInit() # 'current' is a list of random values
        valueC = p.evaluate(current)
        while True:
            successor = p.takeStep(current, valueC)
            valueS = p.evaluate(successor)
            if valueS >= valueC:
                break
            else:
                current = successor
                valueC = valueS
        #return current, valueC
        p.storeResult(current, valueC)

    
    def displaySetting(self):
        print()
        print("Search algorithm: Gradient-descent Hill Climbing")
        HillClibming.displaySetting(self)
        print("Update Rate",self._alpha)
        print("Increment for caluculating derivation",self._dx)
        

    