import csv
import os

def ler_csv(caminho_arquivo):
    with open(caminho_arquivo, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        dados = []
        for row in reader:
            dados.append({
                'Nome': row.get('Nome', ''),
                'Marca': row.get('Marca', ''),
                'ID': row.get('ID', ''),
                'Quantidade': row.get('Quantidade', ''),
                'Tag': row.get('Tag', ''),  # Inclui a coluna Tag
                'Observação': row.get('Observação', '')  # Inclui a coluna Observação
            })
        return dados

def ler_dados_csv():
    estoque_path = os.path.join('data', 'estoque.csv')
    defeito_path = os.path.join('data', 'defeito.csv')
    
    estoque_data = ler_csv(estoque_path)
    defeito_data = ler_csv(defeito_path)
    
    return estoque_data, defeito_data

