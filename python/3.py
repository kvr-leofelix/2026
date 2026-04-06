import numpy as np
import random

# Data generation as provided in the manual
random.seed(20)
n_val = 500  # Note: The prompt has a typo listing n=20 then n=500; we use 500 [cite: 12, 14]
p_val = 0.7
data = np.random.binomial(n_val, p_val, size=n_val)
print(data)
def compute_empirical_pmf(data, num_bins):
    # 1. Calculate counts and bin edges
    counts, bin_edges = np.histogram(data, bins=num_bins) 
    
    # 2. Compute probabilities (Empirical PMF)
    total_elements = len(data)
    pmf_values = counts / total_elements 
    
    # 3. Present the results [cite: 19]
    print(f"--- Empirical PMF (Bins: {num_bins}) ---")
    for i in range(len(pmf_values)):
        interval = f"[{bin_edges[i]:.2f}, {bin_edges[i+1]:.2f})"
        print(f"Interval {interval}: Probability {pmf_values[i]:.4f}")
    
    # 4. Verification 
    total_sum = np.sum(pmf_values)
    all_positive = np.all(pmf_values >= 0)
    
    print("\n--- Verification ---")
    print(f"Sum of PMF: {total_sum:.4f}")
    print(f"Is valid PMF? {'Yes' if np.isclose(total_sum, 1.0) and all_positive else 'No'}")

# Running the function
compute_empirical_pmf(data, num_bins=10)

# -------------------------------------
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

# 1. Data Generation (strictly following the prompt) [cite: 22-30]
np.random.seed(20)
n = 500

# Dataset 1: Exponential [cite: 26]
lam = 2
d1 = np.random.exponential(scale=1/lam, size=n)

# Dataset 2: Normal [cite: 28]
mu, sigma = 5, 2
d2 = np.random.normal(mu, sigma, size=n)

# Dataset 3: Beta [cite: 30]
A, B = 2, 3
d3 = np.random.beta(a=A, b=B, size=n)

datasets = [d1, d2, d3]
labels = ['Exponential', 'Normal', 'Beta']
x0 = 1.5

# 2. KDE, Plotting, and Evaluation [cite: 32, 33]
plt.figure(figsize=(15, 5))

for i, data in enumerate(datasets):
    # Create the KDE object 
    kde = gaussian_kde(data)
    
    # Evaluate density at x0 
    density_at_x0 = kde.evaluate(x0)[0]
    print(f"{labels[i]} density at x={x0}: {density_at_x0:.4f}")
    
    # Plotting [cite: 32]
    plt.subplot(1, 3, i+1)
    plt.hist(data, bins=30, density=True, alpha=0.5, color='gray', label='Histogram')
    
    x_range = np.linspace(min(data), max(data), 1000)
    plt.plot(x_range, kde(x_range), 'r-', lw=2, label='KDE')
    plt.axvline(x0, color='blue', linestyle='--', label=f'x={x0}')
    plt.title(f"{labels[i]} Distribution")
    plt.legend()

plt.tight_layout()
plt.show()

# 3. Observations [cite: 34]
# - Exponential: Sharp peak at start, decays quickly.
# - Normal: Symmetric "Bell" shape centered at mu=5.
# - Beta: Bound between 0 and 1, shape depends on A and B.