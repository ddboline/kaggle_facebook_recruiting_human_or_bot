#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 18:28:45 2015

@author: ddboline
"""
import csv
import gzip

def feature_extraction():
    with gzip.open('bids.csv.gz', 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        labels = next(csv_reader)
        print labels
        for idx, row in csv_reader:
            print idx, row
            exit(0)
    return

if __name__ == '__main__':
    feature_extraction()