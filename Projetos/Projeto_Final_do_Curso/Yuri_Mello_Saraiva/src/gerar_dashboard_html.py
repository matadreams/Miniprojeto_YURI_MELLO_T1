from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / 'data' / 'processed'
OUT = ROOT / 'dashboard.html'

v = pd.read_csv(PROC / 'vendas_tratadas.csv', parse_dates=['InvoiceDate'])
v['YearMonth'] = v['YearMonth'].astype(str)
v['Country'] = v['Country'].astype(str)
v['Description'] = v['Description'].astype(str)

# Agregações compactas, suficientes para os filtros do dashboard sem embutir 53 MB de dados.
month_country = (v.groupby(['YearMonth', 'Country'], as_index=False)
    .agg(Revenue=('Revenue','sum'), Items=('Quantity','sum'), Orders=('InvoiceNo','nunique')))
product_country = (v.groupby(['Country', 'Description'], as_index=False)
    .agg(Revenue=('Revenue','sum'), Items=('Quantity','sum'), Orders=('InvoiceNo','nunique')))
monthly = (v.groupby('YearMonth', as_index=False)
    .agg(Revenue=('Revenue','sum'), Items=('Quantity','sum'), Orders=('InvoiceNo','nunique')))
country = (v.groupby('Country', as_index=False)
    .agg(Revenue=('Revenue','sum'), Items=('Quantity','sum'), Orders=('InvoiceNo','nunique'))
    .sort_values('Revenue', ascending=False))
products = (v.groupby('Description', as_index=False)
    .agg(Revenue=('Revenue','sum'), Items=('Quantity','sum'), Orders=('InvoiceNo','nunique'))
    .sort_values('Revenue', ascending=False).head(30))

payload = {
    'monthCountry': month_country.to_dict('records'),
    'productCountry': product_country.to_dict('records'),
    'monthly': monthly.to_dict('records'),
    'country': country.to_dict('records'),
    'products': products.to_dict('records'),
    'countries': sorted(v['Country'].unique().tolist()),
    'months': sorted(v['YearMonth'].unique().tolist()),
    'source': 'UCI Machine Learning Repository — Online Retail',
    'period': '01/12/2010 a 09/12/2011',
}

data_json = json.dumps(payload, ensure_ascii=False, separators=(',', ':'))

