#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 18:28:45 2015

@author: ddboline
"""
import csv
import gzip

from collections import defaultdict

MERCHANDISE_TYPES = ('auto parts', 'books and music', 'clothing', 'computers',
                     'furniture', 'home goods', 'jewelry', 'mobile',
                     'office equipment', 'sporting goods')

COUNTRIES = ('ad', 'ae', 'af', 'ag', 'al', 'am', 'an', 'ao', 'ar', 'at', 'au',
             'aw', 'az', 'ba', 'bb', 'bd', 'be', 'bf', 'bg', 'bh', 'bi', 'bj',
             'bm', 'bn', 'bo', 'br', 'bs', 'bt', 'bw', 'by', 'bz', 'ca', 'cd',
             'cf', 'cg', 'ch', 'ci', 'cl', 'cm', 'cn', 'co', 'cr', 'cv', 'cy',
             'cz', 'de', 'dj', 'dk', 'dm', 'do', 'dz', 'ec', 'ee', 'eg', 'er',
             'es', 'et', 'eu', 'fi', 'fj', 'fo', 'fr', 'ga', 'gb', 'ge', 'gh',
             'gi', 'gl', 'gm', 'gn', 'gp', 'gq', 'gr', 'gt', 'gu', 'gy', 'hk',
             'hn', 'hr', 'ht', 'hu', 'id', 'ie', 'il', 'in', 'iq', 'ir', 'is',
             'it', 'je', 'jm', 'jo', 'jp', 'ke', 'kg', 'kh', 'kr', 'kw', 'kz',
             'la', 'lb', 'li', 'lk', 'lr', 'ls', 'lt', 'lu', 'lv', 'ly', 'ma',
             'mc', 'md', 'me', 'mg', 'mh', 'mk', 'ml', 'mm', 'mn', 'mo', 'mp',
             'mr', 'mt', 'mu', 'mv', 'mw', 'mx', 'my', 'mz', 'na', 'nc', 'ne',
             'ng', 'ni', 'nl', 'no', 'np', 'nz', 'om', 'pa', 'pe', 'pf', 'pg',
             'ph', 'pk', 'pl', 'pr', 'ps', 'pt', 'py', 'qa', 're', 'ro', 'rs',
             'ru', 'rw', 'sa', 'sb', 'sc', 'sd', 'se', 'sg', 'si', 'sk', 'sl',
             'sn', 'so', 'sr', 'sv', 'sy', 'sz', 'tc', 'td', 'tg', 'th', 'tj',
             'tl', 'tm', 'tn', 'tr', 'tt', 'tw', 'tz', 'ua', 'ug', 'uk', 'us',
             'uy', 'uz', 'vc', 've', 'vi', 'vn', 'ws', 'ye', 'za', 'zm', 'zw',
             'zz')

def feature_extraction():
    bidder_dict = defaultdict(int)
    bid_auc_dict = defaultdict(dict)
    bid_merch_dict = defaultdict(dict)
    bid_device_dict = defaultdict(set)
    bid_country_dict = defaultdict(dict)
    bid_ip_dict = defaultdict(set)
    bid_url_dict = defaultdict(set)
    with gzip.open('bids.csv.gz', 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        labels = next(csv_reader)
        for idx, row_ in enumerate(csv_reader):
            if idx % 100000 == 0:
                print 'processed %d' % idx
            row = dict(zip(labels, row_))
            bid = row['bidder_id']
            bidder_dict[bid] += 1
            if row['auction'] not in bid_auc_dict[bid]:
                bid_auc_dict[bid][row['auction']] = 0
            bid_auc_dict[bid][row['auction']] += 1
            if row['merchandise'] not in bid_merch_dict[bid]:
                bid_merch_dict[bid][row['merchandise']] = 0
            bid_merch_dict[bid][row['merchandise']] += 1
            bid_device_dict[bid].add(row['device'])
            if row['country'] not in bid_country_dict[bid]:
                bid_country_dict[bid][row['country']] = 0
            bid_country_dict[bid][row['country']] += 1
            bid_ip_dict[bid].add(row['ip'])
            bid_url_dict[bid].add(row['url'])
    labels_to_write = ['bidder_id', 'n_auctions', 'n_per_auc', 'n_devices', 
                       'country', 'n_countries', 'n_ip', 'n_url']
    for merch in MERCHANDISE_TYPES:
        labels_to_write.append(merch)
    with gzip.open('bid_reduced.csv.gz', 'w') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(labels_to_write)
        for bidder in sorted(bidder_dict.keys()):
            row_dict = {k: None for k in labels_to_write}
            row_dict['bidder_id'] = bidder
            row_dict['n_auctions'] = len(bid_auc_dict[bidder])
            row_dict['n_per_auc'] = sum(bid_auc_dict[bidder].values())\
                                    / float(len(bid_auc_dict[bidder]))
            row_dict['n_devices'] = len(bid_device_dict[bidder])
            row_dict['country'] = sorted(bid_country_dict[bidder].items(), 
                                         key=lambda x: x[1],
                                         reverse=True)[0][0]
            row_dict['n_countries'] = len(bid_country_dict[bidder])
            row_dict['n_ip'] = len(bid_ip_dict[bidder])
            row_dict['n_url'] = len(bid_url_dict[bidder])
            for merch in MERCHANDISE_TYPES:
                if merch in bid_merch_dict[bidder]:
                    row_dict[merch] = bid_merch_dict[bidder][merch]
                else:
                    row_dict[merch] = 0
            row_val = [row_dict[col] for col in labels_to_write]
            csv_writer.writerow(row_val)
    return

if __name__ == '__main__':
    feature_extraction()
