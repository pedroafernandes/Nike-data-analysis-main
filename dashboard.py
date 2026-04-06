import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

st.set_page_config(
    page_title="Nike Global Dashboard",
    page_icon="👟",
    layout="wide",
)

# ================= ESTILO =================
st.markdown("""
<style>
.stApp { background-color: #111111; color: #FFFFFF; }
section[data-testid="stSidebar"] { background-color: #1a1a1a; }
.stMetric { background-color: #1e1e1e; border-radius: 10px; padding: 10px; }
h1, h2, h3, h4 { color: #FFFFFF; }
.block-container { padding-top: 1.5rem; }
label { color: #cccccc !important; }
div[data-testid="stMetricValue"] { color: #FF0000; font-size: 1.6rem; font-weight: 700; }
div[data-testid="stMetricLabel"] { color: #aaaaaa; }
hr { border-color: #333333; }
</style>
""", unsafe_allow_html=True)

# ================= TAXAS =================
TAXA_USD = {
    'USD': 1.0, 'EUR': 1.08, 'GBP': 1.27, 'CAD': 0.74, 'AUD': 0.63,
    'BRL': 0.18, 'JPY': 0.0066, 'CNY': 0.138, 'INR': 0.012
}

# ================= LOAD =================
@st.cache_data
def load_data():
    df = pd.read_csv("Global_Nike.csv")

    # padronização
    df.columns = df.columns.str.lower().str.strip()

    # remover colunas inúteis
    if 'employee_price' in df.columns:
        df = df.drop(columns='employee_price')

    # tratamento
    df["price_local"] = pd.to_numeric(df["price_local"], errors="coerce")
    df = df.dropna(subset=["price_local", "category", "country_code", "currency"])

    # conversão otimizada (sem apply)
    df["price_usd"] = df["price_local"] * df["currency"].map(TAXA_USD)

    # remover valores inválidos
    df = df.dropna(subset=["price_usd"])

    # desconto
    df["discount_pct"] = df["discount_pct"].fillna(0)

    return df

df = load_data()

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown("## 🎛️ Filtros")

    pais = st.multiselect(
        "País",
        df["country_code"].unique(),
        default=df["country_code"].unique()
    )

    cat = st.multiselect(
        "Categoria",
        df["category"].unique(),
        default=df["category"].unique()
    )

    # NOVO FILTRO
    price_range = st.slider(
        "Preço USD",
        float(df["price_usd"].min()),
        float(df["price_usd"].max()),
        (50.0, 200.0)
    )

# ================= FILTRO =================
df_f = df[
    (df["country_code"].isin(pais)) &
    (df["category"].isin(cat)) &
    (df["price_usd"] >= price_range[0]) &
    (df["price_usd"] <= price_range[1])
]

# ================= HEADER =================
st.title("👟 Nike Global Dashboard")

# ================= KPIs =================
c1, c2, c3, c4 = st.columns(4)

c1.metric("Produtos", len(df_f))
c2.metric("Países", df_f["country_code"].nunique())
c3.metric("Preço mediano", f"${df_f['price_usd'].median():.0f}")
c4.metric("Desconto mediano", f"{df_f['discount_pct'].median():.0f}%")

# ================= GRÁFICO 1 =================
st.subheader("Preço mediano por país")

g1 = df_f.groupby("country_code")["price_usd"].median().sort_values()

fig1, ax1 = plt.subplots()
ax1.bar(g1.index, g1.values)
ax1.tick_params(axis='x', rotation=45)
st.pyplot(fig1)

# ================= GRÁFICO 2 =================
st.subheader("Heatmap preço por categoria")

pivot = df_f.pivot_table(
    values="price_usd",
    index="country_code",
    columns="category",
    aggfunc="median"
)

fig2, ax2 = plt.subplots(figsize=(10,5))
sns.heatmap(pivot, cmap="Reds", ax=ax2)
st.pyplot(fig2)

# ================= GRÁFICO 3 =================
st.subheader("Preço vs Desconto")

resumo = df_f.groupby("country_code").agg({
    "price_usd": "median",
    "discount_pct": "median"
})

fig3, ax3 = plt.subplots()
ax3.scatter(resumo["price_usd"], resumo["discount_pct"])
ax3.set_xlabel("Preço")
ax3.set_ylabel("Desconto")
st.pyplot(fig3)