html = r'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Vendas e desempenho — Yuri Mello Saraiva</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js"></script>
<style>
:root{--navy:#112d4e;--blue:#1d5d9b;--orange:#e67e22;--green:#198754;--ink:#17202a;--muted:#617083;--bg:#f4f7fb;--card:#fff;--line:#dce5ef}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:14px Inter,Segoe UI,Arial,sans-serif}header{background:linear-gradient(120deg,var(--navy),#174b78);color:white;padding:30px max(22px,calc((100vw - 1240px)/2));}header h1{margin:0 0 8px;font-size:28px}header p{margin:0;color:#dbe9f7}.wrap{max-width:1240px;margin:0 auto;padding:22px}.toolbar,.card,.panel{background:var(--card);border:1px solid var(--line);border-radius:14px;box-shadow:0 3px 14px #183b5b0d}.toolbar{display:flex;gap:14px;align-items:end;flex-wrap:wrap;padding:16px;margin-bottom:18px}.control{display:flex;flex-direction:column;gap:6px;min-width:205px}.control label{font-weight:700;color:var(--muted);font-size:12px;text-transform:uppercase;letter-spacing:.04em}.control select{border:1px solid #c8d4e2;border-radius:8px;padding:10px;background:white;color:var(--ink)}button{border:0;background:var(--navy);color:#fff;border-radius:8px;padding:11px 15px;cursor:pointer;font-weight:700}.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:18px}.card{padding:17px}.card .label{color:var(--muted);font-size:12px;text-transform:uppercase;font-weight:700}.card .value{font-size:25px;font-weight:800;color:var(--navy);margin-top:8px}.grid{display:grid;grid-template-columns:1fr 1fr;gap:18px}.panel{padding:17px;margin-bottom:18px}.panel h2{font-size:17px;margin:0 0 5px;color:var(--navy)}.panel .sub{color:var(--muted);margin:0 0 14px;font-size:12px}.chartbox{height:320px}.wide{grid-column:1/-1}table{width:100%;border-collapse:collapse}th,td{text-align:left;padding:10px 8px;border-bottom:1px solid var(--line)}th{color:var(--muted);font-size:12px;text-transform:uppercase}td.num,th.num{text-align:right}.note{background:#fff8ed;border-left:4px solid var(--orange);padding:12px;border-radius:8px;color:#5e431f;line-height:1.5}footer{max-width:1240px;margin:auto;padding:0 22px 30px;color:var(--muted);font-size:12px;line-height:1.5}@media(max-width:850px){.kpis{grid-template-columns:repeat(2,1fr)}.grid{grid-template-columns:1fr}.wide{grid-column:auto}}@media(max-width:520px){.kpis{grid-template-columns:1fr}.wrap{padding:14px}}
</style>
</head>
<body>
<header><h1>Vendas e desempenho no varejo online</h1><p>Projeto de Recuperação · Yuri Mello Saraiva · Turma 01 — Análise de Dados</p></header>
<main class="wrap">
<section class="toolbar"><div class="control"><label for="countryFilter">País</label><select id="countryFilter"><option value="ALL">Todos os países</option></select></div><div class="control"><label for="monthFilter">Período inicial</label><select id="monthFilter"><option value="ALL">Todo o período</option></select></div><button id="reset">Limpar filtros</button></section>
<section class="kpis"><div class="card"><div class="label">Faturamento bruto</div><div class="value" id="kpiRevenue">—</div></div><div class="card"><div class="label">Pedidos únicos</div><div class="value" id="kpiOrders">—</div></div><div class="card"><div class="label">Itens vendidos</div><div class="value" id="kpiItems">—</div></div><div class="card"><div class="label">Ticket médio</div><div class="value" id="kpiTicket">—</div></div></section>
<section class="grid"><div class="panel wide"><h2>Faturamento mensal</h2><p class="sub">Evolução do faturamento bruto no recorte selecionado.</p><div class="chartbox"><canvas id="monthlyChart"></canvas></div></div><div class="panel"><h2>Top produtos por faturamento</h2><p class="sub">Os 10 produtos de maior faturamento no filtro atual.</p><div class="chartbox"><canvas id="productChart"></canvas></div></div><div class="panel"><h2>Faturamento por país</h2><p class="sub">Concentração geográfica das vendas no filtro atual.</p><div class="chartbox"><canvas id="countryChart"></canvas></div></div><div class="panel wide"><h2>Detalhamento de produtos</h2><p class="sub">Tabela com faturamento, itens e pedidos. Valores em GBP.</p><div style="overflow:auto"><table><thead><tr><th>Produto</th><th class="num">Faturamento (GBP)</th><th class="num">Itens</th><th class="num">Pedidos</th></tr></thead><tbody id="productTable"></tbody></table></div></div><div class="panel wide"><div class="note"><strong>Interpretação e limitações:</strong> os resultados são descritivos e não demonstram causalidade. O faturamento é calculado como Quantity × UnitPrice, em GBP. Cancelamentos e valores não positivos foram excluídos dos indicadores principais. A fonte é o UCI Online Retail, com dados de 01/12/2010 a 09/12/2011.</div></div></section>
</main><footer>Fonte: UCI Machine Learning Repository — Online Retail · Licença CC BY 4.0 · Dashboard desenvolvido para fins acadêmicos por Yuri Mello Saraiva.</footer>
<script>
const DATA = __DATA__;
let charts={};
const money = n => new Intl.NumberFormat('pt-BR',{style:'currency',currency:'GBP'}).format(n);
const integer = n => new Intl.NumberFormat('pt-BR',{maximumFractionDigits:0}).format(n);
const esc = s => String(s).replace(/[&<>'"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]));
function fillFilters(){const c=document.getElementById('countryFilter'),m=document.getElementById('monthFilter');DATA.countries.forEach(x=>c.insertAdjacentHTML('beforeend',`<option>${esc(x)}</option>`));DATA.months.forEach(x=>m.insertAdjacentHTML('beforeend',`<option>${x}</option>`));}
function filteredFacts(){const country=document.getElementById('countryFilter').value, start=document.getElementById('monthFilter').value;return DATA.monthCountry.filter(r=>(country==='ALL'||r.Country===country)&&(start==='ALL'||r.YearMonth>=start));}
function aggregate(rows,key){const out={};rows.forEach(r=>{const k=r[key];if(!out[k])out[k]={Revenue:0,Items:0,Orders:0};out[k].Revenue+=+r.Revenue;out[k].Items+=+r.Items;out[k].Orders+=+r.Orders});return Object.entries(out).map(([k,v])=>({key:k,...v}));}
function destroy(name){if(charts[name])charts[name].destroy();}
function render(){const facts=filteredFacts(), monthly=aggregate(facts,'YearMonth').sort((a,b)=>a.key.localeCompare(b.key)), countries=aggregate(facts,'Country').sort((a,b)=>b.Revenue-a.Revenue), chosen=document.getElementById('countryFilter').value;
let rev=facts.reduce((s,r)=>s+ +r.Revenue,0),items=facts.reduce((s,r)=>s+ +r.Items,0),orders=facts.reduce((s,r)=>s+ +r.Orders,0);document.getElementById('kpiRevenue').textContent=money(rev);document.getElementById('kpiOrders').textContent=integer(orders);document.getElementById('kpiItems').textContent=integer(items);document.getElementById('kpiTicket').textContent=money(orders?rev/orders:0);
const pc=DATA.productCountry.filter(r=>(chosen==='ALL'||r.Country===chosen)&&(document.getElementById('monthFilter').value==='ALL')); // product ranking uses country filter; monthly filter is reflected in KPIs/charts
const products=(chosen==='ALL'?DATA.products:aggregate(pc,'Description')).sort((a,b)=>b.Revenue-a.Revenue).slice(0,10);
destroy('monthly');charts.monthly=new Chart(document.getElementById('monthlyChart'),{type:'line',data:{labels:monthly.map(x=>x.key),datasets:[{label:'Faturamento (GBP)',data:monthly.map(x=>x.Revenue),borderColor:'#1d5d9b',backgroundColor:'#1d5d9b22',fill:true,tension:.25}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{y:{ticks:{callback:v=>'£'+(v/1000).toFixed(0)+'k'}},x:{ticks:{maxRotation:60}}}}});
destroy('product');charts.product=new Chart(document.getElementById('productChart'),{type:'bar',data:{labels:products.map(x=>String(x.key||x.Description).slice(0,28)),datasets:[{label:'Faturamento (GBP)',data:products.map(x=>x.Revenue),backgroundColor:'#e67e22'}]},options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{x:{ticks:{callback:v=>'£'+(v/1000).toFixed(0)+'k'}},y:{ticks:{font:{size:10}}}}}});
destroy('country');charts.country=new Chart(document.getElementById('countryChart'),{type:'bar',data:{labels:countries.slice(0,10).map(x=>x.key),datasets:[{label:'Faturamento (GBP)',data:countries.slice(0,10).map(x=>x.Revenue),backgroundColor:'#198754'}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{x:{ticks:{autoSkip:false,maxRotation:55}},y:{ticks:{callback:v=>'£'+(v/1000).toFixed(0)+'k'}}}}});
document.getElementById('productTable').innerHTML=products.slice(0,20).map(x=>`<tr><td>${esc(x.key||x.Description)}</td><td class="num">${money(x.Revenue)}</td><td class="num">${integer(x.Items)}</td><td class="num">${integer(x.Orders)}</td></tr>`).join('');}
fillFilters();document.getElementById('countryFilter').addEventListener('change',render);document.getElementById('monthFilter').addEventListener('change',render);document.getElementById('reset').addEventListener('click',()=>{document.getElementById('countryFilter').value='ALL';document.getElementById('monthFilter').value='ALL';render()});render();
</script></body></html>'''.replace('__DATA__', data_json)
OUT.write_text(html, encoding='utf-8')
print(f'Gerado: {OUT} ({OUT.stat().st_size:,} bytes)')
