# -*- coding: utf-8 -*-
"""
Created on Tue May  1 13:38:27 2018

@author: fakher
"""

from sklearn import svm
import csv

records = ['100', '101', '102', '103', '104', '105', '106', '107', '108',
           '109', '111', '112', '113', '114', '115', '116', '117', '118', 
           '119', '121', '122', '123', '124', '200', '201', '202', '203',
           '205', '207', '208', '209', '210', '212', '213', '214', '215',
           '217', '219', '220', '221', '222', '223', '228', '230', '231',
           '232', '233', '234']

X = []
y = []

for record in records[:20]:
    file = open('.\\labeled_data\\l_' + record +'.txt', 'r')
    reader = csv.reader(file)
    next(reader)
    
    for row in reader:
        if row == []:
            continue
        line = [int(l) for l in row[:9]]
        X.append(line)
        y.append(row[9])
    file.close()
     
clf = svm.SVC()
clf.fit(X, y)  


file = open('.\\labeled_data\\l_' + '200' +'.txt', 'r')
reader = csv.reader(file)
next(reader)
err = 0
noerr = 0
for row in reader:
    if row == []:
        continue
    line = [int(l) for l in row[:9]]
    p = clf.predict([line])
    if int(p[0]) != int(row[9]):
        err += 1     
    else: 
        noerr += 1
file.close()
