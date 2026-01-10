import streamlit as st
import pandas as pd

styles="""
<style>      
div[data-testid="stButton"] > button {
  height: 3em;
  width: 7em;
  background-color: white
}

div[data-testid="stButton"] p {
  font-size: 20px;
}

div[data-testid="stButton"] {
  display: flex;
  justify-content: right;
}
</style>
"""

def targetPage():
  st.markdown(
styles,
      unsafe_allow_html=True
  )

  st.title("I-Data")

  st.subheader("2-Specify your target column (aka Label)")

  if 'label' not in st.session_state:
    select_label_ui()
  else:
    confirm_label_ui()


def select_label_ui():
  
  df=st.session_state.df
  cols=df.columns

  label=st.selectbox("",cols,index=None)

  if label:
    st.session_state.label = label
    st.rerun()

def confirm_label_ui():
  label=st.session_state.label
  
  st.dataframe(df.head())
  st.text(f"{row_count} rows\n{col_count} columns")
  if st.button("Next",width="stretch"):
    st.session_state.page = "target" 
    st.rerun() 
