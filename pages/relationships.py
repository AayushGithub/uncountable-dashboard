import dash
from dash import html, dcc, callback, Input, Output
import pandas as pd
import datetime
from dash.exceptions import PreventUpdate
from dash import no_update
import plotly.express as px
df = pd.read_json('data.json')

inputList = (list(df['20170104_EXP_56']['inputs'].keys()))
# get the unique values of the inputList
outputList = (list(df['20170104_EXP_56']['outputs'].keys()))
dateList = []
for i in df:
    currDate = (i.split('_')[0])
    dateList.append(datetime.datetime.strptime(currDate, "%Y%m%d").date())
defaultOptionsInput = []
for input_type in inputList:
    defaultOptionsInput.append({"label": input_type, "value": input_type})
defaultOptionsOutput = []
for output_type in outputList:
    defaultOptionsOutput.append({"label": output_type, "value": output_type})
layout = html.Div(
    children=[
        html.Div(
            children=[
                # insert image 
               
                html.H1(
                    children="Explore Relationships between Inputs and Outputs", className="header-title"
                ),
                html.P(
                    children=["By specifiying the input and output, you can see the relationship between the two variables. A",html.Strong(' date range '),"can be specified to see the relationship between the two variables over time. ",html.Strong('Zero Values')," can be optionally excluded.",],
                    className="header-description",
                ),

            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Input", className="menu-title"),
                        dcc.Dropdown(
                            id="input-filter",
                            options=defaultOptionsInput,
                            value="Polymer 1",
                            clearable=False,
                            className="dropdown",
                        ),
                        
                    html.Div(id="warning", className="menu-title"),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Output", className="menu-title"),
                        dcc.Dropdown(
                            id="output-filter",
                            options=defaultOptionsOutput,
                            value="Viscosity",
                            clearable=False,
                            searchable=False,
                            className="dropdown",
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        html.Div(
                            children="Date Range",
                            className="menu-title"
                            ),
                        dcc.DatePickerRange(
                            id="date-range",
                            min_date_allowed=min(dateList),
                            max_date_allowed=max(dateList),
                            start_date=min(dateList),
                            end_date=max(dateList),
                        ),
                    ]
                ),
            html.Div(
                    children=[
                        html.Div(children="Exclude Zero Values", className="menu-title"),
                        dcc.Dropdown(
                            id="zero-filter",
                            options=[
                                {"label": values, "value": values}
                                for values in ["Yes", "No"]
                            ],
                            value="Yes",
                            clearable=False,
                            searchable=False,
                            className="dropdown",
                        ),
                    ],
                ),
                        
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="relationship-chart",
                        config={"displayModeBar": False},
                        figure={
                            "data": [
                                {
                                    "x": 0,
                                    "y": 0,
                                    "type": "lines",
                                    "hovertemplate": " %{y:.2f}"
                                                     "<extra></extra>",
                                },
                            ],
                            "layout": {
                                "title": {
                                    "text": "Relationship between Selected Input and Output",
                                    "x": 0.1,
                                    "xanchor": "left",
                                },
                                "xaxis": {"fixedrange": True},
                                "yaxis": {
                                    "fixedrange": True,
                                },
                                "colorway": ["#17B897"],
                            },
                        },
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
        ]

)

# @callback(
#     Output("input-filter", "options"),
#     Output("warning", "children"),
#     Input("input-filter", "value"),
# )
# def update_multi_options(value):
#     options = defaultOptions
#     input_warning = None
#     if type(value) == str:
#         value = [value]
#     if not value:
#         input_warning = html.P(id="warning", children="At least 1 parameter must be selected", className="menu-title-warning")
#     if len(value) >= 4:
#         input_warning = html.P(id="warning", children="Limit reached: A maximum of 4 inputs can be selected", className="menu-title-warning")
#         options = [
#             {"label": option["label"], "value": option["value"], "disabled": True}
#             for option in options
#         ]
#     return options, input_warning


@callback(
    [Output("relationship-chart", "figure")],
    [
        Input("input-filter", "value"),
        Input("output-filter", "value"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
        Input("zero-filter", "value"),
    ],
)
def update_charts(input_type, output_type, start_date, end_date, zero_filter):
    # initialize empty df
    df = pd.read_json('data.json')
    x = []
    y = []
    for items in df:
        currDate = (items.split('_')[0])
        currDate = datetime.datetime.strptime(currDate, "%Y%m%d").date()
        start_date = datetime.datetime.strptime(str(start_date), "%Y-%m-%d").date()
        end_date = datetime.datetime.strptime(str(end_date), "%Y-%m-%d").date()
        if currDate >= start_date and currDate <= end_date:
            if input_type in df[items]['inputs'] and output_type in df[items]['outputs']:
                valueX = df[items]['inputs'][input_type]
                valueY = df[items]['outputs'][output_type]
                if zero_filter == "Yes":
                    if valueX != 0 and valueY != 0:
                        x.append(valueX)
                        y.append(valueY)
                else:
                    x.append(valueX)
                    y.append(valueY)
            
    # make a dataframe with the data from list
    df = pd.DataFrame({input_type: x, output_type: y})
    # return the graph
    fig = px.scatter(df, x=input_type, y=output_type, title="layout.hovermode='closest' (the default)",)
    fig.update_layout(
        title={
            'text': f"Relationship between {input_type} and {output_type}",
            'x': 0.1,
            'xanchor': "left",
        },
        xaxis={'title': input_type},
        yaxis={'title': output_type},
        colorway=["#17B897"],
    )
    fig.update_layout(transition_duration=500)
    return [fig]