import pandas as pd
import json
import os
import datetime

jsonInEntrata = '{"Q1.3.1": "2", "Q1.4": "2", "Q1.5": "4", "Q1.6": "3", "Q1.7": "2", "Q1.7.1": ["4"], "Q1.7.1.2": "migranti", "Q2.8": "3", "Q2.9.1": "2", "Q2.9.2": "03-07-2021", "Q2.10": "1"}'
json_dict = json.loads(jsonInEntrata)

id = '1'
title = 'testTitle'
label = 'label1'
annotator = 'ChatGPT4AsAnnotator'

# Creazione del dataframe con i dati
df = pd.DataFrame({
    'id': [id],
    'title': [title],
    'label': [label],
    'annotator': [annotator]
})

# Header personalizzato
custom_header = [
    'id', 'title', 'label', 'annotator', 'Q1.1', 'Q1.2', 'Q1.3.1', 'Q1.4', 'Q1.5', 'Q1.6', 'Q1.7', 'Q1.7.1.2',
    'Q2.8', 'Q2.9.1', 'Q2.9.2', 'Q2.10', 'Q1.3_1', 'Q1.3_2', 'Q1.3_3', 'Q1.3_4', 'Q1.3_5', 'Q1.3_6', 'Q1.3_7',
    'Q1.3_8', 'Q1.3_9', 'Q1.7.1_0', 'Q1.7.1_1', 'Q1.7.1_2', 'Q1.7.1_3', 'Q1.7.1_4', 'Q1.7.1_5', 'Q1.7.1_6',
    'Q1.7.1_7', 'Q1.7.1_8', 'Q1.7.1_9', 'Q1.7.1_10', 'Q1.7.1_11', 'Q1.7.1_12', 'Problem'
]
# Aggiunta delle colonne dal dizionario JSON

for key, value in json_dict.items():
    if key not in custom_header:
        df['Problem'] = jsonInEntrata
    else:
        df[key] = value


# Nome del file CSV 
output_file = 'Query/output/output.csv'

missing_columns = [col for col in custom_header if col not in df.columns]

# Imposto i valori delle colonne mancanti a -1
for col in missing_columns:
    df[col] = -1

# Riorganizzo il DataFrame in base alle colonne personalizzate
df = df.reindex(columns=custom_header)  

# Se il file esiste, aggiungi i dati senza l'header
if os.path.isfile(output_file):
    # Controllo se le colonne nel DataFrame non sono presenti nel dizionario JSON
    
    # Aggiungo i dati senza l'header
    df.to_csv(output_file, index=False, header=False, mode='a')
else:
    # Se il file non esiste, aggiungi i dati con l'header
    df.to_csv(output_file, index=False, mode='a', columns=custom_header)


# Salvataggio del jsonInEntrata in un file con timestamp
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
json_dict['timestamp'] = timestamp
json_file = "Query/output/dump/jsonInEntrata.json"

if os.path.isfile(json_file):
    with open(json_file, "r") as f:
        existing_data = json.load(f)
    existing_data.append(json_dict)
    with open(json_file, "w") as f:
        json.dump(existing_data, f)
else:
    with open(json_file, "w") as f:
        json.dump([json_dict], f)