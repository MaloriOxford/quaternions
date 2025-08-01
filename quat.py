import math
from typing import Self

class quat() :
    def __init__(self, q = [1, 0, 0, 0]) :
        '''
        Construct a quaternion.

        Args
        ---
        q : array_like, opt.
            Scalar first quaternion q(w, x, y, z)
        '''
        self.w = float(q[0])
        self.x = float(q[1])
        self.y = float(q[2])
        self.z = float(q[3])
    
    def norm(self) :
        '''
        Returns the 2 norm of the quaternion.
        '''
        return math.sqrt(self.w ** 2 + self.x ** 2 + self.y ** 2 + self.z ** 2)
    
    def normalized(self) :
        '''
        Returns the normalized quaternion.
        '''
        norm = self.norm()

        return quat([
            self.w / norm,
            self.x / norm,
            self.y / norm,
            self.z / norm
        ])

    def conj(self) :
        '''
        Returns the conjugate of the quaternion.
        
        For unit quaternions, this is the inverse, and for unit quaternions representing rotations, it is the inverse rotation.
        '''
        return quat([
            self.w,
            -self.x,
            -self.y,
            -self.z
        ])
    
    def inv(self) :
        '''
        Returns the inverse of the quaternion.
        
        Note: this is equivelant to the conjugate only for unit quaternions.
        '''
        return self.conj() / self.norm()
    
    def rot_apply(self, vec) :
        '''
        Applies the quaternion as a rotation to the vector.
        
        Args
        ---
        vec : array_like
            A vector in R^3 to apply the rotation to

        Returns
        ---
        vec_rot : list
            Original vector rotated by the quaternion
        '''
        if not self.is_unit() :
            raise ArithmeticError('Only unit quaternions are valid representations of rotations')
        
        vec_rot = self.conj() * quat([0, *vec]) * self

        return [
            vec_rot.x,
            vec_rot.y,
            vec_rot.z
        ]
        
    def is_pure(self) :
        '''Check if this is a pure quaternion.'''
        return True if self.w == 0 else False
    
    def is_unit(self) :
        '''Check if this is a unit quaternion.'''
        return True if abs(self.norm() - 1) <= 1e-9 else False
    
    def is_orth(self, p: Self) :
        '''Check if this quaternion is orthogonal to the quaternion p.'''
        return True if (self.w * p.w + self.x * p.x + self.y * p.y + self.z * p.z) <= 1e-9 else False

    def __mul__(self, p: Self) :
        '''
        Quaternion multiplication.  Multiplies self * p.  Assumes scalar first notation q(w, x, y, z).

        Args
        ---
        self : quat
            Left side quaternion
        p : quat
            Right side quaternion

        Returns
        ---
        q2 : ndarray
            self.q * p
        '''

        return quat([
            self.w * p.w - self.x * p.x - self.y * p.y - self.z * p.z,
            self.w * p.x + self.x * p.w - self.y * p.z + self.z * p.y,
            self.w * p.y + self.x * p.z + self.y * p.w - self.z * p.x,
            self.w * p.z - self.x * p.y + self.y * p.x + self.z * p.w,
        ])
    
    def __rmul__(self, p) :
        '''Non-quaternion multiplication by a scalar.'''
        return quat([
            self.w * p,
            self.x * p,
            self.y * p,
            self.z * p
        ])
    
    def __add__(self, p: Self) :
        '''Quaternion addition.'''
        return quat([
            self.w + p.w,
            self.x + p.x,
            self.y + p.y,
            self.z + p.z
        ])
    
    def __truediv__(self, p) :
        '''Scalar division.'''
        return quat([
            self.w / p,
            self.x / p,
            self.y / p,
            self.z / p
        ])

    def __str__(self):
        return f'w: {self.w}, x: {self.x}, y: {self.y}, z: {self.z}'