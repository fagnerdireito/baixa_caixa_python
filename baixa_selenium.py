#!/usr/bin/env python3
import time
import os
from dotenv import load_dotenv
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from flask import Flask, request, redirect, jsonify
from flask_cors import CORS

load_dotenv()

senha_caixa = os.getenv('SENHA_CAIXA')
login_caixa = os.getenv('LOGIN_CAIXA')

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

urlbase = "https://ecobranca.caixa.gov.br/ecobranca/index.jsp"

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'


options = Options()
options.add_argument(f'user-agent={user_agent}')
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

@app.route('/')
def index():
		return "Hello, World!"
# inicia flask
@app.route('/baixa', methods=['GET'])
def baixa():
	nosso_numero_get = request.args.get('numero')
	try:
		driver.get(urlbase)

		time.sleep(5)

		# login
		driver.find_element('xpath', '/html/body/table[3]/tbody/tr[3]/td/form/table/tbody/tr/td[2]/table[1]/tbody/tr[3]/td/input[1]').send_keys(login_caixa)

		driver.find_element('xpath', '/html/body/table[3]/tbody/tr[3]/td/form/table/tbody/tr/td[2]/table[1]/tbody/tr[5]/td/input').send_keys(senha_caixa)

		driver.find_element('xpath', '/html/body/table[3]/tbody/tr[3]/td/form/table/tbody/tr/td[2]/table[2]/tbody/tr[2]/td/a').click()

		driver.find_element('xpath', '/html/body/form/table[3]/tbody/tr[3]/td/table[2]/tbody/tr/td[2]/table[4]/tbody/tr[3]/td/table/tbody/tr/td[2]/a').click()
		# navega até a tela de baixa de boleto
		driver.get('https://ecobranca.caixa.gov.br/ecobranca/baixa_titulo')

		nosso_numero = nosso_numero_get

		driver.find_element('xpath', "/html/body/form/span/table[2]/tbody/tr[3]/td/table[2]/tbody/tr/td[2]/table[1]/tbody/tr[15]/td[2]/input").send_keys(nosso_numero)

		driver.find_element('xpath', "/html/body/form/span/table[2]/tbody/tr[3]/td/table[2]/tbody/tr/td[2]/table[3]/tbody/tr/td/a[2]").click()

		# CHECK IF EXISTS ELEMENT RADIO BUTTON
		try:
			radio_button = driver.find_element('xpath', "/html/body/form/span/table[2]/tbody/tr[2]/td/table[2]/tbody/tr[1]/td/table/tbody/tr[6]/td[1]/input")

			if radio_button:
					# print("Boleto encontrado.")
					# marca radio button
					radio_button.click()
					# clica no botao confirmar
					driver.find_element('xpath', "/html/body/form/span/table[2]/tbody/tr[2]/td/table[2]/tbody/tr[6]/td[2]/a").click()
					# clica no botao confirmar da proxima tela
					driver.find_element('xpath', "/html/body/form/table[2]/tbody/tr[3]/td/table[5]/tbody/tr[3]/td/a[3]").click()

					# pega mensagem de sucesso
					mensagem_sucesso = driver.find_element('xpath', "/html/body/form/table[2]/tbody/tr[3]/td/table[2]/tbody/tr/td[2]/table[1]/tbody/tr[9]/td").text
					# print(mensagem_sucesso)
					return jsonify({'success': mensagem_sucesso})
		except:
			return jsonify({'error': 'Boleto não encontrado.'})
			# print("Boleto não encontrado.")
		# retorno do template
		# return 'Automação executada com sucesso!'
	except Exception as e:
		return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(port=5555)