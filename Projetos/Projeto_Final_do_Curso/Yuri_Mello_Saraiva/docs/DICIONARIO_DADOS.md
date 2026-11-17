# Dicionário de dados

| Campo | Tipo | Descrição | Uso |
|---|---|---|---|
| `InvoiceNo` | texto | Identificador do pedido | Contagem de pedidos únicos |
| `StockCode` | texto | Código do produto | Identificação do produto |
| `Description` | texto | Nome do produto | Ranking e filtro |
| `Quantity` | inteiro | Quantidade do item na linha | Itens vendidos |
| `InvoiceDate` | data/hora | Data e hora do pedido | Análise temporal |
| `UnitPrice` | decimal | Preço unitário em GBP | Cálculo do faturamento |
| `Country` | texto | País associado ao pedido | Comparação geográfica |
| `Revenue` | decimal | `Quantity × UnitPrice`, em GBP | KPI principal |
| `YearMonth` | texto | Ano e mês derivados da data | Eixo mensal |
| `Year` | inteiro | Ano derivado da data | Filtro |
| `Month` | inteiro | Mês derivado da data | Ordenação e filtro |

`CustomerID` existe no arquivo original da UCI, mas foi removido do arquivo tratado por minimização de dados, pois não é necessário para a pergunta agregada deste projeto.
