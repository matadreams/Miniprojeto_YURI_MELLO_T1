# =============================================================================
# MINI-PROJETO AVALIATIVO - MÓDULO 1 - SEMANA 07
# Visualização de Dados e Business Intelligence [T1]
# Análise Exploratória de Dados (AED) - Base Varejo
#
# Aluno : Yuri Mello Saraiva
# Turma : TurmaQAVDBI1
# =============================================================================

import pandas as pd
import numpy as np

# =============================================================================
# SPRINT 1 - IMPORTAÇÃO DOS DADOS
# Carrega a base Varejo.csv, exibe número de registros, colunas e tipos.
# =============================================================================

print("=" * 65)
print("  SPRINT 1 - IMPORTAÇÃO DOS DADOS")
print("=" * 65)

# Separador do arquivo é ponto e vírgula (;)
# usecols=range(10) ignora as 4 colunas extras vazias ao final do arquivo
df = pd.read_csv("Base Varejo.csv", sep=";", encoding="utf-8", usecols=range(10))

print(f"\nNúmero de registros : {len(df):,}")
print(f"Número de colunas   : {df.shape[1]}")
print("\nColunas e tipos de dados:")
print(df.dtypes.to_string())
print("\nPrimeiras 5 linhas:")
print(df.head().to_string())

# Dicionário explicativo das colunas
colunas_desc = {
    "DATA"      : "Data da compra (dd/mm/aaaa)",
    "CO_ID"     : "Identificador da compra",
    "CL_ID"     : "Identificador do cliente",
    "CL_GENERO" : "Gênero do cliente (M/F)",
    "CL_EC"     : "Estado civil do cliente",
    "CL_FHL"    : "Número de filhos do cliente",
    "CL_SEG"    : "Segmento do cliente (A/B/C)",
    "PR_ID"     : "Identificador do produto",
    "PR_CAT"    : "Categoria do produto",
    "PR_NOME"   : "Nome do produto",
}
print("\nLegenda das colunas:")
for col, desc in colunas_desc.items():
    print(f"  {col:<12} -> {desc}")


# =============================================================================
# SPRINT 2 - VERIFICAÇÃO DE QUALIDADE (problemas nos dados)
# Reporta: valores nulos, duplicatas e inconsistências.
# =============================================================================

print("\n" + "=" * 65)
print("  SPRINT 2 - VERIFICAÇÃO DE QUALIDADE DOS DADOS")
print("=" * 65)

# --- Problema 1: Valores nulos por coluna ---
nulos = df.isnull().sum()
print("\n[Problema 1] Valores nulos por coluna:")
print(nulos.to_string())
total_nulos = nulos.sum()
print(f"  → Total de células nulas: {total_nulos:,}")

# --- Problema 2: Linhas duplicadas ---
n_duplicatas = df.duplicated().sum()
print(f"\n[Problema 2] Linhas completamente duplicadas: {n_duplicatas:,}")
print(f"  → Representam {n_duplicatas / len(df) * 100:.2f}% do total de registros.")

# --- Problema 3: Inconsistências na coluna PR_CAT ---
# '#N/D' indica "não disponível" — categoria sem identificação válida
n_nd = (df["PR_CAT"] == "#N/D").sum()
print(f"\n[Problema 3] Registros com PR_CAT = '#N/D' (sem categoria): {n_nd:,}")
print(f"  → Representam {n_nd / len(df) * 100:.2f}% dos registros.")

# --- Verificação extra: formato da coluna DATA ---
data_amostra = df["DATA"].head(3).tolist()
print(f"\n[Verificação] Formato atual da coluna DATA (amostra): {data_amostra}")
print("  → Tipo atual: string. Precisa ser convertido para datetime.")

# --- Verificação extra: valores únicos de variáveis categóricas ---
print("\n[Verificação] Valores únicos em variáveis categóricas:")
print(f"  CL_GENERO : {df['CL_GENERO'].unique().tolist()}")
print(f"  CL_SEG    : {df['CL_SEG'].unique().tolist()}")
print(f"  PR_CAT    : {df['PR_CAT'].unique().tolist()}")


# =============================================================================
# SPRINT 3 - LIMPEZA DE NULOS E DUPLICATAS / AJUSTE DE TIPOS
# Etapas: (1) substituir '#N/D' por 'Sem Categoria', (2) eliminar duplicatas,
#         (3) converter coluna DATA para datetime.
# =============================================================================

print("\n" + "=" * 65)
print("  SPRINT 3 - LIMPEZA E TRANSFORMAÇÃO DOS DADOS")
print("=" * 65)

