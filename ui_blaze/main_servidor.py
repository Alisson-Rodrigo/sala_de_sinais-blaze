import typing
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtPrintSupport import *
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
import sys
import requests
from selenium import webdriver
from time import sleep
from selenium.webdriver.remote.webdriver import By


from tela_principal import Tela_Principal

class Ui_Main(object):
    def setupUi(self, Main):
        Main.setObjectName("Main")
        Main.resize(800, 650)

        self.QtStack = QtWidgets.QStackedLayout()

        self.stack0 = QtWidgets.QMainWindow()

        self.tela_principal = Tela_Principal()
        self.tela_principal.setupUi(self.stack0)

        self.QtStack.addWidget(self.stack0)

@pyqtSlot()
class SeleniumThread(QThread):
    finished = pyqtSignal()

    def __init__(self, main_instance):
        super(SeleniumThread, self).__init__()
        self.main_instance = main_instance

    def run(self):
        self.main_instance.iniciar_servidor()
        self.finished.emit()


class Main(QMainWindow, Ui_Main):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.setupUi(self)
        self.selenium_thread = SeleniumThread(self)  # Passa 'self' como 'main_instance'
        self.tela_principal.pushButton.clicked.connect(self.informacoes_servidor)
        self.contador_win = 0
        self.contador_loss = 0

        #Mensagens Padrao
        self.analise = 'ATENÇÃO, POSSIVEL ENTRADA.\nAnalisando...\n\n☠️ PIRATA DO DOUBLE ☠️'
        self.win = 'Green do Double\nPAGA TUDO!!🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩\n\n☠️ PIRATA DO DOUBLE ☠️'
        self.win_branco = '⬜ Green do branco ⬜\nRECEBA TUDO!!🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩\n\n ☠️ PIRATA DO DOUBLE ☠️'
        self.loss = 'LOSS 🟥\nEssa não deu!\nPare e volte mais tarde\n\n☠️ PIRATA DO DOUBLE ☠️'
        self.nao_confirmacao = 'Não confirmou Entrada \nAguarde o próximo sinal\n\n☠️ PIRATA DO DOUBLE ☠️'

        self.tela_principal.pushButton_2.clicked.connect(self.fechar_programa)
        self.tela_principal.pushButton.clicked.connect(self.informacoes_servidor)
        self.tela_principal.pushButton_4.clicked.connect(self.atualizar_placar_slot)
        self.tela_principal.pushButton_3.clicked.connect(self.contato)

    def contato(self):
        QMessageBox.about(self, "Contato", "Telegram: @piratadodouble\n\nEmail:)")

    def informacoes_servidor (self):
        self.tela_principal.pushButton.clicked.disconnect()
        self.id_telegram = self.tela_principal.lineEdit.text()
        self.token = self.tela_principal.lineEdit_2.text()

        if self.id_telegram == '' or self.token == '':
            QMessageBox.about(self, "Erro", "Preencha todos os campos!")
        else:
            QMessageBox.about(self, "Sucesso", "Servidor iniciado com sucesso!")
            QMessageBox.about(self, "ATENÇÃO", "Confira o seu telegram!\nCaso não tenha iniciado, verifique se o ID e o Token estão corretos!")
            self.selenium_thread.start()


    def esperar(self):
        while True:
            try:
                self.driver.find_element(By.CLASS_NAME,'time-left').find_element(By.TAG_NAME,'span').text
                break
            except:
                pass
            
        while True:
            try:
                self.driver.find_element(By.CLASS_NAME,'time-left').find_element(By.TAG_NAME,'span').text
            except:
                break
                
    def retornar_historico(self):
        return [i['color'] for i in requests.get('https://blaze.com/api/roulette_games/recent').json()][::-1]

                    
    def retornar_ultimo(self):
        return requests.get('https://blaze.com/api/roulette_games/current').json()['color']

    def martin_gale(self,gale,ultimo):
        self.enviar_mensagem(gale)
        self.esperar()
        sleep(1.5)
        ultimo_ = self.retornar_ultimo()
        if ultimo_ != ultimo and ultimo_ != 0:
            self.enviar_mensagem(self.win)
            return True
        elif ultimo_ == 0: 
            self.enviar_mensagem(self.win_branco)
            return True
                    
    def enviar_mensagem(self,mensagem):
        bot_token = f'{self.token}'
        chat_id = f'{self.id_telegram}'
        url_blaze = ''
        url = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={mensagem}\n{url_blaze}&parse_mode=Markdown'
        requests.get(url)

    def run_selenium(self):
        app_selenium = QApplication(sys.argv)
        selenium_app = Main()
        selenium_app.iniciar_servidor()
        app_selenium.exec_()

    @pyqtSlot()
    def atualizar_placar_slot(self):
        self.atualizar_placar(self.contador_win, self.contador_loss)

    def atualizar_placar(self, contador_win, contador_loss):
        print(contador_win, contador_loss)
        self.tela_principal.lineEdit_3.setText(str(contador_win))
        self.tela_principal.lineEdit_4.setText(str(contador_loss))

    def iniciar_servidor(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
    
        self.driver = webdriver.Chrome(options=options)
        self.driver.get('https://blaze.com/pt/games/double')
        sleep(5)

        cor = ['Branco','Preto','Vermelho']
        simbolo = ['⬜','⬛','🟥']
        print('Bot Grupo de sinais iniciado ...')
        self.enviar_mensagem('PIRATA DO DOUBLE INICIADO\nVAMOS PRA CIMA!\n\n☠️ PIRATA DO DOUBLE ☠️')
        while True:
            try:
                print('ok')
                self.esperar()
                sleep(1.5)
                historico = self.retornar_historico()
                ultimo = self.retornar_ultimo()
                historico.append(ultimo)
                padrao = historico[-4:]
                print(padrao)
                confirmacao = f'{simbolo[padrao[0]]} Entrada confirmada no {cor[padrao[0]]}\n{simbolo[0]} Proteção no branco'
                gale1 = f'Vamos para o gale 1 \n{simbolo[padrao[0]]} {cor[padrao[0]]}\n{simbolo[0]} Proteção no Branco'
                gale2 = f'Vamos para o gale 2 \n{simbolo[padrao[0]]} {cor[padrao[0]]}\n{simbolo[0]} Proteção no Branco'

                
                if padrao == [1,1,1,1] or padrao == [2,2,2,2] or padrao == [1,2,1,2] or padrao == [2,1,2,1]:                
                    self.enviar_mensagem(self.analise)
                    self.esperar()
                    sleep(1.5)
                    ultimo = self.retornar_ultimo()
                    while True:
                        if ultimo == padrao[0]:
                            self.enviar_mensagem(confirmacao)
                            self.esperar()
                            sleep(1.5)
                            ultimo_ = self.retornar_ultimo()
                            if ultimo_ != ultimo and ultimo_ != 0:
                                self.enviar_mensagem(self.win)
                                self.contador_win += 1
                                self.atualizar_placar(self.contador_win, self.contador_loss)
                                break
                            elif ultimo_ == 0:
                                self.enviar_mensagem(self.win_branco)
                                self.contador_win += 1
                                self.atualizar_placar(self.contador_win, self.contador_loss)
                                break
                            else:
                                if self.martin_gale(gale1,ultimo):
                                    break
                                else:
                                    if self.martin_gale(gale2,ultimo):
                                        break
                                    else:
                                        self.enviar_mensagem(self.loss)
                                        self.contador_loss += 1
                                        self.atualizar_placar(self.contador_win, self.contador_loss)
                                        break 
                        else:
                            self.enviar_mensagem(self.nao_confirmacao)
                            break
            except Exception as e:
                print(e)
                self.driver.get('https://blaze.com/pt/games/double')
                sleep(10)
                pass
        
     
    def fechar_programa(self):
        self.enviar_mensagem(f'☠️ PIRATA DO DOUBLE ☠️\n\n{self.contador_win} 🟩 X {self.contador_loss} 🟥\n\nPLACAR ATÉ O MOMENTO\n🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩')
        self.driver.quit()
        sys.exit(app.exec_())

        
if __name__ == '__main__':
    app = QApplication(sys.argv)   
    show_main = Main()
    sys.exit(app.exec_())
        