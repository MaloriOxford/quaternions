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

# n = 100000

# rand_quats = np.random.normal([0, 0, 0, 0], [1, 1, 1, 1], (n, 4))
dq0 = dq.from_trans([1, 2, 3], q([1, 1, 1, 1]).normalized())
dq1 = dq.from_trans([3, 2, 3], q([1, 0, 1, 1]).normalized())
transforms = [dq0, dq0.sclerp(dq1, 0.25), dq0.sclerp(dq1, 0.5), dq0.sclerp(dq1, 0.75), dq1]

# for i in tqdm(range(n)) :
#     transforms.append(dq.from_trans(np.random.normal([0, 0, 0], [1, 1, 1]), q(rand_quats[i]).normalized()))

# def path(idx) :
#     a = idx / 50
    
#     x = a ** 3
#     y = a ** 3
#     z = a ** 3

#     return [x, y, z]

points = []

for idx, trans in enumerate(tqdm(transforms)) :
    if idx == 0 :
        components = (trans).as_trans()
    else :
        components = (transforms[idx - 1] * trans).as_trans()

    points.append(components[0])
    dir_x = components[1].rot_apply([0.5, 0, 0])
    dir_y = components[1].rot_apply([0, 0.5, 0])
    dir_z = components[1].rot_apply([0, 0, 0.5])

    ax.arrow3D(*components[0],
            *dir_x,
            mutation_scale = 10,
            arrowstyle = "-|>",
            linestyle = 'solid',
            color = 'red')
    
    ax.arrow3D(*components[0],
            *dir_y,
            mutation_scale = 10,
            arrowstyle = "-|>",
            linestyle = 'solid',
            color = 'green')
    
    ax.arrow3D(*components[0],
            *dir_z,
            mutation_scale=10,
            arrowstyle = "-|>",
            linestyle = 'solid',
            color = 'blue')

points = np.array(points)

scatter = ax.scatter(points[:,0], points[:,1], points[:,2], c=range(np.shape(points)[0]), cmap='viridis')
fig.colorbar(scatter)

ax.plot(points[:,0], points[:,1], points[:,2])

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

# ax.set_xlim(-3, 3)
# ax.set_ylim(-3, 3)
# ax.set_zlim(-3, 3)

plt.show()

########################################################################################################

# dq0 = dq.from_trans([1, 2, 3], q([1, 1, 1, 1]).normalized())
# dq1 = dq.from_trans([3, 2, 3], q([1, 0, 1, 1]).normalized())

# print(dq0.sclerp(dq1, 0.5))
# print(dq0)