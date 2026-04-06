import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import randint,geom,binom,poisson

def analyze_sensor_power(v_min,v_max):
    n=v_max-v_min
    e_v=(((v_max)*(v_max+1)*(2*v_max+1))/6-((v_min)*(v_min+1)*(2*v_min+1))/6)/n
    e_power=((((v_max)*(v_max+1)/2)-((v_min)*(v_min+1)/2))/(n))**2
    if(e_v==e_power):

        is_equal=True
    else:
        is_equal=False
    return e_v,e_power,is_equal

def plot_power_comparison(e_v,e_power):
    plt.figure(figsize=(6,5))
    plt.bar(("E[V^2]","E[V]^2"),(e_v,e_power))
    plt.title (" Expectation Inequality : E[V^2] vs (E[V]) ^2")
    plt.show()
    
def assess_flood_risk(return_period,project_years):
    p=1/return_period
    risk_prob=0
    for i in range(1,project_years):
        risk_prob+=((p)*(1-p)**(i-1))
    return risk_prob

def plot_risk_accumulation(return_period,v_max_years):
    plt.figure(figsize=(10,5))
    p=1/return_period
    year=list(range(1,v_max_years+1))
    plt.plot(year,[1-(1-p)**n for n in year])
    plt.title ( f" Flood Risk Accumulation (T={ return_period })")
    plt.show()
def optimize_camera_quality (n , p , cost_test , cost_fail ) :
    expected_defects=n*p

    cost_inspect=cost_test*n
    cost_install=expected_defects*cost_fail
    if (cost_install<=cost_inspect):
        strategy="JUST INSTALL"
        savings=abs(cost_inspect-cost_install)
    else:
        strategy="inspect first"
        savings =abs(cost_inspect-cost_install)
    
    return expected_defects , strategy , savings

def plot_defect_pmf(n,p):
    plt.figure(figsize=(10,5))
    x=np.arange(binom.ppf(0.001,n,p),binom.ppf(0.999,n,p))
    pmf=binom.pmf(x,n,p)
    plt.stem(x,pmf,basefmt=" ")
    plt.title ( f" Defect Distribution (n={n} , p={p})")
    plt.show ()

def plan_server_capacity(lam,reliability_target):
    required_capacity=poisson.ppf(reliability_target,lam)
    return int(required_capacity)
def plot_reliability_cdf(lam,capacity_threshold):
    plt.figure(figsize=(10,5))
    x=np.arange(0,capacity_threshold*1.5)
    cdf = poisson.cdf(x,lam)
    plt.step(x,cdf)
    plt.show()

if __name__=="__main__":
    print("--- PART A: sensor power")
    ev,epow,eq=analyze_sensor_power(1,5)
    print ( f"E[V]: {ev} , E[V ^2]: { epow } , Equal ?: {eq}")
    plot_power_comparison ( ev , epow )
    print ("\n- - - Part B: Bridge Risk ---")
    risk = assess_flood_risk (100 , 4)
    print ( f" Risk during 4 - year construction : { risk :.4f}")
    plot_risk_accumulation (100 , 20)
    print ("\n- - - Part C: Camera Quality ---")
    edef , strat , sav = optimize_camera_quality (200 , 0.05 , 2.0 , 50.0)
    print ( f" Strategy : { strat } , Savings : {sav}")
    plot_defect_pmf (200 , 0.05)
    print ("\n- - - Part D: Server Reliability ---")
    cap = plan_server_capacity (15 , 0.999)
    print ( f" Required Capacity : {cap}")
    plot_reliability_cdf(15,cap)





