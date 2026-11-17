# Projeto Final — Yuri Mello Saraiva

**Curso:** Análise de Dados  
**Turma:** Turma 01 — Análise de Dados  
**Tema:** Vendas e desempenho no varejo online

## Pergunta de negócio

Quais países, produtos e períodos concentram o maior faturamento e volume de pedidos, e que oportunidades de acompanhamento comercial os dados sugerem?

## Entregáveis

- [`dashboard.html`](dashboard.html): dashboard interativo com filtros, KPIs, gráficos e tabela.
- [`src/analise_vendas.py`](src/analise_vendas.py): ETL, indicadores e visualizações.
- [`src/gerar_dashboard_html.py`](src/gerar_dashboard_html.py): geração do dashboard HTML.
- [`docs/DICIONARIO_DADOS.md`](docs/DICIONARIO_DADOS.md): dicionário dos campos.
- [`docs/POWER_BI_GUIA.md`](docs/POWER_BI_GUIA.md): registro da alternativa Power BI e dos tipos corretos.
- `outputs/figures/`: gráficos estáticos de apoio.
- `data/processed/`: indicadores e tabelas agregadas.
- [`data/README.md`](data/README.md): instruções reproduzíveis para obter a base pública.

## Resultados principais

A análise encontrou 530.104 vendas válidas, 19.960 pedidos únicos, 5.588.376 itens vendidos e £10.666.684,54 de faturamento bruto. O ticket médio foi de £534,40. O Reino Unido concentrou aproximadamente 84,6% do faturamento válido.

## Fonte e limitações

A fonte é o dataset Online Retail do UCI Machine Learning Repository, com dados de 01/12/2010 a 09/12/2011 e licença CC BY 4.0. O faturamento é `Quantity × UnitPrice`, em GBP. A análise é descritiva e não demonstra causalidade, margem, lucro ou desempenho atual.

O dashboard HTML é a entrega interativa principal. O arquivo Power BI não foi incluído porque a conversão regional do Power Query apresentou inconsistências; o guia registra como corrigir os tipos caso o professor exija `.pbix`.
