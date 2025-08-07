from quat import quat as q
from dual_quat import dual_quat as dq
import quat_plot

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d.proj3d import proj_transform
from mpl_toolkits.mplot3d.axes3d import Axes3D
import numpy as np
from tqdm import tqdm

########################################################################################################

# q0 = q([1, 0, 0, 0]).normalized()
# q1 = q([0, 0, 0, -1]).normalized()

# rots = [q0, *q0.slerp_n(q1, 10), q1]
# points = [[0,0,0]]

########################################################################################################

# transforms = []

# cleaning = [
#     dq.from_trans([0,0,0],q()),
#     dq.from_trans([0,0,-1],q()),
#     dq.from_trans([0,-0.5,-1],q()),
#     dq.from_trans([0,-0.5,0],q()),
#     dq.from_trans([0,-1,0],q()),
#     dq.from_trans([0,-1,-1],q()),
#     dq.from_trans([0,-1.5,-1],q()),
#     dq.from_trans([0,-1.5,0],q())
#     ]

# nets = [
#     dq.from_trans([-3,-2.5,-0.5],q([-1, 0, 0, 1.25]).normalized()),
#     dq.from_trans([-4.55,-2.05,-0.5],q([-1, 0, 0, 0.75]).normalized()),
#     dq.from_trans([3,2.5,-0.5],q([1, 0, 0, 0.75]).normalized()),
#     dq.from_trans([4.55,2.05,-0.5],q([1, 0, 0, 1.25]).normalized()),

#     dq.from_trans([-3,-2.5,-0.5],q([-1, 0, 0, 1.25]).normalized()),
#     dq.from_trans([-4.55,-2.05,-0.5],q([-1, 0, 0, 0.75]).normalized()),
#     dq.from_trans([3,2.5,-0.5],q([1, 0, 0, 0.75]).normalized()),
#     dq.from_trans([4.55,2.05,-0.5],q([1, 0, 0, 1.25]).normalized()),
# ]

# home = dq.from_trans([0, 0, 0], q())

# transforms.append(home)

# for idx_n, ne in enumerate(nets) :
#     for idx_c, cl in enumerate(cleaning) :
#         next_point = ne * cl

#         if idx_c > 0 :
#             transforms.extend(transforms[-1].lerp_n(next_point, 5))
#             transforms.append(next_point)

#         elif idx_c == 0 :
#             transforms.extend(transforms[-1].lerp_n(next_point * dq.from_trans([-1, 0, 0], q()), 5))
#             transforms.extend(transforms[-1].lerp_n(next_point, 5))

#             transforms.append(next_point)
        
#         if idx_c == len(cleaning) - 1 :
#             transforms.extend(next_point.lerp_n(next_point * dq.from_trans([-1, 0, 0], q()), 5))


# transforms.extend(transforms[-1].lerp_n(home, 10))
# transforms.append(home)

# points = []

# for idx, trans in enumerate(tqdm(transforms)) :
#     components = trans.as_trans()

#     points.append(components[0])

########################################################################################################

# points = np.array(points)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# scatter = ax.scatter(points[:,0], points[:,1], points[:,2], c=range(np.shape(points)[0]), cmap='viridis')
# fig.colorbar(scatter)

# ax.plot(points[:,0], points[:,1], points[:,2])

# # quat_plot.plot_quats(ax, rots, 'facing')
# quat_plot.plot_dual_quats(ax, transforms, 'facing')

# ax.set_xlabel('x')
# ax.set_ylabel('y')
# ax.set_zlabel('z')

# axis_limits = 7
# ax.set_xlim(-axis_limits, axis_limits)
# ax.set_ylim(-axis_limits, axis_limits)
# ax.set_zlim(-axis_limits, axis_limits)

# plt.show()

########################################################################################################

dqs = []
n = 5
lim = 10
coef = (lim / 2) / n

for r in tqdm(range(n)) :
    for i in range (n) :
        for j in range(n) :
            for k in range(n) :
                dqs.append(dq(q(np.random.normal([1, 0, 0, 0])).normalized(), [r * coef, i * coef, j * coef, k * coef]))
                dn = dqs[-1].norm()
                dqs[-1] = dq((dqs[-1].r / dn.r), (dn.r * dqs[-1].d + -dn.d * dqs[-1].r) / (dn.r ** 2))

# dq0 = dq(q([1, 1, 1, 1]).normalized(),q([10, 2, 3, 4]))

# dn = dq0.norm()

# Normalize dq0
# dq0 = dq((dq0.r / dn.r), (dn.r * dq0.d + -dn.d * dq0.r) / (dn.r ** 2))

quat_plot.plot_dual_quats(ax, dqs, 'basis')

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

# axis_limits = 4
# ax.set_xlim(-axis_limits, axis_limits)
# ax.set_ylim(-axis_limits, axis_limits)
# ax.set_zlim(-axis_limits, axis_limits)

plt.show()

# print(dq0, '\n', 2 * dq0.d * dq0.r.conj(), '\n', dq0.is_unit())