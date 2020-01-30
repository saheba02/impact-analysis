# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 23:38:16 2020

@author: Naresh
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.figure_factory as ff

import pandas as pd


def gantt_fig(df):
    data = []

    for row in df.itertuples():
        data.append(dict(Task=str(row.Task), Start=str(row.Start),
                         Finish=str(row.Finish), Resource=str(row.Task)))

    colors = {'PSG NIGHTS': 'rgb(220, 0, 0)',
          'BLUE ECG': 'rgb(1, 0.9, 0.16)',
          'BLUE ACC': 'rgb(0, 255, 100)'}
    
    fig = ff.create_gantt(data, index_col='Resource',
                          reverse_colors=False, show_colorbar=True,
                          showgrid_x=True, title='Time overlap Chart',group_tasks=True)
    
    fig.layout.xaxis.tickformat = '%m-%d %H:%M'
    fig['layout'].update( margin=dict(l=310))

    return fig

df = pd.read_pickle('Sleep_study_Psg_blue_pods.pickle')
df['SUBJ'] = df['SUBJ'].apply(lambda x:'{:05}'.format(int(x)))

options = df['SUBJ'].unique()

app = dash.Dash()

app.layout = html.Div([html.H1('PSG Blue Pods'),
                       dcc.Dropdown(id='my-dropdown',
                                    options=[{'label': n, 'value': n}
                                             for n in options],
                                    value=options[0]),
                       dcc.Graph(id='display-selected-value')
                      ]
                     )



@app.callback(
    dash.dependencies.Output('display-selected-value', 'figure'),
    [dash.dependencies.Input('my-dropdown', 'value')])
def update_gantt(value):
    df2plot = df[df['SUBJ']==value].reset_index(drop=True)
    fig = gantt_fig(df2plot)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True,port=5055)