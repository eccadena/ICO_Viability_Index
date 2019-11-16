import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table as dt
import pandas as pd
from pathlib import Path


path = Path(r'C:\Users\marcl\Documents\fintech\ICO_Viability_Index\data\cleandata\track_cmc_merged_df.csv')
df = pd.read_csv(path)

external_stylesheets = [r'C:\Users\marcl\Documents\fintech\ICO_Viability_Index\Dashboard\assets\style.css']

def generate_table(dataframe, max_rows):
    # return html.Table(
    #     # Header
    #     [html.Tr([html.Th(col) for col in dataframe.columns])] +

    #     # Body
    #     [html.Tr([
    #         html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
    #     ]) for i in range(min(len(dataframe), max_rows))]
    return dt.DataTable(
        sort_action='native',
        #filter_action='native',  #Allows user to enter dynamic text for a filer of row
        page_action='native',
        page_size= 50,
        hidden_columns=[],
        style_cell={
            'padding': '12px 15px',
            'width': 'auto',
            'textAlign': 'center',
            'font-size': '1em',
            'line-height': '1.2',
            'font-weight': '400',
            'font-family': '"Open Sans", "HelveticaNeue", "Helvetica Neue", Helvetica, Arial, sans-serif',
            'color': 'rgb(50, 50, 50)'
        },
        columns=[{"name": i, "id": i} for i in dataframe.columns],
        data=dataframe.to_dict("rows"),
        
    )




app = dash.Dash(__name__, 
    external_stylesheets=external_stylesheets
    )

app.layout = html.Div(children=[
    html.H1(children='Digital Asset Viability Index Dashboard'),
    dcc.Tabs(id="tabs-example", value='tab-1-example', children=[
        dcc.Tab(label='ICO Rating List', value='tab-1-example'),
        dcc.Tab(label='Trends Analysis', value='tab-2-example'),
        dcc.Tab(label='Methodology', value='tab-3-example')
    ]),
    html.Div(id='tabs-content-example')
])

@app.callback(Output('tabs-content-example', 'children'),
              [Input('tabs-example', 'value')])

def render_content(tab):
    if tab == 'tab-1-example':
        return html.Div([
            html.H3('ICO Rank'),
            generate_table(df, 100),
        ])
    elif tab == 'tab-2-example':
        return html.Div([
            html.H3('Trends Analysis'),
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
    elif tab == 'tab-3-example':
        return html.Div([
            html.H3('Methodology'),
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