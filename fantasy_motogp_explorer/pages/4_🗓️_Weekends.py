import streamlit as st
from st_aggrid import GridOptionsBuilder, AgGrid

from common.resources import logo
from fantasy import FantasyStats
from streamlit_extras.dataframe_explorer import dataframe_explorer

st.set_page_config(layout="wide")

logo()
st.title("Weekends 🗓️")

with st.spinner("Loading data"):
    data = FantasyStats().weekends

t_schedule, t_events = st.tabs(["Year Schedule", "Weekend Events"])
with t_schedule:
    schedule = (
        data.info
        .sort_values(["status", "start"], ascending=[False, True])
        [["displayed_name"]+list(col for col in data.info.columns if col != "displayed_name")]
    )
    schedule.columns = [col.replace("_", " ").title() for col in schedule.columns]
    gb = GridOptionsBuilder.from_dataframe(
        schedule,
        resizable=True,
        wrapHeaderText=True,
        autoHeaderHeight=True
    )
    gb.configure_side_bar()
    gb.configure_first_column_as_index(resizable=True)
    go = gb.build()
    grid = AgGrid(
        schedule,
        go,
        key="schedule",
        fit_columns_on_grid_load=True,
        update_on=["stateChanged"]
    )

with t_events:
    events = (
        data.info[["displayed_name"]]
        .join(data.events).sort_values(["status", "event_id"], ascending=[False, True])
    )
    events = events[["displayed_name"]+list(col for col in events.columns if col != "displayed_name")]
    events.columns = [col.replace("_", " ").title() for col in events.columns]
    gb = GridOptionsBuilder.from_dataframe(
        events,
        resizable=True,
        wrapHeaderText=True,
        autoHeaderHeight=True
    )
    gb.configure_side_bar()
    gb.configure_first_column_as_index(resizable=True)
    go = gb.build()
    for col_def in go["columnDefs"]:
        name = col_def["field"]
        col_def["width"] = min(95, 100 + max([len(x) * 7 for x in name.split(" ")]))
    grid = AgGrid(
        events,
        go,
        key="events",
        fit_columns_on_grid_load=True,
        update_on=["stateChanged"]
    )
