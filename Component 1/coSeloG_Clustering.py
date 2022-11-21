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

log = xes_importer.apply(str(pathlib.Path().resolve()) + "/CoSeLoG.xes")

df_log = pm4py.convert_to_dataframe(log)
df_log['concept:name'] = df_log['concept:name'] + " - " + df_log['lifecycle:transition']

trimmed_log = pm4py.filter_variants_by_coverage_percentage(df_log, 0.001)
variants_count = case_statistics.get_variant_statistics(trimmed_log)
variants_length = sorted(variants_count, key=lambda x: x['count'], reverse=True)

writer = []

dict_convert = {'A': 'Confirmation of receipt - complete',
                'B': 'T02 Check confirmation of receipt - complete',
                'C': 'T03 Adjust confirmation of receipt - complete',
                'D': 'T04 Determine confirmation of receipt - complete',
                'E': 'T05 Print and send confirmation of receipt - complete',
                'F': 'T06 Determine necessity of stop advice - complete',
                'G': 'T10 Determine necessity to stop indication - complete',
                'H': 'T16 Report reasons to hold request - complete',
                'I': 'T17 Check report Y to stop indication - complete',
                'J': 'T19 Determine report Y to stop indication - complete',
                'K': 'T20 Print report Y to stop indication - complete',
                'L': 'T11 Create document X request unlicensed - complete',
                'M': 'T12 Check document X request unlicensed - complete',
                'N': 'T14 Determine document X request unlicensed - complete',
                'R': 'T15 Print document X request unlicensed - complete',
                'P': 'T07-1 Draft intern advice aspect 1 - complete',
                '-': '-'}

with open('coSeloG_maffa.csv', newline='') as f:
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


with open("coSeloG_output_for_arx.csv", "w") as f:
    f.write("variant,row_1,row_2,row_3,row_4,row_5,row_6,row_7,row_8,row_9,row_10,row_11,row_12,row_13,row_14,row_15,"
            "row_16,row_17,row_18,row_19,row_20,row_21,row_22\n")
    for trace in writer:
        f.write("%s\n" % trace)
