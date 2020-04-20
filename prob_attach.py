def attach_prob(src, trg):
    """Attaches the probability to the nodes wrt the source they got infected [assumed to be]. For now, analysis done on the basis of number of contacts the source made with the target node. [NOTE]: The target node might infect the source node as well, as well as, there might be more than one source infecting the same target, we add up the probabilities, and finally trim it if it exceeds 1."""
    contact_times = len(trg.edge_dict[src.id])

    if contact_times < 3 and contact_times >= 1:
        trg.inf_prob += src.inf_prob/20

    elif contact_times < 7 and contact_times >=3:
        trg.inf_prob += src.inf_prob/10

    elif contact_times < 10 and contact_times >= 7:
        trg.inf_prob += src.inf_prob/6

    elif contact_times < 14 and contact_times >= 10:
        trg.inf_prob += src.inf_prob/3

    else:
        trg.inf_prob += src.inf_prob/2

    # Trimming the excess probability to restrict it exceeding 1.
    trg.inf_prob = min(1, trg.inf_prob)