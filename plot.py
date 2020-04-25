import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pylab
import csv

def final_plot(path, N=100, n_days=80):
    """ path= path of file to read the set of points from; N=Total population; n_days=no. of days"""

    # Time in days, t.
    t = []
    # No. of healthy people after ith day, H[i].
    H = []
    H_Err = []
    # No. of infected people after ith day, I[i].
    I = []
    I_Err = []
    # No. of isolated_healthy people after ith day, I_H[i].
    I_H = []
    I_H_Err =[]
    # No. of isolated_infected people after ith day, I_H[i].
    I_INF = []
    I_INF_Err = []

    df = pd.read_csv(path, header=None)
    cols = n_days*4
    day = 1
    
    for i in range(cols):
        curr_mean = df[i].mean()
        curr_dev = df[i].std()

        if(i%4 == 0):
            t.append(day)
            day += 1
            H.append((float(curr_mean))/N)
            H_Err.append((float(curr_dev))/N)
        elif (i%4==1):
            I.append((float(curr_mean))/N)
            I_Err.append((float(curr_dev))/N)
        elif (i%4==2):
            I_H.append((float(curr_mean))/N)
            I_H_Err.append((float(curr_dev))/N)
        elif (i%4==3):
            I_INF.append((float(curr_mean))/N)
            I_INF_Err.append((float(curr_dev))/N)


    # Plot the data on four separate curves for H(t), I(t), I_H(t) and I_INF(t).
    fig = plt.figure(facecolor='w')
    ax = fig.add_subplot(111, facecolor='#dddddd', axisbelow=True)
    ax.errorbar(t, H, yerr=H_Err, uplims=True, lolims=True, color='g', alpha=0.5, lw=2, label='Healthy')
    ax.errorbar(t, I, yerr=I_Err, uplims=True, lolims=True, color='r', alpha=0.5, lw=2, label='Infected')
    ax.errorbar(t, I_H, yerr=I_H_Err, uplims=True, lolims=True, color='b', alpha=0.5, lw=2, label='Isolated-Healthy')
    ax.errorbar(t, I_INF,yerr=I_INF_Err, uplims=True, lolims=True, color='#ffa500', alpha=0.5, lw=2, label='Isolated-Infected')
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

# final_plot(path="plotfile.txt", N=100, n_days=80)
