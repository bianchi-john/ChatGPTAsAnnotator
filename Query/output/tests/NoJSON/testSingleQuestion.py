import os
from openai import AzureOpenAI
import json
from dotenv import load_dotenv  # Optional, depending on your key storage method


filename = 'aa3f5101-f028-4a4d-8491-407298431a7e.json'
specific_prompt = "Can you print all the single sentences of this articles delimeted by this caracter '§'?"


print('Starting conversation ...')
output = ''
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
filepath = os.path.join(articles_dir, filename)
if os.path.isfile(filepath) and filename.endswith(".json"):
    article_content = read_json_file(filepath)
    # Rimuovi i campi 'url' e 'id'
    article_content.pop('url', None)
    article_content.pop('id', None)
    # Rinomina la chiave 'meta_title' in 'title'
    article_content['title'] = article_content.pop('meta_title')
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

print(output)

