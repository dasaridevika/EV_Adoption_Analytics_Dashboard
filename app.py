# app.py

import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="EV Adoption Dashboard",
    page_icon="🚗",
    layout="wide"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

[data-testid="metric-container"]{
    background-color:#1F2937;
    border:1px solid #374151;
    padding:15px;
    border-radius:15px;
    box-shadow:0px 4px 12px rgba(0,0,0,0.15);
}

[data-testid="metric-container"] label{
    color:white !important;
}

[data-testid="metric-container"] div{
    color:white !important;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

df = pd.read_csv("ev_cleaned.csv")

# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.title("🚗 EV Dashboard")

city = st.sidebar.multiselect(
    "Select City Type",
    options=df["city_type"].dropna().unique(),
    default=df["city_type"].dropna().unique()
)

education = st.sidebar.multiselect(
    "Select Education Level",
    options=df["education_level"].dropna().unique(),
    default=df["education_level"].dropna().unique()
)

df = df[
    (df["city_type"].isin(city)) &
    (df["education_level"].isin(education))
]

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🚗 EV Adoption Analysis Dashboard")
st.markdown("---")

# --------------------------------------------------
# KPI SECTION
# --------------------------------------------------

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Total Respondents",
    f"{len(df):,}"
)

col2.metric(
    "Avg Income",
    f"{df['annual_income'].mean():,.0f}"
)

col3.metric(
    "Avg Awareness",
    round(df["environmental_awareness_score"].mean(), 2)
)

col4.metric(
    "Avg Anxiety",
    round(df["range_anxiety_score"].mean(), 2)
)

high_pct = (
    (df["ev_adoption_likelihood"] == "High")
    .mean() * 100
)

col5.metric(
    "High Adoption %",
    f"{high_pct:.2f}%"
)

st.markdown("---")

# --------------------------------------------------
# DONUT CHART
# --------------------------------------------------

st.subheader("📊 EV Adoption Distribution")

adoption_count = (
    df["ev_adoption_likelihood"]
    .value_counts()
    .reset_index()
)

adoption_count.columns = ["Adoption", "Count"]

fig_donut = px.pie(
    adoption_count,
    names="Adoption",
    values="Count",
    hole=0.55,
    color="Adoption",
    color_discrete_map={
        "High": "#00C853",
        "Medium": "#FFD600",
        "Low": "#D50000"
    }
)

fig_donut.update_layout(
    paper_bgcolor="#F5F7FA",
    plot_bgcolor="#F5F7FA"
)

st.plotly_chart(
    fig_donut,
    use_container_width=True
)

# --------------------------------------------------
# INCOME ANALYSIS
# --------------------------------------------------

income_analysis = (
    df.groupby("ev_adoption_likelihood")["annual_income"]
    .mean()
    .reset_index()
)

fig_income = px.bar(
    income_analysis,
    x="ev_adoption_likelihood",
    y="annual_income",
    color="ev_adoption_likelihood",
    title="💰 Income Influence on EV Adoption",
    color_discrete_map={
        "High": "#00C853",
        "Medium": "#FFD600",
        "Low": "#D50000"
    }
)

fig_income.update_layout(showlegend=False)

# --------------------------------------------------
# AWARENESS ANALYSIS
# --------------------------------------------------

awareness_analysis = (
    df.groupby("ev_adoption_likelihood")[
        "environmental_awareness_score"
    ]
    .mean()
    .reset_index()
)

fig_awareness = px.bar(
    awareness_analysis,
    x="ev_adoption_likelihood",
    y="environmental_awareness_score",
    color="ev_adoption_likelihood",
    title="🌱 Environmental Awareness",
    color_discrete_map={
        "High": "#00C853",
        "Medium": "#FFD600",
        "Low": "#D50000"
    }
)

fig_awareness.update_layout(showlegend=False)

# --------------------------------------------------
# RANGE ANXIETY
# --------------------------------------------------

anxiety_analysis = (
    df.groupby("ev_adoption_likelihood")[
        "range_anxiety_score"
    ]
    .mean()
    .reset_index()
)

fig_anxiety = px.bar(
    anxiety_analysis,
    x="ev_adoption_likelihood",
    y="range_anxiety_score",
    color="ev_adoption_likelihood",
    title="🔋 Range Anxiety",
    color_discrete_map={
        "High": "#00C853",
        "Medium": "#FFD600",
        "Low": "#D50000"
    }
)

fig_anxiety.update_layout(showlegend=False)

# --------------------------------------------------
# HOME CHARGING
# --------------------------------------------------

charging_analysis = (
    df.groupby("ev_adoption_likelihood")[
        "home_charging_available"
    ]
    .mean()
    .reset_index()
)

charging_analysis[
    "home_charging_available"
] *= 100

fig_charge = px.bar(
    charging_analysis,
    x="ev_adoption_likelihood",
    y="home_charging_available",
    color="ev_adoption_likelihood",
    title="🏠 Home Charging Availability",
    color_discrete_map={
        "High": "#00C853",
        "Medium": "#FFD600",
        "Low": "#D50000"
    }
)

fig_charge.update_layout(showlegend=False)

# --------------------------------------------------
# 2 X 2 GRID
# --------------------------------------------------

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(
        fig_income,
        use_container_width=True
    )

with col2:
    st.plotly_chart(
        fig_awareness,
        use_container_width=True
    )

st.markdown("---")

col3, col4 = st.columns(2)

with col3:
    st.plotly_chart(
        fig_anxiety,
        use_container_width=True
    )

with col4:
    st.plotly_chart(
        fig_charge,
        use_container_width=True
    )


# --------------------------------------------------
# HEATMAP
# --------------------------------------------------

st.markdown("---")
st.subheader("📈 Correlation Heatmap")

numeric_df = df.select_dtypes(include="number")

corr = numeric_df.corr()

fig, ax = plt.subplots(figsize=(12, 8))

sns.heatmap(
    corr,
    annot=True,
    fmt=".2f",
    cmap="RdYlGn",
    ax=ax
)

st.pyplot(fig)

# --------------------------------------------------
# KEY FINDINGS
# --------------------------------------------------

st.markdown("---")

st.header("📌 Executive Summary")

st.success("""
✅ Higher income increases EV adoption.

✅ Environmental awareness positively influences EV adoption.

✅ Home charging availability improves adoption.

✅ Range anxiety reduces EV adoption likelihood.

✅ EV knowledge and technology affinity support EV adoption.
""")

# --------------------------------------------------
# DOWNLOAD DATA
# --------------------------------------------------

csv = df.to_csv(index=False)

st.download_button(
    label="📥 Download Filtered Dataset",
    data=csv,
    file_name="ev_filtered.csv",
    mime="text/csv"
)