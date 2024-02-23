# CHANDLER MATEKA
# Final Project - Program #2: Data Visualization

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def scatter_plot(df):
    fig, ax = plt.subplots()

    for index in range(len(df) - 1):
        if df['GE Value'].isnull()[index]:
            df = df.drop([index])
    df = df.reindex(range(len(df)))

    ax.scatter(df.index, df['GE Value'])

    return ax

def main_scatter():
    df = pd.read_json('equipmentData.json')
    scatter_plot(df)
    plt.show()

if __name__ == '__main__':
    main_scatter()