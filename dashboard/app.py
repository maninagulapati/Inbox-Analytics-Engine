import streamlit as st
import pandas as pd
import os
import plotly.express as px
import numpy as np

st.set_page_config(layout="wide")
st.title("📈 Email Report Dashboard")

UPLOAD_DIR = "data/uploads"
folders = [f for f in os.listdir(UPLOAD_DIR) if os.path.isdir(os.path.join(UPLOAD_DIR, f))]

if not folders:
    st.warning("No uploaded reports yet.")
    st.stop()

selected_report = st.selectbox("📁 Choose a report", folders)
sheets_path = os.path.join(UPLOAD_DIR, selected_report)
csv_files = [f for f in os.listdir(sheets_path) if f.endswith(".csv")]

selected_sheet = st.selectbox("📄 Choose a sheet", csv_files)
df = pd.read_csv(os.path.join(sheets_path, selected_sheet))

# Try to parse a date column
date_col = None
for col in df.columns:
    try:
        df[col] = pd.to_datetime(df[col])
        date_col = col
        break
    except:
        continue

numeric_cols = df.select_dtypes(include="number").columns.tolist()
categorical_cols = df.select_dtypes(include="object").nunique()
categorical_cols = categorical_cols[categorical_cols < 20].index.tolist()

# Clean nulls and outliers
df.dropna(thresh=len(df.columns) - 1, inplace=True)
for col in numeric_cols:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    df = df[(df[col] >= Q1 - 1.5 * IQR) & (df[col] <= Q3 + 1.5 * IQR)]

# Data Preview
st.subheader("📊 Sheet Data Preview")
st.dataframe(df)

# Data Summary
st.subheader("📋 Data Summary")
st.write(df.describe(include="all"))

# KPI Cards
if numeric_cols:
    st.subheader("📌 Key Performance Indicators")
    cols = st.columns(min(3, len(numeric_cols)))
    for i, col in enumerate(numeric_cols[:3]):
        value = df[col].sum()
        cols[i].metric(label=col, value=f"{value:,.2f}")

# Time Series Trends
if date_col and numeric_cols:
    st.subheader("📈 Time Series Trends")
    df = df.sort_values(by=date_col)
    for col in numeric_cols[:3]:
        fig = px.line(df, x=date_col, y=col, title=f"{col} over time")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("📅 Quarterly Progress")
    df["Quarter"] = df[date_col].dt.to_period("Q").astype(str)
    qdata = df.groupby("Quarter")[numeric_cols].sum().reset_index()
    fig = px.line(qdata, x="Quarter", y=numeric_cols, markers=True)
    st.plotly_chart(fig, use_container_width=True)

# Pie Chart for Region-like columns
if categorical_cols:
    st.subheader("🗺️ Category Distribution")
    cat_col = st.selectbox("Choose a category", categorical_cols)
    pie_data = df[cat_col].value_counts().reset_index()
    pie_data.columns = [cat_col, "count"]
    fig = px.pie(pie_data, names=cat_col, values="count", hole=0.4)
    st.plotly_chart(fig, use_container_width=True)

# Manual Chart Explorer
if numeric_cols:
    st.subheader("🧪 Manual Chart Explorer")
    x = st.selectbox("X-axis", df.columns)
    y = st.selectbox("Y-axis", numeric_cols)
    chart = st.selectbox("Chart Type", ["Line", "Bar", "Area", "Scatter"])

    if chart == "Line":
        fig = px.line(df, x=x, y=y)
    elif chart == "Bar":
        fig = px.bar(df, x=x, y=y)
    elif chart == "Area":
        fig = px.area(df, x=x, y=y)
    elif chart == "Scatter":
        fig = px.scatter(df, x=x, y=y)

    st.plotly_chart(fig, use_container_width=True)
