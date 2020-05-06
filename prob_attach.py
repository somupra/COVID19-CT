from params import RADIUS
def attach_prob(src, trg, curr_day, city):
    """Attaches the probability to the nodes wrt the source they got infected [assumed to be]. For now, analysis done on the basis of number of contacts the source made with the target node. [NOTE]: The target node might infect the source node as well, as well as, there might be more than one source infecting the same target, we add up the probabilities, and finally trim it if it exceeds 1."""

    print("Day {0} :: attaching prob for source ({1}, {2}) and ({3}, {4})".format(curr_day, src, src.status, trg, trg.status))
    print("reversed edge dict is: ", reversed(trg.edge_dict[src.id]))

    if src.inf_start_time is not None and not trg.is_infected():
        for contact in reversed(trg.edge_dict[src.id]):
            if contact[0] < src.inf_start_time:
                break
            else:
                prob = min(1, src.inf_prob / 2)
                trg.inf_prob = prob
                trg.mark_infection(curr_day, contact[0], city)
                if trg.is_infected():
                    break

    