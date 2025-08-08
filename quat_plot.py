from quat import quat
from dual_quat import dual_quat

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

def plot_quat(ax: Axes3D, q: quat, arrows: str, len: float = 0.5) :
    '''
    Plot a unit quaternion representing a rotation as an arrow.
    
    Args
    ---
    ax : axes3d
        The axis object to plot the arrows on
    q : quat
        The quaternion to plot
    arrows : str
        The arrows to show from ['facing', 'basis']
        facing gives a single arrow in the x direction, basis gives three arrows in the x, y, z directions
    len : float, opt.
        The length of the arrows
    '''
    plot_arrows(ax, q, [0, 0, 0], arrows, len)

def plot_quats(ax: Axes3D, qs: list[quat], arrows: str, len: float = 0.5) :
    '''
    Plot multiple unit quaternions representing rotations as arrows.
    
    Args
    ---
    ax : axes3d
        The axis object to plot the arrows on
    qs : list[quat]
        The quaternions to plot
    arrows : str
        The arrows to show from ['facing', 'basis']
        facing gives a single arrow in the x direction, basis gives three arrows in the x, y, z directions
    len : float, opt.
        The length of the arrows
    '''
    for q in qs :
        plot_quat(ax, q, arrows, len)


def plot_dual_quat(ax: Axes3D, dq: dual_quat, arrows: str, len: float = 0.5) :
    '''
    Plot a unit dual quaternion representing a 3D transform as an arrow.
    
    Args
    ---
    ax : axes3d
        The axis object to plot the arrows on
    dq : dual_quat
        The dual quaternion to plot
    arrows : str
        The arrows to show from ['facing', 'basis']
        facing gives a single arrow in the x direction, basis gives three arrows in the x, y, z directions
    len : float, opt.
        The length of the arrows
    '''
    trans, rot = dq.as_trans()
    plot_arrows(ax, rot, trans, arrows, len)

def plot_dual_quats(ax: Axes3D, dqs: list[dual_quat], arrows: str, len: float = 0.5) :
    '''
    Plot multiple unit dual quaternions representing 3D transforms as arrows.
    
    Args
    ---
    ax : axes3d
        The axis object to plot the arrows on
    dqs : list[dual_quat]
        The dual quaternions to plot
    arrows : str
        The arrows to show from ['facing', 'basis']
        facing gives a single arrow in the x direction, basis gives three arrows in the x, y, z directions
    len : float, opt.
        The length of the arrows
    '''
    for dq in dqs :
        plot_dual_quat(ax, dq, arrows, len)

def plot_arrows(ax: Axes3D, rot: quat, position: list[float], arrows: str, len: float = 0.5) :
    '''
    Plots arrows onto the given axis object.

    Args
    ---
    ax : axes3d
        The axis object to plot the arrows on
    rot : quat
        The orientation of the arrow
    position: list[float]
        The x, y, z position for the base of the arrow
    arrows : str
        The arrows to show from ['facing', 'basis']
        facing gives a single arrow in the x direction, basis gives three arrows in the x, y, z directions
    len : float, opt.
        The length of the arrow
    '''
    if arrows == 'facing' :
        dir_x = rot.rot_apply([len, 0, 0])
        ax.quiver(*position, *dir_x, length=len, normalize=True, color='black')

    elif arrows == 'basis' :
        dir_x = rot.rot_apply([len, 0, 0])
        dir_y = rot.rot_apply([0, len, 0])
        dir_z = rot.rot_apply([0, 0, len])

        ax.quiver(*position, *dir_x, length=len, normalize=True, color='red')
        ax.quiver(*position, *dir_y, length=len, normalize=True, color='green')
        ax.quiver(*position, *dir_z, length=len, normalize=True, color='blue')

    
    # if arrows == 'facing' :
    #     dir_x = rot.rot_apply([len, 0, 0])
    #     ax.arrow3D(*position,
    #             *dir_x,
    #             mutation_scale = 10,
    #             arrowstyle = "-|>",
    #             linestyle = 'solid')

    # elif arrows == 'basis' :
    #     dir_x = rot.rot_apply([len, 0, 0])
    #     ax.arrow3D(*position,
    #             *dir_x,
    #             mutation_scale = 10,
    #             arrowstyle = "-|>",
    #             linestyle = 'solid',
    #             color = 'red')
        
    #     dir_y = rot.rot_apply([0, len, 0])
    #     ax.arrow3D(*position,
    #             *dir_y,
    #             mutation_scale = 10,
    #             arrowstyle = "-|>",
    #             linestyle = 'solid',
    #             color = 'green')
        
    #     dir_z = rot.rot_apply([0, 0, len])
    #     ax.arrow3D(*position,
    #             *dir_z,
    #             mutation_scale=10,
    #             arrowstyle = "-|>",
    #             linestyle = 'solid',
    #             color = 'blue')