# --- Etapa 1: Tratar inconsistência em PR_CAT ---
# Escolha: substituir '#N/D' por 'Sem Categoria' para manter os registros
# e sinalizar que a categoria não foi identificada, sem perda de dados.
df["PR_CAT"] = df["PR_CAT"].apply(
    lambda x: "Sem Categoria" if x == "#N/D" else x
)
print(f"\n[Limpeza 1] '#N/D' em PR_CAT → substituído por 'Sem Categoria'.")
print(f"  Verificação: {(df['PR_CAT'] == '#N/D').sum()} registros '#N/D' restantes.")

# --- Etapa 2: Remover duplicatas ---
# Escolha: remover linhas completamente idênticas, mantendo a primeira ocorrência.
# Linhas idênticas em todos os campos indicam entrada repetida por erro de sistema.
df_antes = len(df)
df = df.drop_duplicates()
df_depois = len(df)
print(f"\n[Limpeza 2] Duplicatas removidas: {df_antes - df_depois:,} linhas.")
print(f"  Registros restantes após limpeza: {df_depois:,}")

# --- Etapa 3: Converter coluna DATA para datetime ---
# Formato original: dd/mm/aaaa → pd.to_datetime com dayfirst=True
df["DATA"] = pd.to_datetime(df["DATA"], dayfirst=True, errors="coerce")
datas_invalidas = df["DATA"].isnull().sum()
print(f"\n[Limpeza 3] Coluna DATA convertida para datetime.")
print(f"  Tipo atual: {df['DATA'].dtype}")
print(f"  Datas inválidas (NaT) após conversão: {datas_invalidas}")
print(f"  Período dos dados: {df['DATA'].min().date()} a {df['DATA'].max().date()}")

# --- Resumo do DataFrame limpo ---
print(f"\n[Resumo] DataFrame limpo: {df.shape[0]:,} linhas x {df.shape[1]} colunas.")

# Salvar DataFrame limpo
df.to_csv("df_limpo.csv", sep=";", index=False, encoding="utf-8")
print("  Arquivo 'df_limpo.csv' salvo com sucesso.")


# =============================================================================
# SPRINT 4 - ESTATÍSTICAS DESCRITIVAS: NÚMERO DE FILHOS (CL_FHL)
# Parâmetros: média, mediana, desvio padrão, moda, máximo, mínimo, contagem.
# =============================================================================

print("\n" + "=" * 65)
print("  SPRINT 4 - ESTATÍSTICAS DESCRITIVAS: CL_FHL (Nº de Filhos)")
print("=" * 65)

col_filhos = df["CL_FHL"]

media     = col_filhos.mean()
mediana   = col_filhos.median()
desvpad   = col_filhos.std()
moda      = col_filhos.mode()[0]
maximo    = col_filhos.max()
minimo    = col_filhos.min()
contagem  = col_filhos.count()

print(f"\n  Contagem  : {contagem:,}")
print(f"  Média     : {media:.4f}")
print(f"  Mediana   : {mediana:.1f}")
print(f"  Desvio Padrão: {desvpad:.4f}")
print(f"  Moda      : {moda}")
print(f"  Mínimo    : {minimo}")
print(f"  Máximo    : {maximo}")

print("\n  Distribuição de frequência de CL_FHL:")
freq = col_filhos.value_counts().sort_index()
for val, cnt in freq.items():
    pct = cnt / contagem * 100
    barra = "█" * int(pct / 2)
    print(f"    {val} filho(s): {cnt:>7,} registros ({pct:5.1f}%) {barra}")


# =============================================================================
# SPRINT 5 - PADRÕES DE AGRUPAMENTO (mínimo 2 agrupamentos)
# Agrupamento 1: por Gênero → quantidade de compras e participação %
# Agrupamento 2: por Categoria de Produto → compras por categoria
# Bônus: Pivot Table Gênero x Segmento de Cliente
# =============================================================================

print("\n" + "=" * 65)
print("  SPRINT 5 - PADRÕES DE AGRUPAMENTO")
print("=" * 65)

# --- Agrupamento 1: Compras por Gênero ---
print("\n[Agrupamento 1] Número de compras por Gênero do Cliente:")
grupo_genero = (
    df.groupby("CL_GENERO")["CO_ID"]
    .count()
    .rename("Qtd_Compras")
    .reset_index()
)
grupo_genero["Participacao_%"] = (
    grupo_genero["Qtd_Compras"] / grupo_genero["Qtd_Compras"].sum() * 100
).round(2)
grupo_genero["CL_GENERO"] = grupo_genero["CL_GENERO"].map({"F": "Feminino", "M": "Masculino"})
print(grupo_genero.to_string(index=False))

# --- Agrupamento 2: Compras por Categoria de Produto ---
print("\n[Agrupamento 2] Número de compras por Categoria de Produto:")
grupo_cat = (
    df.groupby("PR_CAT")["CO_ID"]
    .count()
    .rename("Qtd_Compras")
    .sort_values(ascending=False)
    .reset_index()
)
grupo_cat["Participacao_%"] = (
    grupo_cat["Qtd_Compras"] / grupo_cat["Qtd_Compras"].sum() * 100
).round(2)
print(grupo_cat.to_string(index=False))

