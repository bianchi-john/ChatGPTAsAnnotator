def seeDistinctValues(df):
    ############ CONTROLLO I SINGOLI VALORI DISTINTI PER COLONNA ################
    saltaLePrimetre = 1
    for col in df.columns:
        saltaLePrimetre = saltaLePrimetre + 1
        if (saltaLePrimetre > 4):
            print(f"Colonna {col}:")
            print(df[col].unique())