import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

st.set_page_config(
    page_title="Nike Global Dashboard",
    page_icon="👟",
    layout="wide",
)

st.markdown("""
<style>
    /* Fundo escuro estilo Nike */
    .stApp { background-color: #111111; color: #FFFFFF; }
    section[data-testid="stSidebar"] { background-color: #1a1a1a; }
    .stMetric { background-color: #1e1e1e; border-radius: 10px; padding: 10px; }
    h1, h2, h3, h4 { color: #FFFFFF; }
    .block-container { padding-top: 1.5rem; }
    label { color: #cccccc !important; }
    div[data-testid="stMetricValue"] { color: #FF0000; font-size: 1.6rem; font-weight: 700; }
    div[data-testid="stMetricLabel"] { color: #aaaaaa; }
    .stSelectbox label, .stMultiselect label { color: #cccccc !important; }
    hr { border-color: #333333; }
</style>
""", unsafe_allow_html=True)

TAXA_USD = {
    'USD': 1.0, 'EUR': 1.08, 'GBP': 1.27, 'CAD': 0.74,
    'AUD': 0.63, 'NZD': 0.58, 'CHF': 1.13, 'DKK': 0.145,
    'NOK': 0.09, 'SEK': 0.09, 'CZK': 0.044, 'PLN': 0.25,
    'HUF': 0.0027, 'RON': 0.22, 'BGN': 0.55, 'HRK': 0.14,
    'ILS': 0.27, 'TRY': 0.028, 'ZAR': 0.054, 'MXN': 0.051,
    'BRL': 0.18, 'CLP': 0.001, 'COP': 0.00024, 'ARS': 0.001,
    'INR': 0.012, 'IDR': 0.000062, 'MYR': 0.22, 'PHP': 0.017,
    'SGD': 0.74, 'THB': 0.028, 'TWD': 0.031, 'VND': 0.000039,
    'KRW': 0.00071, 'JPY': 0.0066, 'CNY': 0.138,
    'EGP': 0.020, 'HKD': 0.13, 'SAR': 0.27, 'AED': 0.27,
}

NIKE_RED   = "#FF0000"
NIKE_WHITE = "#FFFFFF"
BG_COLOR   = "#111111"
CARD_BG    = "#1e1e1e"

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("Global_Nike.csv")
    except FileNotFoundError:
        st.error("❌ Arquivo 'Global_Nike.csv' não encontrado. Coloque o CSV no mesmo diretório do dashboard.")
        st.stop()

    if 'employee_price' in df.columns:
        df = df.drop(columns='employee_price')
    df['discount_pct'] = df['discount_pct'].fillna(0)
    df['price_usd'] = df.apply(
        lambda r: r['price_local'] * TAXA_USD.get(r['currency'], None), axis=1
    )
    return df

df = load_data()

plt.rcParams.update({
    "figure.facecolor":  BG_COLOR,
    "axes.facecolor":    CARD_BG,
    "axes.edgecolor":    "#444444",
    "axes.labelcolor":   NIKE_WHITE,
    "xtick.color":       "#aaaaaa",
    "ytick.color":       "#aaaaaa",
    "text.color":        NIKE_WHITE,
    "grid.color":        "#333333",
    "grid.linestyle":    "--",
    "grid.alpha":        0.4,
})

with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/a/a6/Logo_NIKE.svg", width=100)
    st.markdown("## 🎛️ Filtros Globais")

    paises_disponiveis = sorted(df['country_code'].dropna().unique())
    paises_sel = st.multiselect(
        "🌍 Países",
        options=paises_disponiveis,
        default=paises_disponiveis,
        help="Filtre os países exibidos nos gráficos"
    )

    categorias_disponiveis = sorted(df['category'].dropna().unique())
    cats_excluir = ['PHYSICAL_GIFT_CARD', 'DIGITAL_GIFT_CARD']
    cats_padrao  = [c for c in categorias_disponiveis if c not in cats_excluir]
    cats_sel = st.multiselect(
        "👕 Categorias",
        options=categorias_disponiveis,
        default=cats_padrao,
        help="Filtre as categorias de produto"
    )

    st.markdown("---")
    st.caption("Fonte: Global Nike Catalogue 2026 — Kaggle")


df_f = df[df['country_code'].isin(paises_sel) & df['category'].isin(cats_sel)]


st.markdown("""
<div style='display:flex;align-items:center;gap:16px;margin-bottom:0.5rem'>
    <h1 style='margin:0;font-size:2.2rem;letter-spacing:2px'>NIKE</h1>
    <span style='color:#FF0000;font-size:2rem;font-weight:700'>Global Catalogue 2026</span>
</div>
<p style='color:#888;margin-top:0'>Análise de preços e descontos em 45 países</p>
<hr>
""", unsafe_allow_html=True)


