import os
import numpy as np
import pandas as pd
import sys
sys.path.append('modules')
from customParser import parse1_1, parse1_2, parse1_3, parse1_4, parse1_3_1, parse1_5, parse1_6, parse1_7, parse1_7_1

output_path = 'Query/Output/'
name = input(f"Provide a name for output file (Don't include the extension): ")
output_file = output_path + name + '.csv' 

print('')
# Ask the user for the prefix that the files should have
substring = input("Enter the substring that the files should have: ")

#############################################################
#############################################################
######## Unique all individual files into one ###############
#############################################################
#############################################################

# Define the header list
header = ["id", "title", "annotator"]

# Create an empty DataFrame
df = pd.DataFrame(columns=header)

# Read the data from the CSV file
data = pd.read_csv("Annotations/Annotations.csv")

# Select the id and title columns
id_column = data["id"]
title_column = data["title"]

# Create a new DataFrame using the selected columns
df = pd.DataFrame({
    "id": id_column,
    "title": title_column
})

# Add the remaining columns (assuming they are present in the original DataFrame)
df["annotator"] = ["ChatGPT4AsAnnotator" for _ in range(len(id_column))]  # Replace with actual annotator data if available
# Drop duplicate rows based on 'id' column
df = df.drop_duplicates(subset=['id'], keep='first')



# Ottieni i nomi dei file nella directory
directory = "Articles/articles"
file_names = os.listdir(directory)
file_names = [file.split('.')[0] for file in file_names]  # Rimuovi l'estensione .json

# Filtra il dataframe rimuovendo gli articoli di cui non c'è il file
df = df[df['id'].isin(file_names)]

# Get the list of CSV files in the "RawOutput" directory
folder = "Query/QueryCaller/RawOutput/"

# Initialize an empty DataFrame to store the merged data
merged_df = df.copy()

# List of files in the folder that match the prefix entered
files_with_prefix = [file for file in os.listdir(folder) if substring in file]


# For each file found, read the content
for file in files_with_prefix:
    current_data = pd.read_csv(os.path.join(folder, file))

    # Check if the current data has an 'id' column
    if not 'id' in current_data.columns:
        print(f"Il file CSV '{file}' non contiene una colonna 'id'.")
        continue
    # Remove annotator column if exist
    if 'annotator' in current_data.columns:
        current_data = current_data.drop(columns=['annotator'])

    # Merge the current data with the merged DataFrame based on the 'id' column
    merged_df = merged_df.merge(current_data, on='id', how='left')


df = merged_df

#############################################################
#############################################################
######## Parse the results individually #####################
#############################################################
#############################################################


######################## Q1.1 ###############################

df['Q1.1'] = df['Q1.1'].apply(parse1_1)

# ######################## Q1.2 ###############################

df['Q1.2'] = df['Q1.2'].apply(parse1_2)
# remove the ".0" from the column results
df['Q1.2'] = df['Q1.2'].astype(str).apply(lambda x: x.replace('.0', '') if '.0' in x else x)


# ######################## Q1.3 ###############################

df['Q1.3'] = df['Q1.3'].apply(parse1_3)

# ######################## Q1.3.1 #############################

df['Q1.3.1'] = df['Q1.3.1'].apply(parse1_3_1)

# ######################## Q1.4 ###############################

df['Q1.4'] = df['Q1.4'].apply(parse1_4)

# ######################## Q1.5 ###############################

df['Q1.5'] = df['Q1.5'].apply(parse1_5)
# remove the ".0" from the column results
df['Q1.5'] = df['Q1.5'].astype(str).apply(lambda x: x.replace('.0', '') if '.0' in x else x)

# ######################## Q1.6 ###############################

df['Q1.6'] = df['Q1.6'].apply(parse1_6)
# remove the ".0" from the column results
df['Q1.6'] = df['Q1.6'].astype(str).apply(lambda x: x.replace('.0', '') if '.0' in x else x)

# ######################## Q1.7 ###############################

df['Q1.7'] = df['Q1.7'].apply(parse1_7)

# ######################## Q1.7.1 #############################

df['Q1.7.1'] = df['Q1.7.1'].apply(parse1_7_1)

#############################################################

# Define new column order
new_order = ["id", "title", "annotator", "Q1.1", "Q1.2", "Q1.3", "Q1.3.1", "Q1.4", "Q1.5", "Q1.6", "Q1.7", "Q1.7.1"]

# Reorder the dataframe columns
df = df[new_order]

df.to_csv(output_file, index=None)

print('')
# Print the merged DataFrame
print(df)
print(df.dtypes)

print('')
# Sostituire le stringhe vuote con NaN
df.replace('', np.nan, inplace=True)

# Calcolare il numero di righe vuote per colonna
empty_rows_per_column = df.isnull().sum()
print('Empty cell per each column: ')
print(empty_rows_per_column)
print('')
print('************')
print('DONE')
print('************')

