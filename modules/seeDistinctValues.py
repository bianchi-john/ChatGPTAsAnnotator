def seeDistinctValues(df):
    ############ CONTROLLO I SINGOLI VALORI DISTINTI PER COLONNA ################
    saltaLePrimeQuattro = 1
    for col in df.columns:
        saltaLePrimeQuattro = saltaLePrimeQuattro + 1
        if (saltaLePrimeQuattro > 4):
            print(f"Colonna {col}:")
            print(df[col].unique())