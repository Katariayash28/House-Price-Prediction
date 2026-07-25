import streamlit as st
import pandas as pd
import plotly.express as px

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="House Price Prediction",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===============================
# CUSTOM CSS
# ===============================
st.markdown("""
<style>

.main{
    background-color:#0E1117;
}

h1,h2,h3,h4,h5,h6{
    color:white;
}

p{
    color:#D3D3D3;
}

[data-testid="stSidebar"]{
    background-color:#1E1E2F;
}

.metric-card{
    background:#262730;
    padding:20px;
    border-radius:15px;
    text-align:center;
    box-shadow:0px 0px 10px rgba(0,0,0,.4);
}

.big-font{
    font-size:40px;
    font-weight:bold;
    color:#00E6A8;
}

.small-font{
    font-size:18px;
    color:white;
}

.footer{
    text-align:center;
    color:gray;
    padding-top:50px;
}

</style>
""", unsafe_allow_html=True)

# ===============================
# LOAD DATA
# ===============================

@st.cache_data
def load_data():
    df = pd.read_csv("data/kc_house_data.csv")
    return df

df = load_data()

# ===============================
# SIDEBAR
# ===============================

st.sidebar.image(
    "https://img.icons8.com/fluency/240/home.png",
    width=120
)

st.sidebar.title("🏠 House Price Prediction")

st.sidebar.markdown("---")

st.sidebar.success("Professional House Price Prediction Platform")

st.sidebar.markdown("""
### Navigation

🏠 Home

📊 Dashboard

🤖 Prediction

📈 Model Performance

💡 Business Insights

📂 Dataset Explorer

👨‍💻 About
""")

st.sidebar.markdown("---")

st.sidebar.info(
"""
Built using

✔ Python

✔ Streamlit

✔ Plotly

✔ Scikit-Learn

✔ Machine Learning
"""
)

# ===============================
# HOME PAGE
# ===============================

st.title("🏠 House Price Prediction")

st.subheader("House Price Prediction & Analytics Platform")

st.write("")

st.markdown("""
Welcome to **HouseVision AI**, an interactive Machine Learning application
built to analyze housing data, visualize market trends,
and predict house prices using predictive analytics.

This project demonstrates an end-to-end Data Science workflow including:

- Data Cleaning
- Exploratory Data Analysis
- Data Visualization
- Machine Learning
- Business Insights
- Model Deployment
""")

st.write("")

# ===============================
# KPI
# ===============================
st.markdown("## 📊 Executive Dashboard")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        label="🏠 Total Houses",
        value=f"{len(df):,}",
        delta=None
    )

with col2:

    st.metric(
        label="💰 Average Price",
        value=f"${df['price'].mean():,.0f}"
    )

with col3:

    st.metric(
        label="📈 Maximum Price",
        value=f"${df['price'].max():,.0f}"
    )


col4, col5, col6 = st.columns(3)

with col4:

    st.metric(
        label="📉 Minimum Price",
        value=f"${df['price'].min():,.0f}"
    )

with col5:

    st.metric(
        label="📐 Avg Living Area",
        value=f"{df['sqft_living'].mean():.0f} sqft"
    )

with col6:

    st.metric(
        label="🛏 Avg Bedrooms",
        value=f"{df['bedrooms'].mean():.1f}"
    )

st.divider()

st.write("")
st.write("")
# ======================================================
# DASHBOARD FILTERS
# ======================================================

st.markdown("## 🎛 Dashboard Filters")

col1, col2, col3 = st.columns(3)

with col1:

    price_range = st.slider(
        "Price Range ($)",
        int(df.price.min()),
        int(df.price.max()),
        (
            int(df.price.min()),
            int(df.price.max())
        )
    )

with col2:

    bedrooms = st.multiselect(
        "Bedrooms",
        sorted(df.bedrooms.unique()),
        default=sorted(df.bedrooms.unique())
    )

with col3:

    waterfront = st.selectbox(
        "Waterfront",
        ["All","Yes","No"]
    )

filtered_df = df[
    (df.price>=price_range[0]) &
    (df.price<=price_range[1]) &
    (df.bedrooms.isin(bedrooms))
]

if waterfront=="Yes":
    filtered_df=filtered_df[filtered_df.waterfront==1]

elif waterfront=="No":
    filtered_df=filtered_df[filtered_df.waterfront==0]

# ======================================================
# PRICE DISTRIBUTION
# ======================================================

st.markdown("## 💰 House Price Distribution")

fig = px.histogram(
    filtered_df,
    x="price",
    nbins=60,
    color="waterfront",
    template="plotly_dark",
    marginal="box"
)

