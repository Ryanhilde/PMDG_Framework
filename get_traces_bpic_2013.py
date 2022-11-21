import pathlib
import pm4py
from pm4py.statistics.traces.generic.log import case_statistics
from pm4py.objects.log.exporter.xes import exporter as xes_exporter
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.objects.conversion.log import converter as log_converter
import csv

log = xes_importer.apply(str(pathlib.Path().resolve()) + "/Road_Traffic_Fine_Management_Process.xes")

df_log = pm4py.convert_to_dataframe(log)
df_log['concept:name'] = df_log['concept:name'] + " + " + df_log['lifecycle:transition']

event_log = pm4py.convert_to_event_log(df_log)

trimmed_log = pm4py.filter_variants_by_coverage_percentage(event_log, 0.00014)
variants_count = case_statistics.get_variant_statistics(trimmed_log)
variants_length = sorted(variants_count, key=lambda x: x['count'], reverse=True)

print(len(variants_length))

variants = []
frequencies = []
abstracted_variants = []

dict_convert = {'Accepted + In Progress': 'A',
                'Queued + Awaiting Assignment': 'B',
                'Accepted + Assigned': 'C',
                'Accepted + Wait': 'D',
                'Accepted + Wait - Vendor': 'E',
                'Accepted + Wait - Customer': 'F',
                'Completed + In Call': 'G',
                'Accepted + Wait - User': 'H',
                'Accepted + Wait - Implementation': 'I',
                'Completed + Cancelled': 'J',
                'Completed + Resolved': 'K',
                'Completed + Closed': 'L',
                'Unmatched + Unmatched': 'M'}

for i in variants_length:
    variants.append(i['variant'].split(','))
    frequencies.append(i['count'])

for j in variants:
    local_list = []
    for k in j:
        local_list.append(dict_convert.get(k))
    abstracted_variants.append(local_list)

counter = 0

with open("road_traffic.csv", "w") as f:
    for row in abstracted_variants:
        f.write("> " + str(counter) + '\n')
        f.write("%s\n" % ','.join(str(col) for col in row))
        counter += 1