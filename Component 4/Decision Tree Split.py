import pathlib

import pm4py
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.algo.transformation.log_to_features import algorithm as log_to_features
from pm4py.objects.log.util import get_class_representation
from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn import metrics

attribute = "attribute"
log = xes_importer.apply("log.xes")

data, feature_names = log_to_features.apply(log, parameters={"str_ev_attr": [attribute]})
target, classes = get_class_representation.get_class_representation_by_str_ev_attr_value_value(log, "lifecycle:transition")

precision = 0
recall = 0
f1_score = 0

for i in range(1000):
    X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.2, random_state=i)
    clf = tree.DecisionTreeClassifier()
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    precision += metrics.precision_score(y_test, y_pred, average='weighted')
    recall += metrics.recall_score(y_test, y_pred, average='weighted')
    f1_score += metrics.f1_score(y_test, y_pred, average='weighted')

print("precision: " + str(precision/1000))
print("recall: " + str(recall/1000))
print("F1-Score: " + str(f1_score/1000))
