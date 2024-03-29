import dash
from mc_simulation.layout import APP_LAYOUT
import dash_bootstrap_components as dbc


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = APP_LAYOUT
app.run_server(debug=True)