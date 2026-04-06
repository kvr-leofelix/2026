import numpy as np
import matplotlib . pyplot as plt
from scipy.stats import binom
from scipy.optimize import minimize_scalar
def calculate_quality_costs (n , p , cost_test , cost_fail ) :
    """
    Returns :
    tuple : ( expected_defects , cheaper_strategy_name , savings )
    """
    # Calculate Expected Defects
    expected_defects = n*p
    # Calculate Costs
    cost_inspect = n*cost_test
    cost_ship = expected_defects*cost_fail

    strategy = "ship" if cost_ship<cost_inspect else "inspect"
    
    savings = abs(cost_ship-cost_inspect)
    return expected_defects , strategy , savings
def plot_defect_distribution (n , p ) :
    """
    Generates a bar chart of the PMF.
    """
    # Create x- axis values ( number of defects )
    k_values = np.arange (0 , n + 1)
    # Calculate PMF values
    pmf_values = binom.pmf(k_values, n, p)
    # Plotting code
    plt . figure ( figsize =(10 , 5) )
    plt.bar(k_values, pmf_values)
    plt . title ( f" Defect Distribution (n={n} , p={p})")
    plt . xlabel (" Number of Defects ")
    plt . ylabel (" Probability ")
    plt . show ()
# Main execution block for testing
if __name__ == "__main__":
    n , p = 200 , 0.05
    cost_test , cost_fail = 2.0 , 50.0
    ed , strat , sav = calculate_quality_costs (n , p , cost_test , cost_fail )
    print ( f" Expected Defects : {ed :.2f} , Strategy : { strat } , Savings : {sav :.2f}")
    plot_defect_distribution (n , p )