import dash
from dash import html, dcc, callback, Input, Output
import pandas as pd
import datetime
df = pd.read_json('data.json')

inputList = (list(df['20170104_EXP_56']['inputs'].keys()))
# get the unique values of the inputList
outputList = (list(df['20170104_EXP_56']['outputs'].keys()))
dateList = []
for i in df:
    currDate = (i.split('_')[0])
    dateList.append(datetime.datetime.strptime(currDate, "%Y%m%d").date())


layout = html.Div(
    children=[
        html.Div(
            children=[
                # insert image 
               
                html.H1(
                    children="Uncountable Dashboard", className="home-heading"
                ),
                html.P(
                    children="This is the submission for the take home assignment for Aayush Gandhi",
                    className="home-para",
                ),
                html.Br(),
                html.P(
                    children="The dataset is stored in Uncountable Front End Dataset.json, labelled as data.json internally. The dataset is a json dictionary with the outer keys being the name of the experiment, and containing information of their date.  For each experiment there are two dictionaries “inputs” and “outputs” which have the actual data for each experiment.",
                    className="home-para",
                ),
                html.Br(),
                html.P(
                    children="The dashboard is built using Dash, a Python framework for building analytical web applications. The dashboard is hosted on Heroku, and the code can be made available.",
                    className="home-para",
                ),
                html.Br(),
                html.P(
                    children="The dashboard has four pages, the first page is the home page, which contains the information about the dashboard. The second page is the explore page, which allows uses to see the variance or 1 or more variables with time, with the ability to see local maximums, minimums, and averages for days with several experiment sets. The third page is the relationships page, which allows the user to select an input and output, and see the relationship between the two variables. The fourth page is the time/experiment query page, which allows the user to select a specific set of values, and see the relationship between them in a tabular format.",
                    className="home-para",
                ),
            ],
            className="header-home",
        )]
)
