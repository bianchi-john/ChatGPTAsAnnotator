# ChatGPT As Annotator

## Steps to Use the Heretics Project:

1. **Get ChatGPT Answers**:
    1.1. Run `Query/QueryCaller.py`.
    1.2. Select the prompt using `Query/QueryCaller/PromptFile/promptFile.csv`.
    1.3. Parse the answers and consolidate them into a single CSV using `Query/QueryCaller/OutputParser.py`. Ensure the output format matches the required format.

2. **Clean, Cast, and Create a Unique Dataset**:
    - Use `Code/PrepareAnnotations.ipynb` to clean, cast, and combine the answers from both ChatGPT and annotators.

3. **Run Comparison between Human Annotators**:
    - Execute `Code/Comparison.ipynb` to compare the responses of human annotators.

4. **Create an Excel File for Comparison**:
    - Utilize `Code/CreateExcel.py` to generate an Excel file for visualizing the comparison results.