import streamlit as st



def button(text,alignment,type='secondary',height='3em',width='7em',bg='white',size='20px'):

  styles=f"""
<style>      
div[data-testid="stButton"] > button {{
  height: {height};
  width: {width};
  background-color: {bg}
}}

div[data-testid="stButton"] p {{
  font-size: {size};
}}

div[data-testid="stButton"] {{
  display: flex;
  justify-content: {alignment};
}}
</style>
"""

  st.markdown(
styles,
      unsafe_allow_html=True
  )

  return st.button(text,width="stretch" if alignment=='right' or alignment=='center' else "content",type=type)