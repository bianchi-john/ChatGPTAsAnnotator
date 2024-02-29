#Note: The openai-python library support for Azure OpenAI is in preview.
      #Note: This code sample requires OpenAI Python library version 1.0.0 or higher.
import os
from openai import AzureOpenAI
import json
from dotenv import load_dotenv
load_dotenv()


client = AzureOpenAI(
  azure_endpoint = "https://chatgpt4asannotator.openai.azure.com/openai/deployments/ChatGPT4AsAnnotator/chat/completions?api-version=2024-02-15-preview", 
  api_key = os.getenv("AZURE_OPENAI_KEY"),
  api_version="2024-02-15-preview",
)

messages = [
                {
                  "role": "system",
                  "content": "Use the following step-by-step instructions to respond to user inputs./nStep 1 - The user will provide text delimited with XML tags/nStep 2 -  Given the following questions (delimited by triple quotes), answer them./n'''/nQ1 : What items are in Sara's house? Check all that apply./n   1. A table/n 2. A keychain /n 3. A pen /n 4. A book /n Q2 What is Sara's last name? Check one. /n 1. White, /n 2. Red, /n 3. Black'''/nStep 3 - Output a JSON object structured where the keys represent the question Ids and the values represent the corresponding answer numbers, like: /n{/n'Q1': ['1' and or '2' and or '3'and or '4'], /n'Q2': '1' or '2' or '3'/n}"                },
                {
                  "role": "user",
                  "content": "<article>Once upon a time in a quaint little village nestled between misty mountains and whispering woods, there lived a woman named Sara Red. She was known far and wide for her gentle heart and kind spirit. Sara lived in a cozy cottage, but it was unlike any other. In her home, there was no table for dining, no fancy chairs or grandiose furniture. Instead, the cottage was adorned with simple, yet magical, things. At the center of her living room, there stood a polished wooden key ring. It was no ordinary key ring; it held the keys to Sara's deepest desires and fondest memories. Each key was a treasure, unlocking a part of her life's journey. Beside the key ring lay a slender pen, its ink never running dry. This pen was Sara's companion in weaving stories and poems that danced with the stars. It whispered secrets of the universe and dreams yet to be explored. But the most extraordinary of all was the book that lay on the windowsill, bathed in the golden glow of the setting sun. This book, with its worn pages and faded cover, was Sara's most cherished possession. It was a book of 100 tales, each a magical adventure that took her on a journey through enchanted lands and mystical realms. And so, in her humble abode, Sara Red lived a life filled with wonder and enchantment. For in her world, the absence of a table was a blessing, as it allowed her to live amidst the magic of her key ring, pen, and book, where fairy tales came to life and dreams took flight. </article>"                }
            ]

completion = client.chat.completions.create(
  model="ChatGPT4AsAnnotator", # model = "deployment_name"
  messages = messages,
  temperature=0.7,
  top_p=0.01,
  frequency_penalty=0,
  presence_penalty=0,
  stop=None
)

output = completion.choices[0].message

json_output = json.dumps(output.__dict__, indent=4)


# Create the 'output' directory if it doesn't exist
os.makedirs('Query/output', exist_ok=True)

# Now you can write the JSON output to a file
with open('Query/output/TestSceltaMultipla.json', 'w') as file:
    file.write(json_output)