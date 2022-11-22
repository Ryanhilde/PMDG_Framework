import pathlib

import pm4py
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.algo.transformation.log_to_features import algorithm as log_to_features
from pm4py.objects.log.util import get_class_representation
from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn import metrics
import warnings

warnings.filterwarnings('ignore')  # "error", "ignore", "always", "default", "module" or "once"

#original_log = xes_importer.apply(str(pathlib.Path().resolve()) + "\\Event Logs\\bpi_challenge_2013_incidents.xes")
#df_log = pm4py.convert_to_dataframe(original_log)

#df_log['concept:name'] = df_log['concept:name'] + ' - ' + df_log['lifecycle:transition']
#log = pm4py.filter_variants_by_coverage_percentage(original_log, 0.00014)
# log = xes_importer.apply(str(pathlib.Path().resolve()) + "\\Final Organization Country\\final_organization_country_log_k_20.xes")
# log = xes_importer.apply(str(pathlib.Path().resolve()) + "\\Final Resource Country\\final_resource_country_log_k_20.xes")
# log = xes_importer.apply(str(pathlib.Path().resolve()) + "\\Final Organization Involved\\final_organization_involved_log_k_20.xes")
# log = xes_importer.apply(str(pathlib.Path().resolve()) + "\\new logs\\bpic_Naive_fully_aligned_k_5.xes")

# alignment = "MSA"
attribute = "organization country"
# k = 20

# log = xes_importer.apply("C:/Users/ryanh/OneDrive - San Diego State University (SDSU.EDU)/SDSU Graduate Course Notes/Research/Papers/Code/new logs/BPIC 2013 MSA resource country/bpic_MSA_fully_aligned_k_20.xes")
log = xes_importer.apply("C:/Users/ryanh/OneDrive - San Diego State University (SDSU.EDU)/SDSU Graduate Course Notes/Research/Papers/Code/Event Logs/bpi_challenge_2013_incidents_epsilon_1.0_k2_anonymized.xes")

data, feature_names = log_to_features.apply(log, parameters={"str_ev_attr": [attribute]})
target, classes = get_class_representation.get_class_representation_by_str_ev_attr_value_value(log,
                                                                                               "lifecycle:transition")

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

# gviz = dectree_visualizer.apply(clf, feature_names, classes)
# visualizer.view(gviz)

print("precision: " + str(precision/1000))
print("recall: " + str(recall/1000))
print("F1-Score: " + str(f1_score/1000))
