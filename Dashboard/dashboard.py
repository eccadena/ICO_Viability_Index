import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table as dt
import pandas as pd
from pathlib import Path


path = Path(r'C:\Users\marcl\Documents\fintech\ICO_Viability_Index\data\cleandata\success_NN_1H_df.csv')
df = pd.read_csv(path)

external_stylesheets = [r'C:\Users\marcl\Documents\fintech\ICO_Viability_Index\Dashboard\assets\style.css']

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div(html.Img(src=app.get_asset_url('logo.png'), height=100)),
    #html.H1(children='Digital Asset Viability Index Dashboard'),
    dt.DataTable(
        id='datatable-interactivity',
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
            'padding': '10px 12px',
            'width': 'auto',
            'textAlign': 'center',
            'font-size': '1em',
            'line-height': '1',
            'font-weight': '300',
            'font-family': '"Open Sans", "HelveticaNeue", "Helvetica Neue", Helvetica, Arial, sans-serif',
            'color': 'rgb(50, 50, 50)'
        },
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("rows"),
        hidden_columns=['pct1h', 'pct24h', 'pct7d', 
            'pre_ico_end', 'pre_ico_start', 'Name_y', 
            'type', 'End', 'Start', 'Duration', 'pre_Duration',
            'compound', 'negative', 'neutral', 'positive', 'no_of_posts',
            'longevity', 'custom_index', 'custom_index_scaled', 'success_index',
            'success_PCA', 'predicted_NN']
        
    ),
    html.H2(children='ICO Insights'),
    html.Div(id='datatable-interactivity-container')
])

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

    colors = ['#7FDBFF' if i in derived_virtual_selected_rows else '#0074D9'
              for i in range(len(dff))]

    return [
        dcc.Graph(
            id="ICO strength by Origin",
            figure={
                "data": [
                    {
                        "x": dff["country"],
                        "y": dff["market_cap"],
                        "type": "bar",
                        "marker": {"color": colors},
                    }
                ],
                "layout": {
                    "xaxis": {
                        "automargin": True,
                        "title": {"text": "Country of Origin"}
                    },
                    "yaxis": {
                        "automargin": True,
                        "title": {"text": "Market Cap"}
                    },
                    "height": 250,
                    "margin": {"t": 10, "l": 10, "r": 10},
                },
            },
        ),

        dcc.Graph(
            id="market cap by rating",
            figure={
                "data": [
                    {
                        "x": dff["rating"],
                        "y": dff["market_cap"],
                        "type": "bar",
                        "marker": {"color": colors},
                    }
                ],
                "layout": {
                    "xaxis": {
                        "automargin": True,
                        "title": {"text": "Rating"}
                    },
                    "yaxis": {
                        "automargin": True,
                        "title": {"text": "Market Cap"}
                    },
                    "height": 250,
                    "margin": {"t": 10, "l": 10, "r": 10},
                },
            },
        )
 
    ]


if __name__ == '__main__':
    app.run_server(debug=True)