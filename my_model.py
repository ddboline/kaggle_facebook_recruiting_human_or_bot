#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 23:39:05 2015

@author: ddboline
"""
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier

from sklearn.cross_validation import train_test_split

from sklearn.metrics import roc_auc_score

from load_data import load_data

def test_model(model, xtrain, ytrain):
    xTrain, xTest, yTrain, yTest = train_test_split(xtrain, ytrain,
                                                    test_size=0.2)
    model.fit(xTrain, yTrain)
    
    yprob = model.predict_proba(xTest)
    
    print 'score', roc_auc_score(yTest, yprob[:,1])
    return

def prepare_submission(model, xtest, ytest, yid):
    yprob = model.predict_proba(xtest)
    print yprob.shape, ytest.shape
    for idx, row in ytest.iterrows():
        if row['bidder_id'] in yid:
            idy = yid.index(row['bidder_id'])
            ytest.loc[idx, 'prediction'] = yprob[idy, 1]
        else:
            ytest.loc[idx, 'prediction'] = 0.051167 # pure hack
    print ytest.shape
    ytest.to_csv('submission.csv', index=False)
    return

if __name__ == '__main__':
    xtrain, ytrain, xtest, ytest, yid = load_data(do_plots=False)

#    model = LogisticRegression()
#    model = RandomForestClassifier()
    model = GradientBoostingClassifier()
    
    test_model(model, xtrain, ytrain)

    model.fit(xtrain, ytrain)
    
    prepare_submission(model, xtest, ytest, yid)
