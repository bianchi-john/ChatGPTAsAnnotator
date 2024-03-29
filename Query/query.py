import os
from openai import AzureOpenAI
import json
import pandas as pd
import datetime
from dotenv import load_dotenv  # Optional, depending on your key storage method

output_file = 'Query/output/outputChatGPT.csv'
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
                        "content": "Use the following step-by-step instructions to respond to user inputs./nStep 1 - The user will provide you with a text of a newspaper article. /nStep 2 -  Given the following questions (delimited by triple quotes), answer them to assess the quality of the journal article.''' /nQ1.1: What type of news article are you reviewing? (Check one):/n    1.  Straight news, or 'hard news'/n    2.  Editorial/opinion/n    3.  Feature/investigation/n    4.  Satire/n    5.  Lifestyle content, obituary, 'listicle', or other 'soft news'/n/nQ1.2: How accurately does the story’s headline describe the content of the story?/n    1.  Extremely inaccurately/n    2.  Somewhat inaccurately/n    3.  Somewhat accurately/n    4.  Extremely accurately/n/nQ1.3: Does the story’s headline contain any of the following elements? (Check all that apply):/n    1.  A proper noun/n    2.  A question/n    3.  A colon/n    4.  A quotation/n    5.  Words or phrases that are entirely capitalized (all caps)/n    6.  The pronoun 'this'/n    7.  Generalizing terms (ex: 'never', 'always')/n    8.  Explanation phrases, such as 'Here’s why...'/n    9.  Hyperbolic, emotional or sensationalized language/n/nQ1.3.1: If the headline contains a quotation, does that same quotation appear in the content of the story?/n    1.  No/n    2.  Yes/n/nQ1.4: Does the article begin with a fact-based lead?/n    1.  No/n    2.  Yes/n/nQ1.5 Please rate the degree of bias in the article copy:/n    1.  Extremely biased/n    2.  Mostly biased/n    3.  Somewhat biased/n    4.  Entirely unbiased/n/nQ1.6 Does the article use sensationalised language:/n    1.  Extremely sensationalised/n    2.  Somewhat sensationalised/n    3.  Mainly neutral/n    4.  Entirely neutral/n/nQ1.7: Does this story negatively target a specific group or individual?/n    1.  No/n    2.  Yes/n/nQ1.7.1: If the answer 1.7 is yes, please specify the group or individual negatively target. (Check all that apply):/n	0.  Conservatives/n	1.  Liberals/n	2.  Gender/n	3.  LGBTQ/n	4.  Immigrants/n	5.  Jews/Judaism/n	6.  Islam/Muslims/n	7.  Christians/Christianity/n	8.  Religion (Other)/n	9.  Race/ethnicity/n	10.  Reputation (Organisation)/n	11.  Reputation (Person)/n	12.  Other/n/nQ1.7.1.2: If answer 1.7.1 is yes, please specify who you are referring to:/n/nQ2.8: How much information is provided in the article’s byline?/n    1.  There is no attribution to any individual, newswire, or specific team of the site/n    2.  There is partial information given for the author’s name/n    3.  There is a full name for the author/authors and/or the specific newswire service name/n/nQ2.9.1: Can you determine the date of the event covered by the article?/n    1.  No/n    2.  Yes/n/nQ2.9.2: If the answer to Q2.9.1 is yes (2. Yes), enter the date of the event being reported (DD/MM/YYYY):/n/nQ2.10: Is the story covering a news event or development that occurred within 30 days prior to the article’s publication date?/n    1.  No/n    2.  Yes/n'''/nStep 3 - Output a valid JSON object structured where the keys represent the question Ids and the values represent the corresponding answer numbers, like: /n{/n'Q1.1': '1' or '2' or '3' or '4' or '5', /n'Q1.2': '1' or '2' or '3' or '4',/n'Q1.3': ['1' and or '2' and or '3' and or '4' and or '5' and or '6' and or '7' and or '8' and or '9'],/n'Q1.3.1': '1' or '2',/n'Q1.4': '1' or '2',/n'Q1.5': '1' or '2' or '3' or '4',/n'Q1.6': '1' or '2' or '3' or '4',/n'Q1.7': '1' or '2',/n'Q1.7.1: ['1' and or '2' and or '3' and or '4' and or '5' and or '6' and or '7' and or '8' and or '9' and or '10' and or '11', and or '12'] , /n'Q1.7.1.2': 'Enter the answer',/n'Q2.8': '1' or '2' or '3',/n'Q2.9.1': '1' or '2',/n'Q2.9.2': '', /n'Q2.10': '1' or '2',/n}"
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

