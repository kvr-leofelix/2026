import matplotlib.pyplot as plt
import numpy as np
import random

serverList = [1, 2, 3, 4]
likeProb = [0.15, 0.25, 0.35, 0.25]

cdfValues = []
a = 0
for p in likeProb:#go through each element in probability
    a += p
    cdfValues.append(a)

print(f"Calculated CDF: {cdfValues}")

plt.figure(figsize=(14, 6))

plt.subplot(1, 2, 1)
plt.bar(serverList, likeProb, color='teal', alpha=0.7)
plt.title("PMF Distribution")
plt.xlabel("Server ID")

plt.ylabel("P(X)")

plt.subplot(1, 2, 2)
plt.step(serverList, cdfValues, where='post', color='red', marker='d')
plt.title("CDF Distribution")
plt.xlabel("Server ID")


plt.ylabel("F(X)")
plt.grid(True)
plt.show()

probhumOdd = likeProb[0] + likeProb[2]#now add up the prob
print(f"Probabilty of odd servers: {probhumOdd}")

probNotOne = 1 - likeProb[0]
condProb_3 = likeProb[2] / probNotOne
print(f"Proability of S3 given not S1: {round(condProb_3, 4)}")

simCount = 10000
randomData = random.choices(serverList, weights=likeProb, k=simCount)#choose among 1000 digi

exProbs = []
for s in serverList:
    count = randomData.count(s)

    exProbs.append(count / simCount)

plt.figure(figsize=(9, 6))
xLocs = np.arange(len(serverList))

plt.bar(xLocs - 0.2, likeProb, 0.4, label='Theoretical', color='navy')
plt.bar(xLocs + 0.2, exProbs, 0.4, label='Empirical', color='orange')

plt.xticks(xLocs, serverList)
plt.legend()
plt.title("Comparison of Results")


plt.show()