import json

# Variabile JSON fornita
output = '''{
    "Step 2": "Yes",
    "Step 3": "No",
    "Step 4": "No",
    "Step 5": "No",
    "Step 6": "No",
    "Step 7": "No",
    "Step 8": "No",
    "Step 9": "No",
    "Step 10": "Yes"
}'''

# Carica la stringa JSON in un dizionario Python
data = json.loads(output)

# Crea una lista per contenere i numeri degli step con valore "Yes"
yes_steps = [step.split()[1] for step, value in data.items() if value == "Yes"]
yes_steps = [str(int(x) - 1) for x in yes_steps]

# Unisci i numeri degli step con il carattere ';'
yes_steps_str = ';'.join(yes_steps)

# Crea il risultato finale
result = f"{'Q1.3'}: {yes_steps_str}"

# Stampa il risultato
print(result)
