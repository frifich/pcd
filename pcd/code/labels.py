# -*- coding: utf-8 -*-
"""
Created on Tue May  1 16:42:32 2018

@author: fakher
"""

from wfdb import rdann
import features 
import csv

records = ['100', '101', '102', '103', '104', '105', '106', '107', '108',
           '109', '111', '112', '113', '114', '115', '116', '117', '118', 
           '119', '121', '122', '123', '124', '200', '201', '202', '203',
           '205', '207', '208', '209', '210', '212', '213', '214', '215',
           '217', '219', '220', '221', '222', '223', '228', '230', '231',
           '232', '233', '234']


def get_label(record):
    ann = rdann('.\\data\\' + record, 'atr')
    return ann.symbol

def label_record(record):
    """ 
    writes the following label 
    ["pre_QQ", "post_QQ", "amp_QQ", 
     "pre_RR", "post_RR", "amp_RR", 
     "pre_SS", "post_SS", "amp_SS",
     "label"]
    
    with label = 1 if normal and -1 if sick
    """
    
    label_file = open('.\\labeled_data\\l_' + record + '.txt', 'w')
    fq, fr, fs = features.compute_record_features(record)
    label = get_label(record)
    writer = csv.writer(label_file)
    
    samples = min(len(label), len(fq['pre']))
    for i in range(samples):
        sick = 0
        if label[i] == 'N' :
            sick = 1
        else :
            sick = -1
        writer.writerow([fq['pre'][i], fq['post'][i], fq['amp'][i], 
                             fq['pre'][i], fq['post'][i], fq['amp'][i],
                             fq['pre'][i], fq['post'][i], fq['amp'][i],
                             sick])    
    label_file.close()

for record in records:
    label_record(record)
    
    
    
    
    

    
    
