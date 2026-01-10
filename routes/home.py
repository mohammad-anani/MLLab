import streamlit as st

styles="""
<style>
div[data-testid="stButton"] > button {
  height: 5em;
  width: 20em;
}

  div[data-testid="stButton"] p {
  font-size: 38px;
}

div[data-testid="stButton"] {
  display: flex;
  justify-content: center;
}
</style>
"""

def homePage():
  st.markdown(
styles,
unsafe_allow_html=True
)

  st.title("🤖 ML Lab 🧪", text_alignment="center"
  )

  st.subheader("Welcome to the Machine Learning Lab where you can configure your model without writing a line of code!", text_alignment="center"
  )

  if st.button("Start", type="primary",width="stretch"):
    st.session_state.page = "upload" 
    st.rerun() 
