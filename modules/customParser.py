import pandas as pd
import re
import numpy as np


def parse1_1(row):
    def sostituisci_1_2(stringa):
        """Sostituisce tutti gli '1' con '2' (e viceversa) nella stringa data."""
        stringa_nuova = stringa.replace("1", "2")  # Sostituisce tutti gli '1' con '2'
        stringa_nuova = stringa_nuova.replace("2", "1")  # Sostituisce tutti i '2' con '1' (opzionale)
        return stringa_nuova
    def process_block(block, yes_condition, no_condition):
        if yes_condition in block:
            return "1"
        elif no_condition in block:
            return "2"
        else:
            return "2"
    def build_output(blocks, yes_condition, no_condition):
        output = ""
        for block in blocks:
            output += process_block(block, yes_condition, no_condition)
        if len(output) == 1:
            output = '1' + "2222"
        return output
    if row is None or str(row) == 'nan':
        return row
    row = str(row).replace('\n', ' ')
    if "Step" in row:
        blocks = row.split("Step")[1:]
        output = build_output(blocks, "1", "2")
    else:
        blocks = row.split(".")[1:]
        output = build_output(blocks, "Yes", "No")
    if len(output) == 5:
        return sostituisci_1_2(output)
    else:
        print('There are these problems for column 1.1: ')
        print(row)
        print(output)


#######################################################################

def parse1_2(row):
    if not isinstance(row, float):
        # Cerca il pattern con regex
        match = re.search(r'Step 2.*?(\d)[\.\)]', row, re.DOTALL)
        if match:
            return int(match.group(1))
    return None
#######################################################################


def parse1_3(row):
    def process_block(block):
        try:
            answerNumber = int(re.search(r'\d+', block).group() if re.search(r'\d+', block) else None) - 1
        except:
            return ''
        if answerNumber:
            if "Yes" in block:
                return  ';' + str(answerNumber)
        return ''
    def build_output(blocks):
        output = ""
        for block in blocks:
            output += process_block(block)
        return output
    if row is None or str(row) == 'nan':
        return row
    row = str(row).replace('\n', ' ')
    if "Step" in row:
        blocks = row.split("Step")[1:]
        output = build_output(blocks)
    else:
        blocks = row.split(".")[1:]
        output = build_output(blocks, "Yes", "No")
    if len(output) > 0:
        return (output[1:] if output.startswith(';') else output)




#######################################################################


def parse1_3_1(row):
    answerNumber = ''
    if not isinstance(row, float):
        answerNumber = re.search(r'-?\d+', row).group() if re.search(r'-?\d+', row) else None
    return(answerNumber)

#######################################################################

def parse1_4(row):
    """
        This function converts the string "No" to 1 and "Yes" to 2.

        Subjects:
        response: The string to convert ("No" or "Yes").

        Returns:
        An integer: 1 if answer is "No", 2 if answer is "Yes".
    """
    if not isinstance(row, float):
        if row.upper() == "NO":
            return 1
        elif row.upper() == "YES":
            return 2
        else:
            raise ValueError(f"Non valid string for 1.4: {row}")

#######################################################################

def parse1_5(row):
    if not isinstance(row, float):
        # Cerca il pattern con regex
        pattern = re.compile(r"Step 3.*?(\d)\.?\s*[-\:\)\.]", re.DOTALL)
        match = pattern.search(row)
        if match:
            return int(match.group(1))
    return None

#######################################################################

def parse1_6(row):
    if not isinstance(row, float):
        # Cerca il pattern con regex
        pattern = re.compile(r"Step 4.*?(\d)\.?\s*[-\:\)\.]", re.DOTALL)
        match = pattern.search(row)
        if match:
            return int(match.group(1))
    return None

#######################################################################

def parse1_7(row):
    if not isinstance(row, float):
        return 1 if "No" in row else int(re.search(r'\d+', row).group())
    return row


#######################################################################

def parse1_7_1(row):
    def process_block(block):
        try:
            answerNumber = int(re.search(r'\d+', block).group() if re.search(r'\d+', block) else None) - 1
        except:
            return ''
        if answerNumber:
            if "Yes" in block:
                return  ';' + str(answerNumber)
        return ''
    def build_output(blocks):
        output = ""
        for block in blocks:
            output += process_block(block)
        return output
    if row is None or str(row) == 'nan':
        return row
    row = str(row).replace('\n', ' ')
    if "Step" in row:
        blocks = row.split("Step")[1:]
        output = build_output(blocks)
    else:
        blocks = row.split(".")[1:]
        output = build_output(blocks, "Yes", "No")
    if len(output) > 0:
        return (output[1:] if output.startswith(';') else output)

