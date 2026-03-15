import streamlit as st
import plotly.graph_objects as go

from backend.oi_levels import get_oi_levels

st.title("Options Market Structure")

data = get_oi_levels()

spot = data["spot"]

fig = go.Figure()

fig.add_hline(y=spot, line_color="white", annotation_text="Spot")

for strike in data["top_resistances"]["strike"]:
    fig.add_hline(y=strike, line_color="red")

for strike in data["top_supports"]["strike"]:
    fig.add_hline(y=strike, line_color="green")

st.plotly_chart(fig)
