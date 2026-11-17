"""Projeto de Recuperação - Visualização de Dados e BI
Aluno: Yuri Mello Saraiva | Turma 01 - Análise de Dados

Pipeline reproduzível: Extract -> Transform -> Load -> EDA -> visualizações.
Fonte: UCI Machine Learning Repository - Online Retail.
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "Online Retail.xlsx"
PROCESSED = ROOT / "data" / "processed"
FIGURES = ROOT / "outputs" / "figures"
PROCESSED.mkdir(parents=True, exist_ok=True)
FIGURES.mkdir(parents=True, exist_ok=True)

# -----------------------------
# 1. Extract
# -----------------------------
df_raw = pd.read_excel(RAW, engine="openpyxl")
linhas_brutas = len(df_raw)

# -----------------------------
# 2. Transform
# -----------------------------
df = df_raw.copy()
df.columns = [c.strip() for c in df.columns]
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
df["UnitPrice"] = pd.to_numeric(df["UnitPrice"], errors="coerce")
df["InvoiceNo"] = df["InvoiceNo"].astype(str).str.strip()
df["Country"] = df["Country"].astype(str).str.strip()
df["Description"] = df["Description"].astype(str).str.strip()

# Cancelamentos são identificados por InvoiceNo iniciada por C.
df["IsCancellation"] = df["InvoiceNo"].str.upper().str.startswith("C")
df["GrossSales"] = df["Quantity"] * df["UnitPrice"]

# Mantém apenas vendas válidas para os KPIs principais: quantidade e preço positivos,
# data válida e descrição não vazia. Cancelamentos são excluídos dos KPIs de venda.
valid = (
    df["InvoiceDate"].notna()
    & df["Quantity"].notna()
    & df["UnitPrice"].notna()
    & (df["Quantity"] > 0)
    & (df["UnitPrice"] > 0)
    & (~df["IsCancellation"])
    & (~df["Description"].isin(["", "nan", "None"]))
)
df_sales = df.loc[valid].copy()
df_sales["Revenue"] = df_sales["Quantity"] * df_sales["UnitPrice"]
df_sales["YearMonth"] = df_sales["InvoiceDate"].dt.to_period("M").astype(str)
df_sales["Year"] = df_sales["InvoiceDate"].dt.year
df_sales["Month"] = df_sales["InvoiceDate"].dt.month
df_sales["MonthName"] = df_sales["InvoiceDate"].dt.strftime("%b")
df_sales["Country"] = df_sales["Country"].replace({"nan": "Não informado"})

# Não carregamos CustomerID no arquivo final: não é necessário para a pergunta de negócio.
cols = ["InvoiceNo", "StockCode", "Description", "Quantity", "InvoiceDate", "UnitPrice", "Country", "Revenue", "YearMonth", "Year", "Month"]
df_sales[cols].to_csv(PROCESSED / "vendas_tratadas.csv", index=False, encoding="utf-8-sig")

# -----------------------------
# 3. Indicadores e tabelas de apoio
# -----------------------------
indicadores = {
    "linhas_brutas": linhas_brutas,
    "linhas_vendas_validas": len(df_sales),
    "pedidos_unicos": int(df_sales["InvoiceNo"].nunique()),
    "faturamento_total_gbp": float(df_sales["Revenue"].sum()),
    "itens_vendidos": int(df_sales["Quantity"].sum()),
    "ticket_medio_gbp": float(df_sales.groupby("InvoiceNo")["Revenue"].sum().mean()),
    "periodo_inicio": str(df_sales["InvoiceDate"].min().date()),
    "periodo_fim": str(df_sales["InvoiceDate"].max().date()),
    "cancelamentos_brutos": int(df["IsCancellation"].sum()),
}
pd.DataFrame([indicadores]).to_json(PROCESSED / "indicadores.json", orient="records", indent=2, force_ascii=False)

mensal = df_sales.groupby("YearMonth", as_index=False).agg(
    Revenue=("Revenue", "sum"), Orders=("InvoiceNo", "nunique"), Items=("Quantity", "sum")
)
mensal.to_csv(PROCESSED / "vendas_mensais.csv", index=False, encoding="utf-8-sig")

pais = df_sales.groupby("Country", as_index=False).agg(
    Revenue=("Revenue", "sum"), Orders=("InvoiceNo", "nunique"), Items=("Quantity", "sum")
).sort_values("Revenue", ascending=False)
pais.to_csv(PROCESSED / "vendas_por_pais.csv", index=False, encoding="utf-8-sig")

produto = df_sales.groupby(["StockCode", "Description"], as_index=False).agg(
    Revenue=("Revenue", "sum"), Items=("Quantity", "sum"), Orders=("InvoiceNo", "nunique")
).sort_values("Revenue", ascending=False)
produto.head(20).to_csv(PROCESSED / "top_produtos.csv", index=False, encoding="utf-8-sig")

# -----------------------------
# 4. Visualizações
# -----------------------------
plt.style.use("seaborn-v0_8-whitegrid")
navy = "#12355B"
orange = "#E67E22"

fig, ax = plt.subplots(figsize=(12, 5.5))
ax.plot(mensal["YearMonth"], mensal["Revenue"], color=navy, linewidth=2.5, marker="o", markersize=3)
ax.set_title("Faturamento mensal (GBP)", fontsize=15, weight="bold")
ax.set_xlabel("Mês")
ax.set_ylabel("Faturamento em libras esterlinas (GBP)")
ax.tick_params(axis="x", rotation=60)
fig.tight_layout()
fig.savefig(FIGURES / "01_faturamento_mensal.png", dpi=180)
plt.close(fig)

fig, ax = plt.subplots(figsize=(10, 6))
top_paises = pais.head(10).sort_values("Revenue")
ax.barh(top_paises["Country"], top_paises["Revenue"], color=orange)
ax.set_title("Top 10 países por faturamento", fontsize=15, weight="bold")
ax.set_xlabel("Faturamento (GBP)")
ax.set_ylabel("País")
fig.tight_layout()
fig.savefig(FIGURES / "02_top_paises.png", dpi=180)
plt.close(fig)

fig, ax = plt.subplots(figsize=(10, 6))
top_produtos = produto.head(10).sort_values("Revenue")
labels = top_produtos["Description"].str.slice(0, 38)
ax.barh(labels, top_produtos["Revenue"], color=navy)
ax.set_title("Top 10 produtos por faturamento", fontsize=15, weight="bold")
ax.set_xlabel("Faturamento (GBP)")
ax.set_ylabel("Produto")
fig.tight_layout()
fig.savefig(FIGURES / "03_top_produtos.png", dpi=180)
plt.close(fig)

fig, ax = plt.subplots(figsize=(10, 5.5))
ax.bar(mensal["YearMonth"], mensal["Orders"], color="#4C956C")
ax.set_title("Pedidos únicos por mês", fontsize=15, weight="bold")
ax.set_xlabel("Mês")
ax.set_ylabel("Quantidade de pedidos")
ax.tick_params(axis="x", rotation=60)
fig.tight_layout()
fig.savefig(FIGURES / "04_pedidos_mensais.png", dpi=180)
plt.close(fig)

# Relatório textual para facilitar a redação e a conferência.
with open(PROCESSED / "resumo_analitico.txt", "w", encoding="utf-8") as f:
    f.write(f"Linhas brutas: {linhas_brutas:,}\n")
    f.write(f"Linhas válidas de venda: {len(df_sales):,}\n")
    f.write(f"Pedidos únicos: {indicadores['pedidos_unicos']:,}\n")
    f.write(f"Faturamento total: GBP {indicadores['faturamento_total_gbp']:,.2f}\n")
    f.write(f"Itens vendidos: {indicadores['itens_vendidos']:,}\n")
    f.write(f"Ticket médio: GBP {indicadores['ticket_medio_gbp']:,.2f}\n")
    f.write(f"Período: {indicadores['periodo_inicio']} a {indicadores['periodo_fim']}\n\n")
    f.write("Top 5 países por faturamento:\n")
    f.write(pais.head(5).to_string(index=False))
    f.write("\n\nTop 5 produtos por faturamento:\n")
    f.write(produto.head(5).to_string(index=False))

print("ETL e análise concluídos.")
print(pd.Series(indicadores))
