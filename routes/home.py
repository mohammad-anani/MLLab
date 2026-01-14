import streamlit as st
from util.routeButton import routeButton


def homePage():
  st.title("🤖 ML Lab 🧪", text_alignment="center")
  st.subheader("Welcome to the Machine Learning Lab where you can configure your model without writing a line of code!", text_alignment="center")
  routeButton("Start",alignment="center",route="upload", type="primary",height='5em',width='20em',bg='#27b446ff',size='38px')