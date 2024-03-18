    # VECCHIE REGOLE CON LE CONSEQUENZIALITÀ
    
    # rules = (
    #     (df['Q1.1'] == -1) |
    #     (df['Q1.2'] == -1) |
    #     (df['Q1.4'] == -1) |
    #     (df['Q1.6'] == -1) |
    #     (df['Q1.7'] == -1) |
    #     ((df['Q1.7'] == 2) & (df['Q1.7.1'] == -1)) |
    #     ((df['Q1.7.1'] != -1) & (df['Q1.7.1.2'] == -1)) |
    #     (df['Q2.8'] == -1) |
    #     (df['Q2.9.1'] == -1) |
    #     ((df['Q2.9.2'] != '') & (df['Q2.9.1'] == -1)) |
    #     (df['Q2.10'] == -1)
    # )   


##########################################################################################################################################
################## VERIFICO CHE TUTTI I DATI OBBLIGATORI SIANO STATI INSERITI, ALTRIMENTI TRONCO LA RIGA #################################
##########################################################################################################################################

import pandas as pd

def deleteNotCoerent(df):
    # Verifica che tutti i dati obbligatori siano stati inseriti
    removeEmpty = (
        (df['Q1.1'] == -1) &
        (df['Q1.2'] == -1) &
        (df['Q1.3.1'] == -1) &
        (df['Q1.4'] == -1) &
        (df['Q1.5'] == -1) &
        (df['Q1.6'] == -1) &
        (df['Q1.7'] == -1) &
        (df['Q2.8'] == -1) &
        (df['Q2.9.1'] == -1) &
        (df['Q2.10'] == -1)
    )

    # Conta il numero di righe rimosse
    num_rows_removed = df[removeEmpty].shape[0]

    # Rimuove le righe del dataframe che rispettano le regole di removeEmpty
    df = df[~removeEmpty]

    # Stampa il numero di righe rimosse
    print(f"Numero di righe rimosse: {num_rows_removed}")

    return df
