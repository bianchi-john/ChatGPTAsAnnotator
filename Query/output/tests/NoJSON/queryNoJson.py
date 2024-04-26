import os
from openai import AzureOpenAI
import json
import pandas as pd
import datetime
from dotenv import load_dotenv  # Optional, depending on your key storage method

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

specific_prompt = "Q1.1: What type of news article are you reviewing? (Check one):/n    1.  Straight news, or 'hard news'/n    2.  Editorial/opinion/n    3.  Feature/investigation/n    4.  Satire/n    5.  Lifestyle content, obituary, 'listicle', or other 'soft news'/n/nQ1.2: How accurately does the story’s headline describe the content of the story? (Check one):/n    1.  Inaccurately/n    2.  Partly inaccurately/n    3.  Partly accurately/n    4.  Accurately/n/nQ1.3: Does the story’s headline contain any of the following elements? (Check all that apply):/n    1.  A proper noun/n    2.  A question/n    3.  A colon/n    4.  A quotation/n    5.  Words or phrases that are entirely capitalized (all caps)/n    6.  The pronoun 'questo'/n    7.  Generalizing terms (ex: 'mai', 'sempre')/n    8.  Explanation phrases, such as 'Ecco perché...'/n    9.  Hyperbolic, emotional or sensationalized language/n    -1. None of them is present/n/nQ1.3.1: If the headline contains a quotation, does that same quotation appear in the content of the story? (Check one):/n    1.  No/n    2.  Yes/n    -1. No quotation present/n/nQ1.4: Does the article begin with a fact-based lead? (Check one):/n    1.  No/n    2.  Yes/n/nQ1.5 Please rate the degree of bias in the article copy (Check one):/n    1.  Biased/n    2.  Partly biased/n    3.  Partly biased/n    4.  Unbiased/n/nQ1.6 Does the article use sensationalised language? (Check one):/n    1.  Sensationalised/n    2.  Partly sensationalised/n    3.  Partly neutral/n    4.  Neutral/n/nQ1.7: Does this story negatively target a specific group or individual? (Check one):/n    1.  No/n    2.  Yes/n/nQ1.7.1: If the answer 1.7 is yes, please specify the group or individual negatively target. (Check all that apply ex: 1;2;3 or 1):/n	0.  Conservatives/n	1.  Liberals/n	2.  Gender/n	3.  LGBTQ/n	4.  Immigrants/n	5.  Jews/Judaism/n	6.  Islam/Muslims/n	7.  Christians/Christianity/n	8.  Religion (Other)/n	9.  Race/ethnicity/n	10.  Reputation (Organisation)/n	11.  Reputation (Person)/n	12.  Other/n    -1. None of them is present/n/n/nQ1.7.1.2: If answer 1.7.1 is yes, please specify who you are referring to: (Check one):/n/nQ2.8: How much information is provided in the article’s byline? (Check one)/n    1.  There is no attribution to any individual, newswire, or specific team of the site/n    2.  There is partial information given for the author’s name/n    3.  There is a full name for the author/authors and/or the specific newswire service name/n/nQ2.9.1: Can you determine the date of the event covered by the article? (Check one):/n    1.  No/n    2.  Yes/n/nQ2.9.2: If the answer to Q2.9.1 is yes (2. Yes), enter the date of the event being reported (DD/MM/YYYY):/n/nQ2.10: Is the story covering a news event or development that occurred within 30 days prior to the article’s publication date? (Check one):/n    1.  No/n    2.  Yes."

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


articles_dir = "Articles/articles" 

counter = 0

# Funzione per convertire la risposta di chatGPT in un json
def stringa_to_json(stringa):
    # Dividere la stringa in righe e rimuovere eventuali spazi bianchi in eccesso
    righe = [line.strip() for line in stringa.split('\n') if line.strip()]

    # Inizializzare un dizionario per contenere i dati
    dati = {}

    # Iterare sulle righe estrarre le chiavi e i valori
    for riga in righe:
        chiave, valore = riga.split(':')
        chiave = chiave.strip().replace(' ', ',')  # Modifica il formato della chiave
        valore = valore.split('.')[0].strip()  # Ottieni solo il numero della risposta
        dati[chiave] = valore

    # JSON risultante
    json_string = json.dumps(dati, indent=4)
    json_string = json.loads(json_string)
    return json_string

# Altro tentativo nel caso la funzione stringa_to_json dia errore
def stringa_to_json_second(stringa):
    # Dividere la stringa in righe e rimuovere eventuali spazi bianchi in eccesso
    righe = [line.strip() for line in stringa.split('\n') if line.strip()]

    # Inizializzare un dizionario per contenere i dati
    dati = {}

    # Variabile per tenere traccia della chiave corrente
    current_key = None

    # Iterare sulle righe estrarre le chiavi e i valori
    for riga in righe:
        # Se la riga inizia con "Q", allora è una nuova chiave
        if riga.startswith("Q"):
            current_key = riga.split(" ")[0].replace(':', ',')
            dati[current_key] = {}
            current_key = current_key.replace(',', '')
            current_key = current_key.replace(':', '')
        # Altrimenti, se la riga non inizia con "Q" e c'è una chiave corrente, allora è una risposta
        elif current_key:
            valore = riga.split(".")[0].strip().split()[-1]
            dati[current_key] = valore

    # JSON risultante
    json_string = json.dumps(dati, indent=4)
    json_string = json.loads(json_string)

    return json_string

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
                json_in_risposta = stringa_to_json(output)
            # Se l'output non è un JSON valido allora me lo salvo in una chiave speciale oltre che a fare il dump alla fine
            except Exception as e:
                try:
                    json_in_risposta = stringa_to_json_second(output)
                except Exception as e:
                    continue
            # Extract relevant information from response
            filenames.pop(0)  # Rimuovi il filename dalla lista dopo il successo
            counter = counter + 1

            id = article_content['id']
            title = article_content['meta_title']
            annotator = 'ChatGPT4AsAnnotator'  # Assuming annotator name is constant

            # Creazione del dataframe con i dati
            df = pd.DataFrame({
                'id': [id],
                'title': [title],
                'annotator': [annotator]
            })

            # Header personalizzato
            custom_header = [
                'id', 'title', 'annotator', 'Q1.1', 'Q1.2', 'Q1.3', 'Q1.3.1', 'Q1.4', 'Q1.5', 'Q1.6', 'Q1.7', 'Q1.7.1', 'Q1.7.1.2',
                'Q2.8', 'Q2.9.1', 'Q2.9.2', 'Q2.10', 'Problem'
            ]
            # Aggiunta delle colonne dal dizionario JSON

            for key, value in json_in_risposta.items():
                if key not in custom_header:
                    df['Problem'] = json_in_risposta
                else:
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

    print('Dati ottenuti per l\'articolo: ' + article_content['id'])

