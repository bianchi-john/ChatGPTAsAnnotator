import pandas as pd
from sklearn import preprocessing 
label_encoder = preprocessing.LabelEncoder() 



##########################################################################################################################################
####################################################### CASTO I TIPI E PULISCO ###########################################################
##########################################################################################################################################


def convert_values(value):
    if isinstance(value, str):
        # Rimuovi parentesi quadre
        value = value.strip("[]")
        # Sostituisci virgole con punti e virgola
        value = value.replace(",", ";")
        value = value.replace("'", "")
        value = value.replace(" ", "")
        value = value.replace("/n", "")
    return value


# Trasformo in one hot la 1.1 di annotatori
def oneDotOne(value):
    # Converti il valore in una stringa
    value_str = str(value)
    # Controlla se il valore è una stringa non vuota
    if value_str:
        # Controlla se ci sono le occorrenze di '1', '2', '3' nella stringa
        if '-1' in value_str:
            return value_str 
        elif '1' in value_str:
            value_str = value_str.replace("1", "2;1;1;1;1")
        elif '2' in value_str:
            value_str = value_str.replace("2", "1;2;1;1;1")
        elif '3' in value_str:
            value_str = value_str.replace("3", "1;1;2;1;1")
        elif '3' in value_str:
            value_str = value_str.replace("4", "1;1;1;2;1")
        elif '3' in value_str:
            value_str = value_str.replace("5", "1;1;2;1;2")

    return value_str


def cleanAndCast(df):
    # Sostituzione delle stringhe vuote con NaN
    df.replace('', pd.NA, inplace=True)

    # Sostituzione di NaN con -1
    df = df.fillna(-1)

    ####
    # Converto le colonne numeriche in INT
    ####
    columns_to_convert = ['Q1.2', 'Q1.3.1', 'Q1.4', 'Q1.5', 'Q1.6', 'Q1.7']
    # Sotituisco i NaN in -1
    df[columns_to_convert] = df[columns_to_convert].fillna(-1)
    # Applico il cast
    for col in columns_to_convert:
        df[col] = df[col].astype(int)

    ####################################################################################
    # Faccio label encoder di (Q1.3, 1.7.1) e trasformo in one hot la 1.1 di annotatori
    ####################################################################################
        
    #Pulisco prima di fare label encoder di (Q1.3, 1.7.1)
    df['Q1.7.1'] = df['Q1.7.1'].apply(convert_values)
    df['Q1.3'] = df['Q1.3'].apply(convert_values)
    
    # Casto a stringa
    df['Q1.7.1']= df['Q1.7.1'].astype(str) 
    df['Q1.3']= df['Q1.3'].astype(str)

    # Trasformo in one hot la 1.1 di annotatori
    condition = df['annotator'] != 'ChatGPT4AsAnnotator'
    if condition.any():  # Controlla se almeno un valore soddisfa la condizione
        df['Q1.1'] = df['Q1.1'].apply(oneDotOne)

    # Label encoder
    df['Q1.7.1']= label_encoder.fit_transform(df['Q1.7.1']) 
    df['Q1.3']= label_encoder.fit_transform(df['Q1.3']) 
    df['Q1.1']= label_encoder.fit_transform(df['Q1.1'])

    # Elimino le colonne ridondanti
    columns_to_drop = ['Q1.7.1_-1', 'Problem', 'Q1.7.1_', 'Q1.3_-1']
    for col in columns_to_drop:
        try:
            df.drop(col, axis=1, inplace=True)
        except KeyError:
            # Ignora se la colonna non esiste nel DataFrame
            pass

    # I restore the result
    return(df)