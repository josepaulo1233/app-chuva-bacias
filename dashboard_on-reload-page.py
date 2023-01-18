from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import datetime
import os
from urllib.request import urlopen
import json
import numpy as np
from datetime import datetime as dt

## versão 2

psat_files = '/home/josepaulo/demo-app3/psat_files'
json_files = '/home/josepaulo/demo-app3/json_files'

with urlopen('https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson') as response: Brazil = json.load(response) # Javascrip object notation

grande_shp = open(json_files + '/rio_grande.json')
grande_shp = json.load(grande_shp)

uruguai_shp = open(json_files + '/rio_uruguai.json')
uruguai_shp = json.load(uruguai_shp)

iguacu_shp = open(json_files + '/rio_iguacu.json')
iguacu_shp = json.load(iguacu_shp)

tocantins_shp = open(json_files + '/rio_tocantins.json')
tocantins_shp = json.load(tocantins_shp)

saofrancisco_shp = open(json_files + '/rio_saofrancisco.json')
saofrancisco_shp = json.load(saofrancisco_shp)

paranaiba_shp = open(json_files + '/rio_paranaiba.json')
paranaiba_shp = json.load(paranaiba_shp)

parana_shp = open(json_files + '/rio_parana.json', encoding='UTF-8')
parana_shp = json.load(parana_shp)

paranapanema_shp = open(json_files + '/rio_paranapanema.json', encoding='UTF-8')
paranapanema_shp = json.load(paranapanema_shp)

def gera_mapa_latlon_psat(data_do_arquivo):

    df = pd.read_table(psat_files + '/' + data_do_arquivo, delim_whitespace=True, header=None)
    df.columns = ['nome','lat','lon','prec']
    df.set_index('nome', inplace=True)

    points = ['PSATAGV' , 'PSATCMG', 'PSATCES', 'PSATELC', 'PSATFUN', 'PSATFUR', 'PSATMRB', 'PSATPRG', 'PSATPAS','PSATPTB', 'PSATPTC',
              'PSATFZA', 'PSATJSG', 'PSATSCX', 'PSATSCL', 'PSATUVT',
              'PSATBSM', 'PSATFLE', 'PSATITP', 'PSATIVM', 'PSATPTQ','PSATISOT', 'PSATJUP', 'PSATSDG', 'PSATFZBT', 'PSATPPRA',
              'PSATESP', 'PSATSRC', 'PSATFRCL','PSATCBI', 'PSATCBIV', 'PSATEMB', 'PSATIMBR', 'PSATNPTE', 'PSATARV', 'PSATSFC', 'PSATSSM',
              'PSATCNI', 'PSATCPV', 'PSATCHT', 'PSATJUR', 'PSATMAU', 'PSATROS',
              'PSATQMD', 'PSATRBX', 'PSATSFR', 'PSATSRM', 'PSATTMR', 'PSATBOQ',
              'PSATSME', 'PSATBTE', 'PSATARAG', 'PSATLAJ', 'PSATPTRL', 'PSATLJET', 'PSATUCR',
              'PSATBGR', 'PSATCNV', 'PSATFCH', 'PSATITA', 'PSATMCD', 'PSATMOJ', 'PSATQQX', 'PSATPSJ']

    df = df.loc[points]

    fig = go.Figure(go.Scattermapbox(
            lon = df['lon'],
            lat = df['lat'],
            text = 'Cógido: ' + df.index + '<br>' + 'Chuva: ' + df['prec'].astype(str) + 'mm',
            mode = 'markers',
            marker=go.scattermapbox.Marker(
            size=10,
            color=df['prec'],
            opacity=1,
            showscale=True,
            colorscale= 'YlOrRd',
            cmax=50,
            cmin=0)

    ))

    fig.update_layout(
            mapbox = {
            'style': "open-street-map",
            'center': { 'lon': -55, 'lat': -15},
            'zoom':3,
            'layers': [
                {
                'source': Brazil,
                'type':'fill', 'below':'traces','color': 'gray', 'opacity' : 0.5
                },
                {
                'source': grande_shp,
                'type':'fill', 'below':'traces','color': 'blue', 'opacity' : 0.5
                },
                {
                'source': saofrancisco_shp,
                'type':'fill', 'below':'traces','color': 'red', 'opacity' : 0.5
                },
                {
                'source': iguacu_shp,
                'type':'fill', 'below':'traces','color': 'yellow', 'opacity' : 0.5
                },
                {
                'source': paranaiba_shp,
                'type':'fill', 'below':'traces','color': 'green', 'opacity' : 0.5
                },
                {
                'source': tocantins_shp,
                'type':'fill', 'below':'traces','color': 'magenta', 'opacity' : 0.5
                },
                {
                'source': uruguai_shp,
                'type':'fill', 'below':'traces','color': 'orange', 'opacity' : 0.5
                },
                {
                'source': parana_shp,
                'type':'fill', 'below':'traces','color': 'gold', 'opacity' : 0.5
                },
                {
                'source': paranapanema_shp,
                'type':'fill', 'below':'traces','color': 'cyan', 'opacity' : 0.5
            }],
            },
            height=500, margin={"r":0,"t":0,"l":0,"b":0}, hoverlabel=dict(
            font_size=16,
            font_family="Montserrat"),
    )

    return fig

