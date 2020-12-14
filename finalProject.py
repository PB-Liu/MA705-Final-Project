# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 22:05:17 2020

@author: Pengbo
"""

# 0. Import packages and raw data 

import pandas as pd 
import datetime
import re 
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import dash_table



df = pd.read_csv('jobs.csv')


# 1. Data Cleaning 


# 1.1 drop all redundant columns 

df1 = df.drop(['Id', 'Start time',  'Deadline', 'How to apply', 'PhilJobs page', 
        'Info link', 'Application link'], axis =1)


#%%
# 1.2 add a new column 'year'; filter the dateframe for years since 2015

dt = df1['Date posted']

years = []

for date in dt:
    date_obj = datetime.datetime.strptime(date, '%Y-%m-%d')
    year = datetime.datetime.strftime(date_obj,'%Y')
    years.append(year)

df1['Year'] = years 
df1 = df1[df1['Year'] >= '2014-1-1']

#%%


#%%
# 1.3 Simplify the "Contract Type" column 


def replace(x): 
    new = []
    for term in x:
        if re.search("Tenure-track", term):
            term = "Tenure-track"
        elif re.search("Tenured", term):
            term = "Tenured"
        elif re.search("open", term):
            term = "Contract open"
        new.append(term)
    return new

df1["Contract type"] = replace(df1["Contract type"])
        

#%%

# 2. Data Processing: creating dataframes for dashboard 

#2.1 Define functions to re-classify job areas into 11 major categories 


def me(x):
    if re.search('metaphysics|epistemology|philosophy of religion|philosophy of action|agency|theoretical|knowledge',
                 x,  re.IGNORECASE):
        return True 
    else: return False 

def ml(x): 
    if re.search('philosophy of mind|philosophy of language|semantics|perception',
                 x,  re.IGNORECASE):
        return True 
    else: return False 

def sl(x):
    if re.search('science|physics|biology|computing|logic|mathematics|cogniti|decision theory|economics|psychology',
                 x,  re.IGNORECASE):
        return True 
    else: return False 

def eth(x): 
    if re.search('ethics|value theory|practical|moral|ethical|environmental|climate',
                 x,  re.IGNORECASE):
        return True 
    else: return False 
    
def sp(x):
    if re.search('social|political|democracy|law|policy',
                 x,  re.IGNORECASE):
        return True 
    else: return False 
    
def rg(x):
    if re.search('race|gender|feminis|racial',
                 x,  re.IGNORECASE):
        return True 
    else: return False 
    
def wh(x):
    if re.search('ancient|greek|roman|modern|kant|medieval|catholic|renaissance|century|jewish|pragmatism|history|analytic',
                 x,  re.IGNORECASE):
        return True 
    else: return False 
    
def con(x):
    if re.search('continental|phenomenology|existentialism|European Philosophy|French|german',
                 x,  re.IGNORECASE):
        return True 
    else: return False 

def nw(x):
    if re.search('asian|african|islam|latin|arabic|chinese|indian|buddhis|native|comparative|non-western',
                 x,  re.IGNORECASE):
        return True 
    else: return False 

def aes(x):
    if re.search('aesthetics|art|film',
                 x,  re.IGNORECASE):
        return True 
    else: return False 

def op(x):
    if re.search('open',
                 x,  re.IGNORECASE):
        return True 
    else: return False 
    
#%%

#%%

#2.2 Generate a new dataframe to display openings according to the AOS(are of specialization)

def convert(df):
    areas = []
    years = []
    c_type= []
    for i in range(len(df)):
        row = df.iloc[i]
        x = str(row['AOS']) # +str(row['AOC']) to get openings according to both AOS and AOC (area of competence)
        year = row['Year']
        job = row['Contract type']
        if me(x):
            areas.append('Metaphysics & Epistemology')
            years.append(year)
            c_type.append(job)   
        if ml(x):
            areas.append('Mind & Language')
            years.append(year)
            c_type.append(job)   
        if sl(x):
            areas.append('Science, Logic & Maths')
            years.append(year)
            c_type.append(job)   
        if eth(x):
            areas.append('Ethics')
            years.append(year)
            c_type.append(job)   
        if sp(x): 
            areas.append('Social & Political')
            years.append(year)
            c_type.append(job)   
        if rg(x):
            areas.append('Race & Gender')
            years.append(year)
            c_type.append(job)   
        if wh(x):
            areas.append('Western History')
            years.append(year)
            c_type.append(job)   
        if con(x):
            areas.append('Continental')
            years.append(year)
            c_type.append(job)   
        if nw(x):
            areas.append('Non-Western')
            years.append(year)
            c_type.append(job)
        if aes(x):
            areas.append('Aesthetics & Art')
            years.append(year)
            c_type.append(job)    
        if op(x):
            areas.append('Open')
            years.append(year)
            c_type.append(job)  
        if not(me(x) or ml(x) or sl(x) or eth(x) or sp(x) or rg(x) 
               or wh(x) or con(x) or nw(x) or aes(x) or op(x)):
            areas.append('Other')
            years.append(year)
            c_type.append(job)    
    tuples = list(zip(years,areas,c_type))
    new_df = pd.DataFrame(tuples, columns = ['Year', 'Area', "Type"]).sort_values('Year')
    new_df = new_df.reset_index(drop = True)
    return new_df
            

df2 = convert(df1)



#%%

# 2.3 Group and summarize the data 1) by years, areas, and contract types and 2) years and areas 


grouped = df2.groupby(["Year","Area", "Type"])
df3 = grouped["Area"].count().to_frame(name = 'Openings').reset_index()


grouped2 = df2.groupby(["Year","Area"])
df4 = grouped2["Area"].count().to_frame(name = 'Openings').reset_index()


#%%

# 3. Creating Dashboard

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div([
    html.H1("The Philosophy Job Market: 2015 - 2020", style={'text-align': 'center'}),
    dcc.Markdown('''
                 #### A summary of philosophy job openings from 2015 to 2020
                 
                 Data from [PhilJobs](https://philjobs.org)
               
                 '''),
    html.Div(
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df3.columns],
            data=df3.to_dict('records'),
            style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold'
            },
            sort_action = 'native',
            sort_mode ='multi',
            column_selectable="multi",
            selected_columns=[],
            page_current = 0,
            page_size = 10,
            style_data = {
                'whiteSpace': 'normal',
                'height': 'auto'
                }
        ),
        ),
    html.Div(className = "column", style = {'columnCount': 2}, children = [
        html.Div([
            html.Div([
                html.H2("Types & Areas of Jobs by Year"),
                dcc.Dropdown(
                    id = "slct_year",
                    options = [
                          {"label": "2015", "value": "2015"},
                          {"label": "2016", "value": "2016"},
                          {"label": "2017", "value": "2017"},
                          {"label": "2018", "value": "2018"},
                          {"label": "2019", "value": "2019"},
                          {"label": "2020", "value": "2020"}],
                    multi= False, 
                    value = "2020"
                    ),
                dcc.Graph(id='dist', figure={}, style={'display': 'inline-block'})
                ]),
            html.Div([
                html.H2("Trends of Jobs by Area"),
                dcc.Dropdown(id="slct_area",
                      options=[
                          {"label": "Metaphysics & Epistemology", "value": 'Metaphysics & Epistemology'},
                          {"label": 'Mind & Language', "value": 'Mind & Language'},
                          {"label": 'Ethics', "value": 'Ethics'},
                          {"label": 'Social & Political', "value": 'Social & Political'},
                          {"label": 'Science, Logic & Mathematics', "value": 'Science, Logic & Maths'},
                          {"label": 'Western History', "value": 'Western History'}, 
                          {"label": 'Continental philosophy', "value": 'Continental'},
                          {"label": 'Non-Western Philosophy', "value": 'Non-Western'},
                          {"label": 'Race & Gender', "value": 'Race & Gender'},
                          {"label": 'Aesthetics & Art', "value": 'Aesthetics & Art'},
                          {'label': 'Open', "value": "Open"}
                    ],
                      value=['Ethics', 'Metaphysics & Epistemology', 'Western History', 'Social & Political'],
                      multi = True
                    ),
                dcc.Graph(id='areaTrends', figure={})
            ]),
        ])
        ])
    ])

    

@app.callback(
    Output('table', 'style_data_conditional'),
    [Input('table', 'selected_columns')]
)
def update_styles(selected_columns):
    return [{
        'if': {'column_id': i},
        'background_color': '#D2F3FF'
    } for i in selected_columns]



@app.callback(
    Output(component_id='areaTrends', component_property='figure'),
    Input(component_id='slct_area', component_property='value'),
)

def update_graph1(option_slctd):
    # print(option_slctd)
    # print(type(option_slctd))


    dff = df4.copy()
    dff = dff[dff["Area"].isin(option_slctd)]

    # Plotly Express
    fig1 = px.line(dff, x="Year", y= "Openings", color = 'Area')
    
    return fig1 

@app.callback(
    Output(component_id='dist', component_property='figure'),
    Input(component_id = 'slct_year', component_property ='value')
)

def update_graph2(option_year):
    df5 = df2[df2["Year"]== option_year]
    grouped5 = df5.groupby(["Year","Area","Type"])
    df5 = grouped5["Area"].count().to_frame(name = 'Openings').reset_index()
    fig2 = px.sunburst(df5, path=['Type','Area'], values='Openings')
    fig2.update_traces(textinfo='label+percent entry')
    return fig2


if __name__ == '__main__':
    app.run_server(debug=True)











