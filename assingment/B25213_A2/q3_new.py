import matplotlib.pyplot as plt
import random
 
servers = [1, 2, 3, 4]
p = [0.15, 0.25, 0.35, 0.25]
 
# Task 1: Compute CDF manually using a loop
cdf = []
total = 0
 
for i in p:
    total += i
    cdf.append(total)
 
print(f"CDF: {cdf}")
 
# PMF plot
plt.stem(servers, p,)
plt.title("Probability Mass Function (PMF)")
plt.xlabel("Server ID")
plt.ylabel("Probability")
plt.show()
 
# CDF plot 
plt.step(servers, cdf, where='post', marker='o')
plt.title("Cumulative Distribution Function (CDF)")
plt.xlabel("Server ID")
plt.ylabel("Cumulative Probability")
plt.grid(True)
plt.show()
 
# Odd-numbered server
p_odd = p[0] + p[2]
print(f"Probability(Odd Server): {p_odd}")
 
# Conditional Probability P(S3 | S1 is unavailable)
p_s1_unav = p[1] + p[2] + p[3] 
cond_p_s3 = p[2] / p_s1_unav
print(f"Conditional Prob P(S3 | not S1): {cond_p_s3:.4f}")
 
# Simulate 10,000 task assignments
n = 10000
counts = {1: 0, 2: 0, 3: 0, 4: 0}
 
for i in range(n):
    r = random.random()  # Generates a number between 0 and 1
    if r < cdf[0]:
        counts[1] += 1
    elif r < cdf[1]:
        counts[2] += 1
    elif r < cdf[2]:
        counts[3] += 1
    else:
        counts[4] += 1
 
empirical_freqs = [counts[i] / n for i in servers]
 
x = range(len(servers))
width = 0.35
 
plt.bar([i - width/2 for i in x], p, width, label='Theoretical', color='skyblue')
plt.bar([i + width/2 for i in x], empirical_freqs, width, label='Empirical', color='orange')
 
print(f"Theoretical: {p}")
print(f"Empirical: {empirical_freqs}") 
 
plt.xlabel('Server ID')
plt.ylabel('Probability')
plt.title('Theoretical vs Empirical Frequencies (10,000 Trials)')
plt.xticks(x, servers)
plt.legend()
plt.show()