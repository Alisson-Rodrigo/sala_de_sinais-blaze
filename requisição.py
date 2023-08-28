import selenium
from selenium import webdriver
from time import sleep


navegador = webdriver.Chrome()
navegador.get('https://telegrupos.com.br/pirata-do-double-24hrs-de-sinais-gratuitos33/')


while True:
    navegador.get('https://telegrupos.com.br/pirata-do-double-24hrs-de-sinais-gratuitos33/')
    navegador.refresh()  # Use o método 'refresh' para atualizar a página
    sleep(5)  # Aguarda 60 segundos antes de fechar o navegador
