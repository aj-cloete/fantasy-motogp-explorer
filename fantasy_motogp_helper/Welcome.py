import streamlit as st
from streamlit_extras.app_logo import add_logo

st.set_page_config(layout="wide")
st.markdown("# Welcome to Fantasy MotoGP Helper!")
st.sidebar.markdown("# Welcome!")


@st.cache_data
def logo():
    return add_logo("https://www.motogp.com/resources/v6.3.5/i/svg-files/elements/motogp-logo.svg", height=46)


logo()
