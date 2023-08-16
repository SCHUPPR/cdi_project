# -*- coding: utf-8 -*-
"""
Created on Sat Aug 12 11:37:43 2023

@author: Reece
"""

import pandas as pd
import numpy as np
from load_data import raw_df
import functions as cdi

pd.set_option('display.max_columns', None)


# Loading the raw dataframe

raw_df = raw_df

# Exploratory Analysis 

# ----------------------------------------------------------------------------

# Examining weight and nutrition data

topics = cdi.get_topics(raw_df)
topic_weight = "Nutrition, Physical Activity, and Weight Status"

# Creating the topic pivot df for question-slice creation
weight_nutrition_df = cdi.get_topic_pivot(topic_weight)

# Getting questions in which to create slices of
questions_weight = cdi.get_topic_questions(topic_weight)

# Creating the adult obesity pivot slice df
question_obesity = "Obesity among adults aged >= 18 years"
adult_obesity_df = cdi.get_topic_pivot_slice(weight_nutrition_df, question_obesity)
adult_obesity_df = cdi.drop_pivot_nans(adult_obesity_df)
adult_obesity_df = cdi.get_yearly_change(adult_obesity_df)

yearly_obesity_rate_changes = list(adult_obesity_df["yearly_change"])
mean_year_obesity_change = adult_obesity_df["yearly_change"].mean()

# Calculating the mean obesity rate in the US for each year

obesity_years = [col for col in adult_obesity_df.columns if col != "yearly_change"]
mean_yearly_obesity_rate_us = dict(zip(obesity_years, [None] * len(obesity_years)))
for col in adult_obesity_df:
    if col != "yearly_change":
        mean_yearly_obesity_rate_us[col] = adult_obesity_df[col].mean()

# print(mean_yearly_obesity_rate_us)

# Creating the adult healthy weight pivot slice
question_healthy = "Healthy weight among adults aged >= 18 years"
adult_healthy_df = cdi.get_topic_pivot_slice(weight_nutrition_df, question_healthy)
adult_healthy_df = cdi.drop_pivot_nans(adult_healthy_df)
adult_healthy_df = cdi.get_yearly_change(adult_healthy_df)

healthy_years = [col for col in adult_healthy_df.columns if col != "yearly_change"]
mean_yearly_healthy_rate_us = dict(zip(healthy_years, [None] * len(healthy_years)))
for col in adult_healthy_df:
    if col != "yearly_change":
        mean_yearly_healthy_rate_us[col] = adult_healthy_df[col].mean()

# print(mean_yearly_healthy_rate_us)

# -----------------------------------------------------------------------------

# Examing alcohol-related trends

topic_alcohol = "Alcohol"

# Creating the topic pivot df for question-slice creation
alcohol_df = cdi.get_topic_pivot(topic_alcohol)

questions_alcohol = cdi.get_topic_questions(topic_alcohol)
# 'Alcohol use among youth'
# 'Binge drinking prevalence among youth'
# 'Binge drinking prevalence among adults aged >= 18 years'


usa_alcohol_df = cdi.get_usa_yearly_overall(alcohol_df)
usa_alcohol_df = cdi.drop_pivot_nans(usa_alcohol_df)
usa_alcohol_df = cdi.get_yearly_change(usa_alcohol_df)

usa_questions_alc_df = usa_alcohol_df.loc[["Alcohol use among youth",
                                            "Binge drinking prevalence among youth",
                                            "Binge drinking prevalence among adults aged >= 18 years"]]

