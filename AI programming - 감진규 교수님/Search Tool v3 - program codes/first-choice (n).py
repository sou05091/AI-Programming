#from numeric import *
from problem import Numeric

def main():
    # Create an instance of numerical optimization problem
    p = Numeric()   # 'p': (expr, domain)
    p.setVariables()
    # Call the search algorithm
    solution, minimum = firstChoice(p)
    # Show the problem and algorithm settings
    p.storeResult(solution, minimum)
    #describeProblem(p)
    p.describe()
    displaySetting(p)
    # Report results
    #displayResult(solution, minimum)
    p.report()

def firstChoice(p):
    LIMIT_STUCK = 100
    current = p.randomInit()   # 'current' is a list of values
    valueC = p.evaluate(current)
    i = 0
    while i < LIMIT_STUCK:
        successor = p.randomMutant(current)
        valueS = p.evaluate(successor)
        if valueS < valueC:
            current = successor
            valueC = valueS
            i = 0              # Reset stuck counter
        else:
            i += 1
    return current, valueC

def displaySetting(p):
    print()
    print("Search algorithm: First-Choice Hill Climbing")
    print()
    print("Mutation step size:", p.getDelta())
    
# def randomMutant(current, p): ###
#     i = random.randint(0, len(current) - 1)
#     if random.uniform(0,1)>0.5:
#         d = p.getDelta
#     else:
#         d = -p.getDelta
#     return p.mutate(current, i, d) # Return a random successor

main()
