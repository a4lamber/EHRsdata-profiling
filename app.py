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
from dash import dcc,html,Output,Input


# import some ad-hoc methods i wrote 
from dataGraphProfile import get_num_cat_dtype,get_categorical_distribution,get_pattern
from dataGraphProfileIO import find_csvs,get_report

"""
Read csv files
"""
path = "./rawdata"
files = find_csvs(path)


#load data into a DataFrame object:
df_default = pd.DataFrame({
  "example": [1, 2, 3],
  "value": [1, 2, 3]
})
"""
Dash layout tuning
"""

app = dash.Dash(__name__)


app.layout = html.Div(children=[
   # a dropdown menu for selecting dataset   
   html.Div([
      html.H1(children='Dropdown'),
      #html.Div(children='''
      #Dash: First graph.'''),

      dcc.Dropdown(
         id='dropdown',
         options = [
            {'label': html.Span([i], style={'color':'Black','font-size':20}),'value':i} for i in [file for file in files]
         ]
      ),
   ]),
   # stat table
   html.Div([
      html.H1(children='Column-wise summary'),
      dash.dash_table.DataTable(
        id='table',
        columns=[{'name': i, 'id': i} for i in df_default.columns],
        data=df_default.to_dict('records')
   )
    ]),
   
   html.Div([
      html.H1(children='Percentage of null'),
      #html.Div(children='''
      #Dash: First graph.'''),

      dcc.Graph(
         id='graph1'
      ),
   ]),
   # Uniquiness
   html.Div([
      html.H1(children='Uniquiness'),
      #html.Div(children='''
      #Dash: Second graph. '''),

      dcc.Graph(
         id='graph2'
      ),
   ]),
   # categorical variable length distribution
   html.Div([
      html.H1(children='Categorical variable length distribution'),
      #html.Div(children='''
      #Dash: Second graph. '''),

      dcc.Graph(
         id='graph3'
      ),
   ]),
   html.Div([
      html.H1(children='Numerical variable distribution (normalized)'),
      #html.Div(children='''
      #Dash: Second graph. '''),

      dcc.Graph(
         id='graph4'
      ),
   ]),
   html.Div([
      html.H1(children='Pattern flag'),
      #html.Div(children='''
      #Dash: Second graph. '''),

      dcc.Graph(
         id='graph5'
      ),
   ]),
])

##############################################################
######################## callbacks ###########################
##############################################################

@app.callback(
    dash.dependencies.Output('table', 'columns'),
    dash.dependencies.Output('table', 'data'),
    dash.dependencies.Input('dropdown', 'value')
)

def update_table(value):
   """
   function callback for summary dash table
   Args:
       value (_type_): _description_

   Returns:
       columns, data for dash_table
   """
   if value is not None: 
      # in dropdown
      df = get_report(value)
      columns = [{'name': i, 'id': i} for i in df.columns]
      data = df.to_dict('records')
   else:
      # when start-up
      columns = [{'name': i, 'id': i} for i in df_default.columns]
      data = df_default.to_dict('records')

   return columns,data


# Function callback for all the graphs

@app.callback(
   # callback for fig 1
    dash.dependencies.Output(component_id='graph1', component_property='figure'),
    [dash.dependencies.Input('dropdown','value')]
)


def update_fig1(value):
   """
   callback for the graph 123
   Args:
       value (_type_): _description_

   Returns:
       _type_: _description_
   """
   
   if value is not None:
      df = pd.read_csv(value)

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
      return fig1
   else:
      return {}


@app.callback(
   # callback for fig 2
    dash.dependencies.Output(component_id='graph2', component_property='figure'),
    [dash.dependencies.Input('dropdown','value')]
)

def update_fig2(value):
   """
   update figure 2
   Args:
       value (_type_): _description_
   """
   if value is not None:
      df = pd.read_csv(value)
      
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

      return fig2
   else:
      return {}


# ----------------------------------------------------------------------------------
@app.callback(
   # callback for fig 3
    dash.dependencies.Output(component_id='graph3', component_property='figure'),
    [dash.dependencies.Input('dropdown','value')]
)

def update_fig3(value):
   """
   update figure 3
   Args:
       value (_type_): _description_
   """
   if value is not None:
      df = pd.read_csv(value)
      
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

      return fig3
   else:
      return {}


@app.callback(
   # callback for fig 4
    dash.dependencies.Output(component_id='graph4', component_property='figure'),
    [dash.dependencies.Input('dropdown','value')]
)

def update_fig4(value):
   """
   update figure 4
   Args:
       value (_type_): _description_
   """
   if value is not None:
      df = pd.read_csv(value)
      numerical_columns,cate_columns = get_num_cat_dtype(df)

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

      return fig4
   else:
      return {}


@app.callback(
   # callback for fig 5
    dash.dependencies.Output(component_id='graph5', component_property='figure'),
    [dash.dependencies.Input('dropdown','value')]
)

def update_fig5(value):
   """
   update figure 5
   Args:
       value (_type_): _description_
   """
   if value is not None:
      df = pd.read_csv(value)
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

      return fig5
   else:
      return {}


if __name__ == '__main__':
    app.run_server(debug=True)

