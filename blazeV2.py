import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.remote.webdriver import By
from time import sleep
import requests



driver = webdriver.Chrome()
driver.get('https://blaze.com/pt/games/double')
sleep(5)

#Mensagens Padrao
analise = 'POSSIVEL ENTRADA, ATENÇÃO.\nANALISANDO...\n\n☠️ PIRATA DO DOUBLE ☠️'
analise = 'ATENÇÃO, POSSIVEL ENTRADA.\nAnalisando...\n\n☠️ PIRATA DO DOUBLE ☠️'
win = 'Green do Double\nPAGA TUDO!!🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩\n\n☠️ PIRATA DO DOUBLE ☠️'
win_branco = '⬜ Green do branco ⬜\nRECEBA TUDO!!🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩\n\n ☠️ PIRATA DO DOUBLE ☠️'
loss = 'LOSS 🟥\nEssa não deu!\nPare e volte mais tarde\n\n☠️ PIRATA DO DOUBLE ☠️'
nao_confirmacao = 'Não confirmou Entrada \nAguarde o próximo sinal\n\n☠️ PIRATA DO DOUBLE ☠️'
contador_win_brancos = 0
##############################

def esperar():
    while True:
        try:
            driver.find_element(By.CLASS_NAME,'time-left').find_element(By.TAG_NAME,'span').text
            break
        except:
            pass
    
    while True:
        try:
            driver.find_element(By.CLASS_NAME,'time-left').find_element(By.TAG_NAME,'span').text
        except:
            break
        
def retornar_historico():
    return [i['color'] for i in requests.get('https://blaze.com/api/roulette_games/recent').json()][::-1]

            
def retornar_ultimo():
    return requests.get('https://blaze.com/api/roulette_games/current').json()['color']

def martin_gale(gale,ultimo):
    enviar_mensagem(gale)
    esperar()
    sleep(1.5)
    ultimo_ = retornar_ultimo()
    if ultimo_ != ultimo and ultimo_ != 0:
        enviar_mensagem(win)
        return True
    elif ultimo_ == 0: 
        enviar_mensagem(win_branco)
        return True
            
def enviar_mensagem(mensagem):
    bot_token = '5579273948:AAGpi0tVvDNPm-ULPoorakmRfY1zZGdewgY'
    chat_id = '-1001630591855'
    url_blaze = ''
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={mensagem}\n{url_blaze}&parse_mode=Markdown'
    requests.get(url)


cor = ['Branco','Preto','Vermelho']
simbolo = ['⬜','⬛','🟥']


print('Bot Grupo de sinais iniciado ...')
enviar_mensagem('PIRATA DO DOUBLE INICIADO\nVAMOS PRA CIMA!\n\n☠️ PIRATA DO DOUBLE ☠️')
contador_win = 0
contador_loss = 0

while True:
    try:
        print('ok')
        esperar()
        sleep(1.5)
        historico = retornar_historico()
        ultimo = retornar_ultimo()
        historico.append(ultimo)
        padrao = historico[-4:]
        print(padrao)
        confirmacao = f'{simbolo[padrao[0]]} Entrada confirmada no {cor[padrao[0]]}\n{simbolo[0]} Proteção no branco'
        gale1 = f'Vamos para o gale 1 \n{simbolo[padrao[0]]} {cor[padrao[0]]}\n{simbolo[0]} Proteção no Branco'
        gale2 = f'Vamos para o gale 2 \n{simbolo[padrao[0]]} {cor[padrao[0]]}\n{simbolo[0]} Proteção no Branco'

    
        if padrao == [1,1,1,1] or padrao == [2,2,2,2] or padrao == [1,2,1,2] or padrao == [2,1,2,1]:                
            enviar_mensagem(analise)
            esperar()
            sleep(1.5)
            ultimo = retornar_ultimo()
            while True:
                if ultimo == padrao[0]:
                    enviar_mensagem(confirmacao)
                    esperar()
                    sleep(1.5)
                    ultimo_ = retornar_ultimo()
                    if ultimo_ != ultimo and ultimo_ != 0:
                        enviar_mensagem(win)
                        contador_win += 1
                        print (contador_win, contador_loss)
                        break
                    elif ultimo_ == 0:
                        enviar_mensagem(win_branco)
                        contador_win += 1
                        break
                    else:
                        if martin_gale(gale1,ultimo):
                            break
                        else:
                            if martin_gale(gale2,ultimo):
                                break
                            else:
                                enviar_mensagem(loss)
                                break 
                else:
                    enviar_mensagem(nao_confirmacao)
                    break
    except Exception as e:
        print(e)
        driver.get('https://blaze.com/pt/games/double')
        sleep(10)
        pass