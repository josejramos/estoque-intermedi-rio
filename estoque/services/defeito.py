# defeito.py

import csv

def enviar_para_defeito(produtos_defeito):
    defeito_csv = 'data/defeito.csv'
    
    with open(defeito_csv, mode='a', newline='') as file:
        writer = csv.writer(file)
        for produto in produtos_defeito:
            writer.writerow(produto)

