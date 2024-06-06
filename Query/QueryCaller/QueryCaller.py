import os
from openai import AzureOpenAI
import json
import pandas as pd
import datetime
from dotenv import load_dotenv  # Optional, depending on your key storage method
import re
import os
import csv

output_file = 'Query/QueryCaller/RawOutput/'
limite = 9999999
promptNumber = 0

# I ask the user to give a name for the output file.
name = input(f"Provide a name for output file (Don't include the extension): ")
output_file = output_file + name + '.csv' 


# I ask the user if they would like to set a maximum limit of items to be annotated.
confirm = input(f"Do you want a maximum file limit? (y/n): ")
if confirm.lower() == 'y':
    limite = input(f"Set the number: ")
    limite = int(limite)

# I ask the user which prompt they want to use.
promptDf = pd.read_csv('Query/QueryCaller/PromptFile/promptFile.csv')
print('')
print (promptDf)
print('')
promptIndex = input(f"Witch promt number do you want to use? ")
row = promptDf[promptDf['Number'] == int(promptIndex)].iloc[0]
description = row['Description']
headerName = row['HeaderName']
specific_prompt = row['Query']
print('You selected the prompt described as:')
print(description)


print('Starting conversation ...')

# Load environment variables, if necessary (replace with real values).
load_dotenv()
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")

client = AzureOpenAI(
    azure_endpoint="https://chatgpt4asannotator.openai.azure.com/openai/deployments/ChatGPT4AsAnnotator/chat/completions?api-version=2024-02-15-preview",
    api_key=AZURE_OPENAI_KEY,
    api_version="2024-02-15-preview",
)

# I read the json files of the articles
def read_json_file(filepath):
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading JSON file '{filepath}': {e}")
        return None

articles_dir = "Articles/articles" 

counter = 0

# Read the CSV file and get the IDs to delete.
try:
    ids_to_remove = set()
    with open(output_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            ids_to_remove.add(row['id'])
except:
    print('No previus csv file has been found')

# Get all the files in the directory
filenames = os.listdir(articles_dir)

# I remove the files already in the csv that I indicated as output, assuming there are any (this is for possible interruptions).
filenames = [filename for filename in filenames if filename.split('.')[0] not in ids_to_remove]

while filenames:  # Continue as long as there are still filenames to process.
    filename = filenames[0]  # Get the first filename in the list
    filepath = os.path.join(articles_dir, filename)
    if os.path.isfile(filepath) and filename.endswith(".json"):
        article_content = read_json_file(filepath)
        if article_content:
            article_id = article_content['id']
            article_url = article_content['url']
            article_content.pop('url', None)
            article_content.pop('id', None)
            article_content['title'] = article_content.pop('meta_title')
            print('Sending request for: ' + str(article_id))
            messages = [
                {
                    "role": "system",
                    "content": str(specific_prompt)
                },
                {
                    # Creazione del dataframe con i dati
                    "role": "user",
                    "content": str(article_content)
                }
            ]
            completion = client.chat.completions.create(
                model="ChatGPT4AsAnnotator", # model = "deployment_name"
                messages = messages,
                 # The temperature is zero because it concerns the degree of creativity of the messages but our outputs are numbers so we don't need it, in fact increasing it would risk having an invalid JSON produced
                temperature=0, 
                # Maximum Length either because the texts of the articles vary.
                # This is also about creativity and we need it low so I'll throw it in at a minimum
                top_p=0.01,
                # frequence and presence are used to avoid repetition but we don't care so they are left to default to 0
                frequency_penalty=0,
                presence_penalty=0,
                # Stop Sequences we don't need it because we don't have an end sequence beyond which it should not generate so I give it “None”
                stop=None
            )
            output = completion.choices[0].message.content
            # Extract relevant information from response
            filenames.pop(0)   # Remove filename from the list after success.
            counter = counter + 1
            id = article_id
            title = article_content['title']
            # Creating the dataframe with the data
            df = {
                'id': [id],
            }
            # Suddividere headerName se contiene spazi
            header_parts = headerName.split()
            for part in header_parts:
                df[part] = [output]

            df = pd.DataFrame(df)

            if os.path.isfile(output_file):
                df.to_csv(output_file, index=False, header=False, mode='a')
            else:
                df.to_csv(output_file, index=False, mode='a')
            if (limite):               
                if (counter >= limite):
                    print('Limit reached')
                    break
    
    print('Data obtained for the article:' + str(article_id))
    print('-------------------------------------------------')
