import streamlit as st
import pandas as pd

# Load dataset
df = pd.read_csv("your_file_name.csv")

# Convert dates
df["Due_Date"] = pd.to_datetime(df["Due_Date"])
df["Payment_Date"] = pd.to_datetime(df["Payment_Date"], errors='coerce')

# Fill missing delay values
df["Delay_Days"] = df["Delay_Days"].fillna(0)

st.title("B2B Payment Dashboard")

# 🔹 KPI Section
total = len(df)
paid = len(df[df["Payment_Status"] == "Paid"])
pending = len(df[df["Payment_Status"] != "Paid"])
avg_delay = df["Delay_Days"].mean()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Invoices", total)
col2.metric("Paid Invoices", paid)
col3.metric("Pending Payments", pending)
col4.metric("Avg Delay Days", round(avg_delay, 2))

# 🔹 Filters
region = st.selectbox("Select Region", df["Region"].unique())
client = st.selectbox("Select Client", df["Client_Name"].unique())

filtered_df = df[(df["Region"] == region) & (df["Client_Name"] == client)]

# 🔹 Payments by Region
st.subheader("Payments by Region")
region_data = df.groupby("Region")["Invoice_Amount"].sum()
st.bar_chart(region_data)

# 🔹 Status Distribution
st.subheader("Invoice Status Distribution")
status_data = df["Payment_Status"].value_counts()
st.bar_chart(status_data)

# 🔹 Delay Trend
st.subheader("Delay Trend Analysis")
trend = df.groupby(df["Due_Date"].dt.month)["Delay_Days"].mean()
st.line_chart(trend)

# 🔹 Revenue Trend
st.subheader("Revenue Collection Trend")
revenue = df.groupby("Due_Date")["Invoice_Amount"].sum()
st.line_chart(revenue)

# 🔹 Show Filtered Data
st.subheader("Filtered Data")
st.dataframe(filtered_df)
