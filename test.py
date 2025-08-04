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

transforms = []

cleaning = [
    dq.from_trans([0,0,0],q()),
    dq.from_trans([0,0,-1],q()),
    dq.from_trans([0,-0.5,-1],q()),
    dq.from_trans([0,-0.5,0],q()),
    dq.from_trans([0,-1,0],q()),
    dq.from_trans([0,-1,-1],q()),
    dq.from_trans([0,-1.5,-1],q()),
    dq.from_trans([0,-1.5,0],q())
    ]

nets = [
    dq.from_trans([-3,-2.5,-0.5],q([-1, 0, 0, 1.25]).normalized()),
    dq.from_trans([-4.55,-2.05,-0.5],q([-1, 0, 0, 0.75]).normalized()),
    dq.from_trans([3,2.5,-0.5],q([1, 0, 0, 0.75]).normalized()),
    dq.from_trans([4.55,2.05,-0.5],q([1, 0, 0, 1.25]).normalized()),

    dq.from_trans([-3,-2.5,-0.5],q([-1, 0, 0, 1.25]).normalized()),
    dq.from_trans([-4.55,-2.05,-0.5],q([-1, 0, 0, 0.75]).normalized()),
    dq.from_trans([3,2.5,-0.5],q([1, 0, 0, 0.75]).normalized()),
    dq.from_trans([4.55,2.05,-0.5],q([1, 0, 0, 1.25]).normalized()),
]

for idx_n, ne in enumerate(nets) :
    for idx_c, cl in enumerate(cleaning) :
        if idx_c > 0:
            temp = transforms[-1].sclerp_n(ne * cl, 5)
            for i in range(5) :
                transforms.append(temp[i])
            
        if idx_c == 0 and idx_n > 0 :
            temp = transforms[-1].sclerp_n(transforms[-1] * dq.from_trans([-1, 0, 0], q([1, 0, 0, 0.01]).normalized()), 5)
            for i in range(5) :
                transforms.append(temp[i])
            
            if idx_n % 2 == 0 :
                temp = transforms[-1].sclerp_n(dq.from_trans([0, 0, -0.5], q()), 20)
                for i in range(20) :
                    transforms.append(temp[i])
                
                temp = transforms[-1].sclerp_n((ne * cl) * dq.from_trans([-0.5, 0, 0], q([1, 0, 0, 0.01]).normalized()), 20)
                for i in range(20) :
                    transforms.append(temp[i])

            if idx_n % 2 != 0 :
                temp = transforms[-1].sclerp_n((ne * cl) * dq.from_trans([-1, 0, 0], q([1, 0, 0, 0.01]).normalized()), 5)
                for i in range(5) :
                    transforms.append(temp[i])

            temp = transforms[-1].sclerp_n(ne * cl, 5)
            for i in range(5) :
                transforms.append(temp[i])

        transforms.append(ne * cl)

points = []

for idx, trans in enumerate(tqdm(transforms)) :
    components = trans.as_trans()

    points.append(components[0])

########################################################################################################

points = np.array(points)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

scatter = ax.scatter(points[:,0], points[:,1], points[:,2], c=range(np.shape(points)[0]), cmap='viridis')
fig.colorbar(scatter)

ax.plot(points[:,0], points[:,1], points[:,2])

# quat_plot.plot_quats(ax, rots, 'facing')
quat_plot.plot_dual_quats(ax, transforms, 'facing')

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

axis_limits = 7
ax.set_xlim(-axis_limits, axis_limits)
ax.set_ylim(-axis_limits, axis_limits)
ax.set_zlim(-axis_limits, axis_limits)

plt.show()

########################################################################################################

# dq0 = dq.from_trans([1, 2, 3], q([1, 1, 1, 1]).normalized())
# dq1 = dq.from_trans([3, 2, 3], q([1, 0, 1, 1]).normalized())

# print(dq0.sclerp(dq1, 0.5))
# print(dq0)