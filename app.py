from dash import Dash, html
import dash_bootstrap_components as dbc
from rcg_web.code.formatting import container_content, nav, faq

### TODO: add calendar picker and webhooks
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.SLATE]
    )
app.title= "Rap Caviar Gender Tracker"
server = app.server

app.layout = html.Div(
    children=[
        html.A(id="Top"),
        dbc.Container([  
        dbc.Row(
            dbc.Col(
                container_content['title'],
                width={"size":True}
            ), style={"margin-bottom":"0rem"}
        ),
        # date
        dbc.Row(
            dbc.Col(container_content['date'], 
                width={"size":True})
        ),
        dbc.Row(
            dbc.Col(nav)
        ),

        # count
        html.A(id="Count"),
        dbc.Row(
            children=container_content['full_count']
        ),

        # bar chart
        html.A(id="bar_chart"),
        dbc.Row(children=container_content['bar_chart'],
            style={'margin':"2rem 0rem"}
            ),

        # tally
        html.A(id="Tally"),
        dbc.Row(
            children=container_content['tally'],
            style={'margin':"2rem 0rem"}
                ),

         # full chart
        html.A(id="Chart"),
        dbc.Row(
            children=container_content['full_chart'],
            style={'margin':"2rem 0rem"}
        ),
        # full chart
        # html.A(id="Chart"),
        # dbc.Row(container_content['full_chart'],
        #     style={'margin':"2rem 0rem"}
        # ),
        html.A(id="FAQ"),
        dbc.Row(
            dbc.Col([
                html.H3(html.A('FAQs', href="#top"), className="subheader"),
                faq
                ])
        )
            ], style={'margin':"2rem auto"}
        
    )])

if __name__ == "__main__":
    app.run_server()