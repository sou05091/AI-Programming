from problem import Numeric

def main():
    # Create an instance of numerical optimization problem
    p = Numeric()
    p.setVariables()   # 'p': (expr, domain)
    # Call the search algorithm
    solution, minimum = gradientDescent(p)
    # Show the problem and algorithm settings
    p.storeResult(solution, minimum)
    p.describe()
    displaySetting(p)
    # Report results
    p.report()

def gradientDescent(p):
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
    return current, valueC

def displaySetting(p):
    print()
    print("Search algorithm: Gradient-descent Hill Climbing")
    print()
    print("step size:", p.getAlpha())

main()
