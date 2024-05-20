import dash
from mc_simulation.frontend.layout import APP_LAYOUT
import dash_bootstrap_components as dbc
from mc_simulation.backend.callbacks import mc_simulation_callbacks


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app.layout = APP_LAYOUT
app.run_server(debug=True)
