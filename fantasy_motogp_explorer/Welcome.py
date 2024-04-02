import streamlit as st

from common.resources import logo

st.set_page_config(layout="wide")

logo()

st.title("Welcome to Fantasy MotoGP Explorer!")
st.subheader("Explore all the data related to the Fantasy MotoGP game")
st.markdown("We have 4 sections to choose from.  Each section contains basic info and some more detailed information.")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.page_link("pages/1_🚴_Riders.py", label="**Riders**", icon="🚴")
    st.markdown("All the riders in the MotoGP fantasy game")

with col2:
    st.page_link("pages/2_🏍️_Constructors.py", label="**Constructors**", icon="🏍️")
    st.markdown("All the constructors in the MotoGP fantasy game")

with col3:
    st.page_link("pages/3_🛠️_Teams.py", label="**Teams**", icon="🛠")
    st.markdown("All the teams in the MotoGP fantasy game")

with col4:
    st.page_link("pages/4_🗓️_Weekends.py", label="**Weekends**", icon="🗓")
    st.markdown("All the weekends with MotoGP action along with their times (in UTC)")
