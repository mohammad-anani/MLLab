import streamlit as st
from util.to_roman import to_roman
from util.routeButton import routeButton
from util.config import route_names
from routes.dataRoutes.upload import uploadPage
from routes.home import homePage
from routes.dataRoutes.target import targetPage
from routes.dataRoutes.drop import dropPage
from routes.dataRoutes.filter import filterPage
from routes.dataRoutes.impute import imputePage
from routes.dataRoutes.encode import encodePage
from routes.dataRoutes.finalize import finalizePage
from routes.dataRoutes.review import reviewPage
from routes.modelRoutes.choose import choosePage 
from routes.modelRoutes.tune import tunePage 
from routes.modelRoutes.ensemble import ensemblePage 
from routes.modelRoutes.report import reportPage  
from routes.modelRoutes.review import review2Page
from routes.predict import predictPage


routes = {name: globals()[f"{name}Page"] for name in route_names}
sections=[('Data',1,8),('Model',9,13),('Predict',14,14)]

if 'page' not in st.session_state:
  st.session_state.page=route_names[0]

if 'data' not in st.session_state:
  st.session_state.data={}
if 'model' not in st.session_state:
  st.session_state.model={}

page=st.session_state.page
page_index=route_names.index(page)

def get_section_index():
  for i, (_, start, end) in enumerate(sections):
    if start <= page_index <= end:
      return i
  return None

section_index=get_section_index()

if page_index>0:
  routeButton("Back","left",route_names[page_index-1])

if section_index!=None:
  st.title(to_roman(section_index+1)+"- "+sections[section_index][0])
  
routes.get(st.session_state.page, homePage)()

