import os
from openai import AzureOpenAI
import json
import pandas as pd
import datetime
from dotenv import load_dotenv  # Optional, depending on your key storage method

output_file = 'Query/output/outputChatGPT_SingleQ1_1.csv'
limite = 999999999

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

articles_dir = "Articles/articles"  # Update with your articles directory path
counter = 0

for filename in os.listdir(articles_dir):
    counter = counter + 1
    filepath = os.path.join(articles_dir, filename)
    if os.path.isfile(filepath) and filename.endswith(".json"):
        article_content = read_json_file(filepath)
        if article_content:
            messages = [
                {
                "role": "system",
                "content": "Use the following step-by-step instructions to respond to user inputs./nStep 1 - The user will provide you with a text of a newspaper article. /nStep 2 -  Given the following questions (delimited by triple quotes), answer them to assess the quality of the journal article.''' /nQ1.1: What type of news article are you reviewing? (Check one):/n    1.  Straight news, or 'hard news'/n    2.  Editorial/opinion/n    3.  Feature/investigation/n    4.  Satire/n    5.  Lifestyle content, obituary, 'listicle', or other 'soft news'/n'''/nStep 3 - Output a valid JSON object structured where the keys represent the question Ids and the values represent the corresponding answer numbers, like: /n{/n'Q1.1': '1' or '2' or '3' or '4' or '5', /n}"                },
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
                json_in_risposta = json.loads(output)
            # Se l'output non è un JSON valido allora me lo salvo in una chiave speciale oltre che a fare il dump alla fine
            except Exception as e:
                try:
                    # Provo a leggerlo come ho visto che di solito mi da i json formattati male
                    temp = output.replace("json", "").replace("\n", "").replace("```", "").replace(" ", "").replace("{", "{\"").replace(",", "\", \"").replace(":", "\": \"").replace("}", "\"}").replace("\"[", "[\"").replace("]\"", "\"]").replace("\"\"", "\"")
                    json_in_risposta = json.loads(temp)
                except Exception as e:
                    json_in_risposta = {"Problem": str(output)}
                    print('ChatGPT ha restituito un json non valido per l\' articolo ' + article_content['id'])
            # Extract relevant information from response
            id = article_content['id']
            title = article_content['meta_title']
            label = article_content['meta_label']
            annotator = 'ChatGPT4AsAnnotator'  # Assuming annotator name is constant

            # Creazione del dataframe con i dati
            df = pd.DataFrame({
                'id': [id],
                'title': [title],
                'label': [label],
                'annotator': [annotator]
            })

            # Header personalizzato
            custom_header = [
                'id', 'title', 'label', 'annotator', 'Q1.1', 'Q1.2', 'Q1.3', 'Q1.3.1', 'Q1.4', 'Q1.5', 'Q1.6', 'Q1.7', 'Q1.7.1', 'Q1.7.1.2',
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

            # Se il file esiste, aggiungi i dati senza l'header

            if os.path.isfile(output_file):                    
                # Aggiungo i dati senza l'header
                df.to_csv(output_file, index=False, header=False, mode='a')
            else:
                # Se il file non esiste, aggiungi i dati con l'header
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

