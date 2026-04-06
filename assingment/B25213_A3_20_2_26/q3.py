from scipy . stats import geom
import matplotlib.pyplot as plt
import numpy as np
def calculate_flood_risk ( return_period , project_years ) :
    """
    Returns :
    float : The probability of failure during the project
    3
    """
    # Calculate p from Return Period
    p = 1/return_period
    # Calculate Cumulative Risk
    risk_prob = geom.cdf(project_years,p)
    return risk_prob
def plot_risk_accumulation ( return_period , max_years ) :
    """
    Generates a line plot of Risk vs Project Duration .
    """
    p = 1/return_period
    years = np . arange (1 , max_years + 1)
    # Calculate risk for each year in the array
    risks = geom.cdf(years,p)
    # Plotting code
    plt . figure ( figsize =(10 , 5) )
    # [Add code to plot line chart ]
    plt.plot(years,risks,marker='o')
    plt . title ( f" Risk Accumulation over { max_years } Years (T={ return_period })")
    plt . xlabel (" Project Duration ( Years )")
    plt . ylabel (" Probability of Encounter ")
    plt . grid ( True )
    plt . show ()
# Main execution block for testing
if __name__ == "__main__":
    T , years = 100 , 20
    risk = calculate_flood_risk (T , years )
    print ( f" Risk of {T} - year flood in { years } years : { risk :.4f}")
    plot_risk_accumulation (T , 30)