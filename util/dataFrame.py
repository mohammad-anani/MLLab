import streamlit as st
import pandas as pd

def dataFrame(df):
  row_count,col_count=df.shape

  st.dataframe(df.head())
  st.text(f"{row_count} rows\n{col_count} columns")