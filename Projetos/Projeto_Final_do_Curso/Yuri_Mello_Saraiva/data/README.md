# Dados

Os arquivos agregados necessários para conferir os resultados estão em `processed/`.

A base transacional completa não foi duplicada nesta pasta por seu tamanho. Para reproduzir o projeto, baixe o arquivo público `Online Retail.xlsx` da página oficial da UCI:

https://archive.ics.uci.edu/dataset/352/online+retail

Coloque o arquivo em `data/raw/Online Retail.xlsx` e execute:

```bash
python src/analise_vendas.py
python src/gerar_dashboard_html.py
```

A fonte é pública e licenciada sob CC BY 4.0. Não inclua credenciais, dados privados ou arquivos restritos.
