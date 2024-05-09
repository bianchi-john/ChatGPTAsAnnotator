import os

def deleteNotCoerent(df, name):
    # Definisci il percorso della cartella 'Other'
    folder_path = 'Other'

    # Verifica se la cartella 'Other' esiste, altrimenti creala
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Definisci i campi di interesse
    required_fields = ['Q1.2', 'Q1.4', 'Q1.5', 'Q1.6', 'Q1.7']

    # Verifica se una, due o tre dei valori nei campi di interesse sono -1
    has_negative_one = (df[required_fields] == -1).any(axis=1)

    # Verifica se tutti i valori nei campi di interesse sono -1
    all_negative_one = (df[required_fields] == -1).all(axis=1)

    # Seleziona le righe con tutti valori -1 e quelle con almeno un valore -1
    all_negative_one_rows = df[all_negative_one]
    one_or_more_negative_one_rows = df[has_negative_one]

    # Rimuovi le righe con tutti valori -1 dalle righe con almeno un valore -1
    one_negative_one_rows = one_or_more_negative_one_rows.loc[~all_negative_one]

        # Salva le righe con tutti valori -1 in un file CSV
    if not all_negative_one_rows.empty:
        file_path_all_negative_one = os.path.join(folder_path, str(name) + '_tutti_i_valori_sono_-1.csv')
        all_negative_one_rows.to_csv(file_path_all_negative_one, index=False)
        number = all_negative_one_rows.shape[0]
        print(f"Numero di righe con tutti valori impostati a -1 (mancanti) per {name}: {number}")

    # Salva le righe con almeno un valore impostato a -1 nella cartella 'Other'
    if not one_negative_one_rows.empty:
        file_path_one_negative_one = os.path.join(folder_path, str(name) + '_almeno_un_valore_-1.csv')
        one_negative_one_rows.to_csv(file_path_one_negative_one, index=False)
        number = one_negative_one_rows.shape[0]
        print(f"Numero di righe con almeno un valore mancante nei campi obbligatori per {name}: {number}")
    else:
        print(f"Non ci sono righe con almeno un valore mancante nei campi obbligatori per {name}")

    # Rimuovi le righe con almeno un valore -1 dal dataframe originale
    #df = df[~has_negative_one]

    # Rimuovi le righe tutti i valori a -1 dal dataframe originale
    df = df[~all_negative_one]

    return df
