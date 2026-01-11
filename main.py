import streamlit as st
from routes.dataRoutes.upload import uploadPage
from routes.home import homePage
from routes.dataRoutes.target import targetPage
from routes.dataRoutes.drop import dropPage
from routes.dataRoutes.filter import filterPage



if 'page' not in st.session_state:
  st.session_state.page='home'


ROUTES = {
    "home": homePage,
    "upload": uploadPage,
    "target": targetPage,
    "drop":dropPage,
    "filter":filterPage
}

ROUTES.get(st.session_state.page, homePage)()
