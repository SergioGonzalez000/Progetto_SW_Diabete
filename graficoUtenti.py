import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Genera dati fittizi per diversi intervalli temporali
np.random.seed(42)

# Giorni (ultimi 30 giorni)
date_days = pd.date_range(end=pd.Timestamp.today(), periods=30)
y_days = np.random.rand(30) * 100

# Settimane (ultime 20 settimane)
date_weeks = pd.date_range(end=pd.Timestamp.today(), periods=20, freq='W')
y_weeks = np.random.rand(20) * 100

# Mesi (ultimi 12 mesi)
date_months = pd.date_range(end=pd.Timestamp.today(), periods=12, freq='ME')
y_months = np.random.rand(12) * 100

# Anni (ultimi 10 anni)
date_years = pd.date_range(end=pd.Timestamp.today(), periods=10, freq='YE')
y_years = np.random.rand(10) * 100

# Tracce
trace_days = go.Scatter(x=date_days, y=y_days, mode='lines+markers', name='Giorni')
trace_weeks = go.Scatter(x=date_weeks, y=y_weeks, mode='lines+markers', name='Settimane')
trace_months = go.Scatter(x=date_months, y=y_months, mode='lines+markers', name='Mesi')
trace_years = go.Scatter(x=date_years, y=y_years, mode='lines+markers', name='Anni')

# Layout con menu a tendina
fig = go.Figure()

# Aggiungi tutte le tracce (inizialmente nascoste tranne una)
fig.add_trace(trace_days)
fig.add_trace(trace_weeks)
fig.add_trace(trace_months)
fig.add_trace(trace_years)

# Mostra solo "giorni" inizialmente
fig.update_traces(visible=False)
fig.data[0].visible = True

# Dropdown per selezione intervallo
fig.update_layout(
    updatemenus=[
        dict(
            active=0,
            buttons=list([
                dict(label="Giorni", method="update", args=[{"visible": [True, False, False, False]}, {"title": "Valori giornalieri"}]),
                dict(label="Settimane", method="update", args=[{"visible": [False, True, False, False]}, {"title": "Valori settimanali"}]),
                dict(label="Mesi", method="update", args=[{"visible": [False, False, True, False]}, {"title": "Valori mensili"}]),
                dict(label="Anni", method="update", args=[{"visible": [False, False, False, True]}, {"title": "Valori annuali"}]),
            ]),
            direction="down"
        )
    ],
    title="Valori temporali (interattivi)",
    xaxis_title="Data",
    yaxis_title="Valore Y",
    template="plotly_dark"
)

fig.show()
