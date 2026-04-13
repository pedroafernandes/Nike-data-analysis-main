
# 👟 Nike Global Data Analysis & Dashboard
Este projeto realiza uma análise detalhada do catálogo global da Nike em 2026, focando em estratégias de precificação, descontos e variações de mercado entre 45 países. Além da análise exploratória em Python, o projeto conta com um dashboard interativo feito em Streamlit.

## 🎯 Objetivos do Projeto
Análise de Preços: Investigar como a Nike posiciona seus preços em diferentes mercados globais após a conversão para uma moeda comum (USD).

Identificação de Outliers: Detectar países com preços muito acima ou abaixo da média global para entender estratégias locais.

Análise Preditiva: Criar bases para futuras análises de faturamento cruzando o poder de compra de cada país com os preços praticados.
## 🤝 Trabalho em Dupla

Este projeto foi desenvolvido em dupla, com colaboração entre os integrantes em todas as etapas.
alunos:
Pedro Antônio de Souza Fernandes Filho
João Paulo Koury de Mendonça


## 👥 Público-alvo

Este dashboard foi desenvolvido para:

- **Estratégia de precificação global** – times da Nike que monitoram alinhamento de preços em 45 países e detectam outliers estratégicos (ex: Índia com preço alto, Egito com preço baixo).
- **Analistas de dados** – que desejam replicar ou estender a análise com filtros interativos (país, categoria, faixa de preço) e visualizações prontas (heatmaps, gráficos de barras, scatter plot).
- **Gestores de categorias** – para comparar medianas de preço e desconto entre `CLOTHING`, `FOOTWEAR`, `ACCESSORIES` e outros segmentos.
- **Pesquisadores de mercado** – interessados em como uma marca premium mantém consistência global (maioria dos países entre $80–$100 USD) enquanto adapta descontos localmente.
- **Estudantes de Business Intelligence** – como exemplo de dashboard executivo com métricas claras, design escuro e código reproduzível em Streamlit.
- 
## 🛠️ Tecnologias e Bibliotecas
As seguintes ferramentas foram utilizadas no desenvolvimento:

Python 3.10 ou superior

Pandas: Para manipulação e tratamento dos dados.

Matplotlib & Seaborn: Para criação de gráficos estatísticos.

Streamlit: Para a criação do dashboard interativo.

Numpy: Para suporte a operações matemáticas.

## 📊 Principais Conclusões da Análise
De acordo com os dados processados:

Consistência Global: A Nike mantém preços consistentes na maioria dos países, com a maior concentração entre $80 e $100 USD.

Países Fora da Curva (Outliers):

Índia: Apresenta o maior preço mediano observado (~$167 USD).

Egito: Apresenta um dos menores preços medianos (~$16 USD).

Japão e Coreia do Sul: Também foram identificados como pontos fora da curva em termos de posicionamento estratégico ou descontos.

Estratégia de Desconto: A análise revelou que, apesar da concentração de preços, a estratégia de descontos varia significativamente para lidar com as particularidades de cada mercado local.
## 📊 Dataset

O dataset utilizado neste projeto é muito grande para ser armazenado diretamente no repositório do GitHub.
Por isso, ele deve ser baixado manualmente através do link abaixo:

🔗 **Download do dataset:**
https://www.kaggle.com/datasets/bsthere/nike-global-catalogue-2026

---

## 📥 Como baixar o dataset

1. Acesse o link acima
2. Crie uma conta ou faça login no Kaggle
3. Clique no botão **"Download"**
4. O arquivo será baixado em formato `.zip`

---

## 📂 Como configurar no projeto

1. Extraia o arquivo `.zip` baixado
2. Localize o arquivo `.csv` dentro da pasta extraída
3. Coloque o arquivo `.csv` na raiz do projeto (mesma pasta do código)

A estrutura deve ficar assim:

```
📁 projeto-dashboard
 ┣ 📄 app.ipynb          # Notebook com a análise exploratória
 ┣ 📄 dashboard.py      # Script do Dashboard Streamlit
 ┣ 📄 Global_Nike.csv   # Dataset (após o download)
 ┗ 📄 README.md
```
## 🚀 Como Executar o Dashboard
Certifique-se de ter o Python instalado. Depois, siga os passos:

1. Instale as dependências necessárias:

```bash
pip install streamlit pandas seaborn matplotlib numpy
streamlit run dashboard.py
```
2. Execute a aplicação:

```Bash
streamlit run dashboard.py
```

---

## ⚠️ Observação

Certifique-se de que o nome do arquivo `.csv` seja exatamente igual ao utilizado no código.
Caso seja diferente, altere o nome do arquivo ou ajuste no seu script Python.

---



