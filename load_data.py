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
    
    indf['country'] = indf['country'].map({k: i for (i, k)
                                          in enumerate(COUNTRIES)})
    indf.loc[:, 'country'][indf['country'].isnull()] = -1
    indf['country'] = indf['country'].astype(int)

    indf = indf.drop(labels=['payment_account', 'address'], 
                     axis=1)
    return indf

def load_data(do_plots=False):
    train_df = pd.read_csv('train.csv.gz', compression='gzip')
    test_df = pd.read_csv('test.csv.gz', compression='gzip')
    submit_df = pd.read_csv('sampleSubmission.csv.gz', compression='gzip')
    bid_df = pd.read_csv('bid_reduced.csv.gz', compression='gzip')

    train_df = train_df.merge(bid_df, on='bidder_id', how='inner')
    test_df = test_df.merge(bid_df, on='bidder_id', how='inner')
    
    train_df = clean_data(train_df)
    test_df = clean_data(test_df)
    
    if do_plots:
        from plot_data import plot_data
        plot_data(train_df, prefix='html_train')
        plot_data(test_df, prefix='html_test')

    print train_df.dtypes
    print test_df.dtypes
    print submit_df.dtypes

    xtrain = train_df.drop(labels=['outcome','bidder_id'], axis=1).values
    ytrain = train_df['outcome'].values
    xtest = test_df.drop(labels=['bidder_id'], axis=1).values
    ytest = submit_df
    y_id = list(test_df['bidder_id'])

    return xtrain, ytrain, xtest, ytest, y_id

if __name__ == '__main__':
    xtrain, ytrain, xtest, ytest, y_id = load_data(do_plots=False)

    print [x.shape for x in (xtrain, ytrain, xtest, ytest)]
