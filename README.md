# 🛒 Análise Exploratória de Dados — Base Varejo

Mini-Projeto Avaliativo | Módulo 1 – Semana 07  
Curso: Visualização de Dados e Business Intelligence [T1]  
Aluno: **Yuri Mello Saraiva** | Turma: **TurmaQAVDBI1**

---

## 📋 Sobre o Projeto

Este projeto realiza uma **Análise Exploratória de Dados (AED)** sobre a base de varejo disponibilizada no Kaggle, com o objetivo de transformar dados brutos em informações acionáveis para o negócio.

A base `Base Varejo.csv` contém **830.000 registros** de compras com informações de data, cliente, produto e categoria.

---

## 📁 Estrutura do Repositório

```
MiniProjeto_Final/
└── Yuri_Mello_Saraiva/
    ├── script.py       # Script principal da AED
    ├── df_limpo.csv    # Base tratada gerada pelo script
    └── README.md       # Este arquivo
```

---

## ▶️ Como Executar

```bash
# 1. Baixe a base de dados do Kaggle e coloque na mesma pasta do script
#    https://www.kaggle.com/datasets/namespaiva/base-varejo/data

# 2. Instale a dependência (caso necessário)
pip install pandas

# 3. Execute o script
python script.py
```

O script gera saída no terminal com todas as etapas e salva `df_limpo.csv` na mesma pasta.

---

## 🔍 Etapas da Análise

| Sprint | Etapa | Descrição |
|--------|-------|-----------|
| 1 | Importação | Carregamento da base, exibição de dimensões e tipos |
| 2 | Diagnóstico | Identificação de nulos, duplicatas e inconsistências |
| 3 | Limpeza | Substituição de `#N/D`, remoção de duplicatas, conversão de data |
| 4 | Estatística | Média, mediana, desvio padrão, moda, min, max e contagem de `CL_FHL` |
| 5 | Agrupamento | Análises por gênero, categoria e pivot gênero × segmento |
| 6 | Versionamento | Envio ao GitHub |

---

## 📊 Principais Insights

1. **Qualidade:** 11,6% dos registros eram duplicatas — provavelmente reprocessamento do sistema.
2. **Gênero:** Clientes femininos respondem por ~52% das compras; base bastante equilibrada.
3. **Categoria:** *ALIMENTOS* domina com 52% das compras; varejo com perfil de supermercado.
4. **Filhos:** Maioria dos clientes não tem filhos (moda = 0); distribuição assimétrica à direita.
5. **Segmento:** Segmento B (classe média) concentra ~64% das compras — alvo prioritário para campanhas.
6. **Limitação:** Ausência de coluna de valor/preço impede análise de faturamento real.

---

## 📚 Reflexão Teórica: ETL e Qualidade de Dados

### O que é ETL?

**ETL** (Extract, Transform, Load) é o processo pelo qual dados brutos são extraídos de uma ou mais fontes, transformados para um formato adequado à análise e carregados em um destino (banco de dados, data warehouse ou arquivo limpo).

Neste projeto, cada etapa do ETL foi aplicada explicitamente:

- **Extract (Extração):** `pd.read_csv()` carregou os 830.000 registros do CSV com separador `;`.
- **Transform (Transformação):**
  - Substituição de `#N/D` por `"Sem Categoria"` (padronização de strings).
  - Remoção de 96.553 linhas duplicadas (deduplicação).
  - Conversão da coluna `DATA` de string para `datetime64` via `pd.to_datetime()`.
- **Load (Carga):** O DataFrame limpo foi salvo como `df_limpo.csv`, pronto para alimentar dashboards ou análises mais avançadas.

### Por que a Qualidade de Dados importa?

Dados de má qualidade geram análises incorretas, decisões erradas e perda de confiança nos sistemas de BI. Os principais pilares da qualidade de dados são:

| Dimensão | Definição | Problema encontrado nesta base |
|----------|-----------|-------------------------------|
| **Completude** | Ausência de valores nulos | Não havia nulos — ponto positivo |
| **Unicidade** | Sem registros duplicados | 96.553 duplicatas (~11,6%) |
| **Consistência** | Valores padronizados | `#N/D` em `PR_CAT` sem padrão definido |
| **Validade** | Dados no formato correto | `DATA` em string em vez de datetime |
| **Relevância** | Campos úteis para análise | Sem coluna de valor monetário |

### Conclusão da reflexão

A etapa de limpeza e transformação é, muitas vezes, a mais demorada e crítica de qualquer projeto de dados. Um dado limpo, documentado e com tipos corretos reduz erros nas análises subsequentes, acelera a construção de dashboards e garante que stakeholders tomem decisões baseadas em informações confiáveis.

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.x**
- **pandas** — manipulação e análise de dados
- **NumPy** — operações numéricas (importado implicitamente)

---

## 📎 Fonte dos Dados

[Kaggle — Base Varejo](https://www.kaggle.com/datasets/namespaiva/base-varejo/data)
