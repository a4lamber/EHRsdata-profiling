'''
 # @ Author: Your name
 # @ Create Time: 2023-04-01 21:44:41
 # @ Modified by: Your name
 # @ Modified time: 2023-04-01 21:44:45
 # @ Description: example of embedding plotly diagram in dash
 '''
 
import dash
from dash import dcc,html
from dash.dependencies import Input, Output

import pandas as pd
import plotly.express as px


app = dash.Dash(__name__)
df_bar = pd.DataFrame({
   "Season": ["Summer", "Winter", "Autumn", "Spring"],
   "Rating": [3,2,1,4]
})

fig = px.bar(df_bar, x="Season", y="Rating", barmode="group")

app.layout = html.Div(children=[
   # elements from the top of the page
   html.Div([
      html.H1(children='Dash app1'),
      html.Div(children='''
      Dash: First graph.'''),

      dcc.Graph(
         id='graph1',
         figure=fig
      ),
   ]),
   # New Div for all elements in the new 'row' of the page
   html.Div([
      html.H1(children='Dash app2'),
      html.Div(children='''
      Dash: Second graph. '''),

      dcc.Graph(
         id='graph2',
         figure=fig
      ),
   ]),
])

if __name__ == '__main__':
    app.run_server(debug=True)

