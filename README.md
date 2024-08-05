Sistema de Gestão de Estoque
Este projeto é um sistema de gestão de estoque desenvolvido com Flask. Ele permite o cadastro de produtos, realização de vendas, movimentação de produtos para baixa e defeito, e geração de relatórios. O sistema utiliza arquivos CSV para armazenar as informações.

Funcionalidades
Cadastro de Produtos: Adicione novos produtos ao estoque ou atualize a quantidade existente.
Realização de Vendas: Registre vendas e ajuste a quantidade de produtos no estoque.
Movimentação para Baixa: Mova produtos para a lista de baixa.
Envio para Defeito: Registre produtos com defeito e envie-os para um arquivo específico.
Relatórios: Gere relatórios com os dados do estoque e produtos com defeito.
Download de Arquivos: Faça download dos arquivos CSV com os dados do estoque, defeito e baixa.
Requisitos
Python 3
Flask
Instalação
Clone o Repositório

bash
Copiar código
git clone https://github.com/seu-usuario/sistema-gestao-estoque.git
cd sistema-gestao-estoque
Instale as Dependências

É recomendável criar um ambiente virtual para instalar as dependências.

bash
Copiar código
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install flask
Inicie o Servidor

bash
Copiar código
python app.py
O servidor estará disponível em http://localhost:5000.

Estrutura do Projeto
app.py: Arquivo principal do aplicativo Flask.
templates/: Diretório contendo os templates HTML.
index.html: Página inicial com o formulário de cadastro.
venda.html: Página para registrar vendas.
sucesso_venda.html: Página exibida após uma venda bem-sucedida.
erro.html: Página exibida em caso de erro.
baixa.html: Página para visualizar a movimentação de produtos para baixa.
relatorio.html: Página para exibir relatórios de estoque e defeitos.
data/: Diretório onde os arquivos CSV são armazenados.
estoque.csv: Contém informações sobre os produtos em estoque.
defeito.csv: Contém informações sobre produtos com defeito.
baixa.csv: Contém informações sobre produtos em baixa.
services/: Diretório contendo funções auxiliares.
defeito.py: Funções relacionadas ao envio de produtos para defeito.
venda.py: Funções relacionadas à realização de vendas.
ler_dados.py: Funções para ler dados dos arquivos CSV.
baixa.py: Funções para movimentação de arquivos e leitura de dados de baixa.
Rotas
Página Inicial
Método: GET
Rota: /
Descrição: Exibe o formulário de cadastro de produtos.
Cadastro de Produtos
Método: POST
Rota: /cadastrar
Descrição: Cadastra ou atualiza um produto no estoque.
Realização de Vendas
Método: GET, POST
Rota: /venda
Descrição: Registra uma venda e atualiza a quantidade do produto no estoque.
Sucesso da Venda
Método: GET
Rota: /sucesso_venda
Descrição: Página exibida após uma venda bem-sucedida.
Movimentação para Baixa
Método: POST
Rota: /mover
Descrição: Move um produto para a lista de baixa.
Visualização de Baixa
Método: GET
Rota: /baixa
Descrição: Exibe a lista de produtos movidos para baixa.
Envio para Defeito
Método: POST
Rota: /enviar_para_defeito
Descrição: Envia produtos para o arquivo de defeito e atualiza o estoque.
Relatório
Método: GET
Rota: /relatorio
Descrição: Exibe relatórios de estoque e defeitos.
Download de Arquivos
Método: GET
Rota: /download/<arquivo>
Descrição: Permite o download dos arquivos CSV do estoque, defeito ou baixa.
Funções Auxiliares
verificar_arquivo_csv(): Verifica a existência dos arquivos CSV e cria-os se necessário.
realizar_venda(): Função para processar a venda de produtos.
enviar_para_defeito(): Função para registrar produtos com defeito.
mover_arquivo(): Função para mover produtos para a lista de baixa.
ler_dados_csv(): Função para ler dados dos arquivos CSV.
Executando a Aplicação
O servidor Flask será iniciado no endereço e porta especificados no arquivo app.py. Acesse a aplicação no navegador usando o endereço exibido no terminal.

Contribuição
Se desejar contribuir para este projeto, siga estas etapas:

Faça um fork do repositório.
Crie uma nova branch (git checkout -b feature/nova-funcionalidade).
Faça suas alterações e commit (git commit -am 'Adiciona nova funcionalidade').
Envie para o repositório remoto (git push origin feature/nova-funcionalidade).
Abra um Pull Request.
Licença
Este projeto está licenciado sob a Licença MIT. Veja o arquivo LICENSE para mais detalhes.
