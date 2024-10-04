import urllib.parse
import requests
import json
import os
from pymongo import MongoClient
from dotenv import load_dotenv
from time import sleep

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
    tag = urllib.parse.quote(input("Digite a TAG do usuário: "))
    url_historico = url+'players/'+tag+'/battlelog'
    response = requests.get(url=url_historico,headers=headers)
    jsons = json.loads(response.text)
    for item in jsons:
        collection.insert_one(item)
    print("Historico inserido!")
    

def salva_dados_jogador():
    collection = db_connection.get_collection('Dados_jogador')
    tag = urllib.parse.quote(input("Digite a TAG do usuário: "))
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
    tag = urllib.parse.quote(input("Digite a TAG do usuário: "))
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
    tag = urllib.parse.quote(input("Digite a TAG do usuário: "))
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

def menu():
    print("\n" *(os.get_terminal_size().lines - 1))
    print("=" * os.get_terminal_size().columns)
    print(F"[0] salvar historico de conta \n [1] salvar dados do jogador \n [2] buscar dados de um jogador \n [3] buscar historico de um jogador \n [4] SAIR ")
    opcao = input()
    return opcao
while True:
    opcao = menu()
    match opcao:
        case '0':
            salva_historico()
            sleep(2)
        case '1':
            salva_dados_jogador()
            sleep(2)
        case '2':
            get_player_data()
            sleep(2)
        case '3':
            get_player_history()
            sleep(2)
        case '4':
            print('Saindo do sistema...')
            break