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
        return math.sqrt(self.sum_sq(self))
    
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
        
        vec_rot = self * quat([0, *vec]) * self.conj()

        return [
            vec_rot.x,
            vec_rot.y,
            vec_rot.z
        ]
    
    def from_axis(theta: float, u: list[float]) :
        '''
        Constructs a unit quaternion from the axis angle representation.

        q = cos(theta/2) + u sin(theta/2)

        Args
        ---
        theta : float
            The angle of the rotation in radians between 0 and pi
        u : list[float]
            Unit vector representing the angle the rotation is about
        '''
        theta = theta / 2
        coef = math.sin(theta) / math.sqrt(u[0] ** 2 + u[1] ** 2 + u[2] ** 2)
        return quat([math.cos(theta), u[0] * coef, u[1] * coef, u[2] * coef])

    def as_axis(self) :
        '''
        Returns the axis angle representation of a unit quaternion.

        q = cos(theta/2) + u sin(theta/2)

        Returns
        ---
        theta : float
            The angle of the rotation in radians between 0 and pi
        u : list[float]
            Unit vector representing the angle the rotation is about
        '''
        if not self.is_unit() :
            raise ArithmeticError('Only unit quaternions are valid representations of rotations')
        
        if abs(self.w - 1) <= 1e-9 :
            return 0, [0, 0, 0]
        
        theta = math.acos(self.w)
        coef = math.sin(theta)
        return 2 * theta, [self.x / coef, self.y / coef, self.z / coef]

        
    def is_pure(self) :
        '''Check if this is a pure quaternion.'''
        return True if self.w == 0 else False
    
    def is_unit(self) :
        '''Check if this is a unit quaternion.'''
        return True if abs(self.norm() - 1) <= 1e-9 else False
    
    def is_orth(self, p: Self) :
        '''Check if this quaternion is orthogonal to the quaternion p.'''
        return True if self.sum_sq(p) <= 1e-9 else False
    
    def sum_sq(self, p: Self) :
        '''Returns the sum of the squares of the elements of two quaternions.'''
        return self.w * p.w + self.x * p.x + self.y * p.y + self.z * p.z

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
            self.w * p.x + self.x * p.w + self.y * p.z - self.z * p.y,
            self.w * p.y - self.x * p.z + self.y * p.w + self.z * p.x,
            self.w * p.z + self.x * p.y - self.y * p.x + self.z * p.w,
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
    
    def __eq__(self, p):
        if type(p) == quat :
            return (self.w, self.x, self.y, self.z) == (p.w, p.x, p.y, p.z)
        else :
            return NotImplemented

    def __str__(self):
        return f'w: {self.w}, x: {self.x}, y: {self.y}, z: {self.z}'