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

log = xes_importer.apply(str(pathlib.Path().resolve()) + "/Road_Traffic_Fine_Management_Process.xes")
df_log = pm4py.convert_to_dataframe(log)

writer = []

trimmed_log = pm4py.filter_variants_by_coverage_percentage(df_log, 0.000007)

variants_count = case_statistics.get_variant_statistics(trimmed_log)
variants_length = sorted(variants_count, key=lambda x: x['count'], reverse=True)

dict_convert = {'A': 'Create Fine',
                'B': 'Send Fine',
                'C': 'Insert Fine Notification',
                'D': 'Add penalty',
                'E': 'Payment',
                'F': 'Send for Credit Collection',
                'G': 'Insert Date Appeal to Prefecture',
                'H': 'Send Appeal to Prefecture',
                'I': 'Receive Result Appeal from Prefecture',
                'J': 'Notify Result Appeal to Offender',
                'K': 'Appeal to Judge',
                '-': '-',
                ',': ','}

with open('road_traffic_output.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)

variant_pairs = {}

filter_variants = trimmed_log.groupby("case:concept:name")['concept:name'].apply(lambda tags: ','.join(tags))

for i in filter_variants.unique():
    variant_pairs[i] = filter_variants.index[filter_variants == i].tolist()


for i in data:
    variants_to_arx = []
    current_variant = []
    for j in i:
        variant = ''.join(map(str, j))
        for i in variant:
            current_variant.append(dict_convert.get(i))
    cleaned_variant = [i for i in current_variant if i != '-']
    trace_id = variant_pairs.get(','.join(map(str, cleaned_variant)))

    for i in trace_id:
        trace_instance = []
        trace_instance.append(i)
        trace_instance.extend(current_variant)
        writer.append(trace_instance)


with open("road_traffic_output_for_arx.csv", "w") as f:
    f.write("variant,row_1,row_2,row_3,row_4,row_5,row_6,row_7,row_8,row_9,row_10,row_11,row_12,row_13,row_14,row_15\n")
    for trace in writer:
        f.write("%s\n" % trace)
