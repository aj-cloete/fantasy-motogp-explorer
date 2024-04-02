import time

import streamlit as st
from streamlit_extras.dataframe_explorer import dataframe_explorer

from fantasy import FantasyStats

st.title("Weekends 🗓️")
# st.sidebar.markdown("# Weekends 🗓️")

data = FantasyStats().weekends
schedule, events = st.tabs(["Year Schedule", "Weekend Events"])
with schedule:
    st.table(
        dataframe_explorer(
            data.info.sort_values(["status", "start"], ascending=[False, True]),
            case=False
        )
    )
with events:
    st.table(
        dataframe_explorer(
            data.info[["name", "displayed_name"]].join(data.events).sort_values(["status", "event_id"], ascending=[False, True]),
            case=False
        )
    )
