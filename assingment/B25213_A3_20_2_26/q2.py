from scipy.stats import poisson
import matplotlib.pyplot as plt
import numpy as np
def calculate_server_capacity ( lam , reliability_target ) :
    """
    Returns :
    int : The minimum capacity C required
    """
    # Use Inverse CDF ( Percent Point Function )
    required_capacity = poisson.cdf(reliability_target,lam)
    return int( required_capacity )
def plot_reliability_cdf ( lam , capacity_threshold ) :
    """
    Generates a step plot of the CDF and marks the capacity threshold .
    """
    # Generate x values (0 to 2* lambda )
    x = np.arange (0 ,int( lam * 2))
    # Calculate CDF values
    cdf_values = poisson.cdf(x,lam)
    # Plotting code
    
    plt.figure ( figsize =(10 , 5) )
    plt.step(x,cdf_values,label="cdf")
    plt.axvline(x=capacity_threshold)
    # [Add code to plot step chart ]
    # [Add code to draw vertical line at capacity_threshold ]
    plt.title ( f" Server Reliability CDF ( Lambda ={ lam })")
    plt.xlabel (" Requests per Second ")
    plt.ylabel (" Cumulative Probability ")
    plt.grid ( True )
    plt.show ()
    # Main execution block for testing
if __name__ == "__main__":
    lam , target = 15 , 0.999
    cap = calculate_server_capacity ( lam , target )
    print ( f" Required Capacity for { target *100}% reliability : {cap}")
    plot_reliability_cdf ( lam , cap )
