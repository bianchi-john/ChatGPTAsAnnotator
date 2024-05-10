import json
import re

output = "Step 2 - Yes\n\nStep 3 - No\n\nStep 4 - Yes\n\nStep 5 - No\n\nStep 6 - No\n\nStep 7 - 4. Extremely Accurately\n\nStep 8 - \n1. A proper noun - Yes\n2. A colon (:) - No\n3. A question - No\n4. Presence of quoted text - No\n5. Presence of at least one word written in capital letters - No\n6. The pronoun 'questo' and its derivatives - No\n7. Generalizing terms (such as 'mai', 'sempre') - No\n8. Explanation phrases, such as 'Ecco perché...' - No\n\nStep 9 - Yes\n\nStep 10 - -1. No quotation present\n\nStep 11 - Yes\n\nStep 12 - 4. Unbiased\n\nStep 13 - 4. Neutral\n\nStep 14 - No\n\nStep 15 - \n0. Political - Yes\n1. Religion - No\n2. Race/ethnicity - No\n3. Orientation - No\n4. The article negatively targets other groups or minorities - No"
#output = 'Step 2: Yes\n\nStep 3: No\n\nStep 4: Yes\n\nStep 5: No\n\nStep 6: No\n\nStep 7: 3\n\nStep 8: \n1. Yes\n2. No\n3. No\n4. No\n5. No\n6. No\n7. No\n8. No\n\nStep 9: No\n\nStep 10: -1\n\nStep 11: No\n\nStep 12: 3\n\nStep 13: 4\n\nStep 14: No\n\nStep 15:\n0. No\n1. No\n2. No\n3. No\n4. No'
# Split the output by the step delimiter
steps = output.split('Step ')[1:]

# Initialize a dictionary to store step number and values
step_values = {}

# Define the regular expressions for "yes" and "no" and -1
pattern_yes = re.compile(r'\b(?:yes)\b', re.IGNORECASE)
pattern_no = re.compile(r'\b(?:no)\b', re.IGNORECASE)
pattern_minus_one = re.compile(r'-1')

# Iterate through each step and extract step number and value
for step in steps:
    # Check if ' - ' or ':' exists in the step
    if ' - ' in step or ':' in step:
        # Split the step into step number and value
        if ' - ' in step:
            step_number, step_content = step.split(' - ', 1)
        else:
            step_number, step_content = step.split(':', 1)
        # Remove leading and trailing whitespaces
        step_content = step_content.strip()
        # Extracting answer values based on the step number
        if step_number in ['2', '3', '4', '5', '6', '9', '10', '11', '14']:
            if re.search(pattern_minus_one, step_content):
                value = -1
            elif re.search(pattern_yes, step_content):
                value = 2
            elif re.search(pattern_no, step_content):
                value = 1
            else:
                value = -1
        elif step_number == '8' or step_number == '15':
            # Extract numbers associated with "Yes" using regular expression
            value = ';'.join(re.findall(r'\b(\d+)\. Yes\b', step_content))
        elif step_number == '7' or step_number == '12' or step_number == '13':
            # Extract numbers using regular expression
            value = int(''.join(filter(str.isdigit, step_content)))
        elif step_number == '16':
            # Preserve the entire text for Step 16
            value = step_content
        else:
            # If the step number doesn't match any special case, assign the step content directly
            value = step_content
        
        # Assign the value to the step number
        # Extract only numbers from step number
        step_number = re.findall(r'\d+', step_number)[0]
        step_values[step_number] = value
    else:
        # If there's no ' - ', assume the step number is the whole string
        # Extract only numbers from step number
        step_number = re.findall(r'\d+', step.strip())[0]
        # In this case, assign the value as an empty string
        step_values[step_number] = ''



# Convert the dictionary to JSON format
output_json = json.dumps(step_values, indent=4)
output_json = json.loads(output_json)

# Verifichiamo se la chiave "16" non è presente nel dizionario
if '16' not in output_json:
    # Se non è presente, la aggiungiamo con una stringa vuota
    output_json['16'] = ''

# Definiamo le nuove chiavi
new_keys = {
    "2": "Q1.1.1",
    "3": "Q1.1.2",
    "4": "Q1.1.3",
    "5": "Q1.1.4",
    "6": "Q1.1.5",
    "7": "Q1.2",
    "8": "Q1.3",
    "9": "Q1.3.9",
    "10": "Q1.3.1",
    "11": "Q1.4",
    "12": "Q1.5",
    "13": "Q1.6",
    "14": "Q1.7",
    "15": "Q1.7.1",
    "16": "Q1.7.1.2"
}

# Creiamo un nuovo dizionario con le chiavi rinominate
renamed_data = {new_keys.get(k, k): v for k, v in output_json.items()}

# Estrai i valori delle chiavi specificate
q1_1_values = [str(renamed_data[key]) for key in renamed_data if key.startswith("Q1.1")]

# Unisci i valori con punto e virgola
q1_1_combined = ";".join(q1_1_values)

# Rimuovi le chiavi di Q1.1 dal dizionario
for key in list(renamed_data.keys()):
    if key.startswith("Q1.1"):
        del renamed_data[key]

# Aggiungi la nuova chiave Q1.1 con i valori concatenati
renamed_data["Q1.1"] = q1_1_combined


# Se il valore di Q1.3.9 è '2', aggiungi '9' alla chiave Q1.3 e rimuovi la chiave Q1.3.9
if renamed_data.get('Q1.3.9') == 2:
    # Aggiungi '9' alla chiave Q1.3
    if renamed_data.get('Q1.3') == '':
        renamed_data['Q1.3'] = '9'
    else:
        renamed_data['Q1.3'] += ';9'

# Elimina la chiave e il valore di Q1.3.9 indipendentemente dal suo valore
del renamed_data['Q1.3.9']

# Convertiamo il nuovo dizionario in JSON
renamed_json = json.dumps(renamed_data, indent=4)

print(renamed_json)
