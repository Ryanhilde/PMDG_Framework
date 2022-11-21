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


def compute_score(event_1, event_2):

    if event_1 == 'Accepted + Wait' or 'Accepted + Wait - Vendor' or 'Accepted + Wait - Customer' or 'Accepted + Wait - User' or 'Accepted + Wait - Implementation':
        if event_2 == 'Accepted + Waiting':
            return 1
        if event_2 == 'Accepted':
            return 2
    if event_1 == 'Accepted + In Progress' or 'Accepted + Assigned' or 'Queued + Awaiting Assignment':
        if event_2 == 'Accepted + Ongoing':
            return 1
        if event_2 == 'Accepted':
            return 2
    if event_1 == 'Completed + In Call' or 'Completed + Cancelled' or 'Completed + Resolved' or 'Completed + Closed':
        if event_2 == 'Completed':
            return 1


log = xes_importer.apply(str(pathlib.Path().resolve()) + "/bpi_challenge_2013_incidents.xes")
df_log = pm4py.convert_to_dataframe(log)
df_log['concept:name'] = df_log['concept:name'] + " + " + df_log['lifecycle:transition']
filtered_log = pm4py.filter_variants_by_coverage_percentage(df_log, 0.00014)

# iles = os.path.join("/Users/ryanhildebrant/PycharmProjects/PACE/output_for_arx_*.csv")
# files = glob.glob(files)

# df = pd.concat(map(pd.read_csv, files))
# df.to_csv('test_log.csv', index=False)

variants = {}

arx_file = pd.read_csv("K = 20.csv")

count = 0
for index in arx_file.index:
    event_list = []
    for event in range(1, 20):
        if arx_file['row_' + str(event)][index] != '*':
            if arx_file['row_' + str(event)][index] != '-':
                event_list.append(arx_file['row_' + str(event)][index])

        if event_list:
            variants[arx_file['variant'][index]] = event_list

df_log = df_log[df_log['case:concept:name'].isin(arx_file['variant'].values.tolist())]

unmatched_variants = []
score = 0
for i in arx_file['variant'].values:
    if len(df_log[df_log['case:concept:name'] == i]['concept:name'].tolist()) == len(variants[i]):
        if df_log[df_log['case:concept:name'] == i]['concept:name'].tolist() != variants[i]:

            for event_1, event_2 in zip(df_log[df_log['case:concept:name'] == i]['concept:name'].tolist(), variants[i]):
                if event_1 != event_2:
                    score += compute_score(event_1, event_2)

        df_log[df_log['case:concept:name'] == i] = df_log[df_log['case:concept:name'] == i].replace(
            df_log[df_log['case:concept:name'] == i]['concept:name'].tolist(), variants[i])

    else:
        unmatched_variants.append(i)

print(score)
