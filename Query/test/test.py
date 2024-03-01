import os
import json
import csv

outPath = 'Query/test/output/output.csv'


def read_json_file(filepath):
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading JSON file '{filepath}': {e}")
        return None

def write_to_csv(output_file, data, header=None, append=False):
    with open(output_file, 'a' if append else 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if header and not append:
            writer.writerow(header)
        for row in data:
            writer.writerow(row)

originale = '{"Q1.1": "1", "Q1.2": "4", "Q1.3": ["1"], "Q1.3.1": "2", "Q1.4": "2", "Q1.5": "4", "Q1.6": "3", "Q1.7": "2", "Q1.7.1": ["4"], "Q1.7.1.2": "migranti", "Q2.8": "3", "Q2.9.1": "2", "Q2.9.2": "03-07-2021", "Q2.10": "1"}'
json_dict = json.loads(originale)

asd = 9

id = '1'
title = 'testTitle'
label = 'label1'
annotator = 'ChatGPT4AsAnnotator'

# Crea i dati CSV
csv_data = [[id, title, label, annotator]]

# Aggiungi il dizionario JSON come riga separata
csv_data.append(list(json_dict.values()))


if not os.path.exists(outPath):
    write_to_csv(outPath, header=[
        'id', 'title', 'label', 'annotator', 'Q1.1', 'Q1.2', 'Q1.3', 'Q1.3.1', 'Q1.4', 'Q1.5', 'Q1.6', 'Q1.7', 'Q1.7.1', 'Q1.7.1.2', 'Q2.8', 'Q2.9.1', 'Q2.9.2', 'Q2.10'
    ], data='')



csv_data = [[id, title, label, annotator] + [json_dict[key] for key in json_dict]]

write_to_csv(outPath, csv_data, append=True)
print("Output successfully written to output.csv")
