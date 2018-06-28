import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from main import app
from viz_apps import app1, app2


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/viz/viz1':
         return app1.layout
    elif pathname == '/viz/viz2':
         return app2.layout
    else:
        return "404"


if __name__ == '__main__':
    app.run_server(host="0.0.0.0", debug=True)
