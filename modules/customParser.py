import pandas as pd
import re
import numpy as np


def parse1_1(row):
    if not isinstance(row, float):
        # Regular expression to match both formats
        pattern = re.compile(r"(?:Step )?(\d+)[\.\s-]*[^\d\n]*?(\d+|Yes|No)\.?")
        matches = pattern.findall(row)
        
        # Convert matches to dictionary
        step_dict = {}
        for step, answer in matches:
            step = int(step)
            # Convert "Yes" to 1 and "No" to 0
            if answer == "Yes":
                answer = 1
            elif answer == "No":
                answer = 0
            else:
                answer = int(answer)
            step_dict[step] = answer

        if len(step_dict) == 0:
            print('stringa: "' + row + '"')
        
        return convert_dict(step_dict)
    
    return ''



# Function to convert values and fill in missing ones
def convert_dict(d):
    # Replace 2 with 1 and 1 with 2
    converted = {k: (1 if v == 2 else 2) for k, v in d.items()}
    
    # Fill in missing values (2, 3, 4, 5, 6) with 1
    for key in range(2, 7):
        if key not in converted:
            converted[key] = 1
    
    # Sort values by key
    sorted_values = [str(converted[key]) for key in sorted(converted.keys())]
    result = ";".join(sorted_values)
    if (result == "1;1;1;1;1"):
        return ""
    else:
        return result


#######################################################################

def parse1_2(row):
    valid_values = ['1', '2', '3', '4', '']
    if not isinstance(row, float):
        # Cerca il pattern con regex
        match = re.search(r'Step 2.*?(\d)[\.\)]', row, re.DOTALL)
        if match:
            value = match.group(1)
            if value in valid_values:
                return value
    return ''


#######################################################################


def parse1_3(row):
    try:

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
    except Exception as e:
        print(f"Error processing row: {row}")
        print(f"Exception: {e}")
        return ('')




#######################################################################



def parse1_3_1(row):
    answerNumber = ''
    try:
        if not isinstance(row, float):
            answerNumber = re.search(r'-?\d+', row).group() if re.search(r'-?\d+', row) else None
    except Exception as e:
        print(f"Error processing row: {row}")
        print(f"Exception: {e}")
        return ('')
    return answerNumber


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
    return ''

#######################################################################

def parse1_5(row):
    if not isinstance(row, float):
        # Cerca il pattern con regex
        pattern = re.compile(r"Step 3.*?(\d)\.?\s*[-\:\)\.]", re.DOTALL)
        match = pattern.search(row)
        if match:
            return int(match.group(1))
    return ''

#######################################################################

def parse1_6(row):
    if not isinstance(row, float):
        # Cerca il pattern con regex
        pattern = re.compile(r"Step 4.*?(\d)\.?\s*[-\:\)\.]", re.DOTALL)
        match = pattern.search(row)
        if match:
            return int(match.group(1))
    return ''

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

