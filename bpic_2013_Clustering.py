import itertools
import time

import numpy as np
from sklearn.cluster import AffinityPropagation
from sklearn.cluster import AgglomerativeClustering
import distance
import csv
import itertools
import seaborn as sns
import matplotlib.pyplot as plt
import pathlib
import pm4py
from pm4py.statistics.traces.generic.log import case_statistics
from pm4py.objects.log.exporter.xes import exporter as xes_exporter
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.objects.conversion.log import converter as log_converter

log = xes_importer.apply(str(pathlib.Path().resolve()) + "/bpi_challenge_2013_incidents.xes")
df_log = pm4py.convert_to_dataframe(log)
df_log['concept:name'] = df_log['concept:name'] + " + " + df_log['lifecycle:transition']
filtered_log = pm4py.filter_variants_by_coverage_percentage(df_log, 0.00014)

variants_count = case_statistics.get_variant_statistics(filtered_log)
variants_length = sorted(variants_count, key=lambda x: x['count'], reverse=True)

keys = []
values = []
for i in variants_length:
    keys.append(i['variant'])
    values.append(i['count'])

variants_dict = dict(zip(keys, values))

dict_convert = {'A': 'Accepted + In Progress',
                'B': 'Queued + Awaiting Assignment',
                'C': 'Accepted + Assigned',
                'D': 'Accepted + Wait',
                'E': 'Accepted + Wait - Vendor',
                'F': 'Accepted + Wait - Customer',
                'G': 'Completed + In Call',
                'H': 'Accepted + Wait - User',
                'I': 'Accepted + Wait - Implementation',
                'J': 'Completed + Cancelled',
                'K': 'Completed + Resolved',
                'L': 'Completed + Closed',
                'M': 'Unmatched + Unmatched',
                '-': '-'}

with open('test.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)

trace_variants = np.asarray(list(itertools.chain.from_iterable(data)))

for i in trace_variants:
    print(i)

lev_similarity = -1 * np.array([[distance.levenshtein(w1, w2) for w1 in trace_variants] for w2 in trace_variants])

affprop = AffinityPropagation(affinity="precomputed")
affprop.fit(lev_similarity)

variants = []

for cluster_id in np.unique(affprop.labels_):
    cluster_variants = []
    exemplar = trace_variants[affprop.cluster_centers_indices_[cluster_id]]
    exemplar_list = []
    for i in exemplar:
        exemplar_list.append(dict_convert.get(i))
    cluster = np.unique(trace_variants[np.nonzero(affprop.labels_ == cluster_id)])
    cluster_list = []
    for j in cluster:
        temp_list = []
        for k in j:
            temp_list.append(dict_convert.get(k))
        cluster_list.append(temp_list)
    for i in cluster_list:
        inter_cluster_variants = []
        for j in i:
            inter_cluster_variants.append(j)
        ''.join(map(str, inter_cluster_variants))
        cluster_variants.append(inter_cluster_variants)
    variants.append(cluster_variants)

counter = 0

filter_variants = filtered_log.groupby("case:concept:name")['concept:name'].apply(lambda tags: ','.join(tags))

variant_pairs = {}

for i in filter_variants.unique():
    variant_pairs[i] = filter_variants.index[filter_variants == i].tolist()

for i in variants:
    variants_to_arx = []
    current_variant = []
    for j in i:
        variant = ','.join(map(str, j))
        cleaned_variant = variant.replace('-,', '')

        if variants_dict.get(cleaned_variant) is None:
            cleaned_variant = cleaned_variant.replace(',-', '')
        current_variant.append(variant_pairs.get(cleaned_variant))
        variants_to_arx += int(variants_dict.get(cleaned_variant)) * [variant]

    current_variant = itertools.chain.from_iterable(current_variant)

    with open("output_for_arx_" + str(counter) + ".csv", "w") as f:
        f.write("variant,row_1,row_2,row_3,row_4,row_5,row_6,row_7,row_8,row_9,row_10,row_11,row_12,row_13,row_14,"
                "row_15,row_16,row_17,row_18,row_19\n")
        for case_id, trace in zip(current_variant, variants_to_arx):
            f.write(str(case_id) + ",")
            f.write("%s\n" % trace)
    counter += 1
