import csv

def mover_arquivo(id_, tag):
    base_dados_path = 'data/defeito.csv'
    baixa_path = 'data/baixa.csv'
    
    try:
        # Ler o arquivo base de dados e filtrar a linha desejada
        with open(base_dados_path, mode='r', newline='') as base_file:
            reader = csv.DictReader(base_file)
            linhas = list(reader)
        
        linha_para_mover = None
        for linha in linhas:
            if linha.get('ID') == id_ and linha.get('tag') == tag:  # Use .get() para evitar KeyError
                linha_para_mover = linha
                break
        
        if linha_para_mover:
            # Remover a linha da base de dados
            linhas = [linha for linha in linhas if not (linha.get('ID') == id_ and linha.get('tag') == tag)]
            
            # Escrever a linha removida para o arquivo baixa.csv
            with open(baixa_path, mode='a', newline='') as baixa_file:
                fieldnames = linha_para_mover.keys()
                writer = csv.DictWriter(baixa_file, fieldnames=fieldnames)
                
                # Se o arquivo estiver vazio, escreva o cabeçalho
                if baixa_file.tell() == 0:
                    writer.writeheader()
                
                writer.writerow(linha_para_mover)
            
            # Reescrever a base de dados sem a linha removida
            with open(base_dados_path, mode='w', newline='') as base_file:
                writer = csv.DictWriter(base_file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(linhas)
            
            return True
        else:
            print("Nenhuma linha encontrada com o ID e tag fornecidos.")
            return False

    except Exception as e:
        print(f"Erro ao mover o arquivo: {e}")
        return False

def ler_baixa_csv():
    baixa_path = 'data/baixa.csv'
    dados = []

    try:
        with open(baixa_path, mode='r', newline='') as baixa_file:
            reader = csv.DictReader(baixa_file)
            for linha in reader:
                dados.append(linha)
    
    except FileNotFoundError:
        print(f"O arquivo {baixa_path} não foi encontrado.")
    
    except Exception as e:
        print(f"Erro ao ler o arquivo baixa.csv: {e}")

    return dados
