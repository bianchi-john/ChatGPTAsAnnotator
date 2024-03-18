import pandas as pd



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
    # Faccio one hot delle colonne a valore multuiplo (Q1.3, 1.7.1)
    ####################################################################################
        
    #Pulisco prima di fare one hot
    df['Q1.7.1'] = df['Q1.7.1'].apply(convert_values)
    df['Q1.3'] = df['Q1.3'].apply(convert_values)
        
    # Creiamo una nuova colonna per ciascun valore unico trovato nella colonna "Q1.3"
    listQ_1_3 = [1,2,3,4,5,6,7,8,9]
    for value in listQ_1_3:
        df[f'Q1.3_{value}'] = -1

    # Creiamo una nuova colonna per ciascun valore unico trovato nella colonna "Q1.7"
    listQ1_7_1 = [0,1,2,3,4,5,6,7,8,9,10,11,12]
    for value in listQ1_7_1:
        df[f'Q1.7.1_{value}'] = -1

    # Assegniamo 1 a ciascuna colonna appena creata se il valore corrisponde a quello nella colonna "Q1.3"
    for idx, row in df.iterrows():
        values = str(row['Q1.3']).split(';')  # Convertiamo in stringa prima di fare lo split
        for value in values:
            df.at[idx, f'Q1.3_{value}'] = 1


    # Assegniamo 1 a ciascuna colonna appena creata se il valore corrisponde a quello nella colonna "Q1.7.1"
    for idx, row in df.iterrows():
        values = str(row['Q1.7.1']).split(';')  # Convertiamo in stringa prima di fare lo split
        for value in values:
            df.at[idx, f'Q1.7.1_{value}'] = 1
    

    # Elimino le colonne ridondanti
    columns_to_drop = ['Q1.3', 'Q1.7.1', 'Q1.7.1_-1', 'Problem', 'Q1.7.1_', 'Q1.3_-1']
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


        

    # Restitusco il risultato
    return(df)