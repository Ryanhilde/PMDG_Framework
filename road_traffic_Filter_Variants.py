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
    if event_1 == 'Create Fine' or 'Send Fine' or 'Insert Fine Notification':
        if event_2 == 'Fine':
            return 1
        if event_2 == 'Payment or Collection':
            return 2
    if event_1 == 'Add penalty' or 'Payment' or 'Send for Credit Collection':
        if event_2 == 'Payment':
            return 1
        if event_2 == 'Appeal':
            return 2
    if event_1 == 'Insert Date Appeal to Prefecture' or 'Send Appeal to Prefecture' or 'Receive Result Appeal from Prefecture':
        if event_2 == 'Appeal to Prefecture':
            return 1
        if event_2 == 'Appeal':
            return 2
    if event_1 == 'Notify Result Appeal to Offender' or 'Appeal to Judge':
        if event_2 == 'Appeal to Court':
            return 1
        if event_2 == 'Appeal':
            return 2

log = xes_importer.apply(str(pathlib.Path().resolve()) + "/Road_Traffic_Fine_Management_Process.xes")
df_log = pm4py.convert_to_dataframe(log)
event_log = pm4py.convert_to_event_log(df_log)
filtered_log = pm4py.filter_variants_by_coverage_percentage(event_log, 0.000007)

# iles = os.path.join("/Users/ryanhildebrant/PycharmProjects/PACE/output_for_arx_*.csv")
# files = glob.glob(files)

# df = pd.concat(map(pd.read_csv, files))
# df.to_csv('test_log.csv', index=False)

variants = {}

arx_file = pd.read_csv("road traffic msa k = 5.csv")

count = 0
for index in arx_file.index:
    event_list = []
    for event in range(1, 16):

        if arx_file['row_' + str(event)][index] != '*':
            if arx_file['row_' + str(event)][index] != '-':
                event_list.append(arx_file['row_' + str(event)][index])
        if event_list:
            variants[arx_file['variant'][index]] = event_list

df_log = df_log[df_log['case:concept:name'].isin(arx_file['variant'].values.tolist())]


unmatched_variants = []
score = 0


for i in arx_file['variant'].values:
    print(df_log[df_log['case:concept:name'] == i]['concept:name'].tolist())
    print(variants[i])
    print('\n')
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
