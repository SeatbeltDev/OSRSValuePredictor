# CHANDLER MATEKA
# Final Project - Program #2: Data Visualization

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def bar_plot(df):
    fig, ax = plt.subplots()

    nullIndexes = []
    for index in range(len(df) - 1):
        if df['GE Value'].isnull()[index] or df['GE Value'][index] == 'Not sold':
            nullIndexes.append(index)
    df = df.drop(nullIndexes)
    df = df.set_index('Type')
    df = df.reset_index()
    df['GE Value'] = df['GE Value'].astype('int')

    dfmeans = df.groupby('Type').aggregate(np.mean)
    ax.bar(dfmeans.index, dfmeans['GE Value'])
    
    ax.set(title = 'Average Value by Item Type', xlabel = 'Type', ylabel = 'Value in tens of millions')
    for x in ax.get_xticklabels():
        x.set_rotation(90)

    return ax

def scatter_plot(df):
    fig, ax = plt.subplots()

    nullIndexes = []
    for index in range(len(df) - 1):
        if df['GE Value'].isnull()[index] or df['GE Value'][index] == 'Not sold':
            nullIndexes.append(index)
    df = df.drop(nullIndexes)
    df = df.set_index('Type')
    df = df.reset_index()

    df['GE Value'] = df['GE Value'].astype('int')
    # nullIndexes = []
    # for index in range(len(df) - 1):
    #     if df['GE Value'][index] > 300000000 or df['GE Value'][index] < 1000000:
    #         nullIndexes.append(index)
    # df = df.drop(nullIndexes)
    
    ax.scatter(df['Strength'], df['GE Value'])

    ax.set(title = 'Correlation Between Strength Bonus and Value', xlabel = 'Strength Bonus', ylabel = 'Value in Billions')
    for x in ax.get_xticklabels():
        x.set_rotation(90)

    return ax

def violin_plot(df):
    fig, ax = plt.subplots()

    nullIndexes = []
    for index in range(len(df) - 1):
        if df['GE Value'].isnull()[index] or df['GE Value'][index] == 'Not sold':
            nullIndexes.append(index)
    df = df.drop(nullIndexes)
    df = df.set_index('Type')
    df = df.reset_index()

    df['GE Value'] = df['GE Value'].astype('int')
    # nullIndexes = []
    # for index in range(len(df) - 1):
    #     if df['GE Value'][index] > 300000000 or df['GE Value'][index] < 1000000:
    #         nullIndexes.append(index)
    # df = df.drop(nullIndexes)
    types = df['Type'].unique()

    ax.violinplot([df[df['Type'] == types[0]]['GE Value'].values,
                   df[df['Type'] == types[1]]['GE Value'].values,
                   df[df['Type'] == types[2]]['GE Value'].values,
                   df[df['Type'] == types[3]]['GE Value'].values,
                   df[df['Type'] == types[4]]['GE Value'].values,
                   df[df['Type'] == types[5]]['GE Value'].values,
                   df[df['Type'] == types[6]]['GE Value'].values,
                   df[df['Type'] == types[7]]['GE Value'].values,
                   df[df['Type'] == types[8]]['GE Value'].values,
                   df[df['Type'] == types[9]]['GE Value'].values,
                   df[df['Type'] == types[10]]['GE Value'].values])

    # ax.set_xticks(types)
    ax.set(title = 'Distribution of Value by Item Type', xlabel = 'Type', ylabel = 'Value in millions')
    # ax.set_xticks(df.index.unique()[1:12])
    ax.set_xticklabels(types)
    for x in ax.get_xticklabels():
        x.set_rotation(90)

    return ax

def main_plots():
    df = pd.read_json('equipmentData.json')
    scatter_plot(df)
    plt.show()
    bar_plot(df)
    plt.show()
    violin_plot(df)
    plt.show()

if __name__ == '__main__':
    main_plots()