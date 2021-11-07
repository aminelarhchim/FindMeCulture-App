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
import data_extraction.extract_data







#creation de la dataframe des festivals
objet_festival_db= data_extraction.extract_data.load_data(filename='festivals',init=True)
base = objet_festival_db.data
n= len (base)


#retourne un dictionnaire dont les clés sont les noms des regions et les valeurs sont le nombre de festivals par région
dic= compte_reg(base,0)
rm=region_maximale (base)
moy=moyenne_festivals (base)




##Dash style shit
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css',dbc.themes.BOOTSTRAP]

app = dash.Dash('une nuit festive', external_stylesheets=external_stylesheets)

app.title= "une nuit festive"
colors = {
    'background': 'white',
    'text': '#7FDBFF'
}

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Une Nuit Festive En France ',
        style={
            'textAlign': 'center',
            'color': 'blue'
        }
    )])

 

        
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



card1= create_card ("le nombre total de festivales", n)
card2= create_card ("la région ayant le plus grand nombre de festivals", rm)
card3= create_card ("la moyenne des festivals par région est",int(moy) )

#Body of the web app

app.layout = html.Div(
    style = {'backgroundColor':'#B9E4F6'},
    children=[  
        #Header
        html.H1(style = {'color':'#07425B',"font-size" : "45px", 'text-align': 'center'}, children='les festivals en France'),
        html.Div(children=''),
        
        #Cards
        
        dbc.Row([
            dbc.Col ( children = [' ' ], md = 1 ),
            dbc.Col( children=[card1],style= {'height': '200px', 'width' : '200px'} ,md=3),
            dbc.Col( children=[card2],style= {'height': '200px', 'width' : '200px'},md=3),
            dbc.Col( children=[card3],style= {'height': '200px', 'width' : '200px'}, md=3)] ),
            
            
       
        dbc.Row([
            dbc.Col(id= "leftG" , children= [
                html.Div (id="leftT1",style = {'color':'black', 'font-size':'30px','textAlign':'center'},children="Répartition des festivals selon les mois de l'année"),
                
                html.Div(id = "LEFTG1", children = [html.Img(src=app.get_asset_url('histogramme_festival_par_mois.png'),style= {'transform': 'scale(0.8)','width': '700px','height': '700px'})]),
                html.Div (id="leftT2",style = {'color':'black', 'font-size':'30px'},children="Répartition des festivals selon les régions"),
                html.Div(id = "LEFTG2", children = [html.Img(src=app.get_asset_url('repartition_festivals_regions.png'),style= {'transform': 'scale(0.8)','width': '700px','height': '700px'})])]),
                
                
            dbc.Col(id= "RightG" , children= [
                
                html.Div (id="rightT1",style = {'color':'black', 'font-size':'30px','textAlign':'center'},children="Répartition des festivals selon les départements"),
                html.Div(id = "rightG1", children = [html.Img(src=app.get_asset_url('repartition_departements_festivals.png'),style= {'transform': 'scale(0.8)','width': '700px','height': '700px'})]),
        
                
                html.Div (id="rightT2",style = {'color':'black', 'font-size':'30px','textAlign':'center'},children="Nombre de departement accueillant entre x et y festivals"),
                html.Div(id = "rightG2", children = [html.Img(src=app.get_asset_url('festivals_seuil_departements_histo.png'),style= {'transform': 'scale(0.8)','width': '700px','height': '700px'})])])
                
                
    ])])

        
         
 
if __name__ == '__main__':
    app.run_server(debug=True)
