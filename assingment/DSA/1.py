import numpy as np
import matplotlib.pyplot as plt

# a=np.ones((5,5),dtype='int16')
# print(a)
# a=[]
# t=int(input("enter the threshold"))

def readfile(filename):
    with open(filename,'r') as f:
        lines=[]
        for line in f:
              if not line.startswith("#"):
                  lines.append(line.strip())
                  print(lines)
    # print(lines)
readfile("hey.txt")


# threshold code
# ar,ac=a.shape
# for i in range(ar):
#     for j in range(ac):
#             if a(i,j)>t:
#                   a[i,j]=1
#             else:
#                   a[i,j]=0

# print(a)
# print(a.shape)
