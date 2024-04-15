import os
from openai import AzureOpenAI
import json
import pandas as pd
import datetime
from dotenv import load_dotenv  # Optional, depending on your key storage method

output_file = 'Query/output/outputChatGPT_ITA.csv'
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
    mancanti_indices = [50]
    for mancante in mancanti_indices:
        if counter == mancante:
            filepath = os.path.join(articles_dir, filename)
            if os.path.isfile(filepath) and filename.endswith(".json"):
                article_content = read_json_file(filepath)
                if article_content:
                    messages = [
                        {
                        "role": "system",
                        "content": "Utilizzare le seguenti istruzioni passo-passo per rispondere agli input dell'utente./nStep 1 - L'utente ti fornirà il testo di un articolo di giornale./nStep 2 - Rispondi alle seguenti domande (delimitate da virgolette triple) per valutare la qualità dell'articolo di giornale.''' /nQ1.1: Di che tipo di articolo stai facendo la recensione? (Scegli una categoria)/n    1.  Notizia diretta o 'hard news'/n    2.  Editoriale/opinione/n    3.  Approfondimento/inchiesta/n    4.  Satira/n    5.  Contenuto di lifestyle, necrologio, articolo tipo 'listicle' o altre notizie 'soft'/n/nQ1.2: Quanto è accurato il titolo dell'articolo nel descrivere la storia?/n    1.  In modo estremamente impreciso/n    2.  In modo piuttosto impreciso/n    3.  In modo abbastanza accurato/n    4.  Estremamente accurato/n/nQ1.3: Il titolo dell'articolo contiene uno o più di questi elementi? (Seleziona tutte le opzioni pertinenti)/n    1.  Un nome proprio/n    2.  Una domanda/n    3.  Due punti/n    4.  Una citazione/n    5.  Parole o frasi interamente in maiuscolo/n    6.  Il pronome 'questo'/n    7.  Termini generalizzanti (es. 'mai', 'sempre')/n    8.  Frasi esplicative, come 'Ecco perché...'/n    9.  Linguaggio iperbolico, emotivo o sensazionalistico/n/nQ1.3.1: Se il titolo dell'articolo contiene una citazione,la stessa citazione compare nel contenuto della storia?/n    1. No/n    2. Sì/n/nQ1.4: La parte introduttiva dell'articolo di giornale è basata su fatti?/n    1. No/n    2. Sì/n/nQ1.5 Valuta il grado di tendenziosità/bias dell'articolo di giornale:/n    1.  Estremamente tendenzioso/biased/n    2.  Alquanto tendenzioso/biased/n    3.  Non molto tendenzioso/biased/n    4.  Completamente imparziale/unbiased/n/nQ1.6 Quanto è sensazionalistico il testo dell'articolo di giornale? Valutalo con una di queste opzioni:/n    1. Estremamente sensazionalista/n    2. Alquanto sensazionalista/n    3. Tendenzialmente neutro/n    4. Completamente neutro/n    /nQ1.7: Questa storia prende di mira in modo negativo un gruppo specifico o un individuo?/n    1. No/n    2. Sì/n/nQ1.7.1: Se la risposta alla domanda 1.7 è Sì, per favore specifica il gruppo o l'individuo preso di mira in modo negativo dall'articolo (Seleziona tutte le opzioni pertinenti):/n    0. Conservatori/n    1. Liberali/n    2. Genere/n    3. LGBTQ/n    4. Immigrati/n    5. Ebrei/Giudaismo/n    6. Islam/Musulmani/n    7. Cristiani/Cristianesimo/n    8. Religione (Altro)/n    9. Razza/etnia/n    10. Reputazione (Organizzazione)/n    11. Reputazione (Persona)/n    12. Altro/n/nQ1.7.1.2: Se nella risposta per 1.7.1 hai indicato l'opzione 12 (Altro), indica a quale gruppo o individuo fai riferimeto:/n/nQ2.8: Quanto informazioni sono fornite nella firma dell'articolo?/n    1. Non vi è alcuna attribuzione a un individuo, agenzia di stampa o a un team specifico del sito/n    2. Sono fornite informazioni parziali sul nome dell'autore/n    3. Vi è il nome completo dell'autore/autori e/o il nome specifico del servizio di agenzia di stampa/n/nQ2.9.1: Puoi determinare la data dell'evento descritto nell'articolo?/n    1. No/n    2. Sì/n/nQ2.9.2:  Se la risposta a Q2.9.1 è sì (2. Sì), inserisci la data dell'evento di cui tratta l'articolo di giornale (GG/MM/AAAA):/n/nQ2.10: La storia tratta di fatti avvenuti nei 30 giorni precedenti alla data di pubblicazione dell'articolo?/n    1.  No/n    2.  Yes/n'''/nStep 3 - Genera un oggetto JSON valido strutturato in modo che le chiavi rappresentino gli ID delle domande e i valori rappresentino i numeri delle risposte corrispondenti, come:/n{/n'Q1.1': '1' o '2' o '3' o '4' o '5', /n'Q1.2': '1' o '2' o '3' o '4',/n'Q1.3': ['1' e/o '2' e/o '3' e/o '4' e/o '5' e/o '6' e/o '7' e/o '8' e/o '9'],/n'Q1.3.1': '1' o '2',/n'Q1.4': '1' o '2',/n'Q1.5': '1' o '2' o '3' o '4',/n'Q1.6': '1' o '2' o '3' o '4',/n'Q1.7': '1' o '2',/n'Q1.7.1: ['1' e/o '2' e/o '3' e/o '4' e/o '5' e/o '6' e/o '7' e/o '8' e/o '9' e/o '10' e/o '11', e/o '12'] , /n'Q1.7.1.2': 'inseriscri la risposta',/n'Q2.8': '1' o '2' o '3',/n'Q2.9.1': '1' o '2',/n'Q2.9.2': '', /n'Q2.10': '1' o '2',/n}"
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

