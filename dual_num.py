from typing import Self
import math

class dual_num() :
    def __init__(self, real, dual) :
        self.r = real
        self.d = dual

    def sqrt(self) :
        '''Returns the posative dual number square root if it exists.'''
        if self.r == 0 and self.d == 0 :
            return dual_num(0, 0)
        
        elif self.r > 0 :
            return dual_num(math.sqrt(self.r), self.d / (2 * math.sqrt(self.r)))
        
        else :
            raise ArithmeticError(f'Dual number square root does not exist for {self}')
        
    def __truediv__(self, p) :
        '''Scalar or dual number division.'''
        if type(p) == dual_num :
            return dual_num((self.r * p.r) / p.r ** 2, (p.r * self.d - p.d * self.r) / p.r ** 2)
        
        else :
            return dual_num(self.r / p, self.d / p)

    def __str__(self) :
        return f'r: {self.r}, d: {self.d}'