from quat import quat as q
from dual_quat import dual_quat as dq
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d.proj3d import proj_transform
from mpl_toolkits.mplot3d.axes3d import Axes3D
import numpy as np

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

n = 100

rand_quats = np.random.normal([0, 0, 0, 0], [1, 1, 1, 1], (n, 4))

transforms = []

for i in range(n) :
    transforms.append(dq.from_trans(np.random.normal([5, 5, 5], [4, 2, 3]), q(rand_quats[i]).normalized()))


points = np.zeros((n, 3))

for idx, trans in enumerate(transforms) :
    points[idx] = trans.as_trans()[0]
    dir = trans.as_trans()[1].rot_apply([1, 0, 0])

    ax.arrow3D(*trans.as_trans()[0],
            *dir,
            mutation_scale=10,
            arrowstyle="-|>",
            linestyle='dashed')

scatter = ax.scatter(points[:,0], points[:,1], points[:,2], c=range(np.shape(points)[0]), cmap='viridis')

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.set_zlim(0, 10)

fig.colorbar(scatter)

plt.show()