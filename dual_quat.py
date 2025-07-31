from quat import quat
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

    def __str__(self) :
        return f'r: ({self.r}); e: ({self.d})'

    

q0 = quat([0, 105, 5, 5])
q1 = quat([0.5, -0.5, 0.5, 0.5])
dq = dual_quat.from_trans(q0, q1)

print(dq)

# print(q0.normalized().norm())

# vec = [1, 2, 3]
# vec_rot = q1.rot_apply(vec)

# print(math.sqrt(vec[0] ** 2 + vec[1] ** 2 + vec[2] ** 2))
# print(math.sqrt(vec_rot[0] ** 2 + vec_rot[1] ** 2 + vec_rot[2] ** 2))

# print(vec, vec_rot)