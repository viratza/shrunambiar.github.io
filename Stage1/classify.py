def shuffle_in_unison(a, b):
    assert len(a) == len(b)
    shuffled_a = np.empty(a.shape, dtype=a.dtype)
    shuffled_b = np.empty(b.shape, dtype=b.dtype)
    permutation = np.random.permutation(len(a))
    for old_index, new_index in enumerate(permutation):
        shuffled_a[new_index] = a[old_index]
        shuffled_b[new_index] = b[old_index]
    return shuffled_a, shuffled_b


# Logistic Regression
from sklearn import datasets
from sklearn import metrics
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn import tree

from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectFromModel
from sklearn.pipeline import Pipeline

from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import precision_score

import scipy
import pandas as pd
import numpy as np

# dftrain = pd.read_csv('distancetoverbtrain.csv')
# dftest = pd.read_csv('distancetoverbtest.csv')

dftrain = pd.read_csv('classifier_input_train.csv')
dftest = pd.read_csv('classifier_input_test.csv')

#features = ['n-gram', 'PRE_DIST_VERB', 'POST_DIST_VERB', 'PrecedingTitle', 'PRE_DIST_FROM_THE', 'PRE_DIST_FROM_POSITION', 'NEGATIVE_FEATURE', 'POSITIVE_FEATURE', 'Surrounding_Caps','Apostrophe', 'POST_IS_PREPOSITION', 'RELATIONSHIP', 'POST_IS_SPEAK_VERB', 'PRE_IS_SPEAK_VERB', 'Distance from Dot_Comma']
features = ['n-gram', 'POST_DIST_VERB', 'PrecedingTitle', 'PRE_DIST_FROM_POSITION', 'NEGATIVE_FEATURE', 'POSITIVE_FEATURE']


data = dftrain[features].as_matrix()
target = dftrain['classtype'].as_matrix()

# data, target = shuffle_in_unison(data, target)

# X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.1)
model = DecisionTreeClassifier()

model.fit(data, target)
print(model)

expected = dftest['classtype'].as_matrix()

predicted = model.predict(dftest[features].as_matrix())

n = len(expected)

print(metrics.classification_report(expected, predicted))
print(metrics.confusion_matrix(expected, predicted))

#
# l = zip(features, model.feature_importances_)
# l.sort(key = lambda x:x[1], reverse=True)
# print l
whitelist = ['Tony Blair', 'Alan Milburn', 'Charles Kennedy', 'David Blunkett', 'George Bush', 'Gordon Brown'] # 64

whitelist = ['Tony Blair', 'Alan Milburn', 'Charles Kennedy', 'David Blunkett', 'George Bush', 'Gordon Brown',
'Michael Howard'] # 66

#whitelist = ['Tony Blair']

whitelist2 = [w + "'s" for w in whitelist]

blacklist = ['BBC']

for i in range(n):
    if predicted[i] == False and (dftest.iloc[i]['All-Words'] in whitelist or dftest.iloc[i]['All-Words'] in whitelist2):
        predicted[i] = True
    elif predicted[i] == True and dftest.iloc[i]['All-Words'] in blacklist:
        predicted[i] = False


print(metrics.classification_report(expected, predicted))
print(metrics.confusion_matrix(expected, predicted))

extracted_entities = []

for i in range(n):
    if predicted[i] == True:
        extracted_entities.append(dftest.iloc[i]['All-Words'])

f = open("extracted_entities.txt", "w")
for ele in extracted_entities:
    f.write(ele)
    f.write("\n")

f.close()

