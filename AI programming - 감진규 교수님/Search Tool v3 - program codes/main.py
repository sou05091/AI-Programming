from problem import *
from optimizer import *

def main():
    p, pType = selectProblem() # pType: 1(numeric) or 2(Tsp)
    alg = selectAlgorithm(pType)
    alg.run(p)
    p.describe()
    alg.displaySetting()
    p.report()
    
def selectProblem():
    print("Select the problem type:")
    print(" 1. Numeric")
    print(" 2. TSP")
    pType = int(input("Enter the number: "))
    if pType == 1:
        p = Numeric()
    elif pType == 2:
        p = Tsp()
    else:
        print("wrong number!")
    p.setVariables()
    return p, pType

def selectAlgorithm(pType):
    print("Select the algorithym type:")
    print(" 1. Steepest ascent")
    print(" 2. First-Choice")
    print(" 3. Gradient Descent")
    algType = int(input("Enter the number: "))
    optimizers = {1: 'SteepestAscent()', 2:'FirstChoice()', 3:'GradientDescent()'} 
    alg = eval(optimizers[algType])
    alg.setVariables(pType)
    return alg
    
main()