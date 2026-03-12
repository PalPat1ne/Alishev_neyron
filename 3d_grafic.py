import matplotlib.pyplot as plt
import numpy as np
import argparse
from mpl_toolkits import mplot3d
from matplotlib.patches import Patch

prs = argparse.ArgumentParser()
prs.add_argument('in_file')
args = prs.parse_args()

d = np.loadtxt(args.in_file)

x1 = d[:,0]
x2 = d[:,1]
y  = d[:,2]

X1 = []
X2 = []

b = x1[0]
for a in x1:
    if a >= b:
        X1.append(a)
    else:
        break
    b = a

b = x2[0]
X2.append(b)
for a in x2:
    if a > b:
        X2.append(a)
    b = a

s1 = np.array(X1).size
s2 = np.array(X2).size

Y = []
for i in range(len(X1)):
    k = []
    for j in range(len(X2)):
        k.append(y[i*len(X1)+j])
    Y.append(k)

fig = plt.figure(figsize=(10, 8))
ax = plt.axes(projection='3d')

X_1, X_2 = np.meshgrid(np.array(X1), np.array(X2))

surface = ax.plot_surface(X_1, X_2, np.array(Y),
                          rstride=1, cstride=1, cmap='viridis')

ax.set_xlabel('x1', fontsize=14, fontweight='bold', labelpad=16, color='black')
ax.set_ylabel('x2', fontsize=14, fontweight='bold', labelpad=16, color='black')
ax.set_zlabel('y', fontsize=14, fontweight='bold', labelpad=12, color='black')
ax.set_title('3D graph y(x1, x2)', fontsize=15, fontweight='bold', pad=18)
ax.tick_params(axis='x', labelsize=11, pad=4, colors='black')
ax.tick_params(axis='y', labelsize=11, pad=4, colors='black')
ax.tick_params(axis='z', labelsize=11, pad=6, colors='black')

colorbar = fig.colorbar(surface, ax=ax, shrink=0.65, pad=0.1)
colorbar.ax.tick_params(labelsize=11, colors='black')
colorbar.set_label('y', fontsize=13, fontweight='bold', color='black')

legend_patch = Patch(facecolor=plt.cm.viridis(0.7),
                     edgecolor='black',
                     label='Surface y(x1, x2)')
ax.legend(handles=[legend_patch], loc='upper left')

plt.tight_layout()
plt.show()