k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("📦 Produtos",       f"{len(df_f):,}")
k2.metric("🌍 Países",         f"{df_f['country_code'].nunique()}")
k3.metric("👕 Categorias",     f"{df_f['category'].nunique()}")
k4.metric("💵 Preço med. USD", f"${df_f['price_usd'].median():.0f}")
k5.metric("🏷️ Desc. med.",     f"{df_f[df_f['discount_pct']>0]['discount_pct'].median():.0f}%")

st.markdown("<hr>", unsafe_allow_html=True)


st.subheader("📊 Preço mediano em USD por país")

g1_data = (
    df_f.groupby('country_code')['price_usd']
    .median()
    .reset_index()
    .sort_values('price_usd', ascending=False)
)

fig1, ax1 = plt.subplots(figsize=(18, 5))
bars = ax1.bar(g1_data['country_code'], g1_data['price_usd'],
               color=NIKE_RED, alpha=0.85, width=0.7)


mediana_geral = g1_data['price_usd'].median()
ax1.axhline(mediana_geral, color='#FFDD00', linewidth=1.5, linestyle='--', label=f'Mediana global: ${mediana_geral:.0f}')

ax1.set_xlabel("País", fontsize=11)
ax1.set_ylabel("Preço mediano (USD)", fontsize=11)
ax1.set_title("Preço mediano em USD por país", fontsize=13, fontweight='bold', pad=12)
ax1.tick_params(axis='x', rotation=55, labelsize=8)
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:.0f}'))
ax1.legend(facecolor=CARD_BG, edgecolor='#444')
ax1.grid(axis='y')
fig1.tight_layout()
st.pyplot(fig1)
plt.close(fig1)

st.markdown("<hr>", unsafe_allow_html=True)


st.subheader("🌡️ Preço mediano por categoria e país (USD)")

df_g2 = df_f[~df_f['category'].isin(['PHYSICAL_GIFT_CARD', 'DIGITAL_GIFT_CARD'])]
table1 = (
    df_g2.groupby(['country_code', 'category'])['price_usd']
    .median()
    .reset_index()
    .pivot(index='country_code', columns='category', values='price_usd')
)

fig2, ax2 = plt.subplots(figsize=(14, max(6, len(table1) * 0.4)))
cmap = sns.color_palette("Reds", as_cmap=True)
sns.heatmap(table1, annot=True, fmt='.0f', cmap=cmap, ax=ax2,
            linewidths=0.4, linecolor='#222222',
            annot_kws={"size": 8},
            cbar_kws={"shrink": 0.6})
ax2.set_title("Preço mediano por categoria e país (USD)", fontsize=13, fontweight='bold', pad=12)
ax2.set_xlabel("Categoria", fontsize=10)
ax2.set_ylabel("País", fontsize=10)
ax2.tick_params(axis='x', rotation=35, labelsize=8)
ax2.tick_params(axis='y', labelsize=8)
fig2.tight_layout()
st.pyplot(fig2)
plt.close(fig2)

st.markdown("<hr>", unsafe_allow_html=True)


st.subheader("🏷️ % mediana de desconto por país")

g3_data = (
    df_f[df_f['discount_pct'] > 0]
    .groupby('country_code')['discount_pct']
    .median()
    .sort_values(ascending=False)
    .reset_index()
)

fig3, ax3 = plt.subplots(figsize=(18, 5))
ax3.bar(g3_data['country_code'], g3_data['discount_pct'],
        color=NIKE_RED, alpha=0.85, width=0.7)
med_disc = g3_data['discount_pct'].median()
ax3.axhline(med_disc, color='#FFDD00', linewidth=1.5, linestyle='--',
            label=f'Mediana global: {med_disc:.0f}%')
ax3.set_xlabel("País", fontsize=11)
ax3.set_ylabel("% de desconto mediano", fontsize=11)
ax3.set_title("% mediana de desconto por país", fontsize=13, fontweight='bold', pad=12)
ax3.tick_params(axis='x', rotation=55, labelsize=8)
ax3.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:.0f}%'))
ax3.legend(facecolor=CARD_BG, edgecolor='#444')
ax3.grid(axis='y')
fig3.tight_layout()
st.pyplot(fig3)
plt.close(fig3)

st.markdown("<hr>", unsafe_allow_html=True)


st.subheader("🌡️ % de desconto mediano por categoria e país")

