from quat import quat as q
from dual_quat import dual_quat as dq
import matplotlib.pyplot as plt
import numpy as np

q0 = q([0, 105, 5, 5])
q1 = q([0.5, -0.5, 0.5, 0.5])
dq0 = dq.from_trans(q0, q1)
dq1 = dq(q([0.75, 0.25, 0, 0]), [5, 2, 3, 4])
dq2 = dq.from_trans([0, 1, 2, 3], q([1, 2, 3, 4]).normalized())
dq3 = dq0 * dq2

print(dq3.as_trans()[0])
# print(*dq3.as_trans())

# vec = [1, 2, 3]
# vec_rot = q1.rot_apply(vec)

# print(math.sqrt(vec[0] ** 2 + vec[1] ** 2 + vec[2] ** 2))
# print(math.sqrt(vec_rot[0] ** 2 + vec_rot[1] ** 2 + vec_rot[2] ** 2))

# print(vec, vec_rot)

points = np.array([dq0.as_trans()[0], dq2.as_trans()[0], dq3.as_trans()[0]])

ax = plt.figure().add_subplot(projection='3d')
ax.scatter(points[0], points[1], points[2])

plt.show()