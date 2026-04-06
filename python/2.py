import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

# 1. Define the Data (Discrete)
# A die has outcomes 1 through 6
outcomes = [1, 2, 3, 4, 5, 6]

# 2. Define the Probabilities (PMF)
# For a fair die, each number has 1/6 chance
probs = [1/6] * 6 

# 3. Visualize
plt.figure(figsize=(8, 4))
plt.bar(outcomes, probs, color='skyblue', edgecolor='black', width=0.5)

plt.title("PMF: Rolling a Die")
plt.xlabel("Outcome (Discrete)")
plt.ylabel("Probability Mass P(X=x)")
plt.ylim(0, 0.25)
plt.show()