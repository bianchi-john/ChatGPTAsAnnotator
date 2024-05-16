import os
from openai import AzureOpenAI
import json
import pandas as pd
import datetime
from dotenv import load_dotenv  # Optional, depending on your key storage method
import re
import os
import csv

output_file = 'Query/output/'
limite = 9999999
promptNumber = 0

# Chiedo all'utente di indicare un nome per il file di output
name = input(f"Provide a name for output file (remember to include csv extension): ")
output_file = output_file + name


# Chiedo all'utente se vuole stabilire un limite massimo di articoli da annotare
confirm = input(f"Do you want a maximum file limit? (y/n): ")
if confirm.lower() == 'y':
    limite = input(f"Set the number: ")
    limite = int(limite)

# Chiedo all'utente con quale tipo di prompt vuole fare le domande a chatGPT
promptNumber  = input(f"Wich prompt do you want to use? (provide a number of the line \"Query/prompt/prompt.txt\"): ")

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
    # Carica la stringa JSON in un dizionario Python
    data = json.loads(output)

    # Crea una lista per contenere i numeri degli step con valore "Yes"
    yes_steps = [step.split()[1] for step, value in data.items() if value == "Yes"]
    yes_steps = [str(int(x) - 1) for x in yes_steps]

    # Unisci i numeri degli step con il carattere ';'
    yes_steps_str = ';'.join(yes_steps)
    result_dict = {"Q1.7.1": yes_steps_str}
    # Convertire il risultato in JSON
    json_result = json.dumps(result_dict)

    return(json_result)


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


# Leggi il file CSV e ottieni gli ID da eliminare
try:
    ids_to_remove = set()
    with open(output_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            ids_to_remove.add(row['id'])
except:
    print('No previus csv file has been found')

# Ottieni tutti i file nella directory
filenames = os.listdir(articles_dir)

# Rimuovo i file già presenti nel csv che ho indicato come output, ammesso che ce ne siano (questo serve per le possibili interruzioni)
filenames = [filename for filename in filenames if filename.split('.')[0] not in ids_to_remove]

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
            print('Sending request for: ' + str(article_id))
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
                print (completion.choices[0].message.content)
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
                'annotator': [annotator]
            })

            # Header personalizzato
            custom_header = ['id', 'title', 'annotator','Q1.7.1']

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

            if (limite):               
                if (counter >= limite):
                    print('Limite raggiunto')
                    break
    print('Dati ottenuti per l\'articolo: ' + str(article_id))
    print('-------------------------------------------------')
