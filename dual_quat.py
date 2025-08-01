from quat import quat
from dual_num import dual_num
from typing import Self
import math

class dual_quat() :
    def __init__(self, real = quat([1, 0, 0, 0]), dual = quat([1, 0, 0, 0])) :
        '''
        Constructs a generic dual quaternion.

        Args
        ---
        real : array_like or quat
            Real component of the dual quaternion
        dual : array_like or quat
            Real component of the dual quaternion
        '''
        if type(real) == quat :
            self.r = real
        else :
            self.r = quat(real)

        if type(dual) == quat :
            self.d = dual
        else :
            self.d = quat(dual)
        
    def from_trans(translation, rotation) :
        '''
        Constructs a dual quaternion representing transformation of a translation followed by a rotation.

        dual_quat = rotation + epsilon * (1/2 translation * rotation)
        
        Args
        ---
        translation : quat or array_like
            Translation provided either as a pure quaternion or an R^3 translation vector
        rotation : quat or array_like
            Rotation provided as a unit quaternion
        '''
        if type(translation) == quat :
            qt = translation
        elif len(translation) == 3 :
            qt = quat([0, *translation])
        elif len(translation) == 4 :
            qt = quat(translation)

        if not qt.is_pure() :
            raise BaseException(f'Translation {qt} must be a pure quaternion')

        if type(rotation) == quat :
            if rotation.is_unit() :
                qr = rotation
            else :
                raise BaseException(f'Rotation {rotation} must be a unit quaternion')
        else :
            qr = quat(rotation)

        return dual_quat(qr, 0.5 * qt * qr)
    
    def q_conj(self) :
        '''
        Returns the quaternion conjugate of the dual quaternion.
        
        dq = A + eB -> dq* = A* + eB*'''
        return dual_quat(self.r.conj(), self.d.conj())
    
    def d_conj(self) :
        '''
        Returns the dual number conjugate of the dual quaternion.

        dq = A + eB -> bar{dq} = A - eB
        '''
        return dual_quat(self.r, -1 * self.d)
    
    def t_conj(self) :
        '''
        Returns the total conjugate of the dual quaternion.

        dq = A + eB -> bar{dq*} = A* - eB*
        '''
        return self.q_conj().d_conj()
    
    def inv(self) :
        '''Returns the dual quaternion inverse.'''
        r_conj = self.r.conj()
        return dual_quat(r_conj, -1 * r_conj * self.d * r_conj)
    
    def norm(self) :
        '''Returns the 2 norm of the dual quaternion.'''
        norm = self * self.q_conj()

        return dual_num(norm.r.w, norm.d.w).sqrt()
    
    def is_unit(self) :
        return True if self.r.is_unit() and self.r.is_orth(self.d) else False

    def __add__(self, p: Self) :
        '''Dual quaternion addition.'''
        return dual_quat(self.r + p.r, self.d + p.d)
    
    def __mul__(self, p: Self) :
        '''Dual quaternion multiplication.'''
        return dual_quat(self.r * p.r, self.r * p.d + self.d * p.r)
    
    def __rmul__(self, p) :
        '''Scalar multiplication.'''
        return dual_quat(p * self.r, p * self.d)
    
    def __truediv__(self, p) :
        '''Scalar division.'''
        return dual_quat(self.r / p, self.d / p)

    def __str__(self) :
        return f'r: ({self.r}); d: ({self.d})'

    

q0 = quat([0, 105, 5, 5])
q1 = quat([0.5, -0.5, 0.5, 0.5])
dq0 = dual_quat.from_trans(q0, q1)
dq1 = dual_quat(quat([0.75, 0.25, 0, 0]), [5, 2, 3, 4])

print(dq1.norm())

# vec = [1, 2, 3]
# vec_rot = q1.rot_apply(vec)

# print(math.sqrt(vec[0] ** 2 + vec[1] ** 2 + vec[2] ** 2))
# print(math.sqrt(vec_rot[0] ** 2 + vec_rot[1] ** 2 + vec_rot[2] ** 2))

# print(vec, vec_rot)