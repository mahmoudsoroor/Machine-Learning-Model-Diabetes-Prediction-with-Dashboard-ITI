"""Instantiate a Dash app."""
import numpy as np
import pandas as pd
import dash
import dash_table
from dash import html
from dash import dcc
import plotly.graph_objects as go
import plotly.express as px
import pickle


#___________________________________________________________
"""Plotly Dash HTML layout override."""

html_layout = """
<!doctype html>
<html lang="en" class="h-100">
<head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css" integrity="sha384-wvfXpqpZZVQGK6TAh5PVlGOfQNHSoD2xbE+QkPxCAFlNEevoEH3Sl0sibVcOQVnN" crossorigin="anonymous">
    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" crossorigin="anonymous">
    <!-- Google Fonts -->
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700&display=swap"/>
    <!-- Custom CSS for Dash -->
    <link rel="stylesheet" href="/static/dashstyles.css">
    

    <!-- bootstrap Bundle with Popper -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/js/bootstrap.bundle.min.js" async integrity="sha384-ygbV9kiqUc6oa4msXn9868pTtWMgiQaeYH7/t7LECLbyPA2x65Kgf80OJFdroafW" crossorigin="anonymous"></script>
    <title>Dashboard</title>
</head>
<body class="d-flex flex-column h-100 body" style="background-color:#212257">
<nav class="navbar navbar-expand-lg navbar-light bg-white shadow">
   
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                <li class="nav-item">
                    <a class="nav-link " href="/">Home</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link " href="/diagnose">Diagnosis</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link active" href="/dashapp/">Dashboard</a>
                </li>
                
            </ul>
        </div>
    </div>
</nav>
<main role="main" class="flex-shrink-0" >

   <div class="container shadow rounded fadeIn p-5 my-5 bg-white" id="content">

    <h2> Data Visualization </h2>
    <br>
            {%app_entry%}
    </div>

</main>
<footer class="footer mt-auto py-3 text-white">
  
                {%config%}
                {%scripts%}
                {%renderer%}
</footer>
</body>
</html>
"""




#___________________________________________________________
# rf_model = pickle.load("rf_model.pkl")

with open('app/data/rf_model_pkl', 'rb') as pickle_file:
    rf_model = pickle.load(pickle_file)



def init_dashboard(server):
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/dashapp/'
    )

    # Load DataFrame
    df    = pd.read_csv("app/data/diabetes.csv")
    data1  = pd.read_csv("app/data/new_data.csv")
    data2  = pd.read_csv("app/data/features_data.csv")
    data3  =pd.read_csv("app/data/Diabetes-E.csv")
    data4  =  pd.read_csv("app/data/Diabetes-Age.csv")
    data5 = pd.read_csv("app/data/Diabetes-G.csv")
    data6 = pd.read_csv("app/data/data.csv")

    # Create heatmap
    heatmap_fig = px.imshow(data1.corr())

    # Age Distribution
    fig=px.box(df,x='class',y='Age')

    #Exploring label based on gender
    fig1=px.bar(df,x='class',color='Gender',barmode='group')
    #Important Features
    fig2=px.bar(data2,x='Importance (%)',y='Feature',barmode='stack',title="Important Features",hover_data=['Scores'],color="Scores",color_continuous_scale='Portland')
   
    #graph for education
    fig3=px.line(data3,x='Year',y=['< High School - Percentage','High School - Percentage','> High School - Percentage'],markers='Year')
    
    #graph for age 
    fig4=px.line(data4,x='Year',y=['18-44 - Percentage','45-64 - Percentage','65-74 - Percentage','75+ - Percentage'],markers='Year')
    #graph for gender
    fig5=px.line(data5,x='Year',y=['Male - Percentage','Female - Percentage'],markers='Year')
    #explain the increase diabetes
    fig6= px.bar(data6, x='date', y='number',color='Region')
    # Custom HTML layout
    dash_app.index_string = html_layout

    # Create Layout
    dash_app.layout = html.Div(
        children=[
            html.H5(children="Important Features", className="lh-1"),
            dcc.Graph(figure=fig2),
            html.Br(),
            html.Br(),
            html.H5(children="Correlation of feature", className="lh-1"),
            dcc.Graph(figure=heatmap_fig),
            html.Br(),
            html.Br(),
            html.H5(children="Age Distribution", className="lh-1"),
            dcc.Graph(figure=fig),
            html.Br(),
            html.Br(),
            html.H5(children="Exploring label based on Gender", className="lh-1"),
            dcc.Graph(figure=fig1),
            html.Br(),
            html.Br(),
            html.H5(children="Relation between diabetes and Education", className="lh-1"),
            dcc.Graph(figure=fig3),
            html.Br(),
            html.Br(),
            html.H5(children="Relation between diabetes and Age", className="lh-1"),
            dcc.Graph(figure=fig4),
            html.Br(),
            html.Br(),
            html.H5(children="Relation between diabetes and Gender", className="lh-1"),
            dcc.Graph(figure=fig5),
            html.Br(),
            html.Br(),
            html.H5(children="Explain the increase Diabetes", className="lh-1"),
            dcc.Graph(figure=fig6),
            html.Br(),
            html.Br(),
            
        ],
       # id='dash-container'
    )
    return dash_app.server



