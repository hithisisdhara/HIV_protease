#!/usr/bin/env python
# coding: utf-8
import numpy as np
import time
import sys

f = open('PI_DataSet_6_19_expanded.txt')
for line in f:
    header = line.split("\t")
    break
f.close()

vec_start = header.index("P1")
tpv_ind = header.index('FPV')

t0 = time.time()
tpv_data = set()

name = 'PI_DataSet_6_19_PI_count_vec_210.txt'
count = 0
start = time.time()
t0 = start
f = open(name)
for line in f:
    line = line.strip().split("\t")
    vec = line[vec_start:]
    first = [line[tpv_ind]]
    gather = tuple(first + vec)
    tpv_data.add(gather)
    count += 1
    if count % 100000 == 0:
        print (count, time.time() - t0, time.time() - start)
        t0 = time.time()
print (count)

tpv_data = list(tpv_data)
print len(tpv_data)


def isfloat_or_na(num):
    try:
        a = float(num)
        return True
    except:
        if num == 'NA':
            return True
        return False


def clean_and_convert(d):
    return list(map(lambda x: [float(y) for y in x], filter(lambda x: x[0] != 'NA', d)))


clean_tpv_data = clean_and_convert(tpv_data)

del tpv_data

print len(clean_tpv_data)


def threshold_data(th, d):
    return list(map(lambda x: [1] + x[1:] if x[0] <= th else [2] + x[1:], d))


label_tpv_data = threshold_data(3.0, clean_tpv_data)

del clean_tpv_data

print len(label_tpv_data)


def num_classes(d):
    l = len(d)
    more = sum(list(map(lambda x: x[0] - 1, d)))
    p = (more * 100.0) / l
    return 100 - p, p


a, b = num_classes(label_tpv_data)
print '{0:.2f}'.format(a), '{0:.2f}'.format(b)

from sklearn.model_selection import train_test_split

size = 0.4
arr = np.asarray(label_tpv_data)
del label_tpv_data

X_train, X_test, y_train, y_test = train_test_split(arr[:, 1:], arr[:, 0], test_size=size)

del arr

print [t.shape for t in [X_train, X_test, y_train, y_test]]

from sklearn import svm
from sklearn.model_selection import cross_val_score
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import accuracy_score

model = svm.SVC(kernel='linear', C=1, verbose=3)
scores = cross_val_score(model, X_train, y_train, cv=3)
print "inhibitor:",header[tpv_ind]
print "cross val accuracy:", scores


model.fit(X_train, y_train)

preds = model.predict(X_test)
p, r, f, _ = precision_recall_fscore_support(y_test, preds, average='weighted')
a = accuracy_score(y_test, preds)
print "Test accuracy:", '{0:.6f}'.format(a)
print "Test precision:", '{0:.6f}'.format(p)
print "Test recall:", '{0:.6f}'.format(r)
print "Test f1:", '{0:.6f}'.format(f)