def gera_graf(df, index, nome_bacia):

    df = pd.DataFrame(df, index = index)
    df.columns = ['Precipitação']
    graf = px.bar(df, x = df.index, y ='Precipitação', title= f"<b>Precipitação acumulada média na bacia do rio {nome_bacia.upper()}</b>", color='Precipitação', range_color=[0,30], color_continuous_scale='YlOrRd', template='plotly_white', text='Precipitação')
    graf.update_layout(hoverlabel=dict(bgcolor="white", font_size=16, font_family="Cambria"), xaxis_title=None, font_family='Montserrat')
    graf.update_xaxes(tick0=index[0], dtick="d1", tickformat="%d/%b")
    graf.update_traces(hovertemplate = 'Dia = %{x}<br>Precipitação = %{y} mm<extra></extra>', textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    graf.update_coloraxes(colorbar_title=None, colorbar_thickness=15)

    return graf

app = Dash(__name__,
           external_stylesheets=[dbc.themes.MINTY],
           meta_tags=[{'name': 'viewport','content': 'width=device-width, initial-scale=1.0'}])

def server_layout():

    my_txt_files = []
    my_txt_files_name = []
    for file in os.listdir(psat_files):
        if file.endswith(".txt"):
            my_txt_files.append(os.path.join(psat_files, file))
            my_txt_files_name.append(file)

    my_txt_files_name = sorted(my_txt_files_name)
    my_txt_files_name.sort(key=lambda date: dt.strptime(date, "psat_%d%m%Y.txt"))
    my_txt_files_name = my_txt_files_name[-30:]

    values_grande = []
    values_iguacu = []
    values_parana = []
    values_paranapanema = []
    values_paranaiba = []
    values_tocantins = []
    values_saofrancisco = []
    values_uruguai = []

    for filename in my_txt_files_name:

        file = psat_files + '/' + filename

        dff = pd.read_table(file, delim_whitespace=True, header=None)

        # colocando em um dff

        dff.columns=['NAME','LAT','LON','PREC']

        # separando em bacias

        sub_bacias_grande = ['PSATAGV' , 'PSATCMG', 'PSATCES', 'PSATELC', 'PSATFUN', 'PSATFUR', 'PSATMRB', 'PSATPRG', 'PSATPAS','PSATPTB', 'PSATPTC']

        sub_bacias_iguacu = ['PSATFZA', 'PSATJSG', 'PSATSCX', 'PSATSCL', 'PSATUVT']

        sub_bacias_parana = ['PSATBSM', 'PSATFLE', 'PSATITP', 'PSATIVM', 'PSATPTQ','PSATISOT', 'PSATJUP', 'PSATSDG', 'PSATFZBT', 'PSATPPRA']

        sub_bacias_paranaiba = ['PSATESP', 'PSATSRC', 'PSATFRCL','PSATCBI', 'PSATCBIV', 'PSATEMB', 'PSATIMBR', 'PSATNPTE', 'PSATARV', 'PSATSFC', 'PSATSSM']

        sub_bacias_paranapanema = ['PSATCNI', 'PSATCPV', 'PSATCHT', 'PSATJUR', 'PSATMAU', 'PSATROS']

        sub_bacias_saofrancisco = ['PSATQMD', 'PSATRBX', 'PSATSFR', 'PSATSRM', 'PSATTMR', 'PSATBOQ']

        sub_bacias_tocantins = ['PSATSME', 'PSATBTE', 'PSATARAG', 'PSATLAJ', 'PSATPTRL', 'PSATLJET', 'PSATUCR']

        sub_bacias_uruguai = ['PSATBGR', 'PSATCNV', 'PSATFCH', 'PSATITA', 'PSATMCD', 'PSATMOJ', 'PSATQQX', 'PSATPSJ']

        dff.set_index('NAME', inplace=True)

        grande = np.round(dff.loc[sub_bacias_grande]['PREC'].mean(), 0)
        iguacu = np.round(dff.loc[sub_bacias_iguacu]['PREC'].mean(), 0)
        parana = np.round(dff.loc[sub_bacias_parana]['PREC'].mean(), 0)
        paranaiba = np.round(dff.loc[sub_bacias_paranaiba]['PREC'].mean(), 0)
        paranapanema = np.round(dff.loc[sub_bacias_paranapanema]['PREC'].mean(), 0)
        saofrancisco = np.round(dff.loc[sub_bacias_saofrancisco]['PREC'].mean(), 0)
        tocantins = np.round(dff.loc[sub_bacias_tocantins]['PREC'].mean(), 0)
        uruguai = np.round(dff.loc[sub_bacias_uruguai]['PREC'].mean(), 0)

        values_grande.append(grande)
        values_iguacu.append(iguacu)
        values_parana.append(parana)
        values_paranapanema.append(paranapanema)
        values_paranaiba.append(paranaiba)
        values_tocantins.append(tocantins)
        values_saofrancisco.append(saofrancisco)
        values_uruguai.append(uruguai)

    # soma da chuva acumulada

    chuva_grande = np.sum(values_grande)
    chuva_iguacu = np.sum(values_iguacu)
    chuva_parana = np.sum(values_parana)
    chuva_paranapanema = np.sum(values_paranapanema)
    chuva_paranaiba = np.sum(values_paranaiba)
    chuva_tocantins = np.sum(values_tocantins)
    chuva_saofrancisco = np.sum(values_saofrancisco)
    chuva_uruguai = np.sum(values_uruguai)

    diaini = int(my_txt_files_name[0][5:7])
    mesini = int(my_txt_files_name[0][7:9])
    anoini = int(my_txt_files_name[0][9:13])

    diafim = int(my_txt_files_name[-1][5:7])
    mesfim = int(my_txt_files_name[-1][7:9])
    anofim = int(my_txt_files_name[-1][9:13])

    start = datetime.datetime(anoini, mesini, diaini)
    end = datetime.datetime(anofim, mesfim, diafim)
    daterange = pd.date_range(start, end)


    grande = gera_graf(values_grande, daterange, 'grande')
    paranaiba = gera_graf(values_paranaiba, daterange,'paranaiba')
    tocantins = gera_graf(values_tocantins, daterange,'tocantins')
    saofrancisco = gera_graf(values_saofrancisco, daterange,'são francisco')
    paranapanema = gera_graf(values_paranapanema, daterange,'paranapanema')
    parana = gera_graf(values_parana, daterange,'parana')
    iguacu = gera_graf(values_iguacu, daterange,'iguaçu')
    uruguai = gera_graf(values_uruguai, daterange,'uruguai')

    return   dbc.Container([

                dbc.Row([

                    dbc.Col(html.H1('Painel precipitação - PSAT ',
                                    className='text-left text-white mb-4 mt-2'),
                            width=12),
                    html.Hr()

                ], className='alert alert-primary mt-1'),

                dbc.Row([

                    dbc.Col([

                        html.P('Selecione a data desejada'),
                        dcc.Dropdown(id='lista-de-arquivos', multi=False, value=my_txt_files_name[-1], options=my_txt_files_name, className='text-primary w-50'),


                    ], xs=12, sm=12, md=12, lg=5, xl=5)

                ]),

                dbc.Row([

                    dbc.Col([

                        dcc.Graph(id='mapa-grafico', className='mt-4 border-dark shadow-lg p-1 mb-2 bg-white rounded'),

                    ], xs=12, sm=12, md=12, lg=12, xl=12)

                ]),

                dbc.Row([

                    html.H3('Precipitação acumulada média por bacia', className='mt-4 mb-4')

                ]),

                ## tocantins e sao francisco

                dbc.Row([

                    dbc.Col([

                        dcc.Graph(id='graf-tocantins', figure=tocantins, className='mb-4 border-dark shadow-lg p-1 mb-2 bg-white rounded')

                    ], xs=12, sm=12, md=12, lg=5, xl=5),

                    dbc.Col([

                        dcc.Graph(id='graf-saofrancisco', figure=saofrancisco, className='mb-4 border-dark shadow-lg p-1 mb-2 bg-white rounded')

                    ], xs=12, sm=12, md=12, lg=5, xl=5)

                ], justify='around'),

                ## grande e paranaiba

                dbc.Row([

                    dbc.Col([

                        dcc.Graph(id='graf-grande', figure=grande, className='mb-4 border-dark shadow-lg p-1 mb-2 bg-white rounded')

                    ], xs=12, sm=12, md=12, lg=5, xl=5),

                    dbc.Col([

                        dcc.Graph(id='graf-paranaiba', figure=paranaiba, className='mb-4 border-dark shadow-lg p-1 mb-2 bg-white rounded')

                    ], xs=12, sm=12, md=12, lg=5, xl=5)

                ], justify='around'),

                ## parana e paranapanema

                dbc.Row([

                    dbc.Col([

                        dcc.Graph(id='graf-parana', figure=parana, className='mb-4 border-dark shadow-lg p-1 mb-2 bg-white rounded')

                    ], xs=12, sm=12, md=12, lg=5, xl=5),

                    dbc.Col([

                        dcc.Graph(id='graf-paranapanema', figure=paranapanema, className='mb-4 border-dark shadow-lg p-1 mb-2 bg-white rounded')

                    ], xs=12, sm=12, md=12, lg=5, xl=5)

                ], justify='around'),

                ## uruguai e iguacu

                dbc.Row([

                    dbc.Col([

                        dcc.Graph(id='graf-uruguai', figure=uruguai, className='mb-4 border-dark shadow-lg p-1 mb-2 bg-white rounded')

                    ], xs=12, sm=12, md=12, lg=5, xl=5),

                    dbc.Col([

                        dcc.Graph(id='graf-iguacu', figure=iguacu, className='mb-4 border-dark shadow-lg p-1 mb-2 bg-white rounded')

                    ], xs=12, sm=12, md=12, lg=5, xl=5)

                ], justify='around')


            ], fluid=True, className="dbc")

app.layout = server_layout

@app.callback(
        Output('mapa-grafico', 'figure'),
        Input('lista-de-arquivos', 'value')

    )

def update_output(value):

    df = gera_mapa_latlon_psat(value)

    return df

if __name__ == '__main__':
    app.run_server()