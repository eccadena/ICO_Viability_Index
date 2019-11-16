import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table as dt
import pandas as pd
from pathlib import Path

path= Path(r'C:\Users\marcl\Documents\fintech\ICO_Viability_Index\Dashboard\Pokemon.csv')
df = pd.read_csv(path)


def generate_table(dataframe, max_rows):
    # return html.Table(
    #     # Header
    #     [html.Tr([html.Th(col) for col in dataframe.columns])] +

    #     # Body
    #     [html.Tr([
    #         html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
    #     ]) for i in range(min(len(dataframe), max_rows))]
    return dt.DataTable(
        sorting=True,
        filtering=True,
        style_cell={
            'padding': '10px',
            'width': 'auto',
            'textAlign': 'center'
        },
        style_cell_conditional=[
            {
                'if': {'row_index': 'even'},
                'backgroundColor': '#f9f9f9'
            }
        ],
        columns=[{"name": i, "id": i} for i in dataframe.columns],
        data=dataframe.to_dict("rows")
    )


external_stylesheets = [r'C:\Users\marcl\Documents\fintech\ICO_Viability_Index\Dashboard\assets\style.css']

app = dash.Dash(__name__, 
    external_stylesheets=external_stylesheets
    )

app.layout = html.Div(children=[
    html.H1(children='Digital Asset Viability Index Dashboard'),
    dcc.Tabs(id="tabs-example", value='tab-1-example', children=[
        dcc.Tab(label='Tab One', value='tab-1-example'),
        dcc.Tab(label='Tab Two', value='tab-2-example'),
    ]),
    html.Div(id='tabs-content-example')
])

@app.callback(Output('tabs-content-example', 'children'),
              [Input('tabs-example', 'value')])

def render_content(tab):
    if tab == 'tab-1-example':
        return html.Div([
            html.H3('Tab content 1'),
            generate_table(df, 100),
        ])
    elif tab == 'tab-2-example':
        return html.Div([
            html.H3('Tab content 2'),
            dcc.Graph(
                id='graph-2-tabs',
                figure={
                    'data': [{
                        'x': [1, 2, 3],
                        'y': [5, 10, 6],
                        'type': 'bar'
                    }]
                }
            )
        ])

if __name__ == '__main__':
    app.run_server(debug=True)