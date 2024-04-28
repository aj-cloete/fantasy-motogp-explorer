import streamlit as st
from common.resources import logo
from fantasy import FantasyStats
from st_aggrid import AgGrid, GridOptionsBuilder

st.set_page_config(
    page_icon="https://www.motogp.com/resources/v6.3.5/i/svg-files/elements/motogp-logo.svg",
    layout="wide",
)

logo()

st.header("Constructors 🏍️")

# Generate tabs
(t_basic, t_stats, t_history, t_explore) = st.tabs(["Basic Info", "Point Stats", "History", "Explore"])

with st.spinner("Loading data"):
    data = FantasyStats().constructors

with t_basic:
    gb = GridOptionsBuilder.from_dataframe(data.info, resizable=True, wrapHeaderText=True, autoHeaderHeight=True)
    gb.configure_side_bar()
    gb.configure_first_column_as_index(resizable=True)
    go = gb.build()
    for col_def in go["columnDefs"]:
        name = col_def["field"]
        col_def["width"] = min(95, 40 + max([len(x) * 7 for x in name.split(" ")]))
    grid = AgGrid(data.info, go, key="basic", fit_columns_on_grid_load=True, update_on=["stateChanged"])

with t_stats:
    gb = GridOptionsBuilder.from_dataframe(
        data.stats,
        resizable=True,
        wrapHeaderText=True,
        autoHeaderHeight=True,
    )
    gb.configure_side_bar()
    gb.configure_first_column_as_index(resizable=True)
    go = gb.build()
    for col_def in go["columnDefs"]:
        name = col_def["field"]
        col_def["width"] = min(95, 40 + max([len(x) * 7 for x in name.split(" ")]))
    grid = AgGrid(data.stats, go, key="stats", fit_columns_on_grid_load=True, update_on=["stateChanged"])

with t_history:
    gb = GridOptionsBuilder.from_dataframe(data.history, resizable=True, wrapHeaderText=True, autoHeaderHeight=True)
    gb.configure_side_bar()
    gb.configure_first_column_as_index(resizable=True)
    go = gb.build()
    for col_def in go["columnDefs"]:
        name = col_def["field"]
        col_def["width"] = min(95, 40 + max([len(x) * 7 for x in name.split(" ")]))
    grid = AgGrid(data.history, go, key="history", fit_columns_on_grid_load=True, update_on=["stateChanged"])

# with t_explore:
#     df = data.basic_info
#     gb = GridOptionsBuilder.from_dataframe(df)
#     go = gb.build()
#     ag = AgGrid(
#         df,
#         fit_columns_on_grid_load=True,
#         update_on=["stateChanged"],
#         enable_enterprise_modules=True,
#     )