df_g4 = df_f[df_f['discount_pct'] > 0]
table2 = (
    df_g4.groupby(['country_code', 'category'])['discount_pct']
    .median()
    .reset_index()
    .pivot(index='country_code', columns='category', values='discount_pct')
)

fig4, ax4 = plt.subplots(figsize=(14, max(6, len(table2) * 0.4)))
sns.heatmap(table2, annot=True, fmt='.0f', cmap='Reds', ax=ax4,
            linewidths=0.4, linecolor='#222222',
            annot_kws={"size": 8},
            cbar_kws={"shrink": 0.6})
ax4.set_title("% de desconto mediano por categoria e país", fontsize=13, fontweight='bold', pad=12)
ax4.set_xlabel("Categoria", fontsize=10)
ax4.set_ylabel("País", fontsize=10)
ax4.tick_params(axis='x', rotation=35, labelsize=8)
ax4.tick_params(axis='y', labelsize=8)
fig4.tight_layout()
st.pyplot(fig4)
plt.close(fig4)

st.markdown("<hr>", unsafe_allow_html=True)


st.subheader("🔵 Posicionamento: Preço vs Desconto por país")
st.caption("Tamanho da bolha proporcional ao volume de produtos com desconto")

resumo = (
    df_f[df_f['discount_pct'] > 0]
    .groupby('country_code')
    .agg(preco=('price_usd', 'median'), desconto=('discount_pct', 'median'), volume=('price_usd', 'count'))
    .reset_index()
)

fig5, ax5 = plt.subplots(figsize=(14, 7))

scatter = ax5.scatter(
    resumo['preco'], resumo['desconto'],
    s=resumo['volume'] / 30,
    c=resumo['preco'],
    cmap='Reds',
    alpha=0.85,
    edgecolors='#FFFFFF',
    linewidths=0.5
)

for _, row in resumo.iterrows():
    ax5.annotate(row['country_code'],
                 (row['preco'], row['desconto']),
                 fontsize=7.5, color=NIKE_WHITE,
                 xytext=(4, 4), textcoords='offset points')


ax5.axvline(resumo['preco'].median(),    color='#FFDD00', linestyle='--', linewidth=1, alpha=0.7, label='Mediana preço')
ax5.axhline(resumo['desconto'].median(), color='#00BFFF', linestyle='--', linewidth=1, alpha=0.7, label='Mediana desconto')

ax5.set_xlabel("Preço mediano (USD)", fontsize=11)
ax5.set_ylabel("Desconto mediano (%)", fontsize=11)
ax5.set_title("Posicionamento de preço vs desconto por país", fontsize=13, fontweight='bold', pad=12)
ax5.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:.0f}'))
ax5.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:.0f}%'))
ax5.legend(facecolor=CARD_BG, edgecolor='#444')
ax5.grid(True)

cbar = plt.colorbar(scatter, ax=ax5, pad=0.01)
cbar.set_label('Preço mediano (USD)', color=NIKE_WHITE)
cbar.ax.yaxis.set_tick_params(color=NIKE_WHITE)
plt.setp(cbar.ax.yaxis.get_ticklabels(), color=NIKE_WHITE)

fig5.tight_layout()
st.pyplot(fig5)
plt.close(fig5)

st.markdown("<hr>", unsafe_allow_html=True)


st.subheader("📝 Conclusões da Análise")
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("""
    <div style='background:#1e1e1e;border-left:4px solid #FF0000;padding:16px;border-radius:8px'>
    <b>📌 Preços consistentes</b><br>
    A Nike mantém preços concentrados entre <b>$80–$100 USD</b> na maioria dos países,
    refletindo uma estratégia de marca global uniforme.
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown("""
    <div style='background:#1e1e1e;border-left:4px solid #FFDD00;padding:16px;border-radius:8px'>
    <b>⚡ Outliers relevantes</b><br>
    Índia (~$167), Egito (~$16), Japão e Coreia do Sul fogem do padrão global,
    indicando estratégias de posicionamento específicas por mercado.
    </div>""", unsafe_allow_html=True)
with c3:
    st.markdown("""
    <div style='background:#1e1e1e;border-left:4px solid #00BFFF;padding:16px;border-radius:8px'>
    <b>✅ Hipótese parcialmente confirmada</b><br>
    Os dados são concentrados, mas outliers expressivos como Índia e Egito mostram
    estratégias bem distintas dos demais mercados.
    </div>""", unsafe_allow_html=True)

st.markdown("<br><center><small style='color:#555'>Global Nike Catalogue 2026 — Kaggle | Dashboard desenvolvido com Streamlit</small></center>", unsafe_allow_html=True)