from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import csv
import os
from services.defeito import enviar_para_defeito
from services.venda import realizar_venda
from services.ler_dados import ler_dados_csv
from services.baixa import mover_arquivo, ler_baixa_csv


app = Flask(__name__, template_folder='templates')

# Função para verificar se o arquivo CSV existe; se não existir, cria o diretório e o arquivo
def verificar_arquivo_csv():
    if not os.path.exists('data'):
        os.makedirs('data')
    if not os.path.exists('data/estoque.csv'):
        with open('data/estoque.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Nome', 'Marca', 'ID', 'Quantidade'])
    if not os.path.exists('data/defeito.csv'):
        with open('data/defeito.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Nome', 'Marca', 'ID', 'Quantidade', 'Tag', 'Observacao'])
    if not os.path.exists('data/baixa.csv'):
        with open('data/baixa.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Nome', 'Marca', 'ID', 'Quantidade', 'Tag', 'Observacao', 'Data'])

# Rota principal que carrega a página inicial (formulário de cadastro)
@app.route('/')
def index():
    return render_template('index.html')  # Substitua 'index.html' pelo nome do seu template principal

# Rota para cadastrar novos produtos
@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    verificar_arquivo_csv()  # Verifica se os arquivos CSV existem

    nome = request.form['nome']
    marca = request.form['marca']
    produto_id = request.form['id']
    quantidade = int(request.form['quantidade'])  # Converta para inteiro

    # Verifica se o produto já existe no estoque
    produto_existe = False
    produtos = []

    with open('data/estoque.csv', mode='r', newline='') as file:
        reader = csv.reader(file)
        header = next(reader)  # Pula o cabeçalho
        for linha in reader:
            if linha and len(linha) >= 3 and linha[2] == produto_id:  # Verifica pelo ID do produto
                linha[3] = str(int(linha[3]) + quantidade)  # Atualiza a quantidade
                produto_existe = True
            produtos.append(linha)

    # Se o produto não existe, adiciona-o ao arquivo CSV
    if not produto_existe:
        produtos.append([nome, marca, produto_id, str(quantidade)])

    # Escreve os produtos de volta no arquivo CSV
    with open('data/estoque.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)  # Escreve o cabeçalho
        writer.writerows(produtos)  # Escreve os produtos atualizados

    return redirect(url_for('index'))

@app.route('/venda', methods=['GET', 'POST'])
def venda():
    if request.method == 'POST':
        try:
            produto_id = request.form['id']
            quantidade = int(request.form['quantidade'])
            
            # Chama a função para realizar a venda
            realizar_venda(produto_id, quantidade)

            # Redireciona para uma página de sucesso ou outra rota após a venda
            return redirect(url_for('sucesso_venda'))

        except Exception as e:
            # Aqui você pode tratar erros específicos, como quantidade insuficiente, produto não encontrado, etc.
            return render_template('erro.html', erro=str(e))

    # Se o método for GET ou se não for bem-sucedido o POST, renderiza o template venda.html
    return render_template('venda.html')

# Rota para página de sucesso após a venda
@app.route('/sucesso_venda')
def sucesso_venda():
    return render_template('sucesso_venda.html')

@app.route('/mover', methods=['POST'])
def mover():
    id_ = request.form.get('id')
    tag = request.form.get('tag')
    
    if id_ and tag:
        sucesso = mover_arquivo(id_, tag)
        if sucesso:
            return redirect(url_for('baixa'))  # Redireciona para a página de baixa após mover o arquivo
        else:
            return "Erro ao mover arquivo", 500
    return "Dados inválidos", 400

@app.route('/baixa')
def baixa():
    dados = ler_baixa_csv()  # Esta função deve ler os dados do arquivo baixa.csv
    return render_template('baixa.html', dados=dados)


@app.route('/enviar_para_defeito', methods=['POST'])
def enviar_defeito():
    quantidade = int(request.form['quantidade'])  # Quantidade de produtos a serem enviados
    tag = request.form['tag']  # Tag digitada pelo usuário
    observacao = request.form['observacao']  # Observação digitada pelo usuário
    id_produto = request.form['id']  # ID do produto selecionado
    
    produtos_defeito = []

    estoque_csv = 'data/estoque.csv'  # Caminho do arquivo de estoque

    with open(estoque_csv, mode='r', newline='') as file:
        reader = csv.reader(file)
        header = next(reader)  # Lê o cabeçalho do arquivo CSV
        produtos_atualizados = []
        
        for produto in reader:
            if produto[2] == id_produto:  # Verifica ID do produto
                quantidade_atual = int(produto[3])  # Quantidade atual do produto no estoque
                nova_quantidade = quantidade_atual - quantidade
                if nova_quantidade < 0:
                    nova_quantidade = 0  # Garante que a quantidade não seja negativa

                # Atualiza a quantidade no produto do estoque.csv
                produto[3] = str(nova_quantidade)
                produtos_atualizados.append(produto)

                # Cria uma cópia do produto para enviar para defeito.csv
                produto_defeito = produto[:]  # Cria uma cópia do produto
                produto_defeito[3] = str(quantidade)  # Define a quantidade enviada para defeito
                produto_defeito.append(tag)  # Adiciona a Tag digitada
                produto_defeito.append(observacao)  # Adiciona a Observação digitada
                produtos_defeito.append(produto_defeito)

            else:
                produtos_atualizados.append(produto)

    # Escreve os produtos atualizados de volta no arquivo CSV de estoque
    with open(estoque_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)  # Escreve o cabeçalho
        writer.writerows(produtos_atualizados)  # Escreve os produtos atualizados

    # Chama a função enviar_para_defeito com os produtos e detalhes
    enviar_para_defeito(produtos_defeito)

    return redirect(url_for('index'))  # Redireciona para a página inicial após o envio

@app.route('/relatorio')
def relatorio():
    estoque_data, defeito_data = ler_dados_csv()
    return render_template('relatorio.html', estoque_data=estoque_data, defeito_data=defeito_data)

from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import csv
import os
from services.defeito import enviar_para_defeito
from services.venda import realizar_venda
from services.ler_dados import ler_dados_csv
from services.baixa import mover_arquivo, ler_baixa_csv


app = Flask(__name__, template_folder='templates')

# Função para verificar se o arquivo CSV existe; se não existir, cria o diretório e o arquivo
def verificar_arquivo_csv():
    if not os.path.exists('data'):
        os.makedirs('data')
    if not os.path.exists('data/estoque.csv'):
        with open('data/estoque.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Nome', 'Marca', 'ID', 'Quantidade'])
    if not os.path.exists('data/defeito.csv'):
        with open('data/defeito.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Nome', 'Marca', 'ID', 'Quantidade', 'Tag', 'Observacao'])
    if not os.path.exists('data/baixa.csv'):
        with open('data/baixa.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Nome', 'Marca', 'ID', 'Quantidade', 'Tag', 'Observacao', 'Data'])

