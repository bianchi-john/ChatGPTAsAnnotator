import os
from openai import AzureOpenAI
import json
import csv

from dotenv import load_dotenv  # Optional, depending on your key storage method

def read_json_file(filepath):
    """
    Reads a JSON file and returns its content as a dictionary.

    Args:
        filepath (str): The path to the JSON file.

    Returns:
        dict or None: The content of the JSON file as a dictionary,
                        or None if an error occurs.
    """

    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading JSON file '{filepath}': {e}")
        return None

def write_to_csv(output_file, data, header=None, append=False):
    """
    Writes data to a CSV file, handling creation and appending.

    Args:
        output_file (str): The path to the CSV file.
        data (list of lists): The data to write, where each inner list represents a row.
        header (list of str, optional): The header row to write, if provided.
        append (bool, optional): Whether to append data to the existing file (default: False).
    """

    with open(output_file, 'a' if append else 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if header and not append:  # Write header only if not appending
            writer.writerow(header)
        for row in data:
            writer.writerow(row)

originale ='```json\n{\n  "Q1.1": "1",\n  "Q1.2": "4",\n  "Q1.3": ["1"],\n  "Q1.3.1": "2",\n  "Q1.4": "2",\n  "Q1.5": "4",\n  "Q1.6": "3",\n  "Q1.7": "1",\n  "Q2.8": "3",\n  "Q2.9.1": "2",\n  "Q2.9.2": "03-07-2021",\n  "Q2.10": "2"\n}\n```'
# Rimuovi la parte originale ='
json_dict = json.loads(originale)

# Carica la stringa JSON

asd =9

# Write to CSV file, creating it if necessary or appending if it exists
if not os.path.exists('output.csv'):
    write_to_csv('output.csv', header=[
        'id', 'title', 'label', 'annotator', 'Q1.1', 'Q1.2', 'Q1.3', 'Q1.3.1', 'Q1.4', 'Q1.5', 'Q1.6', 'Q1.7', 'Q1.7.1', 'Q1.7.1.2', 'Q2.8', 'Q2.9.1', 'Q2.9.2', 'Q2.10'
    ])

# Extract relevant information from response
id = '1'
title = 'Italia Libera'
label = 'label1'
annotator = 'ChatGPT4AsAnnotator'  # Assuming annotator name is constant

# Create the CSV data
csv_data = [[id, title, label, annotator] + message]


print("Output successfully written to output.csv")
