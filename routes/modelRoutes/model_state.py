import streamlit as st

class ModelState:
    def __getattr__(self, key):
        try:
            return st.session_state.model[key]
        except KeyError:
             raise AttributeError(f"'{type(self).__name__}' object has no attribute '{key}'")

    def __setattr__(self, key, value):
        st.session_state.model[key] = value

    def __getitem__(self, key):
        return st.session_state.model[key]

    def __setitem__(self, key, value):
        st.session_state.model[key] = value

    def __contains__(self, key):
        return key in st.session_state.model
    
    def get(self, key, default=None):
        return st.session_state.model.get(key, default)

def model_state():
  return ModelState()