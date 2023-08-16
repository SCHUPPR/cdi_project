# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 07:48:25 2023

@author: Reece
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme()

# Data Viz and Graph Creation

# -----------------------------------------------------------------------------

# Histogram displaying distributions of the yearly change in obesity and 
# healthy weight proportions across states

from analyze import adult_healthy_df, adult_obesity_df

# fig, axs = plt.subplots(2)

# x_axis = np.arange(-0.8, 1.2, 0.2)

# axs[0].set_title("Yearly Change in Obesity")
# axs[1].set_title("Yearly Change in Healthy Weight")

# adult_obesity_df["yearly_change"].plot(ax=axs[0], kind="hist", color="red",
#                                        bins=12, xticks=x_axis)
# adult_healthy_df["yearly_change"].plot(ax=axs[1], kind="hist", color="lightgreen",
#                                        bins=9, xticks=x_axis, sharex=True)

# -----------------------------------------------------------------------------

# Line graph displaying alcohol-related trends as seen across the US. Data
# is the US average of each variable

from analyze import usa_questions_alc_df

fig, ax = plt.subplots()

usa_alc_transposed = usa_questions_alc_df.T
usa_alc_transposed = usa_alc_transposed.drop("yearly_change") 

sns.lineplot(data=usa_alc_transposed, x=usa_alc_transposed.index,
              y="Alcohol use among youth", label="Youth Alc Use", ax=ax)
sns.lineplot(data=usa_alc_transposed, x=usa_alc_transposed.index,
              y="Binge drinking prevalence among youth", label="Youth Binge Drink",
              ax=ax)
sns.lineplot(data=usa_alc_transposed, x=usa_alc_transposed.index,
              y="Binge drinking prevalence among adults aged >= 18 years", 
              label="Adult Binge Drink", ax=ax)

ax.set_ylabel("Proportion %")
ax.set_xlabel("Year")
ax.set_title("Alcohol-Related Behaviors Remain Stagnant Across the US")