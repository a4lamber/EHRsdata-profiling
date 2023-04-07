'''
 # @ Author: Adam Zhang
 # @ Create Time: 2023-04-01 21:46:38
 # @ Modified by: Adam Zhang
 # @ Modified time: 2023-04-01 21:46:52
 # @ Description: integrate multiple plotly graph together into dash framework.
 '''


import os
import pathlib

import pandas as pd
import numpy as np
import plotly.graph_objects as go

import dash
from dash import dcc,html
from dash.dependencies import Input, Output

import plotly.express as px

# import some ad-hoc methods i wrote 
from dataGraphProfile import get_num_cat_dtype,get_categorical_distribution,get_pattern

"""
Read csv files
"""

path = "./rawdata"
data = pathlib.Path(path)
# recursively read files
csv_files = list(data.rglob("*.csv*"))
# select 1st file for now, need to implement a dropdown list
df = pd.read_csv(csv_files[0])

"""
Scalar: % of null
"""
percentage_of_null = list(df.isnull().sum()/len(df.index))

fig1 = go.Figure()
fig1.add_trace(go.Bar(
    y=df.columns,
    x=percentage_of_null,
    name=r'% of null',
    orientation='h',
    marker=dict(
        color='rgba(246, 78, 139, 0.6)',
        line=dict(color='rgba(246, 78, 139, 1.0)', width=3)
    ),
    showlegend=True
))

fig1.update_layout(
                  title_text=r"% of null",
                  title_font_size=20,
                  xaxis_tickformat = ',.1%'
                  )
"""
Scalar: Uniquiness
"""

uniqueness = (df.nunique() - 1)/(len(df.index) - df.isnull().sum() - 1)

fig2 = go.Figure()
fig2.add_trace(go.Bar(
    y=df.columns,
    x=uniqueness,
    name=r'uniquiness',
    orientation='h',
    marker=dict(
        color='rgba(246, 78, 139, 0.6)',
        line=dict(color='rgba(246, 78, 139, 1.0)', width=3)
    ),
    showlegend=True
))

fig2.update_layout(
                  title_text=r"uniquiness",
                  title_font_size=20,
                  xaxis_tickformat = ',.1%'
                  )


"""
distribution: categorical variables
"""
numerical_columns,cate_columns = get_num_cat_dtype(df)
cat_plot = get_categorical_distribution(df,cate_columns)


fig3 = go.Figure()

# Use x instead of y argument for horizontal plot

for i in range(len(cate_columns)):
      fig3.add_trace(go.Box(x=df[cate_columns].applymap(str).applymap(len).iloc[:,i],
                        name = cate_columns[i]
                        ),
                  )

fig3.update_layout(
                  title_text=r"categorical value distribution",
                  title_font_size=20
                  )

"""
distribution: numerical variables
"""

fig4 = go.Figure()

# Use x instead of y argument for horizontal plot

for i in range(len(numerical_columns)):
    curr_column = df[numerical_columns].iloc[:,i]
    fig4.add_trace(go.Box(x=curr_column/curr_column.max(),
                        name = numerical_columns[i]
                        ),
                  )

fig4.update_layout(
                  title_text=r"numerical value distribution",
                  title_font_size=20,
                  xaxis_tickformat = ',.1%'
                  )

"""
pattern: boolean flag for regex 
"""

df_pattern = get_pattern(df)

fig5 = go.Figure()

fig5.add_trace(go.Heatmap(
                   z=df_pattern.to_numpy().astype(dtype=int),
                   x=["0","a","A"],
                   y=list(df_pattern.index),
                   hoverongaps = False,
                   showlegend=True,
                   colorscale = 'Greys',
                   name = ""
                   ),)
# did some trick to set block size to be same
fig5.update_layout(
                  title_text=r"pattern",
                  title_font_size=20,
                  xaxis = dict(
                      side = "top"
                  )
                  )

"""
Dash layout tuning
"""

app = dash.Dash(__name__)



app.layout = html.Div(children=[
   # elements from the top of the page
   html.Div([
      html.H1(children='Percentage of null'),
      #html.Div(children='''
      #Dash: First graph.'''),

      dcc.Graph(
         id='graph1',
         figure=fig1
      ),
   ]),
   # New Div for all elements in the new 'row' of the page
   html.Div([
      html.H1(children='Uniquiness'),
      #html.Div(children='''
      #Dash: Second graph. '''),

      dcc.Graph(
         id='graph2',
         figure=fig2
      ),
   ]),
   # New Div for all elements in the new 'row' of the page
   html.Div([
      html.H1(children='Categorical variable length distribution'),
      #html.Div(children='''
      #Dash: Second graph. '''),

      dcc.Graph(
         id='graph3',
         figure=fig3
      ),
   ]),
   html.Div([
      html.H1(children='Numerical variable distribution (normalized)'),
      #html.Div(children='''
      #Dash: Second graph. '''),

      dcc.Graph(
         id='graph4',
         figure=fig4
      ),
   ]),
   html.Div([
      html.H1(children='Pattern flag'),
      #html.Div(children='''
      #Dash: Second graph. '''),

      dcc.Graph(
         id='graph5',
         figure=fig5
      ),
   ]),
])

if __name__ == '__main__':
    app.run_server(debug=True)

