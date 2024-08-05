import csv
import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, template_folder='templates')

def realizar_venda(produto_id, quantidade):
    arquivo_estoque = 'data/estoque.csv'
    arquivo_venda = 'data/venda.csv'

    if not os.path.exists(arquivo_estoque):
        raise FileNotFoundError(f'O arquivo {arquivo_estoque} não existe.')

    if not os.path.exists(arquivo_venda):
        with open(arquivo_venda, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Nome', 'Marca', 'ID', 'Quantidade'])

    try:
        produtos_vendidos = []
        estoque_atualizado = []

        produto_encontrado = False
        with open(arquivo_estoque, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for produto in reader:
                if produto['ID'] == produto_id:
                    produto_encontrado = True
                    quantidade_disponivel = int(produto['Quantidade'])
                    if quantidade_disponivel < quantidade:
                        raise ValueError(f'Quantidade solicitada maior que a disponível em estoque.')

                    # Adiciona à lista de vendidos
                    produtos_vendidos.append({
                        'Nome': produto['Nome'],
                        'Marca': produto['Marca'],
                        'ID': produto_id,
                        'Quantidade': quantidade
                    })

                    # Atualiza quantidade no estoque
                    produto['Quantidade'] = str(quantidade_disponivel - quantidade)

                estoque_atualizado.append(produto)

        if not produto_encontrado:
            raise ValueError(f'Produto com ID {produto_id} não encontrado.')

        # Atualiza o arquivo de estoque
        with open(arquivo_estoque, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['Nome', 'Marca', 'ID', 'Quantidade'])
            writer.writeheader()
            writer.writerows(estoque_atualizado)

        # Atualiza o arquivo de vendas
        with open(arquivo_venda, mode='r+', newline='') as file:
            reader = csv.reader(file)
            vendas_atualizadas = list(reader)  # Lê todas as linhas do arquivo
            produto_vendido = False
            for linha in vendas_atualizadas:
                if linha[2] == produto_id:  # Verifica pelo ID do produto
                    quantidade_vendida = int(linha[3]) + quantidade
                    linha[3] = str(quantidade_vendida)
                    produto_vendido = True
                    break

            if not produto_vendido:
                # Se o produto não foi encontrado nas vendas, adiciona uma nova linha
                vendas_atualizadas.append([
                    produtos_vendidos[0]['Nome'],  # Exemplo: Nome do primeiro produto vendido
                    produtos_vendidos[0]['Marca'],  # Exemplo: Marca do primeiro produto vendido
                    produtos_vendidos[0]['ID'],  # Exemplo: ID do primeiro produto vendido
                    str(quantidade)  # Quantidade vendida
                ])

            # Volta ao início do arquivo e escreve as vendas atualizadas
            file.seek(0)
            writer = csv.writer(file)
            writer.writerows(vendas_atualizadas)

    except ValueError as e:
        # Erro específico de venda
        return render_template('erro_venda.html', erro=str(e))

    except Exception as e:
        # Outros erros durante a venda
        return render_template('erro_venda.html', erro=str(e))

    # Venda realizada com sucesso, redireciona para a página de sucesso ou outra rota
    return redirect(url_for('sucesso_venda'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/venda', methods=['POST'])
def venda():
    try:
        produto_id = request.form['id']
        quantidade = int(request.form['quantidade'])

        # Chama a função para realizar a venda
        return realizar_venda(produto_id, quantidade)

    except Exception as e:
        # Trata erros específicos de venda aqui
        return render_template('erro_venda.html', erro=str(e))

@app.route('/sucesso_venda')
def sucesso_venda():
    return render_template('sucesso_venda.html')

if __name__ == '__main__':
    app.run(debug=True)
