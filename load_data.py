#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 18:15:00 2015

@author: ddboline
"""
import pandas as pd

def clean_data(indf):
    return indf

def load_data():
    train_df = pd.read_csv('train.csv.gz', compression='gzip')
    test_df = pd.read_csv('test.csv.gz', compression='gzip')
    submit_df = pd.read_csv('sampleSubmission.csv.gz', compression='gzip')
    bid_df = pd.read_csv('bids.csv.gz', compression='gzip')
    
    for df in train_df, test_df, submit_df, bid_df:
        print df.columns
        print df.shape
        for col in df.columns:
            print col, len(df[col].unique())
    return

if __name__ == '__main__':
    load_data()
