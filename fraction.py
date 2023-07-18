class Fraction:
    def __init__(self, numerator, denominator):
        self.numerator = numerator
        self.denominator = denominator
    
    def reduce(self):
        gcd = self.GCD(self.numerator, self.denominator)
        self.numerator //= gcd
        self.denominator //= gcd
    
    def GCD(self, m, n):
        while n != 0:
            t = n
            n = m % n
            m = t
        return m
