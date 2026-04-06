from scipy . stats import randint
import matplotlib.pyplot as plt
import numpy as np

def calculate_signal_stats ( v_min , v_max ) :
    """
    Returns :
    tuple : (e_v , e_power , is_equal )
    """
    # Create array of possible voltages
    possible_v = np . arange ( v_min , v_max + 1)
    # Calculate E[V]
    e_v = (v_min+v_max)/2
    # Calculate E[V^2] ( Mean of squares )
    e_power =np.square(possible_v).sum()/len(possible_v)
    # Check equality
    if (e_v==e_power):
        is_equal = False
    else:
        is_equal=True
    return e_v , e_power , is_equal
def plot_power_comparison ( e_v , e_power ) :
    """
    Generates a bar chart comparing (E[V]) ^2 and E[V ^2].
    """
    # Calculate (E[V]) ^2
    e_v_squared = e_v ** 2
    labels = ["(E[V]) ^2 ", "E[V ^2] "]
    values = [ e_v_squared , e_power ]
    # Plotting code
    plt . figure ( figsize =(6 , 5) )
    plt.bar(labels,values)
    # [Add code to plot bar chart ]
    plt . title (" Expectation of Square vs Square of Expectation ")
    plt . ylabel (" Value ")
    plt . show ()
# Main execution block for testing
if __name__ == "__main__":
    v_min , v_max = 1 , 5
    ev , epow , eq = calculate_signal_stats ( v_min , v_max )
    print ( f"E[V]: {ev} , E[V ^2]: { epow } , Is Equal : {eq}")
    plot_power_comparison ( ev , epow )
