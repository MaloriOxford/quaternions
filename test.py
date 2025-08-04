from quat import quat as q
from dual_quat import dual_quat as dq
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d.proj3d import proj_transform
from mpl_toolkits.mplot3d.axes3d import Axes3D
import numpy as np
from tqdm import tqdm

class Arrow3D(FancyArrowPatch):

    def __init__(self, x, y, z, dx, dy, dz, *args, **kwargs):
        super().__init__((0, 0), (0, 0), *args, **kwargs)
        self._xyz = (x, y, z)
        self._dxdydz = (dx, dy, dz)

    def draw(self, renderer):
        x1, y1, z1 = self._xyz
        dx, dy, dz = self._dxdydz
        x2, y2, z2 = (x1 + dx, y1 + dy, z1 + dz)

        xs, ys, zs = proj_transform((x1, x2), (y1, y2), (z1, z2), self.axes.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        super().draw(renderer)
        
    def do_3d_projection(self, renderer=None):
        x1, y1, z1 = self._xyz
        dx, dy, dz = self._dxdydz
        x2, y2, z2 = (x1 + dx, y1 + dy, z1 + dz)

        xs, ys, zs = proj_transform((x1, x2), (y1, y2), (z1, z2), self.axes.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))

        return np.min(zs) 

def _arrow3D(ax, x, y, z, dx, dy, dz, *args, **kwargs):
    '''Add an 3d arrow to an `Axes3D` instance.'''

    arrow = Arrow3D(x, y, z, dx, dy, dz, *args, **kwargs)
    ax.add_artist(arrow)


setattr(Axes3D, 'arrow3D', _arrow3D)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')


########################################################################################################

q0 = q([1, 0, 0, 0]).normalized()
q1 = q([0, 0, 0, -1]).normalized()

rots = [q0, *q0.slerp_n(q1, 10), q1]
points = []

for idx, rot in enumerate(tqdm(rots)) :
    points.append([0, 0, 0])
    
    
    arrow_len = 0.25
    arrows = 'facing'

    if arrows == 'facing' :
        dir_x = rot.rot_apply([arrow_len, 0, 0])
        ax.arrow3D(*[0, 0, 0],
                *dir_x,
                mutation_scale = 10,
                arrowstyle = "-|>",
                linestyle = 'solid')

    elif arrows == 'basis' :
        dir_x = rot.rot_apply([arrow_len, 0, 0])
        ax.arrow3D(*[0, 0, 0],
                *dir_x,
                mutation_scale = 10,
                arrowstyle = "-|>",
                linestyle = 'solid',
                color = 'red')
        
        dir_y = rot.rot_apply([0, arrow_len, 0])
        ax.arrow3D(*[0, 0, 0],
                *dir_y,
                mutation_scale = 10,
                arrowstyle = "-|>",
                linestyle = 'solid',
                color = 'green')
        
        dir_z = rot.rot_apply([0, 0, arrow_len])
        ax.arrow3D(*[0, 0, 0],
                *dir_z,
                mutation_scale=10,
                arrowstyle = "-|>",
                linestyle = 'solid',
                color = 'blue')

########################################################################################################

# n = 100000

# rand_quats = np.random.normal([0, 0, 0, 0], [1, 1, 1, 1], (n, 4))

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

# for idx_n, ne in enumerate(nets) :
#     for idx_c, cl in enumerate(cleaning) :
#         if idx_c > 0:
#             temp = transforms[-1].sclerp_n(ne * cl, 5)
#             for i in range(5) :
#                 transforms.append(temp[i])
            
#         if idx_c == 0 and idx_n > 0 :
#             temp = transforms[-1].sclerp_n(transforms[-1] * dq.from_trans([-1, 0, 0], q([1, 0, 0, 0.01]).normalized()), 5)
#             for i in range(5) :
#                 transforms.append(temp[i])
            
#             if idx_n % 2 == 0 :
#                 temp = transforms[-1].sclerp_n(dq.from_trans([0, 0, -0.5], q()), 20)
#                 for i in range(20) :
#                     transforms.append(temp[i])
                
#                 temp = transforms[-1].sclerp_n((ne * cl) * dq.from_trans([-0.5, 0, 0], q([1, 0, 0, 0.01]).normalized()), 20)
#                 for i in range(20) :
#                     transforms.append(temp[i])

#             if idx_n % 2 != 0 :
#                 temp = transforms[-1].sclerp_n((ne * cl) * dq.from_trans([-1, 0, 0], q([1, 0, 0, 0.01]).normalized()), 5)
#                 for i in range(5) :
#                     transforms.append(temp[i])

#             temp = transforms[-1].sclerp_n(ne * cl, 5)
#             for i in range(5) :
#                 transforms.append(temp[i])

#         transforms.append(ne * cl)



# for i in tqdm(range(n)) :
#     transforms.append(dq.from_trans(np.random.normal([0, 0, 0], [1, 1, 1]), q(rand_quats[i]).normalized()))

# def path(idx) :
#     a = idx / 50
    
#     x = a ** 3
#     y = a ** 3
#     z = a ** 3

#     return [x, y, z]

# points = []

# for idx, trans in enumerate(tqdm(transforms)) :
#     # if idx == 0 :
#     #     components = (trans).as_trans()
#     # else :
#     #     components = (transforms[idx - 1] * trans).as_trans()

#     components = trans.as_trans()

#     points.append(components[0])
    
    
#     arrow_len = 0.25
#     arrows = 'facing'

#     if arrows == 'facing' :
#         dir_x = components[1].rot_apply([arrow_len, 0, 0])
#         ax.arrow3D(*components[0],
#                 *dir_x,
#                 mutation_scale = 10,
#                 arrowstyle = "-|>",
#                 linestyle = 'solid')

#     elif arrows == 'basis' :
#         dir_x = components[1].rot_apply([arrow_len, 0, 0])
#         ax.arrow3D(*components[0],
#                 *dir_x,
#                 mutation_scale = 10,
#                 arrowstyle = "-|>",
#                 linestyle = 'solid',
#                 color = 'red')
        
#         dir_y = components[1].rot_apply([0, arrow_len, 0])
#         ax.arrow3D(*components[0],
#                 *dir_y,
#                 mutation_scale = 10,
#                 arrowstyle = "-|>",
#                 linestyle = 'solid',
#                 color = 'green')
        
#         dir_z = components[1].rot_apply([0, 0, arrow_len])
#         ax.arrow3D(*components[0],
#                 *dir_z,
#                 mutation_scale=10,
#                 arrowstyle = "-|>",
#                 linestyle = 'solid',
#                 color = 'blue')

points = np.array(points)

scatter = ax.scatter(points[:,0], points[:,1], points[:,2], c=range(np.shape(points)[0]), cmap='viridis')
fig.colorbar(scatter)

ax.plot(points[:,0], points[:,1], points[:,2])

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

axis_limits = 0.5
ax.set_xlim(-axis_limits, axis_limits)
ax.set_ylim(-axis_limits, axis_limits)
ax.set_zlim(-axis_limits, axis_limits)

plt.show()

########################################################################################################

# dq0 = dq.from_trans([1, 2, 3], q([1, 1, 1, 1]).normalized())
# dq1 = dq.from_trans([3, 2, 3], q([1, 0, 1, 1]).normalized())

# print(dq0.sclerp(dq1, 0.5))
# print(dq0)