def attach_prob(src, trg, curr_day):
    """Attaches the probability to the nodes wrt the source they got infected [assumed to be]. For now, analysis done on the basis of number of contacts the source made with the target node. [NOTE]: The target node might infect the source node as well, as well as, there might be more than one source infecting the same target, we add up the probabilities, and finally trim it if it exceeds 1."""
    print("attaching prob for day ", curr_day)
<<<<<<< HEAD

=======
>>>>>>> c0e9dd528590dfb5f5972d3fb9961cbb03e0f149
    contact_times = len([contact for contact in trg.edge_dict[src.id] if ((contact[0] // 1000)+1) == curr_day])
    # print([contact for contact in trg.edge_dict[src.id]])
    # print([contact for contact in trg.edge_dict[src.id] if ((contact[0] // 1000) + 1) == curr_day])
    print("contacts between:", src, " -- ", trg, " : ", contact_times)
    print("Target Node edge dict: ",trg.edge_dict)
    print("Source Node edge dict: ",src.edge_dict)

    if contact_times:
        if contact_times < 5 and contact_times >= 1:
            trg.inf_prob += src.inf_prob/40

        elif contact_times < 10 and contact_times >=5:
            trg.inf_prob += src.inf_prob/10

        elif contact_times < 16 and contact_times >= 10:
            trg.inf_prob += src.inf_prob/7

        elif contact_times < 20 and contact_times >= 16:
            trg.inf_prob += src.inf_prob/3

        else:
            trg.inf_prob += src.inf_prob/1.5

    # Trimming the excess probability to restrict it exceeding 1.
    trg.inf_prob = min(1, trg.inf_prob)