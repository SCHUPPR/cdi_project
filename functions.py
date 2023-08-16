# -*- coding: utf-8 -*-
"""
Created on Sat Aug 12 13:58:51 2023

@author: Reece
"""

import pandas as pd
from load_data import raw_df

# Function for processing/indexing CDI dataset

def get_topics(df=raw_df):
    """Returns a list of all 'topics' or variable categories
    Input --
        df: pandas dataframe that contains the column 'Topic'
    Output --
        topics: list, all topics within the 'Topic' column of 'df'"""
    topics = df["Topic"].unique()
    
    return topics


def get_topic_questions(topic, df=raw_df):
    """Returns a list of all 'questions' within a topic/category
    Input --
        topic: str, the topic you would like the questions from
        df: default is the raw_df, can change to any other df with 'Topic' column
    Output --
        questions: list of all 'questions' or variables within a topic"""
    dummy_df = df[df["Topic"] == topic]
    questions = dummy_df["Question"].unique()
    
    return questions


def get_crude_overall_data(topic, question, df=raw_df):
    """Returns the data from a given topic and question for all states. Data is
    not stratified by age and gender, but instead crude, not separated by any
    other variable.
    Input --
        topic: str, desired research topic
        question: str, desired question you'd like data from
        df: pandas df, default the raw_df that was loaded
    Output --
        crude_df: pandas df, dataframe of crude data of given topic and question
    """
    question = question.capitalize()
    dummy1 = df[df["Topic"] == topic]
    dummy2 = dummy1[dummy1["Question"] == question]
    crude_df = dummy2[dummy2["StratificationCategory1"] == "Overall"].reset_index(drop=True)
    
    return crude_df


def clean_crude_df(crude_df):
    """Removes unnecessary columns from a crude_df returns from the 
    'get_crude_overall_data' function.
    Input --
        crude_df: pandas df, crude_df from the above function
    Output --
        clean_crude_df: pandas df, crude_df with dropped columns"""
    keep_columns = ["YearStart", "LocationAbbr", "LocationDesc", "Topic",
                    "Question", "DataValueUnit", "DataValueType", "DataValue",
                    "GeoLocation"]
    drop_columns = [col for col in crude_df.columns if col not in keep_columns]
    clean_crude_df = crude_df.drop(columns=drop_columns)
    
    return clean_crude_df


def get_question_pivot(clean_crude_df):
    """Returns a pivot table from the 'clean_crude_df' df. The index is 
    'LocationAbbr', and the columns are variable name and years.
    Input --
        clean_crude_df: pandas df, df of a given topic and question
    Output --
        pivot_df: pandas df, pivot table with index of coutnry abbr and columns
        of each year"""
    variable = clean_crude_df.loc[0, "Question"]
    pivot_df = clean_crude_df.pivot(index="LocationAbbr", columns=["YearStart"], 
                                 values="DataValue")
    pivot_df.insert(0, "Variable", [variable] * pivot_df.shape[0])
    pivot_df.columns.name = None
    
    return pivot_df


def get_topic_pivot(topic, df=raw_df):
    """Generates a pivot table based on a given topic from the column
    'Topic'. The returned pivot df has a multindex, first order being state
    abbreviation, and second order being the questions within the provided
    topic. Columns are years of collection. The data from each year are the 
    'overall' values, not stratified by gender or race.
    Input --
        topic: str, a topic value from the column 'Topic'
        df: pandas df, default value is the raw_df
    Output --
        topic_pivot: pandas df, pivot table following the structure listed
            above."""
    dummy1 = df[df["Topic"] == topic]
    dummy2 = dummy1[dummy1["StratificationCategory1"] == "Overall"].reset_index(drop=True)
    dummy3 = dummy2[dummy2["DataValueType"] == "Crude Prevalence"]
    topic_pivot = dummy3.pivot(index=["LocationAbbr", "Question"],
                               columns=["YearStart"], values="DataValue")
    topic_pivot.columns.name = None
    
    return topic_pivot


def get_topic_pivot_slice(topic_pivot_df, question):
    """Used to slice a 'topic_pivot' df for a particular question value. This
    function replicated what 'get_question_pivot' returns, however by using
    a 'topic_pivot' df you are more versatile and can query for other questions
    from the same df.
    Input --
        topic_pivot_df: pandas df, a df generated by 'get_topic_pivot'
        question: str, a value from the 'Question' column of the desired topic
    Output --
        topic_pivot_slice: pandas df, a slice from a 'topic_pivot' df, including
            all state data from all years for a particular question value."""
    question = question.capitalize()
    topic_pivot_slice = topic_pivot_df.loc[(slice(None), question), slice(None)]
    
    return topic_pivot_slice


def drop_pivot_nans(topic_pivot_df):
    """Firstly drops columns with all NaN values, then drops all rows (states)
    with all NaN values.
    Input --
        topic_pivot_df: pandas df, a pivot df for a given question, generated from 
            either 'get_topic_pivot_slice' or 'get_question_pivot'.
    Output --
        clean_pivot: pandas df, pivot df with only rows and columns that contain
            at least one value"""
    dummy1 = topic_pivot_df.dropna(axis=1, how='all')
    clean_pivot = dummy1.dropna(axis=0, how='all')
    
    return clean_pivot


def get_yearly_change(clean_pivot_df):
    """Generates a new column, 'yearly_change', that holds the difference in 
    values from the earliest year of collection to the last. Calculated like so,
    yearly_change = latest_year - earliest_year.
    Input --
        clean_pivot_df: pandas df, a cleaned pivot table from 'drop_pivot_nans'
    Output --
        pivot_change_df: pandas df, a cleaned pivot with the newly added
            'yearly_change' column"""
    years = clean_pivot_df.columns
    min_year = years.min()
    max_year = years.max()
    clean_pivot_df = clean_pivot_df.astype('float64')
    clean_pivot_df["yearly_change"] = (clean_pivot_df[max_year] - clean_pivot_df[min_year]) / (max_year - min_year)
    
    return clean_pivot_df


def get_usa_yearly_overall(topic_pivot_df):
    """Extracts and concatenates the yearly US values for every question in a 
    particular topic. Returns a new dataframe with only US values.
    Input --
        topic_pivot_df: pandas df, 'topic_pivot_df' from 'get_topic_pivot()'
    Output --
        usa_topic_yearly: pandas df, df with US values for each question"""
    usa_topic_yearly = topic_pivot_df.loc["US"]
    return usa_topic_yearly