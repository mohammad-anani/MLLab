from .routeButton import routeButton
from util.config import route_names
import streamlit as st

def nextButton():
  page=st.session_state.page
  page_index=route_names.index(page)

  if page_index<len(route_names)-1:
    routeButton("Next",'right',route_names[page_index+1])