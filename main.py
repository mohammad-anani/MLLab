import streamlit as st
from routes.dataRoutes.upload import uploadPage
from routes.home import homePage
from routes.dataRoutes.target import targetPage



ROUTES = {
    "home": homePage,
    "upload": uploadPage,
    "target": targetPage,
}

ROUTES.get(st.session_state.page, homePage)()
