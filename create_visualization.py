from datetime import datetime, date
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import pathlib

# Define Dataset
x = [1,2,3,4,5,6,7,8,9,10]
y = [1,2,3,4,5,8,8,9,3,1]

def create_visualization(x,y):
    '''
        Create Visualization
        return:
            - saves the created plot in ./results/
            - dir: path to working directory
            - path: path to saved plot
    '''

    # Font size
    plt.rc('font', size=22)          # controls default text sizes
    plt.rc('axes', titlesize=22)     # fontsize of the axes title
    plt.rc('axes', labelsize=20)    # fontsize of the x and y labels
    plt.rc('xtick', labelsize=18)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=18)    # fontsize of the tick labels
    plt.rc('legend', fontsize=18)    # legend fontsize
    plt.rc('figure', titlesize=22)  # fontsize of the figure title

    #create new plot with matplotlib
    fig, ax = plt.subplots(figsize=(14, 7))

    # add a bar plot to the figure
    ax.bar(x,y, color='grey')
    ax.set(xlabel='Day', ylabel='Hours [h]')

    # define filename with current date e.g. "2021-04-08.png"
    filename = str(date.today()) + ".png"


    dir = pathlib.Path(__file__).parent.absolute()
    folder = r"/results/"
    path = str(dir) + folder + filename
    fig.savefig(path, dpi=fig.dpi)

    return path, dir

path, dir = create_visualization(x,y)