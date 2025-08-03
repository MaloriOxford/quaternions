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
        real : array_like or quat, opt.
            Real component of the dual quaternion
        dual : array_like or quat, opt.
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
            qt = quat([0, translation[0], translation[1], translation[2]])
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
    
    def as_trans(self) :
        '''
        Returns the transformation and rotation defined by a unit dual quaternion.

        dq = A + eB

        Returns
        ---
        translation : list
            Translation vector 2 * B * A^-1
        rotation : quat
            Rotation quaternion A
        '''
        if self.is_unit() :
            vec = 2 * self.d * self.r.conj()
            return [vec.x, vec.y, vec.z], self.r
        else :
            raise BaseException('Only unit dual quaternions are valid representations of 3D transforms')

    def from_screw(u: list[float], m: list[float], theta: float, d: float) :
        '''
        Constructs a unit dual quaternion from the screw parameters of a transform.

        Args
        ---
        u : list[float]
            Unit vector representing the screw axis
        m : list[float]
            Moment vector
        theta : float
            Rotation angle
        d : float
            Displacement distance
        '''
        theta = theta / 2
        cos = math.cos(theta)
        sin = math.sin(theta)
        coef = d / 2

        return dual_quat([cos, u[0] * sin, u[1] * sin, u[2] * sin],
                         [-coef * sin,
                          coef * u[0] * cos + sin * m[0],
                          coef * u[1] * cos + sin * m[1],
                          coef * u[2] * cos + sin * m[2]])

    def as_screw(self) :
        '''
        Returns the screw parameters of a unit dual quaternion.

        Returns
        ---
        u : list[float]
            Unit vector representing the screw axis
        m : list[float]
            Moment vector
        theta : float
            Rotation angle
        d : float
            Displacement distance
        '''
        if not self.is_unit() :
            raise BaseException('Only unit dual quaternions are valid representations of 3D transforms')
        
        theta, u = self.r.as_axis()
        vec, _ = self.as_trans()
        
        d = vec[0]*u[0] + vec[1]*u[1] + vec[2]*u[2]
        
        if not theta == 0 and not theta == math.pi :
            cotan = 1 / math.tan(theta / 2)
        else :
            raise ZeroDivisionError
        
        m = [
            0.5 * (vec[1]*u[2] - vec[2]*u[1] + (vec[0] - d * u[0]) * cotan),
            0.5 * (vec[2]*u[0] - vec[0]*u[2] + (vec[1] - d * u[1]) * cotan),
            0.5 * (vec[0]*u[1] - vec[1]*u[0] + (vec[2] - d * u[2]) * cotan)
        ]
    
        return u, m, theta, d
        
    def sclerp(self, stop: Self, tau: float) :
        '''
        Perform Screw Linear Interpolation (SCLERP) from the current unit dual quaternion to another.

        Args
        ---
        stop : dual_quat
            The unit dual quaternion to perform interpolation to from this one
        tau : float
            A value between 0 and 1 representing how far along the interpolation to retrun a value for

        Returns
        ---
        dq : dual_quat
            A dual quaternion interpolated between self and to
        '''
        if not (self.is_unit() and stop.is_unit()) :
            raise BaseException('Only unit dual quaternions are valid representations of 3D transforms')
        elif not (tau >= 0 and tau <= 1) :
            raise BaseException(f'The value of tau {tau} must be in [0,1]')
        
        start = self
        if start.r.sum_sq(stop.r) < 0 :
            start = -1 * start
            
        return start * (start.inv() * stop) ** tau
    
    def sclerp_n(self, stop: Self, n: float) :
        '''
        Returns n equally spaced dual quaternions interpolated between self and stop.

        Returns
        ---
        dqs : list[dual_quat]
        '''
        if n > 0 :
            d_tau = 1 / (n + 1)
        else :
            raise ZeroDivisionError

        dqs = []
        for i in range(n) :
            dqs.append(self.sclerp(stop, (i + 1) * d_tau))

        return dqs
    
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
        '''Dual quaternion multiplication on the right.
        
        dq2 = self.r * p.r + e * (self.r * p.d + self.d * p.r)
        '''
        return dual_quat(self.r * p.r, (self.r * p.d) + (self.d * p.r))
    
    def __rmul__(self, p) :
        '''Scalar multiplication.'''
        return dual_quat(p * self.r, p * self.d)
    
    def __truediv__(self, p) :
        '''Scalar division.'''
        return dual_quat(self.r / p, self.d / p)
    
    def __pow__(self, p) :
        '''Unit dual quaternion raised to the power p.'''
        u, m, theta, d = self.as_screw()
        return dual_quat.from_screw(u, m, p * theta, p * d)

    def __str__(self) :
        return f'r: ({self.r}); d: ({self.d})'