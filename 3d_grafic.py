import matplotlib.pyplot as plt
import numpy as np
import argparse
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt

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

fig = plt.figure()
ax = plt.axes(projection='3d')

X_1, X_2 = np.meshgrid(np.array(X1), np.array(X2))

ax.plot_surface(X_1, X_2, np.array(Y),
                rstride=1, cstride=1, cmap='viridis')

plt.show()