fig.update_layout(
    height=500,
    title="Distribution of House Prices"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ======================================================
# LIVING AREA & BEDROOM ANALYSIS
# ======================================================

st.markdown("## 🏠 Property Analysis")


col1, col2 = st.columns(2)


with col1:

    fig = px.scatter(
        filtered_df,
        x="sqft_living",
        y="price",
        color="grade",
        template="plotly_dark",
        title="Living Area vs Price",
        hover_data=[
            "bedrooms",
            "bathrooms",
            "zipcode"
        ]
    )

    fig.update_layout(
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with col2:

    fig = px.box(
        filtered_df,
        x="bedrooms",
        y="price",
        template="plotly_dark",
        title="Bedrooms vs Price"
    )

    fig.update_layout(
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )



# ======================================================
# GRADE & CONDITION ANALYSIS
# ======================================================


st.markdown("## ⭐ House Quality Analysis")


col1, col2 = st.columns(2)


with col1:

    fig = px.box(
        filtered_df,
        x="grade",
        y="price",
        color="grade",
        template="plotly_dark",
        title="Impact of House Grade on Price"
    )

    fig.update_layout(
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with col2:

    fig = px.box(
        filtered_df,
        x="condition",
        y="price",
        color="condition",
        template="plotly_dark",
        title="Impact of Condition on Price"
    )

    fig.update_layout(
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
 # ======================================================
# ADVANCED ANALYTICS
# ======================================================

st.divider()

st.markdown("# 🚀 Advanced Market Analytics")


# ======================================================
# HOUSE LOCATION MAP
# ======================================================

st.markdown("## 🌍 House Price Map")


map_df = filtered_df.sample(
    min(2000, len(filtered_df))
)


fig = px.scatter_mapbox(
    map_df,
    lat="lat",
    lon="long",
    color="price",
    size="sqft_living",
    hover_name="zipcode",
    hover_data=[
        "price",
        "bedrooms",
        "bathrooms"
    ],
    zoom=9,
    height=600,
    template="plotly_dark"
)


fig.update_layout(
    mapbox_style="carto-darkmatter",
    margin={
        "r":0,
        "t":0,
        "l":0,
        "b":0
    }
)


st.plotly_chart(
    fig,
    use_container_width=True
)



# ======================================================
# CORRELATION HEATMAP
# ======================================================


st.markdown("## 🔥 Feature Correlation")


numeric_df = filtered_df.select_dtypes(
    include=["int64","float64"]
)


corr = numeric_df.corr()


fig = px.imshow(
    corr,
    text_auto=True,
    aspect="auto",
    color_continuous_scale="RdBu",
    title="Correlation Between Features"
)


fig.update_layout(
    height=700,
    template="plotly_dark"
)


st.plotly_chart(
    fig,
    use_container_width=True
)



# ======================================================
# HOUSE AGE ANALYSIS
# ======================================================


st.markdown("## 🏗️ House Age Analysis")


current_year = 2026


filtered_df["house_age"] = (
    current_year - filtered_df["yr_built"]
)


fig = px.histogram(
    filtered_df,
    x="house_age",
    nbins=40,
    template="plotly_dark",
    title="Distribution of House Age"
)


st.plotly_chart(
    fig,
    use_container_width=True
)



# ======================================================
# YEAR BUILT VS PRICE
# ======================================================


st.markdown("## 📅 Year Built Impact")


fig = px.scatter(
    filtered_df,
    x="yr_built",
    y="price",
    color="grade",
    size="sqft_living",
    template="plotly_dark",
    title="Construction Year vs Price"
)


st.plotly_chart(
    fig,
    use_container_width=True
)



# ======================================================
# ZIPCODE ANALYSIS
# ======================================================


st.markdown("## 📍 Location Pricing Analysis")


zipcode_price = (
    filtered_df
    .groupby("zipcode")["price"]
    .mean()
    .reset_index()
    .sort_values(
        "price",
        ascending=False
    )
    .head(15)
)


fig = px.bar(
    zipcode_price,
    x="zipcode",
    y="price",
    template="plotly_dark",
    title="Top 15 Expensive Zipcodes"
)


st.plotly_chart(
    fig,
    use_container_width=True
)
# ===============================
# DATASET OVERVIEW
# ===============================

st.subheader("Dataset Overview")

c1,c2=st.columns(2)

with c1:

    st.metric("Rows",df.shape[0])

    st.metric("Columns",df.shape[1])

with c2:

    st.metric("Missing Values",df.isnull().sum().sum())

    st.metric("Duplicate Rows",df.duplicated().sum())

st.write("")

st.dataframe(df.head())

# ===============================
# FEATURES
# ===============================

st.subheader("Features Used")

st.write(list(df.columns))

# ===============================
# TECHNOLOGIES
# ===============================

st.subheader("Technology Stack")

tech1,tech2,tech3=st.columns(3)

with tech1:

    st.success("""
Python

Pandas

NumPy
""")

with tech2:

    st.success("""
Plotly

Streamlit

Scikit-Learn
""")

with tech3:

    st.success("""
Machine Learning

Data Analytics

Visualization
""")

# ===============================
# PROJECT HIGHLIGHTS
# ===============================

st.subheader("Project Highlights")

st.info("""
✔ 21,000+ House Records

✔ Interactive Dashboard

✔ Machine Learning Prediction

✔ Business Insights

✔ Plotly Visualizations

✔ Professional UI

✔ Recruiter Ready Project
""")

# ===============================
# FOOTER
# ===============================

st.markdown("---")

st.markdown(
"""
<div class="footer">

Made by <b>Yash Kataria</b>

HouseVision AI • Data Science Portfolio Project

</div>
""",
unsafe_allow_html=True
)