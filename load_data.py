#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 18:15:00 2015

@author: ddboline
"""
import pandas as pd

from feature_extraction import MERCHANDISE_TYPES, COUNTRIES

def clean_data(indf):
    for col in ['outcome', 'n_auctions', 'n_devices', 'n_countries', 'n_ip', 
                'n_url'] + list(MERCHANDISE_TYPES):
        if col in indf.columns:
            indf[col] = indf[col].astype(int)
    
    indf['country'] = indf['country'].map({k: i for (i, k) in enumerate(COUNTRIES)})

    indf = indf.drop(labels=['payment_account', 'address'], 
                     axis=1)
    return indf

def load_data():
    train_df = pd.read_csv('train.csv.gz', compression='gzip')
    test_df = pd.read_csv('test.csv.gz', compression='gzip')
    submit_df = pd.read_csv('sampleSubmission.csv.gz', compression='gzip')
    bid_df = pd.read_csv('bid_reduced.csv.gz', compression='gzip')

    print train_df.shape, test_df.shape
    bid_initial = list(train_df['bidder_id'])
    train_df = train_df.merge(bid_df, on='bidder_id', how='inner')
    test_df = test_df.merge(bid_df, on='bidder_id', how='inner')
    bid_final = list(train_df['bidder_id'])
    for bid in bid_initial:
        if bid not in bid_final:
            print bid
    exit(0)
    
    print train_df.shape, test_df.shape
    train_df = clean_data(train_df)
    test_df = clean_data(test_df)
    print train_df.shape, test_df.shape
#    print train_df[train_df['outcome'] == 0]['n_countries'].describe()
#    print train_df[train_df['outcome'] == 1]['n_countries'].describe()
#    print train_df[train_df['outcome'] == 0]['n_devices'].describe()
#    print train_df[train_df['outcome'] == 1]['n_devices'].describe()
#    print train_df[train_df['outcome'] == 0]['n_auctions'].describe()
#    print train_df[train_df['outcome'] == 1]['n_auctions'].describe()
#    print train_df[train_df['outcome'] == 0]['n_per_auc'].describe()
#    print train_df[train_df['outcome'] == 1]['n_per_auc'].describe()
    
    for df in train_df, test_df:
        print df.columns
        print df.shape
        print df.dtypes
        for col in df.columns:
            print col, len(df[col].unique())
    return

if __name__ == '__main__':
    load_data()
