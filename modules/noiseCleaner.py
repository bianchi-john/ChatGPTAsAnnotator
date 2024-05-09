##########################################################################################################################################
##################################### CONTROLLO CHE NON CI SIANO VALORI STRANI ###########################################################
##########################################################################################################################################

import pandas as pd
import re
import numpy as np

def noiseCleaner(df):

    def Q1_1(df, column):
        condition = df['annotator'] != 'ChatGPT4AsAnnotator'
        if condition.any():  # Controlla se almeno un valore soddisfa la condizione
            df[column] = df[column].astype(str)
            df[column] = df[column].str.replace('.0', '')
            valid_values = ['1', '2', '3', '4', '5', '']
            df[column] = df[column].apply(lambda x: x if x in valid_values else print(str(column) +' \"'+  str(x)+'\"'))

    def Q1_2(df, column):
        df[column] = df[column].astype(str)
        df[column] = df[column].str.replace('.0', '')
        valid_values = ['1', '2', '3', '4', '']
        df[column] = df[column].apply(lambda x: x if x in valid_values else print(str(column) +' \"'+  str(x)+'\"'))

    def Q1_3(df, column):
        # Funzione per controllare se un valore è conforme
        def is_conform(value):
            # Versione che controlla per il formato dei dati delle annnotazioni originali
            try:
                return (value == '') or (all(1 <= int(x) <= 9 for x in value.split(';')) and all(re.match(r'^\d+$', x) for x in value.split(';')))
            except:
                # Versione che controlla per il formato dei 
                try: 
                    return (value == '') or (all(1 <= int(x) <= 9 for x in value.split(',')) and all(re.match(r'^\d+$', x) for x in value.split(',')))
                except:
                    return ('An error occured durign 1.3 value check')

        
        # Trova tutti i valori non conformi
        non_conform_values = df[df[column].apply(lambda x: not is_conform(x))][column]
        
        # Stampa i valori non conformi
        primavolta = 0
        for value in non_conform_values:
            if value != (''):
                if (primavolta == 0):
                    print("Valori non conformi in {}:".format(column))
                primavolta = 1
                print(value)

    def Q1_31(df, column):
        df[column] = df[column].astype(str)
        df[column] = df[column].str.replace('.0', '')

        valid_values = ['1', '2', '']
        df[column] = df[column].apply(lambda x: x if x in valid_values else print(str(column) +' \"'+  str(x)+'\"'))

    def Q1_4(df, column):
        df[column] = df[column].astype(str)
        df[column] = df[column].str.replace('.0', '')
        valid_values = ['1', '2', '']
        df[column] = df[column].apply(lambda x: x if x in valid_values else print(str(column) +' \"'+  str(x)+'\"'))

    def Q1_5(df, column):
        df[column] = df[column].astype(str)
        df[column] = df[column].str.replace('.0', '')
        valid_values = ['1', '2', '3', '4', '0', '']
        df[column] = df[column].apply(lambda x: x if x in valid_values else print(str(column) +' \"'+  str(x)+'\"'))

    def Q1_6(df, column):
        df[column] = df[column].astype(str)
        df[column] = df[column].str.replace('.0', '')
        valid_values = ['1', '2', '3', '4', '0', '']
        df[column] = df[column].apply(lambda x: x if x in valid_values else print(str(column) +' \"'+  str(x)+'\"'))

    def Q1_7(df, column):
        df[column] = df[column].astype(str)
        df[column] = df[column].str.replace('.0', '')
        valid_values = ['1', '2', '0', '']
        df[column] = df[column].apply(lambda x: x if x in valid_values else print(str(column) +' \"'+  str(x)+'\"'))

    def Q1_71(df, column):
        # Funzione per controllare se un valore è conforme
        def is_conform(value):
            # Converti il valore in una stringa
            value_str = str(value)
            # Dividi la stringa solo se è diversa da vuota
            return (value_str == '') or (all(0 <= int(x) <= 12 for x in value_str.split(';') if x.isdigit()))

        # Trova tutti i valori non conformi
        non_conform_values = df[df[column].apply(lambda x: not is_conform(x))][column]

        # Stampa i valori non conformi
        primavolta = 0
        for value in non_conform_values:
            if value != (''):
                if (primavolta == 0):
                    print("Valori non conformi in {}:".format(column))
                primavolta = 1
                print(value)

            

    Q1_1(df, 'Q1.1')

    Q1_2(df, 'Q1.2')

    Q1_3(df, 'Q1.3')

    Q1_31(df, 'Q1.3.1')

    Q1_4(df, 'Q1.4')

    Q1_5(df, 'Q1.5')

    Q1_6(df, 'Q1.6')

    Q1_7(df, 'Q1.7')

    Q1_71(df, 'Q1.7.1')


    return ('')
