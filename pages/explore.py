import dash
from dash import html, dcc, callback, Input, Output
import pandas as pd
import datetime
import plotly.express as px
df = pd.read_json('data.json')

inputList = (list(df['20170104_EXP_56']['inputs'].keys()))
# get the unique values of the inputList
outputList = (list(df['20170104_EXP_56']['outputs'].keys()))
fullList = inputList + outputList
dateList = []
for i in df:
    currDate = (i.split('_')[0])
    dateList.append(datetime.datetime.strptime(currDate, "%Y%m%d").date())

defaultOptions = []
for input_type in fullList:
    defaultOptions.append({"label": input_type, "value": input_type})
layout = html.Div(
    children=[
        html.Div(
            children=[
                # insert image 
               
                html.H1(
                    children="Explore Data as a function of time", className="header-title"
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
                        html.Div(children="Parameter", className="menu-title"),
                        dcc.Dropdown(
                            id="input-filter",
                            options=defaultOptions,
                            value="Polymer 1",
                            clearable=False,
                            searchable=True,
                            multi = True,
                            className="dropdown-multi",
                        ),
                    html.Div(id="warning", className="menu-title"),
                    ]
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
                        html.Div(children="Choose data aggregation type", className="menu-title"),
                        dcc.Dropdown(
                            id="zero-filter",
                            options=[
                                {"label": values, "value": values}
                                for values in ["Maximum", "Average", "Minimum"]
                            ],
                            value="Average",
                            clearable=False,
                            searchable=False,
                            className="dropdown",
                        ),
                    ],
                ),
                        
            ],
            className="menu-explore",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="explore-chart",
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
                                    "text": "Relationship between Selected Input and Time",
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

@callback(
    Output("input-filter", "options"),
    Output("warning", "children"),
    Input("input-filter", "value"),
)
def update_multi_options(value):
    options = defaultOptions
    input_warning = None
    if type(value) == str:
        value = [value]
    if not value:
        input_warning = html.P(id="warning", children="At least 1 parameter must be selected", className="menu-title-warning")
    if len(value) >= 4:
        input_warning = html.P(id="warning", children="Limit reached: A maximum of 4 inputs can be selected", className="menu-title-warning")
        options = [
            {"label": option["label"], "value": option["value"], "disabled": True}
            for option in options
        ]
    return options, input_warning

@callback(
    [Output("explore-chart", "figure")],
    [
        Input("input-filter", "value"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
        Input("zero-filter", "value"),
    ],
)
def update_charts(input_filter, start_date, end_date, zero_filter):

    
    from pandas import json_normalize 
    import json
    df = pd.read_json('data.json')
    filtered_df = pd.DataFrame()
    if not input_filter:
        import plotly.graph_objs as go
        fig = go.Figure()
        fig.update_layout(
            xaxis =  { "visible": False },
            yaxis = { "visible": False },
            annotations = [
                {   
                    "text": "No matching data found. Please select a parameter or different date range.",
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                    "font": {
                        "size": 28
                    }
                }
            ]
        )
        return [fig]
    if type(input_filter) == str:
        input_filter = [input_filter]
    
    for i in input_filter:
        dateList = []
        columnName = []
        for items in df:
            currDate = (items.split('_')[0])
            currDate = datetime.datetime.strptime(currDate, "%Y%m%d").date()
            start_date = datetime.datetime.strptime(str(start_date), "%Y-%m-%d").date()
            end_date = datetime.datetime.strptime(str(end_date), "%Y-%m-%d").date()
            if currDate >= start_date and currDate <= end_date:
                if i in inputList:
                    columnName.append(df[items]['inputs'][i])
                else:
                    columnName.append(df[items]['outputs'][i])
                dateList.append(currDate)
        filtered_df[i] = columnName
    filtered_df['date'] = dateList

    if zero_filter == "Maximum":
        filtered_df = filtered_df.groupby('date').max()
    elif zero_filter == "Average":
        filtered_df = filtered_df.groupby('date').mean()
    elif zero_filter == "Minimum":
        filtered_df = filtered_df.groupby('date').min()

    # plot scatter plot of the data
    df = pd.pivot_table(filtered_df,values = input_filter, index = 'date')
    # scatter plot of the data
    fig = px.line(df, x = df.index, y = input_filter, markers=True)
    if len(input_filter) == 1:
        title = "Relationship between " + input_filter[0] + " and Time"
    else:
        stringStart = "Relationship between "
        for i in range(len(input_filter)):
            stringStart += input_filter[i] + ", "
        # remove the last comma
        stringStart = stringStart[:-2]
        stringStart += " and Time"
        title = stringStart 
    fig.update_layout(
        title={
            "text": title,
            "x": 0.1,
            "xanchor": "left",
        },
        xaxis={"fixedrange": True},
        yaxis={
            "fixedrange": True,
        },
        colorway=["#17B897"],
    )
    return [fig]
