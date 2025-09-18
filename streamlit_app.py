import streamlit as st
import pandas as pd

# Load CSV
df = pd.read_csv("security_id_list.csv")

# Preprocess lowercase columns for searching
df["SM_SYMBOL_NAME_LC"] = df["SM_SYMBOL_NAME"].astype(str).str.lower()
df["SEM_TRADING_SYMBOL_LC"] = df["SEM_TRADING_SYMBOL"].astype(str).str.lower()
df["SEM_EXM_EXCH_ID_LC"] = df["SEM_EXM_EXCH_ID"].astype(str).str.lower()
df["SEM_INSTRUMENT_NAME_LC"] = df["SEM_INSTRUMENT_NAME"].astype(str).str.lower()

st.title("Security Search and Filter")

# Search input
search_text = st.text_input("Search by Symbol, Name, ID, etc.")

# Dropdown filters
exchanges = [""] + sorted(df["SEM_EXM_EXCH_ID"].dropna().unique().tolist())
instruments = [""] + sorted(df["SEM_INSTRUMENT_NAME"].dropna().unique().tolist())

selected_exchange = st.selectbox("Select Exchange", exchanges)
selected_instrument = st.selectbox("Select Instrument", instruments)

# Filter dataframe
filtered_df = df

if search_text:
    q = search_text.lower()
    filtered_df = filtered_df[
        filtered_df["SM_SYMBOL_NAME_LC"].str.contains(q, na=False) |
        filtered_df["SEM_TRADING_SYMBOL_LC"].str.contains(q, na=False)
    ]

if selected_exchange:
    filtered_df = filtered_df[filtered_df["SEM_EXM_EXCH_ID"] == selected_exchange]

if selected_instrument:
    filtered_df = filtered_df[filtered_df["SEM_INSTRUMENT_NAME"] == selected_instrument]

st.write(f"Showing {len(filtered_df)} result(s)")

# Display results as table
st.dataframe(filtered_df[[
    "SEM_TRADING_SYMBOL", "SM_SYMBOL_NAME", "SEM_SMST_SECURITY_ID",
    "SEM_INSTRUMENT_NAME", "SEM_EXM_EXCH_ID", "SEM_EXPIRY_DATE", "SEM_STRIKE_PRICE"
]])
