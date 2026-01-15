import streamlit as st
from routes.modelRoutes.model_state import model_state
from util.nextButton import nextButton

def review2Page():
  st.subheader("Model Configuration Review")

  review_model_basic()
  review_model_tuning()
  review_ensemble()
  nextButton()


def review_model_basic():
  st.subheader("a- Selected Model:")
  model_name = model_state().model
  st.write(markdown_bold("Name:") + " " + model_name)


def review_model_tuning():
  st.subheader("b- Hyperparameter Tuning:")
  tuning = model_state().tuning
  if not tuning or all(v is None for v in tuning.values()):
    st.write("No custom hyperparameter tuning applied.")
    return

  for param, value in tuning.items():
    st.write(markdown_bold(param) + ": " + str(value))


def review_ensemble():
  st.subheader("c- Ensemble Method:")
  ensemble = model_state().ensemble
  method = ensemble.get("method", "None")
  st.write(markdown_bold("Method:") + " " + method)

  if method != "None":
    # Show ensemble-specific parameters
    for param, value in ensemble.items():
      if param != "method":
        st.write(markdown_bold(param) + ": " + str(value))


# Utility functions
def markdown_bold(text):
  return "**" + str(text) + "**"
