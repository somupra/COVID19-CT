import numpy as np
import matplotlib.pyplot as plt
import pylab
import csv

def final_plot(path, N=100):
    # N=Total population; path= path of file to read the set of points from.

    # Time in days, t.
    t = []
    # No. of healthy people after ith day, H[i].
    H = []
    # No. of infected people after ith day, I[i].
    I = []
    # No. of isolated_healthy people after ith day, I_H[i].
    I_H = []
    # No. of isolated_infected people after ith day, I_H[i].
    I_INF = []

    with open(path) as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        for row in plots:
            t.append(int(row[0]))
            H.append((float(row[1]))/N)
            I.append((float(row[2]))/N)
            I_H.append((float(row[3]))/N)
            I_INF.append((float(row[4]))/N)


    # Plot the data on four separate curves for H(t), I(t), I_H(t) and I_INF(t).
    fig = plt.figure(facecolor='w')
    ax = fig.add_subplot(111, facecolor='#dddddd', axisbelow=True)
    ax.plot(t, H, 'g', alpha=0.5, lw=2, label='Healthy')
    ax.plot(t, I, 'r', alpha=0.5, lw=2, label='Infected')
    ax.plot(t, I_H, 'b', alpha=0.5, lw=2, label='Isolated-Healthy')
    ax.plot(t, I_INF, '#ffa500', alpha=0.5, lw=2, label='Isolated-Infected')
    ax.set_xlabel('Time (days)')
    ax.set_ylabel('Fraction of population')
    ax.set_ylim(0,1.2)
    ax.yaxis.set_tick_params(length=0)
    ax.xaxis.set_tick_params(length=0)
    ax.grid(b=True, which='major', c='w', lw=2, ls='-')
    legend = ax.legend()
    legend.get_frame().set_alpha(0.5)
    for spine in ('top', 'right', 'bottom', 'left'):
        ax.spines[spine].set_visible(False)
    plt.title('{0} Isolation'.format(path))
    pylab.savefig('{0}.png'.format(path))
    # plt.title('Level 0 Isolation')
    # pylab.savefig('level0_isoln.png')
    plt.show()
