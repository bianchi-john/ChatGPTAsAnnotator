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
                  "content": "Use the following step-by-step instructions to respond to user inputs./nStep 1 - The user will provide text delimited with XML tags/nStep 2 -  Given the following questions (delimited by triple quotes), answer them to assess the quality of the journal article./n'''/nQ1.1: What type of news article are you reviewing? (Check one): /n    1.  Straight news, or 'hard news'/n    2.  Editorial/opinion/n    3.  Feature/investigation/n    4.  Satire/n    5.  Lifestyle content, obituary, 'listicle', or other 'soft news'/nQ1.2: How accurately does the story’s headline describe the content of the story? /n    1.  Extremely inaccurately/n    2.  Somewhat inaccurately/n    3.  Somewhat accurately/n    4.  Extremely accurately /n/nQ1.3: Does the story’s headline contain any of the following elements? Check all that apply./n    1.  A proper noun/n    2.  A question/n    3.  A colon/n    4.  A quotation/n    5.  Words or phrases that are entirely capitalized (all caps)/n    6.  The pronoun 'this'/n    7.  Generalizing terms (ex: 'never', 'always')/n    8.  Explanation phrases, such as 'Here’s why...'/n    9.  Hyperbolic, emotional or sensationalized language/nQ1.3.1: If the headline contains a quotation, does that same quotation appear in the content of the story?/n    1.  No/n    2.  Yes/nQ1.4: Does the article begin with a fact-based lead? */n    1.  No/n    2.  Yes/nQ1.5 Please rate the degree of bias in the article copy: */n    1.  Extremely biased/n    2.  Mostly biased/n    3.  Somewhat biased/n    4.  Entirely unbiased/n/nQ1.6 Does the article use sensationalised language: */n    1.  Extremely sensationalised/n    2.  Somewhat sensationalised/n    3.  Mainly neutral/n    4.  Entirely neutral/nPlease explain; you may copy and paste text from the article to substantiate your answer: /nQ1.7: Does this story negatively target a specific group or individual? */n    1.  No/n    2.  Yes/nQ1.7.1: If the answer Q1.7 is yes, please specify the group or individual negatively target/n/nQ2.8: How much information is provided in the article’s byline? /n    1.  There is no attribution to any individual, newswire, or specific team of the site/n    2.  There is partial information given for the author’s name/n    3.  There is a full name for the author/authors and/or the specific newswire service name/nQ2.9.1: Can you determine the date of the event covered by the article? /n    1.  No/n    2.  Yes/n       Q2.9.2: If the answer to Q2.9.1 is yes, please record the date of the news event or development covered by the story. (dd-mm-yyyy)/n/nQ2.10: Is the story covering a news event or development that occurred within 30 days prior to the article’s publication date? /n    1.  No/n    2.  Yes/n'''/nStep 3 - Output a JSON object structured where the keys represent the question Ids and the values represent the corresponding answer numbers, like: /n{/n'Q1.1': '1' or '2' or '3' or '4' or '5', /n'Q1.2': '1' or '2' or '3' or '4',/n'Q1.3': '1' and or '2' and or '3' and or '4' and or '5' and or '6' and or '7' and or '8' and or '9',/n'Q1.3.1': '1' or '2',/n'Q1.4': '1' or '2',/n'Q1.5': '1' or '2' or '3' or '4',/n'Q1.6': '1' or '2' or '3' or '4',/n'Q1.7': '1' or '2',/n'Q1.7.1': 'insert response',/n'Q2.8': '1' or '2' or '3',/n'Q2.9.1': '1' or '2',/n'Q2.10': '1' or '2',/n}"
                },
                {
                  "role": "user",
                  "content": "<article> {'id': '18d71db7-f362-46fa-953e-d8353c7f7232', 'meta_dataset': '', 'meta_language': 'Italian', 'meta_label': 'Group 2', 'meta_title': 'Coronavirus, nuove regole: al tavolo al ristorante in pi\u00f9 di 4', 'url': 'https://www.lanuovasardegna.it/regione/2021/05/30/news/emptytag-nuove-regole-al-tavolo-in-piu-di-4-1.40335260', 'text': 'ROMA. Il numero degli italiani vaccinati cresce di giorno in giorno e presto potranno essere superati sia le misure restrittive sia i protocolli che regolamentano da oltre un anno e mezzo le attivit\u00e0 di bar, ristoranti, cinema, palestre e piscine. Con i dati in costante miglioramento - 3.300 casi, i ricoveri in terapia intensiva che si apprestano a scendere sotto i mille e le vittime che per la terza volta nel 2021 scendono sotto le cento in 24 ore (sono 83) - e la riapertura marted\u00ec dei ristoranti al chiuso in tutta Italia, l'auspicio \u00e8 messo nero su bianco nelle linee guida delle Regioni con le quali vengono introdotte alcune modifiche ai protocolli finora in vigore: non ci sar\u00e0 pi\u00f9 il limite di massimo 4 persone al tavolo al ristorante e si potr\u00e0 usufruire delle docce nelle piscine termali e nei centri benessere.\n\nNon cambia nulla, invece, per le feste relative a matrimoni, battesimi, cresime e comunioni: sia che la cerimonia si svolga in area bianca, sia - dal 15 giugno - che si celebri in zona gialla, i partecipanti dovranno avere il green pass, vale a dire il certificato di vaccinazione, di avvenuta guarigione o un tampone con esito negativo effettuato nelle 48 ore precedenti la partecipazione all'evento previsto dal decreto del 18 maggio. La precisazione \u00e8 arrivata in una nota della Conferenza delle Regioni e del ministero della Salute dopo che fonti degli enti locali avevano sostenuto che non fosse necessario. \u00abLe feste conseguenti alle cerimonie civili o religiose, anche al chiuso - scrivono Regioni e ministero - devono svolgersi nel rispetto di protocolli e linee guida\u00bb previsti dal decreto legge 33 del 2020 e \u00abcon la prescrizione che i partecipanti siano muniti di una delle certificazioni verdi di cui all'articolo 9\u00bb del decreto del 18 maggio \u00abanche in zona bianca\u00bb. L'unica novit\u00e0, dunque, sta nel fatto che da domani si potr\u00e0 tornare alle feste di matrimonio in Friuli Venezia Giulia, Molise e Sardegna, le uniche tre regioni che passeranno in zona bianca, mentre nelle altre regioni bisogner\u00e0 aspettare l'entrata in questa fascia (il 7 o il 14 maggio) oppure il 15 giugno, data in cui \u00e8 prevista dal decreto la ripartenza dell'intero settore. Con l'incremento delle vaccinazioni verranno progressivamente meno le condizioni che hanno portato alle restrizioni, sottolineano le Regioni, le quali osservano che la campagna di vaccinazione \u00absi caratterizza per adesione volontaria e offerta gratuita\u00bb. E quindi \u00abun'elevata adesione, favorita da adeguata promozione, determiner\u00e0 le condizioni immunitarie di protezione dallo sviluppo di patologia grave e d'infezione sia dei lavoratori sia degli utenti delle attivit\u00e0\u00bb regolate proprio dalle linee guida, \u00abcontribuendo ad evitare che si ripresentino le condizioni che hanno portato alle diverse restrizioni nel corso degli ultimi 15-16 mesi\u00bb.\n\nUn obiettivo che \u00e8 lo stesso indicato dal ministro della Salute Roberto Speranza: \u00abIl nostro paese sta molto meglio, la strada \u00e8 quella giusta - dice - Dobbiamo tenere alta l'attenzione ma i numeri stanno migliorando e questo \u00e8 il momento di programmare il futuro\u00bb. Le linee guida ribadiscono una serie di restrizioni. Innanzitutto, in ogni attivit\u00e0 \u00abdevono essere usati da parte dei lavoratori dispositivi di protezione delle via aeree finalizzati alla protezione del contagio e deve essere obbligatoria la frequente igienizzazione delle mani\u00bb.'}  </article>"
                }
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

# Salva la stringa JSON in un file
with open('output.json', 'w') as file:
    file.write(json_output)