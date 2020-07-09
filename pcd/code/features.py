# -*- coding: utf-8 -*-
"""
Created on Tue May  1 12:46:55 2018

@author: fakher
"""

import my_pt 
import numpy as np

def compute_wave_features(wave):
    
    poses = wave[0]
    features = {
            "pre": [],
            "post": [],
            "amp": []
           }

    pre = np.array([], dtype=int)
    post = np.array([], dtype=int)
    
    # Pre and Post
    pre = np.append(pre, 0)
    post = np.append(post, poses[1] - poses[0])

    for i in range(1, len(poses)-1):
        pre = np.append(pre, poses[i] - poses[i-1])
        post = np.append(post, poses[i+1] - poses[i])
    pre[0] = pre[1]
    pre = np.append(pre, poses[-1] - poses[-2])  
    post = np.append(post, post[-1])

    features['pre'] = pre
    features['post'] = post
    features['amp'] = wave[1]    
       
    return features

def compute_record_features(record):
    q, r, s = my_pt.QRS_waves(record)
    features_Q = compute_wave_features(q)
    features_R = comp
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    features_S = compute_wave_features(s)
    
    return features_Q, features_R, features_S

 
