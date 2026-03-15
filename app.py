import streamlit as st
import plotly.graph_objects as go
from backend.oi_levels import get_oi_levels

st.set_page_config(layout="wide", page_title="OI Levels")

# Header simple
st.markdown("# Options Market Structure")

data = get_oi_levels()
spot = data["spot"]

# Grid de métricas
metrics = st.columns(5)
metrics[0].metric("Spot", f"${spot:,.0f}")

resistances = data["top_resistances"]["strike"][:3]
for i, r in enumerate(resistances):
    metrics[i+1].metric(f"R{i+1}", f"${r:,.0f}", delta=f"+{r-spot:,.0f}")

supports = data["top_supports"]["strike"][:1]
if len(supports) > 0:
    metrics[4].metric("S1", f"${supports[0]:,.0f}", delta=f"-{spot-supports[0]:,.0f}")

# Gráfico limpio
fig = go.Figure()

all_levels = [spot] + list(resistances) + list(supports)
fig.add_trace(go.Scatter(x=[0], y=[spot], mode='markers', marker=dict(size=0), showlegend=False))

fig.add_hline(y=spot, line_width=3, line_color="white", 
              annotation_text=f"${spot:,.0f}", annotation_position="left")

for strike in resistances:
    fig.add_hline(y=strike, line_color="crimson", line_dash="dot",
                  annotation_text=f"${strike:,.0f}", annotation_position="left")

for strike in supports:
    fig.add_hline(y=strike, line_color="limegreen", line_dash="dot",
                  annotation_text=f"${strike:,.0f}", annotation_position="left")

fig.update_layout(
    height=500,
    template="plotly_dark",
    showlegend=False,
    yaxis=dict(showgrid=False, range=[min(all_levels)*0.98, max(all_levels)*1.02]),
    xaxis=dict(showticklabels=False, showgrid=False, range=[-0.5, 0.5]),
    margin=dict(l=100, r=100, t=30, b=30)
)

st.plotly_chart(fig, use_container_width=True)
