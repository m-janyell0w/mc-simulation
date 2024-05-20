import dash
from mc_simulation.layout import APP_LAYOUT
import dash_bootstrap_components as dbc
from mc_simulation.callbacks import mc_simulation_callbacks


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.COSMO])
app.layout = APP_LAYOUT
app.run_server(debug=True)
