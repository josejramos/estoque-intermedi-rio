Este sistema é responsável pelo cadastro de produtos e pelo controle da saída de mercadorias em caso de vendas. Ele opera em uma rede local e pode ser acessado pelo IP da máquina, juntamente com a porta de saída especificada no backend.

O banco de dados é composto por planilhas de Excel divididas em quatro setores:

venda.csv – Contém informações sobre as vendas realizadas e se comunica com o estoque.csv.
defeito.csv – Registra os produtos com defeito, se comunica com o estoque.csv e também com o baixa.csv. Produtos que vão para defeito têm sua tag e observação registradas no defeito.csv.
estoque.csv – Mantém o controle do estoque de produtos e interage com o venda.csv e o defeito.csv.
baixa.csv – Registra a baixa de produtos e se comunica com o defeito.csv.
O sistema também gera um relatório, que pode ser baixado através do front-end.
