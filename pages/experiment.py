import dash
from dash import html, dcc, callback, Input, Output, dash_table
import pandas as pd
import datetime
import plotly.express as px
import dash_bootstrap_components as dbc
df = pd.read_json('data.json')

inputList = (list(df['20170104_EXP_56']['inputs'].keys()))
# get the unique values of the inputList
outputList = (list(df['20170104_EXP_56']['outputs'].keys()))
fullList = inputList + outputList
dateList = []
experimentList = []
for i in df:
    currDate = (i.split('_')[0])
    dateList.append(datetime.datetime.strptime(currDate, "%Y%m%d").date())
    # format currDate as dd/mm/yyyy
    formattedDate = datetime.datetime.strptime(currDate, "%Y%m%d").strftime("%d/%m/%Y")
    stringName = i.split('_')[2] + " " + f"({formattedDate})"
    experimentList.append(stringName)
# sort experimentList
experimentList.sort()

PAGE_SIZE = 5

layout = html.Div(
    children=[
        html.Div(
            children=[
                # insert image 
               
                html.H1(
                    children="Explore Data for a particular experiment", className="header-title"
                ),
                html.P(
                    children=["Choose a parameter (input or output) and see how it varies as a function of time. ",html.Strong('Multiple experiments')," may have been carried out on the same day. Use the ",html.Strong('data aggregation')," selector to pick what type of data is desired in such cases.",],
                    className="header-description",
                ),

            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Experiment Number", className="menu-title"),
                        dcc.Dropdown(
                            id="experiment-filter",
                            options=experimentList,
                            value="10 (15/01/2017)",
                            clearable=False,
                            searchable=True,
                            className="dropdown",
                        ),
                    html.Div(id="warning", className="menu-title"),
                    ]
                ),
            ],
            className="menu-experiment",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dbc.Container([
                    dbc.Label('Input Data for Experiment'),
                    
                    dash_table.DataTable(id='datatable-paging-inputs',
                    style_cell={'textAlign': 'left'},
    style_cell_conditional=[
        {
            'if': {'column_id': 'Region'},
            'textAlign': 'left'
        }
    ]
                    
                ),
                html.Br(),
                dbc.Label('Output Data for Experiment'),
                dash_table.DataTable(id='datatable-paging-output',
                    style_cell={'textAlign': 'left'},
    style_cell_conditional=[
        {
            'if': {'column_id': 'Region'},
            'textAlign': 'left'
        }
    ]
                    
                ),
                    ]),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
        ]

)

@callback(
    Output('datatable-paging-inputs', 'data'),
    Input("experiment-filter", "value"))
def update_table(experiment_filter):
    # converted back to original format
    experiment = experiment_filter.split(' ')[0]
    # get the date
    date = experiment_filter.split('(')[1].split(')')[0]
    # convert date to original format
    date = datetime.datetime.strptime(date, "%d/%m/%Y").strftime("%Y%m%d")
    # get the experiment number
    experiment = experiment_filter.split('(')[0].strip()
    # get the experiment name
    experimentName = date + "_EXP_" + experiment
    # get the data
    data = df[experimentName]
    # get the inputs
    inputs = data['inputs']
    return [{"Parameter Name": i, "Value": data['inputs'][i]} for i in inputs]

@callback(
    Output('datatable-paging-output', 'data'),
    Input("experiment-filter", "value"))
def update_table(experiment_filter):
    # converted back to original format
    experiment = experiment_filter.split(' ')[0]
    # get the date
    date = experiment_filter.split('(')[1].split(')')[0]
    # convert date to original format
    date = datetime.datetime.strptime(date, "%d/%m/%Y").strftime("%Y%m%d")
    # get the experiment number
    experiment = experiment_filter.split('(')[0].strip()
    # get the experiment name
    experimentName = date + "_EXP_" + experiment
    # get the data
    data = df[experimentName]
    # get the inputs
    output = data['outputs']
    return [{"Parameter Name": i, "Value": data['outputs'][i]} for i in output]