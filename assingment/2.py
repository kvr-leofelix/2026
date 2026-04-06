def sequential_belief_update(flips=5):
    p_fair = 0.99 
    p_h_given_fair = 0.5 
    p_h_given_unfair = 1.0 

    for i in range(1, flips + 1):
        # Law of Total Probability for P(H)
        p_h = (p_h_given_fair * p_fair) + (p_h_given_unfair * (1 - p_fair))
        # Bayes' Theorem to find new P(Fair) 
        p_fair = (p_h_given_fair * p_fair) / p_h
        print(f"After Flip {i} (Heads): P(Fair) = {p_fair:.5f}")

sequential_belief_update()