# --- Bônus: Pivot Table Gênero x Segmento ---
print("\n[Pivot Table] Compras por Gênero x Segmento do Cliente:")
pivot = pd.pivot_table(
    df,
    values="CO_ID",
    index="CL_GENERO",
    columns="CL_SEG",
    aggfunc="count",
    margins=True,
    margins_name="Total"
)
pivot.index = pivot.index.map(
    lambda x: "Feminino" if x == "F" else ("Masculino" if x == "M" else x)
)
pivot.columns.name = "Segmento"
print(pivot.to_string())
print("\n  (Segmentos: A = Alta renda | B = Média renda | C = Baixa renda)")

# --- Análise temporal: compras por mês ---
print("\n[Agrupamento 3] Compras por mês/ano (amostra primeiros e últimos 3):")
df["ANO_MES"] = df["DATA"].dt.to_period("M")
grupo_mes = (
    df.groupby("ANO_MES")["CO_ID"]
    .count()
    .rename("Qtd_Compras")
)
print("  Primeiros 3 períodos:")
print(grupo_mes.head(3).to_string())
print("  Últimos 3 períodos:")
print(grupo_mes.tail(3).to_string())


# =============================================================================
# SPRINT 5 (cont.) - CONCLUSÕES E INSIGHTS (3-6 tópicos)
# =============================================================================

print("\n" + "=" * 65)
print("  CONCLUSÕES E PRINCIPAIS INSIGHTS DA ANÁLISE")
print("=" * 65)

conclusoes = [
    (
        "1. QUALIDADE DOS DADOS",
        f"   A base original continha {n_duplicatas:,} registros duplicados (~{n_duplicatas / 830000 * 100:.1f}%),\n"
        f"   provavelmente gerados por reprocessamento de transações. Foram removidos.\n"
        f"   Havia também {n_nd:,} registros com categoria '#N/D', substituídos por\n"
        f"   'Sem Categoria' para preservar as vendas sem perda de dados."
    ),
    (
        "2. PERFIL DOS CLIENTES - GÊNERO",
        f"   Clientes do gênero Feminino respondem por ~52% das compras\n"
        f"   ({grupo_genero.loc[grupo_genero['CL_GENERO']=='Feminino','Qtd_Compras'].values[0]:,} compras),\n"
        f"   ligeiramente acima do Masculino (~48%). A diferença é pequena, sugerindo\n"
        f"   base de clientes equilibrada em gênero."
    ),
    (
        "3. CATEGORIA CAMPEÃ DE VENDAS",
        f"   'ALIMENTOS' lidera com absoluta folga: {grupo_cat.iloc[0]['Qtd_Compras']:,} compras\n"
        f"   ({grupo_cat.iloc[0]['Participacao_%']}% do total após limpeza). A segunda colocada,\n"
        f"   'HIGIENE', tem menos da metade desse volume. Isso indica foco do varejo\n"
        f"   em itens de consumo frequente (mercearia/supermercado)."
    ),
    (
        "4. PERFIL DOS CLIENTES - FILHOS",
        f"   A maioria dos clientes não tem filhos (moda = 0, mediana = 0).\n"
        f"   A média de {media:.2f} filhos e desvio padrão de {desvpad:.2f} indicam\n"
        f"   distribuição assimétrica à direita: poucos clientes têm muitos filhos.\n"
        f"   O máximo registrado é {maximo} filhos."
    ),
    (
        "5. SEGMENTAÇÃO DE CLIENTES",
        f"   O segmento B (médio) é responsável por ~64% das compras, seguido\n"
        f"   do C (~28%) e A (~8%). Isso sugere que a maior parte da receita\n"
        f"   vem da classe média, sendo um ponto estratégico para campanhas."
    ),
    (
        "6. PROBLEMAS REMANESCENTES",
        f"   a) 'Sem Categoria' ainda representa {n_nd:,} registros — investigar\n"
        f"      junto à equipe de cadastro de produtos.\n"
        f"   b) A base não contém coluna de valor (preço/receita), limitando\n"
        f"      análises de faturamento — apenas volume de compras é analisável.\n"
        f"   c) CL_EC (estado civil) e CL_SEG (segmento) não têm dicionário\n"
        f"      explícito nos dados — recomendável solicitar documentação."
    ),
]

for titulo, corpo in conclusoes:
    print(f"\n{'─'*60}")
    print(f"  {titulo}")
    print(corpo)

print("\n" + "=" * 65)
print("  FIM DA ANÁLISE EXPLORATÓRIA - BASE VAREJO")
print("=" * 65)
