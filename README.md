# ChatGPT As Annotator

## Steps to Use the Heretics Project:

1. **Get ChatGPT Answers**:
    1.1. Run `Query/QueryCaller.py`.
    1.2. Select the prompt using `Query/QueryCaller/PromptFile/promptFile.csv`.
    1.3. Parse the answers and consolidate them into a single CSV using `Query/QueryCaller/OutputParser.py`. Ensure the output format matches the required format.

2. **Clean, Cast, and Create a Unique Dataset**:
    - Use `Code/PrepareAnnotations.ipynb` to clean, cast, and combine the answers from both ChatGPT and annotators.

3. **Run Comparison between Human Annotators**:
    - Execute `Code/Comparison.ipynb` to compare the responses of human annotators and generate a csv with comparisons.
