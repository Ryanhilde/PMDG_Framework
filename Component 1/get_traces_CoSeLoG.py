import pathlib
import pm4py
from pm4py.statistics.traces.generic.log import case_statistics
from pm4py.objects.log.exporter.xes import exporter as xes_exporter
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.objects.conversion.log import converter as log_converter
import csv

log = xes_importer.apply(str(pathlib.Path().resolve()) + "/CoSeLoG.xes")

df_log = pm4py.convert_to_dataframe(log)
df_log['concept:name'] = df_log['concept:name'] + " - " + df_log['lifecycle:transition']

trimmed_log = pm4py.filter_variants_by_coverage_percentage(df_log, 0.001)
variants_count = case_statistics.get_variant_statistics(trimmed_log)
variants_length = sorted(variants_count, key=lambda x: x['count'], reverse=True)

for i in variants_length:
    print(i)

for i in trimmed_log['concept:name'].unique():
    print(i)

variants = []
frequencies = []
abstracted_variants = []

dict_convert = {'Confirmation of receipt - complete': 'A',
                'T02 Check confirmation of receipt - complete': 'B',
                'T03 Adjust confirmation of receipt - complete': 'C',
                'T04 Determine confirmation of receipt - complete': 'D',
                'T05 Print and send confirmation of receipt - complete': 'E',
                'T06 Determine necessity of stop advice - complete': 'F',
                'T10 Determine necessity to stop indication - complete': 'G',
                'T16 Report reasons to hold request - complete': 'H',
                'T17 Check report Y to stop indication - complete': 'I',
                'T19 Determine report Y to stop indication - complete': 'J',
                'T20 Print report Y to stop indication - complete': 'K',
                'T11 Create document X request unlicensed - complete': 'L',
                'T12 Check document X request unlicensed - complete': 'M',
                'T14 Determine document X request unlicensed - complete': 'N',
                'T15 Print document X request unlicensed - complete': 'R',
                'T07-1 Draft intern advice aspect 1 - complete': 'P'}

for i in variants_length:
    variants.append(i['variant'].split(','))
    frequencies.append(i['count'])

for j in variants:
    local_list = []
    for k in j:
        local_list.append(dict_convert.get(k))
    abstracted_variants.append(local_list)

counter = 0

with open("coSeLog.csv", "w") as f:
    for row in abstracted_variants:
        f.write("> " + str(counter) + '\n')
        f.write("%s\n" % ','.join(str(col) for col in row))
        counter += 1
