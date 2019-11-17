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

def render_content(tab):
    if tab == 'tab-1-example':
        return html.Div([
            html.H3('ICO Rank'),
            generate_table(df, 100),
            html.Div(id='datatable-interactivity-container')
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

@app.callback(Output('tabs-content-example', 'children'),
              [Input('tabs-example', 'value')])

#Tab 1 Table Layout Function
def generate_table(dataframe, max_rows):
    return dt.DataTable(
        id='datatable-interactivity',
        sort_action='native',
        editable=True,
        filter_action='native',
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        row_selectable="multi",
        row_deletable=False,
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current= 0,
        page_size= 10,
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

@app.callback(
    Output('datatable-interactivity', 'style_data_conditional'),
    [Input('datatable-interactivity', 'selected_columns')]
)

def update_styles(selected_columns):
    return [{
        'if': { 'column_id': i },
        'background_color': '#D2F3FF'
    } for i in selected_columns]

@app.callback(
    Output('datatable-interactivity-container', "children"),
    [Input('datatable-interactivity', "derived_virtual_data"),
     Input('datatable-interactivity', "derived_virtual_selected_rows")])

def update_graphs(rows, derived_virtual_selected_rows):
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

        dff = df if rows is None else pd.DataFrame(rows)
        
        return [
        dcc.Graph(
            id=column,
            figure={
                "data": [
                    {
                        "x": dff["country"],
                        "y": dff[column],
                        "type": "bar",
                        "marker": {"color": colors},
                    }
                ],
                "layout": {
                    "xaxis": {"automargin": True},
                    "yaxis": {
                        "automargin": True,
                        "title": {"text": column}
                    },
                    "height": 250,
                    "margin": {"t": 10, "l": 10, "r": 10},
                },
            },
        )

if __name__ == '__main__':
    app.run_server(debug=True)