import math
import random
from setup import Setup
# interface 제공
class Problem:
    def __init__(self):
        #_붙여주면 private과 비슷한 역할
        # 최상위 class에서 상속 받음
        Setup.__init__(self)
        self._solution = []
        self._value = 0
        self._numEval = 0
        
    def setVariables(self):
        pass
    def randomInit(self):
        pass    
    def evaluate(self):
        pass
    def mutants(self):
        pass
    def randomMutant(self):
        pass
    def describe(self):
        pass
    def storeResult(self, solution, value):
        self._solution = solution
        self._value = value
    def report(self):
        print()
        print("Total number of evaluations: {0:,}".format(self._numEval))
        
class Numeric(Problem):
    def __init__(self):
        Problem.__init__(self)
        self._expression = ''
        self._domain = []
#        self._delta = 0.01 (setup.py에서 넘겨 받음(최상위 class))     
#        self._alpha = 0.01
#        self._dx = 10 ** (-4)

    def getDelta(self):
        return self._delta   
    
    def getAlpha(self):
        return self._alpha   
               
    def getDx(self):
        return self._dx
    
    def takeStep(self, x, v):
        grad = self.gradient(x, v)
        xCopy = x[:]    
        for i in range(len(x)):
            xCopy[i] -= self._alpha*grad[i]
            
        if self.isLegal(xCopy):
            return xCopy
        else:
            return x
            
    def gradient(self, x, v):
        grad = []
        for i in range(len(x)):
            xCopy = x[:]
            xCopy[i] += self._dx
            df = self.evaluate(xCopy) - v
            g = df / self._dx
            grad.append(g)
        return grad
    
    def isLegal(self, x):
        domain = self._domain
        low, up = domain[1], domain[2]
        for i in range(len(low)):
            if low[i] <= x[i] <= up[i]:
                pass
            else:
                return False
        return True
        
    def setVariables(self):
         ## Read in an expression and its domain from a file.
        ## Then, return a problem 'p'.
        ## 'p' is a tuple of 'expression' and 'domain'.
        ## 'expression' is a string.
        ## 'domain' is a list of 'varNames', 'low', and 'up'.
        ## 'varNames' is a list of variable names.
        ## 'low' is a list of lower bounds of the varaibles.
        ## 'up' is a list of upper bounds of the varaibles.
        filename = input("Enter the file of a function:")
        infile = open(filename,"r")
        self._expression = infile.readline()
        varName = []
        low = []
        up = []
        line = infile.readline()
        while line != '':
            data = line.split(',')
            varName.append(data[0])
            low.append(float(data[1]))
            up.append(float(data[2]))
            line = infile.readline()
        infile.close
        self._domain = [varName,low,up]
        # 이미 다 완성 돼있기 때문에 return이 필요없음
        #return self._expression, self._domain
    
    def randomInit(self):
        # [expression,domain] -> p[1] = domain 선택
        domain = self._domain
        #domain[1] = low -30 // domain[2] = up 30 
        low = domain[1]
        up = domain[2]
        init = []
        for i in range(len(low)):
            r = random.uniform(low[i], up[i])
            init.append(r)
        # 5가지의 low와 up사이의 랜덤값 반환
        return init    # Return a random initial point
                    # as a list of values  
        
    def evaluate(self,current):
        ## Evaluate the expression of 'p' after assigning
        ## the values of 'current' to the variables
        #global NumEval
        self._numEval += 1
        expr = self._expression         # p[0] is function expression
        varNames = self._domain[0]  # p[1] is domain: [varNames, low, up]
        for i in range(len(varNames)):
            assignment = varNames[i] + '=' + str(current[i])
            exec(assignment)
        return eval(expr)
    
    def mutants(self,current):
        neighbors = []
        for i in range(len(current)):
            mutant =  self.mutate(current, i, self._delta)
            neighbors.append(mutant)
            mutant = self.mutate(current, i , -self._delta)
            neighbors.append(mutant)
        return neighbors     # Return a set of successors
    
    def mutate(self,current, i, d): ## Mutate i-th of 'current' if legal
        curCopy = current[:]
        domain = self._domain        # [VarNames, low, up]
        l = domain[1][i]     # Lower bound of i-th -30
        u = domain[2][i]     # Upper bound of i-th  30
        if l <= (curCopy[i] + d) <= u:
            curCopy[i] += d
        return curCopy
     
    def randomMutant(self,current):
        i = random.randint(0, len(current) - 1)
        if random.uniform(0,1)>0.5:
            d = self._delta
        else:
            d = -self._delta
        return self.mutate(current, i, d) # Return a random successor
    
    def describe(self):
        print()
        print("Objective function:")
        print(self._expression)   # Expression
        print("Search space:")
        varNames = self._domain[0] # p[1] is domain: [VarNames, low, up]
        low = self._domain[1]
        up = self._domain[2]
        for i in range(len(low)):
            print(" " + varNames[i] + ":", (low[i], up[i])) 

    def report(self):
        print()
        print("Solution found:")
        print(self.coordinate())  # Convert list to tuple
        print("Minimum value: {0:,.3f}".format(self._value))
        Problem.report(self)
    
    def coordinate(self):
        c = [round(value, 3) for value in self._solution]
        return tuple(c)  # Convert the list to a tuple
    
