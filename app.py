import requests
import random
import sqlite3
import os
from math import comb
from flask import Flask, render_template, request, jsonify, redirect, render_template_string

app = Flask(__name__)

# ==========================================
# CONFIGURAÇÕES DO SISTEMA
# ==========================================
MERCADOPAGO_TOKEN = "SUA_CHAVE_AQUI"

# ==========================================
# CONFIGURAÇÃO DO BANCO DE DADOS (SQLITE)
# ==========================================
def inicializar_banco():
    conexao = sqlite3.connect("lotofacil.db")
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS apostas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numeros TEXT,
            usuario TEXT
        )
    """)
    conexao.commit()
    conexao.close()

inicializar_banco()

# ==========================================
# ROTAS DA APLICAÇÃO
# ==========================================

@app.route('/')
def index():
    # Caminho seguro e relativo para o arquivo HTML
    caminho_html = os.path.join("templates", "index.html")
    
    with open(caminho_html, 'r', encoding='utf-8') as arquivo:
        conteudo_html = arquivo.read()
        
    # Variáveis que seu template espera receber
    admin_mode = False 
    valor_cota = "5,00"
    vendas_aprovadas = 0
    texto_regras = "Regras do sistema..."
    resultado_oficial_str = "Aguardando sorteio"
    
    return render_template_string(
        conteudo_html,
        admin=admin_mode,
        valor_cota=valor_cota,
        vendas=vendas_aprovadas,
        regras=texto_regras,
        resultado_oficial=resultado_oficial_str
    )

@app.route('/api/gerar-fechamento', methods=['POST'])
def api_gerar_fechamento():
    dados = request.json
    numeros_jogados = dados.get('numeros', [])
    
    # Retorno JSON corrigido e devidamente fechado
    resposta = {
        "status": "sucesso",
        "fechamento": [numeros_jogados] 
    }
    return jsonify(resposta)

if __name__ == '__main__':
    app.run(debug=True)