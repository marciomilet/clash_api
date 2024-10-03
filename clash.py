import requests
import json
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('authorization')
url = 'https://api.clashroyale.com/v1/'
connection_string = os.getenv('connection')
client = MongoClient(connection_string)
db_connection = client['ClashRoyale']




headers = {
    'Content-type': 'application/json',
    'Authorization': token
}

def salva_historico():
    collection = db_connection.get_collection('Historico')
    tag = input("Digite a TAG do usuário: ")
    url_historico = url+'players/'+tag+'/battlelog'
    response = requests.get(url=url_historico,headers=headers)
    jsons = json.loads(response.text)
    for item in jsons:
        collection.insert_one(item)

def salva_dados_jogador():
    collection = db_connection.get_collection('Dados_jogador')
    tag = input("Digite a TAG do usuário: ")
    url_jogador = url+'players/'+tag
    response = requests.get(url=url_jogador,headers=headers)
    dados_jogador =json.loads(response.text)
    vitorias = dados_jogador.get('wins')
    derrotas = dados_jogador.get('losses')
    partidas = vitorias+derrotas
    win_rate = str(round((vitorias/partidas)*100 , 2))+'%'

    dados_jogador['win_rate'] = win_rate

    collection.insert_one(dados_jogador)

def get_player_data():
    tag = input("Digite a TAG do usuário: ")
    url_player = url+'players/'+tag
    response = requests.get(url=url_player,headers=headers)

    if(response.status_code == 200):
        resposta = json.loads(response.text)
        vitorias = resposta.get('wins')
        derrotas = resposta.get('losses')
        partidas = vitorias+derrotas
        win_rate = str(round((vitorias/partidas)*100 , 2))+'%'

def get_all_cards():
    response = requests.get(url=url+'cards',headers=headers)
    if(response.status_code == 200):
        items_objeto = json.loads(response.text)
        items_lista = items_objeto.get('items')

        for item in items_lista:
            print('id'+ str(item['id']))
            print('nome'+ item['name'])
            print('=======================')
    else:
        print('erro na requisição')

def get_player_history():
    tag = input("Digite a TAG do usuário: ")
    url_historico = url+'players/'+tag+'/battlelog'
    response = requests.get(url=url_historico,headers=headers)
    resposta_lista = json.loads(response.text)

    for item in resposta_lista:
        partidas_jogador = item['team']
        partidas_oponente = item['opponent']
        for item in partidas_jogador:
            coroas_jogador = item['crowns']
            print('jogador:',coroas_jogador)
        for item in partidas_oponente:
            coroas_oponente = item['crowns']
            print('oponente:',coroas_oponente)
        if coroas_jogador > coroas_oponente:
            print('vitoria')
        else:
            print('derrota')

salva_dados_jogador()