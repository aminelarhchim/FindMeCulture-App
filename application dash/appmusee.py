import sys
import os
from pathlib import Path

scriptpath = Path(os.path.dirname(os.path.abspath(__file__))).parent
sys.path.insert(0,str(scriptpath))

import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from comptage import *
from dash.dependencies import Input, Output
import data_extraction.extract_data





#creation de la dataframe des musées
objet_museum_db= data_extraction.extract_data.load_data(filename='museums',init=True)
base = objet_museum_db.data


n= len (base)




##Dash style shit
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css',dbc.themes.BOOTSTRAP]

app = dash.Dash('une nuit au musée', external_stylesheets=external_stylesheets)

app.title= "une nuit au musée"
colors = {
    'background': 'white',
    'text': '#7FDBFF'
}


 

        
def create_card(title, content):
    card = dbc.Card(
        dbc.CardBody(
            [
            html.H4(title, className="card-title", style = {
                'textAlign': 'center',
                'color':  'black',
                "font-size" : "25px" }),
            html.Br(),
            html.Br(),
            html.H2(content, style = {'textAlign': 'center','color':  'black'},className="card-subtitle"),
            html.Br(),
            
            ]
        ),
        color="blue", inverse=True, style = {'box-shadow': '2px 2px 2px lightgrey'})
    return(card)



card1= create_card ("le nombre total de musées", n)

#Body of the web app

app.layout = html.Div(
    style = {'backgroundColor':'#B9E4F6'},
    children=[  
        #Header
        html.H1(style = {'color':'#07425B',"font-size" : "50px"}, children=' une nuit au musée en France'),
       
            
        #Cards
        
        dbc.Row([
            dbc.Col ( children = [' ' ], md = 4 ),
            dbc.Col( children=[card1],style= {'height': '200px', 'width' : '200px','textAlign':'center'},md=3),
            
            dbc.Col ( children = [' ' ], md = 5 )]),
        


           
        #TextInput
        dbc.Row([
            dbc.Col(id= "leftG" , children= [
                html.Div (id="leftT1",style = {'color':'black', 'font-size':'30px','textAlign':'center'},children="Répartition des musées selon les régions"),
                
                html.Div(id = "LEFTG1", children = [html.Img(src=app.get_asset_url('musee_regions.png'),style= {'transform': 'scale(0.8)','width': '600px','height': '600px'})]),
                html.Div (id="leftT2",style = {'color':'black', 'font-size':'30px'},children="Répartition des musées selon les villes"),
                dcc.Dropdown(
                    style = {'backgroundColor':'#115776',
                    'textColor': 'black',
                    "font-size" : "25px",
                    'width': '300px',
                    'height': '50px',
                    'textAlign':'center'},
                    id= "seuil1",
                    options=[{'label': x, 'value': x} for x in [3,5,8]],
                    
                    value= '3'
                    
                    ), 
                html.Div(id='mydiv1', children='')]),
            dbc.Col(id= "RightG" , children= [
                
                html.Div (id="rightT1",style = {'color':'black', 'font-size':'25px','textAlign':'center'},children="Nombre de musées par million d'habitants et par population selon la région "),
                html.Div(id = "rightG1", children = [html.Img(src=app.get_asset_url('Nombre de musees par million dhab et population par région.png'),style= {'transform': 'scale(1.2)','width': '900px','height': '570px'})]),
        
                
                html.Div (id="rightT2",style = {'color':'black', 'font-size':'30px','textAlign':'center'},children="répartition des musées selon les départements"),
                
                dcc.Dropdown(
                    style = {'backgroundColor':'#115776',
                    'textColor': 'black',
                    "font-size" : "25px",
                    'width': '300px',
                    'height': '50px',
                    'textAlign':'center'},
                    id= "seuil2",
                    options=[{'label': x, 'value': x} for x in [10,15,20]],
                    
                    value= '10'
                
                ), 
                html.Div(id='mydiv2',children='') ])      
                
    ])])



@app.callback(
    Output(component_id='mydiv1', component_property='children'),
    [Input(component_id='seuil1', component_property='value')]
)
def update_output_div1(selectedseuil):
    seuil1=selectedseuil
    if selectedseuil == 3 :
        mydiv1= html.Img(src=app.get_asset_url('musee_par_ville_seuil3.png'),style= {'transform': 'scale(0.8)','width': '700px','height': '600px'})
        return mydiv1
        
    elif selectedseuil == 5 :
        mydiv1= html.Img(src=app.get_asset_url('musee_par_ville_seuil5.png'),style = {'transform': 'scale(0.8)','width': '700px','height': '600px'})
        return mydiv1
    else:
        mydiv1= html.Img(src=app.get_asset_url('musee_villeS_seuil8.png'),style = {'transform': 'scale(0.8)','width': '700px','height': '600px'})
        return  mydiv1
@app.callback(
    Output(component_id='mydiv2', component_property='children'),
    [Input(component_id='seuil2', component_property='value')]
)
def update_output_div2(selectedseuil):
    seuil2=selectedseuil
    if selectedseuil == 10 :
        mydiv2= html.Img(src=app.get_asset_url('musee_departement_seuil10.png'),style= {'transform': 'scale(0.8)','width': '700px','height': '600px'})
        return mydiv2
        
    elif selectedseuil == 15 :
        mydiv2= html.Img(src=app.get_asset_url('musee_departement_seuil15.png'),style = {'transform': 'scale(0.8)','width': '700px','height': '600px'})
        return mydiv2
    else:
        mydiv2= html.Img(src=app.get_asset_url('musee_departement_seuil20.png'),style = {'transform': 'scale(0.8)','width': '700px','height': '600px'})
        return  mydiv2




if __name__ == '__main__':
    app.run_server(debug=True)
