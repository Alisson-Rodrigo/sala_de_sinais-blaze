import requests

def enviar_mensagem(mensagem):
    bot_token = '5579273948:AAGpi0tVvDNPm-ULPoorakmRfY1zZGdewgY'
    chat_id = '-1001630591855'
    url_blaze = ''
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={mensagem}\n{url_blaze}&parse_mode=Markdown'
    requests.get(url)

enviar_mensagem("")