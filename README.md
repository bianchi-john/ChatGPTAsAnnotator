1 - Get chatGPT answers by:
    1.1 - Running Query/QueryCaller.py
    1.2 - Select the prompt using Query/QueryCaller/PromptFile/promptFile.csv
    1.3 - Parse the answers (put into csv version) using Query/QueryCaller/OutputCleaner.py

2 - Clean, cast, and create an unique dataset with the answers of both chatGPT and annotators with Code/PrepareAnnotations.ipynb

3 - Run the comparison between human annotators by using Code/Comparison.ipynb

4 - Create an exel file to watch comparison with Code/CreateExcel.py