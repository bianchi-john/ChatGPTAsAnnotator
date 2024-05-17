import json

def transform_json(input_json_str):
    # Carica il JSON da una stringa
    data = json.loads(input_json_str)
    
    # Mappa i valori "No" a "1" e "Yes" a "2"
    mapping = {"no": "1", "yes": "2"}
    transformed_values = [mapping[value.lower()] for value in data.values()]

    # Crea la nuova stringa formattata
    transformed_str = "" + ";".join(transformed_values)
    
    # Costruisci il nuovo JSON
    result = {"Q1.1": transformed_str}
    
    # Converti il risultato in una stringa JSON
    result_json_str = json.dumps(result)
    
    return result_json_str

# Esempio di utilizzo
input_json_str = '{\n"Step 2": "yes",\n"Step 3": "No",\n"Step 4": "Yes",\n"Step 5": "No",\n"Step 6": "No"\n}'
output_json_str = transform_json(input_json_str)
print(output_json_str)