class Tsp(Problem):
    def __init__(self):
        Problem.__init__(self)
        self._numcities = 0
        self._locations = []
        self._distanceTable = []
        self._delta = 0.01
        ## Read in a TSP (# of cities, locatioins) from a file.
        ## Then, create a problem instance and return it.
        
    def getDelta(self):
        return self._delta  
        
    def setVariables(self):
        ## Read in a TSP (# of cities, locatioins) from a file.
        ## Then, create a problem instance and return it.
        fileName = input("Enter the file name of a TSP: ")
        infile = open(fileName, 'r')
        # First line is number of cities
        self._numcities = int(infile.readline())
        #self._locations = []
        line = infile.readline()  # The rest of the lines are locations
        while line != '':
            self._locations.append(eval(line)) # Make a tuple and append
            line = infile.readline()
        infile.close()
        self._distanceTable = self.calcDistanceTable()
        #return numCities, locations, table
    
    
    def calcDistanceTable(self): ###
        table = []
        for i in range(self._numcities):
            row = []
            for j in range(self._numcities):
                dx = self._locations[i][0] - self._locations[j][0]
                dy = self._locations[i][1] - self._locations[j][1]
                d =  round(math.sqrt(dx**2 + dy**2),1)
                row.append(d)
            table.append(row)
        return table # A symmetric matrix of pairwise distances
    
    def randomInit(self):
        n = self._numcities
        init = list(range(n))
        random.shuffle(init)
        return init
    
    def evaluate(self,current): ###
        ## Calculate the tour cost of 'current'
        ## 'current' is a list of city ids
        #global NumEval
        self._numEval += 1
        n= self._numcities
        table = self._distanceTable
        cost = 0
        for i in range(n-1):
            locFrom = current[i]
            locTo = current[i+1]
            cost += table[locFrom][locTo]  
        cost += table[current[n-1]][current[0]]       
        return cost
    
    def mutants(self,current):
        n = self._numcities
        neighbors = []
        count = 0
        triedPairs = []
        while count <= n:  # Pick two random loci for inversion
            i, j = sorted([random.randrange(n) for _ in range(2)])
            if i < j and [i, j] not in triedPairs:
                triedPairs.append([i, j])
                curCopy = self.inversion(current, i, j)
                count += 1
                neighbors.append(curCopy)
        return neighbors
    
    def inversion(self, current, i, j):  ## Perform inversion
        curCopy = current[:]
        while i < j:
            curCopy[i], curCopy[j] = curCopy[j], curCopy[i]
            i += 1
            j -= 1
        return curCopy
    
    def describe(self):
        print()
        n = self._numcities
        print("Number of cities:", n)
        print("City locations:")
        locations = self._locations
        for i in range(n):
            print("{0:>12}".format(str(locations[i])), end = '')
            if i % 5 == 4:
                print()
                
    def randomMutant(self, current): # Apply inversion
        while True:
            i, j = sorted([random.randrange(self._numcities) for _ in range(2)])
            if i < j:
                curCopy = self.inversion(current, i, j)
                break
        return curCopy
    
    def report(self):
        print()
        print("Best order of visits:")
        #self.tenPerRow(self._solution)       # Print 10 cities per row
        self.tenPerRow()
        print("Minimum tour cost: {0:,}".format(round(self._value)))
        Problem.report(self)
        
    def tenPerRow(self):
        for i in range(len(self._solution)):
            print("{0:>5}".format(self._solution[i]), end='')
            if i % 10 == 9:
                print()