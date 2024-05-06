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




def cleanAndCast(df):
    # Sostituzione delle stringhe vuote con NaN
    df.replace('', pd.NA, inplace=True)

    # Sostituzione di NaN con -1
    df = df.fillna(-1)

    ####
    # Converto le colonne numeriche in INT
    ####
    columns_to_convert = ['Q1.1', 'Q1.2', 'Q1.3.1', 'Q1.4', 'Q1.5', 'Q1.6', 'Q1.7', 'Q2.8', 'Q2.9.1', 'Q2.10']
    # Sotituisco i NaN in -1
    df[columns_to_convert] = df[columns_to_convert].fillna(-1)
    # Applico il cast
    for col in columns_to_convert:
        df[col] = df[col].astype(int)

    ####################################################################################
    # Faccio label encoder di (Q1.3, 1.7.1)
    ####################################################################################
        
    #Pulisco prima di fare label encoder di (Q1.3, 1.7.1)
    df['Q1.7.1'] = df['Q1.7.1'].apply(convert_values)
    df['Q1.3'] = df['Q1.3'].apply(convert_values)
    
    # Casto a stringa
    df['Q1.7.1']= df['Q1.7.1'].astype(str) 
    df['Q1.3']= df['Q1.3'].astype(str)


    # Label encoder
    # df['Q1.7.1']= label_encoder.fit_transform(df['Q1.7.1']) 
    # df['Q1.3']= label_encoder.fit_transform(df['Q1.3']) 




    # Elimino le colonne ridondanti
    columns_to_drop = ['Q1.7.1_-1', 'Problem', 'Q1.7.1_', 'Q1.3_-1']
    for col in columns_to_drop:
        try:
            df.drop(col, axis=1, inplace=True)
        except KeyError:
            # Ignora se la colonna non esiste nel DataFrame
            pass

    
    # Trasformo le date in oggetti datetime
    def convert_to_datetime(value):
        try:
            return pd.to_datetime(value, format='%d/%m/%Y')
        except (TypeError, ValueError):
            return pd.NaT
            
    
    def convert_column_to_datetime(column):
        return column.apply(convert_to_datetime)
    
    df['Q2.9.2'] = convert_column_to_datetime(df['Q2.9.2'])


    # I restore the result
    return(df)