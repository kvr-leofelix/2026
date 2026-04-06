import numpy as np
ma = [
    [0,   0,   0,   0,   0],
    [0, 255, 255,   0,   0],
    [0, 255, 255,   0,   0],
    [0,   0,   0,   0,   0],
    [0,   0,   0,   0,   0]
]
m=np.array(ma)
p,n=np.array(ma).shape
print(n)
a=int(input("enter the threshold value"))
for i in range(p):
    for j in range(n):
        if (m[i,j]>=a):
            m[i,j]=1
        else:
            m[i,j]=0
print(m)