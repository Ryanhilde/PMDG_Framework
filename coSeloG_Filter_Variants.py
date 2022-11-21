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
    if event_1 == 'Confirmation of receipt - complete' or 'T02 Check confirmation of receipt - complete' or \
            'T03 Adjust confirmation of receipt - complete' or 'T04 Determine confirmation of receipt - complete' or \
            'T05 Print and send confirmation of receipt - complete':
        if event_2 == 'confirmation of receipt - complete':
            return 1
        if event_2 == 'confirm receipt or determine advice - complete':
            return 2
        if event_2 == '-':
            return 3

    if event_1 == 'T06 Determine necessity of stop advice - complete' or 'T10 Determine necessity to stop indication ' \
                                                                         '- complete' or \
            'T16 Report reasons to hold request - complete':
        if event_2 == 'Determine advice - complete':
            return 1
        if event_2 == 'confirm receipt or determine advice - complete':
            return 2
        if event_2 == '-':
            return 3
    if event_1 == 'T17 Check report Y to stop indication - complete' or 'T19 Determine report Y to stop indication - ' \
                                                                        'complete' or 'T20 Print report Y to stop ' \
                                                                                      'indication - complete':
        if event_2 == 'stop indication - complete':
            return 1
        if event_2 == 'document X request or stop indication - complete':
            return 2
        if event_2 == '-':
            return 3
    if event_1 == 'T11 Create document X request unlicensed - complete' or 'T12 Check document X request unlicensed - ' \
                                                                           'complete' or \
            'T14 Determine document X request unlicensed - complete' or 'T15 Print ' \
                                                                        'document X ' \
                                                                        'request ' \
                                                                        'unlicensed - ' \
                                                                        'complete':
        if event_2 == 'document X request unlicensed - complete':
            return 1
        if event_2 == 'document X request or stop indication - complete':
            return 2
        if event_2 == '-':
            return 3
    if event_1 == 'T07-1 Draft intern advice aspect 1 - complete':
        if event_2 == 'Determine advice - complete':
            return 1
        if event_2 == 'confirm receipt or determine advice - complete':
            return 2
        if event_2 == '-':
            return 3


log = xes_importer.apply(str(pathlib.Path().resolve()) + "/CoSeLoG.xes")
df_log = pm4py.convert_to_dataframe(log)
df_log['concept:name'] = df_log['concept:name'] + " - " + df_log['lifecycle:transition']
event_log = pm4py.convert_to_event_log(df_log)
trimmed_log = pm4py.filter_variants_by_coverage_percentage(df_log, 0.001)

variants = {}

arx_file = pd.read_csv("coSeloG Naive k = 20.csv")

count = 0
for index in arx_file.index:
    event_list = []
    for event in range(1, 10):

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
                    print(event_1)
                    print(event_2)
                    print('\n')
                    score += compute_score(event_1, event_2)

        df_log[df_log['case:concept:name'] == i] = df_log[df_log['case:concept:name'] == i].replace(
            df_log[df_log['case:concept:name'] == i]['concept:name'].tolist(), variants[i])

    else:
        unmatched_variants.append(i)

print(score)
