from util.button import button
import streamlit as st

def routeButton(text,alignment,route,type='secondary',height='3em',width='7em',bg='white',size='20px'):
  if button(text,alignment,type,height,width,bg,size):
    st.session_state.page = route 
    st.rerun() 