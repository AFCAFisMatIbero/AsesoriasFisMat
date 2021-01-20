import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
import dash_table

data = pd.read_excel('data/BDTeachingLoad.xlsx')
data.columns = data.columns.str.lower()

materias_full = data.materia.unique()
docentes_full = data.docente.unique()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div([
    html.Div([
        html.Div([
            html.Img(src='assets/logoFISMAT.JPg',
                     style={'width': 500, 'height': 100})
        ],
            className='six-columns'),
        html.Div([
            html.H2('Consulta de horarios para asesoría',
                    style={'color': '#dc4b4a'})
        ],
            className='six-columns')
    ], className='row'),

    html.Div([
        html.H5('Selecciona tu materia'),
        dcc.Dropdown(
            id='selector_materia',
            options=[
                {'label': materia, 'value': materia}
                for materia in materias_full
            ]
        ),
        dash_table.DataTable(
            id='tabla_asesores',
            page_action='none',
            style_table={'overflowX': 'auto', 'overflowY': 'auto', 'height': '500px'},
            style_header={
                'backgroundColor': '#c5beb5',
                'fontWeight': 'bold',
                'color': 'white'
            },
            style_cell_conditional=[
                {
                    'if': {'column_id': 'id/correo'},
                    'textAlign': 'left'
                }
            ],
            sort_action='native',
            sort_mode='multi',
            columns=[{'name': col, 'id': col} for col in data.iloc[:, 2:].columns],
            data=data.iloc[:, 2:].to_dict('records')
        )
    ])
])


@app.callback(
    Output('tabla_asesores', 'columns'),
    Output('tabla_asesores', 'data'),
    Input('selector_materia', 'value')
)
def update_table(selector_materia):
    if selector_materia is None:
        filtered_data = data.iloc[:, 2:]
    else:
        filtered_data = data[data.materia == selector_materia].iloc[:, 2:]
    columns = [{'name': col, 'id': col} for col in filtered_data.columns]
    return columns, filtered_data.to_dict('records')


if __name__ == '__main__':
    app.run_server(debug=True)
