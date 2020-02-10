import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import seaborn as sns
import numpy as np
import dash_table
from dash.dependencies import Input, Output, State
import mysql.connector
conn = mysql.connector.connect(host='localhost',user='root',passwd='rfp123',use_pure = True)
cursor = conn.cursor(dictionary = True)
cursor.execute('USE ujian_modul2')
cursor.execute('SELECT * from data_tsa')
result = cursor.fetchall()
cm99 = pd.DataFrame(result)

def generate_table(dataframe, page_size=10):
    return dash_table.DataTable(
        id='dataTable',
        columns=[{
        "name": i,
        'id': i
        } for i in dataframe.columns],
        data=dataframe.to_dict('records'),
        page_action='native',
        page_current=0,
        page_size=page_size
    )

cm99 = pd.read_csv('tsa_claims_dashboard_ujian.csv')
bary1=['Claim Amount','Close Amount','Day Difference','Amount Differences']
bary2=['Claim Amount','Close Amount','Day Difference','Amount Differences']
barx=['Claim Type','Claim Site', 'Disposition']

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(children=[
    html.H1("Ujian Modul 2 Dashboard TSA"),
    html.Div(children="""
        Created by: Rahman
        """),
        dcc.Tabs(children = [
            dcc.Tab(value= 'Tab1', label= 'Dataframe Table', children= [
                html.Div([
                    html.P('Claim Site'),
                    dcc.Dropdown(value='',
                                id='filter-site',
                                options=[{'label':'Checkpoint','value':'Checkpoint'},
                                         {'label':'Other','value':'Other'},
                                         {'label':'Checked Baggage','value':'Checked Baggage'},
                                         {'label':'Motor Vehicle','value':'Motor Vehicle'},
                                         {'label':'All','value':''}])]),
                html.Br(),
                html.Div(children=[
                html.Div([
                    html.P('Max Rows'),
                    dcc.Input(id='filter-row',
                    type='number',
                    value=10)
                ],className='row col-3'),
                html.Button('Search', id='filter')
            ]),
                html.Div(id='div-table',children=[generate_table(cm99,page_size=10)
                ])
            ]),
            dcc.Tab(value= 'Tab2', label= 'Bar-Chart', children= [
            html.Div([
            html.Div(children=[
                html.Div([
                    html.P('Y1'),
                    dcc.Dropdown(value='',
                    id='filter-Y1',
                    options=[{'label':'Claim Amount','value':'Claim Amount'},
                    {'label':'Close Amount','value':'Close Amount'},
                    {'label':'Day Difference','value':'Day Difference'},
                    {'label':'Amount Differences','value':'Amount Differences'}])
                ],className='col-3'),
                html.Div([
                    html.P('Y2'),
                    dcc.Dropdown(value='',
                    id='filter-Y2',
                    options=[{'label':'Claim Amount','value':'Claim Amount'},
                    {'label':'Close Amount','value':'Close Amount'},
                    {'label':'Day Difference','value':'Day Difference'},
                    {'label':'Amount Differences','value':'Amount Differences'}])
                ],className='col-3'),
                html.Div([
                    html.P('X'),
                    dcc.Dropdown(value='',
                    id='filter-X',
                    options=[{'label':'Claim Type','value':'Claim Type'},
                    {'label':'Claim Site','value':'Claim Site'},
                    {'label':'Disposition','value':'Disposition'}])
                ],className='col-3')],className='row'),
                html.Br(),
                html.Div([dcc.Graph(id='graph-bar', figure= {
                'data': [ 
                    {'x': cm99['Claim Type'], 'y': cm99['Claim Amount'], 'type':'bar', 'name':'Claim Amount'},
                    {'x': cm99['Claim Type'], 'y': cm99['Close Amount'], 'type':'bar', 'name':'Close Amount'}
                    ],
                    'layout': {
                        'title': 'Tips Dash Data Visualization'
                            }})])
            ])]),
            dcc.Tab(value= 'Tab3', label= 'Scatter-Chart', children= []),
            dcc.Tab(value= 'Tab4', label= 'Pie-Chart', children= [])
    ],
    content_style= {
        'font_family':'Arial',
        'borderBottom':'1px solid #d6d6d6',
        'borderLeft':'1px solid #d6d6d6',
        'borderRight':'1px solid #d6d6d6',
        'padding':'44px'
    })
],
style={
    'maxWidth':'1200px',
    'margin': '0 auto'
})

@app.callback(
    Output(component_id='div-table',component_property='children'),
    [Input(component_id='filter',component_property='n_clicks')],
    [State(component_id='filter-row',component_property='value'),
    State(component_id='filter-site',component_property='value')]
)

def update_table(n_clicks,row,site):
    cm99 = pd.read_csv('tsa_claims_dashboard_ujian.csv')
    if site != '':
        cm99=cm99[cm99['Claim Site']==site]
    children=[generate_table(cm99,page_size=row)]
    return children

if __name__ == '__main__':
    app.run_server(debug=True)