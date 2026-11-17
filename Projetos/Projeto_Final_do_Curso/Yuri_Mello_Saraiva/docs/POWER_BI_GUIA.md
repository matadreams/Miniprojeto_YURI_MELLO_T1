# Guia de relatório e alternativa Power BI

## Entrega principal

A entrega interativa deste projeto é o arquivo [`dashboard.html`](../dashboard.html), desenvolvido com HTML, CSS, JavaScript e Chart.js. Ele deve ser aberto no navegador e contém filtros, KPIs, gráficos e tabela analítica.

O dashboard foi escolhido como solução final porque o Power BI Desktop apresentou inconsistências de conversão regional dos campos `UnitPrice` e `Revenue` durante a importação. Os valores exibidos no HTML são derivados diretamente do pipeline Python e foram validados antes da publicação.

## Conteúdo do dashboard HTML

- Faturamento bruto, pedidos, itens vendidos e ticket médio;
- filtro por país;
- filtro por período inicial;
- faturamento mensal;
- top 10 produtos;
- faturamento por país;
- tabela de produtos com faturamento, itens e pedidos;
- fonte, período, moeda e limitações.

## Alternativa Power BI, caso solicitada pelo professor

Se o professor exigir especificamente um arquivo `.pbix`, importe `data/processed/vendas_tratadas.csv` no Power BI Desktop e confirme os seguintes tipos:

- `InvoiceNo`: Texto;
- `StockCode`: Texto;
- `Description`: Texto;
- `Quantity`: Número inteiro;
- `InvoiceDate`: Data/Hora;
- `UnitPrice`: Número decimal;
- `Country`: Texto;
- `Revenue`: Número decimal;
- `YearMonth`: Texto;
- `Year` e `Month`: Número inteiro.

As medidas seriam:

```DAX
Faturamento = SUM(vendas_tratadas[Revenue])
Pedidos = DISTINCTCOUNT(vendas_tratadas[InvoiceNo])
Itens vendidos = SUM(vendas_tratadas[Quantity])
Ticket médio = DIVIDE([Faturamento], [Pedidos])
```

Formate `Faturamento` e `Ticket médio` como GBP. Caso use o Power Query, não transforme `InvoiceNo`, `UnitPrice` ou `Revenue` em número inteiro. Para preservar os cancelamentos, `InvoiceNo` precisa permanecer como texto.
