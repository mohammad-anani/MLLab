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

def uploadPage():
  st.markdown(
styles,
      unsafe_allow_html=True
  )

  st.title("I-Data")

  st.subheader("1-Upload you data(csv only)")

  if 'df' not in st.session_state:
    file_uploader_ui()
  else:
    loaded_dataset_ui()


def file_uploader_ui():
  uploaded_file= st.file_uploader("", type="csv")

  if uploaded_file:
    try:
      df = pd.read_csv(uploaded_file)
      st.session_state.df = df
      st.rerun() 
    except Exception as e:
      st.error("Error in file uploading. Try again")

def loaded_dataset_ui():
  df=st.session_state.df
  row_count,col_count=df.shape
  
  st.dataframe(df.head())
  st.text(f"{row_count} rows\n{col_count} columns")
  if st.button("Next",width="stretch"):
    st.session_state.page = "target" 
    st.rerun() 