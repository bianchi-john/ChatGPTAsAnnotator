import os
from openai import AzureOpenAI
import json
import pandas as pd
import datetime
from dotenv import load_dotenv  # Optional, depending on your key storage method
import re



output_file = 'Query/output/'
limite = 9999999
promptNumber = 0

# Chiedo all'utente di indicare un nome per il file di output
name = input(f"Provide a name for output file (remember to include csv extension): ")
output_file = output_file + name

# Chiedo all'utente se vuole sovrascrivere il file nel caso esista già
if os.path.isfile(output_file):
    confirm = input(f"The file '{output_file}' already exists. Do you want to overwrite it? (y/n): ")
    if confirm.lower() != 'y':
        quit()

# Chiedo all'utente se vuole stabilire un limite massimo di articoli da annotare
confirm = input(f"Do you want a maximum file limit? (y/n): ")
if confirm.lower() == 'y':
    limite = input(f"Set the number: ")
    limite = int(limite)

# Chiedo all'utente con quale tipo di prompt vuole fare le domande a chatGPT
promptNumber  = input(f"Wich prompt do you want to use? (provide a number of the line \"Query/prompt/prompt.txt\"): ")

confirm = input(f"Do you want to use only one annotator articles (Manuel)? (y/n): ")
if confirm.lower() == 'y':
    # Testing with only one annotator (Manuel)
    articles_dir = "Articles/articles/ManuelOnly"

print('Starting conversation ...')

# Load environment variables if necessary (replace with your actual values)
load_dotenv()
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")

client = AzureOpenAI(
    azure_endpoint="https://chatgpt4asannotator.openai.azure.com/openai/deployments/ChatGPT4AsAnnotator/chat/completions?api-version=2024-02-15-preview",
    api_key=AZURE_OPENAI_KEY,
    api_version="2024-02-15-preview",
)

# Leggo i file json degli articoli
def read_json_file(filepath):
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading JSON file '{filepath}': {e}")
        return None

# Funzione per parsare la risposta di chatGPT e farla diventare un JSON
def parseOutput(output):
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
        # Check if ' - ' exists in the step
        if ' - ' in step:
            # Split the step into step number and value
            step_number, step_content = step.split(' - ', 1)
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


    return renamed_json

articles_dir = "Articles/articles" 

counter = 0


# Leggo il file che contiene i prompt da dara a Chatgpt
def read_phrases_file(filepath):
    try:
        with open(filepath, 'r') as file:
            phrases = [line.strip() for line in file.readlines()]
            return phrases
    except FileNotFoundError as e:
        print(f"Error reading phrases file '{filepath}': {e}")
        return []

# Esempio di utilizzo:
phrases_file_path = 'Query/prompt/prompt.txt'
phrases_list = read_phrases_file(phrases_file_path)

filenames = os.listdir(articles_dir)

while filenames:  # Continua finché ci sono ancora filenames da processare
    filename = filenames[0]  # Prendi il primo filename della lista
    filepath = os.path.join(articles_dir, filename)
    if os.path.isfile(filepath) and filename.endswith(".json"):
        article_content = read_json_file(filepath)
        if article_content:
            specific_prompt_index = int(promptNumber)  # Indice della frase desiderata
            specific_prompt = phrases_list[specific_prompt_index]
            # Rimuovi i campi 'url' e 'id'
            article_id = article_content['id']
            article_url = article_content['url']
            article_content.pop('url', None)
            article_content.pop('id', None)
            # Rinomina la chiave 'meta_title' in 'title'
            article_content['title'] = article_content.pop('meta_title')
            messages = [
                {
                    "role": "system",
                    "content": str(specific_prompt)
                },
                {
                    "role": "user",
                    "content": str(article_content)
                }
            ]
            completion = client.chat.completions.create(
                model="ChatGPT4AsAnnotator", # model = "deployment_name"
                messages = messages,
                # La tempertura è zero perché riguarda il grado di creatività dei messaggi ma i nostri output sono numeri quindi non ci serve, anzi aumentarla farebbe rischiare di far produrre un JSON non valido
                temperature=0, 
                # Maximum Length nemmeno perché i testi degli articoli variano
                # Anche questo riguarda la creatività e a noi ci serve bassa quindo la butto al minimo
                top_p=0.01,
                # frequence e presence servono per evitare le ripetizioni ma a noi non ce ne frega nulla quindi si lasciano in default a 0
                frequency_penalty=0,
                presence_penalty=0,
                # Stop Sequences non ne abbiamo bisogno perché non abbiamo una sequenza finale oltre la quale non deve generare quindi gli do "None"
                stop=None
            )
            output = completion.choices[0].message.content
            try:
                output= parseOutput(output)
                json_in_risposta = json.loads(output)
            # Se l'output non è un JSON valido allora me lo salvo in una chiave speciale oltre che a fare il dump alla fine
            except Exception as e:
                print('The output returned is malformed. I Retry with the same item')
                print(completion.choices[0].message.content)
                continue
            # Extract relevant information from response
            filenames.pop(0)  # Rimuovi il filename dalla lista dopo il successo
            counter = counter + 1
            id = article_id
            title = article_content['title']
            annotator = 'ChatGPT4AsAnnotator'  # Assuming annotator name is constant
            # Creazione del dataframe con i dati
            df = pd.DataFrame({
                'id': [id],
                'title': [title],
                'label': -1,
                'annotator': [annotator]
            })

            # Header personalizzato
            custom_header = ['id', 'title', 'label', 'annotator', 'Q1.1', 'Q1.2', 'Q1.3', 'Q1.3.1', 'Q1.4', 'Q1.5', 'Q1.6', 'Q1.7', 'Q1.7.1', 'Q1.7.1.2']

            # Aggiunta delle colonne dal dizionario JSON
            for key, value in json_in_risposta.items():
                df[key] = str(value)

            missing_columns = [col for col in custom_header if col not in df.columns]

            # Imposto i valori delle colonne mancanti a -1
            for col in missing_columns:
                df[col] = -1

            # Riorganizzo il DataFrame in base alle colonne personalizzate
            df = df.reindex(columns=custom_header)  

            if os.path.isfile(output_file):
                df.to_csv(output_file, index=False, header=False, mode='a')
            else:
                df.to_csv(output_file, index=False, mode='a', columns=custom_header)


            # Salvataggio del jsonInEntrata in un file con timestamp
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            json_in_risposta['timestamp'] = timestamp
            json_file = "Query/output/dump/dump.json"

            if os.path.isfile(json_file):
                with open(json_file, "r") as f:
                    existing_data = json.load(f)
                existing_data.append(json_in_risposta)
                with open(json_file, "w") as f:
                    json.dump(existing_data, f)
            else:
                with open(json_file, "w") as f:
                    json.dump([json_in_risposta], f)
            if (limite):               
                if (counter >= limite):
                    print('Limite raggiunto')
                    break

    print('Dati ottenuti per l\'articolo: ' + str(article_id))