# Rota principal que carrega a página inicial (formulário de cadastro)
@app.route('/')
def index():
    return render_template('index.html')  # Substitua 'index.html' pelo nome do seu template principal

# Rota para cadastrar novos produtos
@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    verificar_arquivo_csv()  # Verifica se os arquivos CSV existem

    nome = request.form['nome']
    marca = request.form['marca']
    produto_id = request.form['id']
    quantidade = int(request.form['quantidade'])  # Converta para inteiro

    # Verifica se o produto já existe no estoque
    produto_existe = False
    produtos = []

    with open('data/estoque.csv', mode='r', newline='') as file:
        reader = csv.reader(file)
        header = next(reader)  # Pula o cabeçalho
        for linha in reader:
            if linha and len(linha) >= 3 and linha[2] == produto_id:  # Verifica pelo ID do produto
                linha[3] = str(int(linha[3]) + quantidade)  # Atualiza a quantidade
                produto_existe = True
            produtos.append(linha)

    # Se o produto não existe, adiciona-o ao arquivo CSV
    if not produto_existe:
        produtos.append([nome, marca, produto_id, str(quantidade)])

    # Escreve os produtos de volta no arquivo CSV
    with open('data/estoque.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)  # Escreve o cabeçalho
        writer.writerows(produtos)  # Escreve os produtos atualizados

    return redirect(url_for('index'))

@app.route('/venda', methods=['GET', 'POST'])
def venda():
    if request.method == 'POST':
        try:
            produto_id = request.form['id']
            quantidade = int(request.form['quantidade'])
            
            # Chama a função para realizar a venda
            realizar_venda(produto_id, quantidade)

            # Redireciona para uma página de sucesso ou outra rota após a venda
            return redirect(url_for('sucesso_venda'))

        except Exception as e:
            # Aqui você pode tratar erros específicos, como quantidade insuficiente, produto não encontrado, etc.
            return render_template('erro.html', erro=str(e))

    # Se o método for GET ou se não for bem-sucedido o POST, renderiza o template venda.html
    return render_template('venda.html')

# Rota para página de sucesso após a venda
@app.route('/sucesso_venda')
def sucesso_venda():
    return render_template('sucesso_venda.html')

@app.route('/mover', methods=['POST'])
def mover():
    id_ = request.form.get('id')
    tag = request.form.get('tag')
    
    if id_ and tag:
        sucesso = mover_arquivo(id_, tag)
        if sucesso:
            return redirect(url_for('baixa'))  # Redireciona para a página de baixa após mover o arquivo
        else:
            return "Erro ao mover arquivo", 500
    return "Dados inválidos", 400

@app.route('/baixa')
def baixa():
    dados = ler_baixa_csv()  # Esta função deve ler os dados do arquivo baixa.csv
    return render_template('baixa.html', dados=dados)


@app.route('/enviar_para_defeito', methods=['POST'])
def enviar_defeito():
    quantidade = int(request.form['quantidade'])  # Quantidade de produtos a serem enviados
    tag = request.form['tag']  # Tag digitada pelo usuário
    observacao = request.form['observacao']  # Observação digitada pelo usuário
    id_produto = request.form['id']  # ID do produto selecionado
    
    produtos_defeito = []

    estoque_csv = 'data/estoque.csv'  # Caminho do arquivo de estoque

    with open(estoque_csv, mode='r', newline='') as file:
        reader = csv.reader(file)
        header = next(reader)  # Lê o cabeçalho do arquivo CSV
        produtos_atualizados = []
        
        for produto in reader:
            if produto[2] == id_produto:  # Verifica ID do produto
                quantidade_atual = int(produto[3])  # Quantidade atual do produto no estoque
                nova_quantidade = quantidade_atual - quantidade
                if nova_quantidade < 0:
                    nova_quantidade = 0  # Garante que a quantidade não seja negativa

                # Atualiza a quantidade no produto do estoque.csv
                produto[3] = str(nova_quantidade)
                produtos_atualizados.append(produto)

                # Cria uma cópia do produto para enviar para defeito.csv
                produto_defeito = produto[:]  # Cria uma cópia do produto
                produto_defeito[3] = str(quantidade)  # Define a quantidade enviada para defeito
                produto_defeito.append(tag)  # Adiciona a Tag digitada
                produto_defeito.append(observacao)  # Adiciona a Observação digitada
                produtos_defeito.append(produto_defeito)

            else:
                produtos_atualizados.append(produto)

    # Escreve os produtos atualizados de volta no arquivo CSV de estoque
    with open(estoque_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)  # Escreve o cabeçalho
        writer.writerows(produtos_atualizados)  # Escreve os produtos atualizados

    # Chama a função enviar_para_defeito com os produtos e detalhes
    enviar_para_defeito(produtos_defeito)

    return redirect(url_for('index'))  # Redireciona para a página inicial após o envio

@app.route('/relatorio')
def relatorio():
    estoque_data, defeito_data = ler_dados_csv()
    return render_template('relatorio.html', estoque_data=estoque_data, defeito_data=defeito_data)

@app.route('/download/<arquivo>')
def download(arquivo):
    if arquivo == 'estoque':
        return send_from_directory('data', 'estoque.csv', as_attachment=True)
    elif arquivo == 'defeito':
        return send_from_directory('data', 'defeito.csv', as_attachment=True)
    elif arquivo == 'baixa':
        return send_from_directory('data', 'baixa.csv', as_attachment=True)
    else:
        return 'Arquivo não encontrado'
    
def get_ip_address():
    import socket
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address

if __name__ == '__main__':
    ip_address = get_ip_address()
    port = 5000
    print(f'Acesse a aplicação em http://{ip_address}:{port}/')
    app.run(debug=True, host=ip_address, port=port)


