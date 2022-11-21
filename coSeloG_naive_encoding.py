import itertools
import time

import numpy as np
import pandas as pd
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
from pm4py.filtering import *

import os
import glob

log = xes_importer.apply(str(pathlib.Path().resolve()) + "/CoSeloG.xes")
df_log = pm4py.convert_to_dataframe(log)
df_log['concept:name'] = df_log['concept:name'] + " - " + df_log['lifecycle:transition']
filtered_log = pm4py.filter_variants_by_coverage_percentage(df_log, 0.001)

variants_count = case_statistics.get_variant_statistics(filtered_log)
variants_length = sorted(variants_count, key=lambda x: x['count'], reverse=True)

max_list = []

for i in variants_length:
    variant = i['variant'].split(',')
    while len(variant) < 10:
        variant.append('-')
    for j in range(i['count']):
        max_list.append(variant)

variant_pairs = {}
filter_variants = filtered_log.groupby("case:concept:name")['concept:name'].apply(lambda tags: ','.join(tags))

for i in filter_variants.unique().tolist():
    li = list(i.split(","))
    while len(li) < 10:
        li.append('-')
    variant_pairs[str(li)] = filter_variants.index[filter_variants == i].tolist()

with open("coSeloG Naive k = 5.csv.csv", "w") as f:
    f.write("variant,row_1,row_2,row_3,row_4,row_5,row_6,row_7,row_8,row_9,row_10\n")
    for key, value in variant_pairs.items():
        for trace in value:
            f.write(str(trace) + ',')
            f.write("%s\n" % key)
