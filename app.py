import requests
import random
import sqlite3
import os
HEAD
from flask import Flask, render_template, request, jsonify, redirect, render_template_string

from flask import Flask, render_template, render_template_string, request, jsonify, redirect
>>>>>>> a7da25260dceea429f5eb518d6e1724241ceebfa
from math import comb

app = Flask(__name__)

<<<<<<< HEAD
# ==========================================
# CONFIGURAÇÕES DO SISTEMA 
# ==========================================
MERCADOPAGO_TOKEN = "APP_USR-2030455237914285-061213-49091f47d2a141002ac73f272feabe0a-193922692"

# ==========================================
# CONFIGURAÇÃO DO BANCO DE DADOS (SQLITE)
# ==========================================
def inicializar_banco():
    conn = sqlite3.connect('primeprint.db')
    cursor = conn.cursor()
    
    # Tabela de Vendas/Cotas com campos de localização
=======
MERCADOPAGO_TOKEN = "APP_USR-2030455237914285-061213-49091f47d2a141002ac73f272feabe0a-193922692"

def inicializar_banco():
    conn = sqlite3.connect('primeprint.db')
    cursor = conn.cursor()
>>>>>>> a7da25260dceea429f5eb518d6e1724241ceebfa
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_combinacao INTEGER,
            dezenas TEXT,
            cliente TEXT,
            contato TEXT,
<<<<<<< HEAD
            endereco TEXT,
            cidade TEXT,
=======
>>>>>>> a7da25260dceea429f5eb518d6e1724241ceebfa
            pontos INTEGER DEFAULT 0,
            mp_id TEXT,
            status TEXT
        )
    ''')
<<<<<<< HEAD
    
    # Tabela de Configurações do Sistema
=======
>>>>>>> a7da25260dceea429f5eb518d6e1724241ceebfa
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS configuracoes (
            chave TEXT PRIMARY KEY,
            valor TEXT
        )
    ''')
<<<<<<< HEAD
    
    # Inicializa configurações padrão se não existirem
    cursor.execute("INSERT OR IGNORE INTO configuracoes (chave, valor) VALUES ('valor_cota', '10.00')")
    cursor.execute("INSERT OR IGNORE INTO configuracoes (chave, valor) VALUES ('texto_regras', 'As regras do sistema ainda não foram definidas pelo administrador.')")
    cursor.execute("INSERT OR IGNORE INTO configuracoes (chave, valor) VALUES ('resultado_oficial', '')")
    cursor.execute("INSERT OR IGNORE INTO configuracoes (chave, valor) VALUES ('mensagem_concurso', '🔒 As cotas só serão liberadas no dia do concurso indicado.')")
    cursor.execute("INSERT OR IGNORE INTO configuracoes (chave, valor) VALUES ('liberado_geral', 'nao')")
    
=======
    cursor.execute("INSERT OR IGNORE INTO configuracoes (chave, valor) VALUES ('valor_cota', '10.00')")
    cursor.execute("INSERT OR IGNORE INTO configuracoes (chave, valor) VALUES ('texto_regras', 'As regras do sistema ainda não foram definidas pelo administrador.')")
    cursor.execute("INSERT OR IGNORE INTO configuracoes (chave, valor) VALUES ('resultado_oficial', '')")
>>>>>>> a7da25260dceea429f5eb518d6e1724241ceebfa
    conn.commit()
    conn.close()

inicializar_banco()

<<<<<<< HEAD
# Funções auxiliares para leitura e escrita no banco de dados
=======
>>>>>>> a7da25260dceea429f5eb518d6e1724241ceebfa
def obter_config(chave):
    conn = sqlite3.connect('primeprint.db')
    cursor = conn.cursor()
    cursor.execute("SELECT valor FROM configuracoes WHERE chave = ?", (chave,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else ""

def atualizar_config(chave, novo_valor):
    conn = sqlite3.connect('primeprint.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE configuracoes SET valor = ? WHERE chave = ?", (novo_valor, chave))
    conn.commit()
    conn.close()

<<<<<<< HEAD
# ==========================================
# MOTOR MATEMÁTICO COMBINATÓRIO OFICIAL
# ==========================================
=======
>>>>>>> a7da25260dceea429f5eb518d6e1724241ceebfa
def gerar_dezenas_por_id(id_cota):
    id_comb = id_cota - 1
    dezenas = []
    proximo_num = 1
<<<<<<< HEAD
    
=======
>>>>>>> a7da25260dceea429f5eb518d6e1724241ceebfa
    for v in range(15, 0, -1):
        while True:
            c = comb(25 - proximo_num, v - 1)
            if id_comb < c:
                dezenas.append(proximo_num)
                proximo_num += 1
                break
            id_comb -= c
            proximo_num += 1
<<<<<<< HEAD
            
=======
>>>>>>> a7da25260dceea429f5eb518d6e1724241ceebfa
    return dezenas

def obter_id_por_combinacao(jogo):
    jogo_ordenado = sorted(list(set(jogo)))
    if len(jogo_ordenado) != 15:
        return 1
<<<<<<< HEAD
        
    id_comb = 0
    proximo_num = 1
    
=======
    id_comb = 0
    proximo_num = 1
>>>>>>> a7da25260dceea429f5eb518d6e1724241ceebfa
    for i, num in enumerate(jogo_ordenado):
        v = 15 - i
        while proximo_num < num:
            id_comb += comb(25 - proximo_num, v - 1)
            proximo_num += 1
        proximo_num += 1
<<<<<<< HEAD
        
    return id_comb + 1

# ==========================================
# ROTAS DO ECOSSISTEMA
# ==========================================

@app.route('/')
def index():
    admin_mode = request.args.get('admin') == 'true'
    
    # Pega os dados salvos no banco
    valor_cota = float(obter_config('valor_cota'))
    texto_regras = obter_config('texto_regras')
    msg_concurso = obter_config('mensagem_concurso')
    liberado_geral = obter_config('liberado_geral')
    resultado_oficial_str = obter_config('resultado_oficial')
    
    conn = sqlite3.connect('primeprint.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id_combinacao, dezenas, cliente, contato, pontos, status, endereco, cidade FROM vendas WHERE status = 'aprovado'")
    linhas = cursor.fetchall()
    
    vendas_aprovadas = []
    ganhadores_15 = []
    ganhadores_14 = []
    
    for l in linhas:
        cota_info = {
=======
    return id_comb + 1

@app.route('/')
def index():
    admin_mode = request.args.get('admin') == 'true'
    valor_cota = float(obter_config('valor_cota'))
    texto_regras = obter_config('texto_regras')
    
    conn = sqlite3.connect('primeprint.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id_combinacao, dezenas, cliente, contato, pontos, status FROM vendas WHERE status = 'aprovado'")
    linhas = cursor.fetchall()
    conn.close()
    
    vendas_aprovadas = []
    for l in linhas:
        vendas_aprovadas.append()
>>>>>>> a7da25260dceea429f5eb518d6e1724241ceebfa
            "id_combinacao": l[0],
            "dezenas": l[1],
            "cliente": l[2],
            "contato": l[3],
            "pontos": l[4],
<<<<<<< HEAD
            "status": l[5],
            "endereco": l[6],
            "cidade": l[7]
        }
        vendas_aprovadas.append(cota_info)
        
        # Classificação de ganhadores se houver sorteio apurado
        if resultado_oficial_str and resultado_oficial_str.strip():
            if l[4] == 15:
                ganhadores_15.append(cota_info)
            elif l[4] == 14:
                ganhadores_14.append(cota_info)
                
    conn.close()
    
    # Template Admin Estendido com Painel de Ganhadores
    if admin_mode:
        admin_template = '''
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <title>Painel de Controle - Sistema de Cotas</title>
            <style>
                body { font-family: 'Segoe UI', Tahoma, sans-serif; background: #0f172a; color: #f8fafc; padding: 30px; }
                .container { max-width: 900px; margin: 0 auto; background: #1e293b; padding: 30px; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.3); }
                h1 { color: #3b82f6; border-bottom: 2px solid #334155; padding-bottom: 10px; margin-top: 0; }
                h2 { color: #10b981; }
                h3 { color: #facc15; }
                .card { background: #0f172a; padding: 20px; border-radius: 8px; margin-bottom: 20px; border: 1px solid #334155; }
                label { font-weight: bold; color: #94a3b8; display: block; margin-bottom: 5px; }
                input[type="text"], textarea { width: 100%; padding: 10px; border-radius: 6px; border: 1px solid #475569; background: #1e293b; color: #f8fafc; box-sizing: border-box; margin-top: 5px; margin-bottom: 15px; }
                button, .btn { background: #3b82f6; color: white; border: none; padding: 10px 20px; border-radius: 6px; font-weight: bold; cursor: pointer; text-decoration: none; display: inline-block; }
                button:hover, .btn:hover { background: #2563eb; }
                .btn-danger { background: #ef4444; }
                .btn-danger:hover { background: #dc2626; }
                .btn-success { background: #10b981; }
                .btn-success:hover { background: #059669; }
                hr { border: 0; border-top: 1px solid #334155; margin: 20px 0; }
                table { width: 100%; border-collapse: collapse; margin-top: 10px; }
                th, td { padding: 10px; border: 1px solid #334155; text-align: left; }
                th { background: #1e293b; color: #94a3b8; }
                .empty-msg { color: #64748b; font-style: italic; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>⚙️ Painel Administrativo</h1>
                <a href="/" style="color: #94a3b8; text-decoration: none; font-size: 14px;">← Voltar ao site principal</a>
                
                <div class="card" style="border-color: #facc15;">
                    <h2>🏆 Quadro de Ganhadores Apurados</h2>
                    <p style="color: #94a3b8; font-size: 13px;"><em>Nota: Este quadro é preenchido dinamicamente após o processamento da "Varredura" com as 15 dezenas sorteadas.</em></p>
                    <hr style="border-top: 1px solid #475569;">
                    
                    <h3>👑 Ganhadores com 15 Pontos</h3>
                    <table>
                        <tr>
                            <th>Cota/ID</th>
                            <th>Cliente</th>
                            <th>Contato</th>
                            <th>Dezenas</th>
                        </tr>
                        {% for g15 in ganhadores_15 %}
                        <tr>
                            <td><b>#{{ g15.id_combinacao }}</b></td>
                            <td>{{ g15.cliente }}</td>
                            <td>{{ g15.contato }}</td>
                            <td style="font-family: monospace; font-size: 13px; color: #3b82f6;">{{ g15.dezenas }}</td>
                        </tr>
                        {% else %}
                        <tr><td colspan="4" class="empty-msg">Nenhum ganhador de 15 pontos apurado no momento.</td></tr>
                        {% endfor %}
                    </table>

                    <hr style="border-top: 1px solid #475569;">

                    <h3>🥈 Ganhadores com 14 Pontos</h3>
                    <table>
                        <tr>
                            <th>Cota/ID</th>
                            <th>Cliente</th>
                            <th>Contato</th>
                            <th>Dezenas</th>
                        </tr>
                        {% for g14 in ganhadores_14 %}
                        <tr>
                            <td><b>#{{ g14.id_combinacao }}</b></td>
                            <td>{{ g14.cliente }}</td>
                            <td>{{ g14.contato }}</td>
                            <td style="font-family: monospace; font-size: 13px; color: #3b82f6;">{{ g14.dezenas }}</td>
                        </tr>
                        {% else %}
                        <tr><td colspan="4" class="empty-msg">Nenhum ganhador de 14 pontos apurado no momento.</td></tr>
                        {% endfor %}
                    </table>
                </div>

                <div class="card">
                    <h3>💰 Valor da Cota</h3>
                    <form action="/atualizar_valor_cota" method="POST">
                        <label>Preço atual (R$):</label>
                        <input type="text" name="novo_valor" value="{{ valor_cota }}">
                        <button type="submit">Atualizar Valor</button>
                    </form>
                </div>

                <div class="card">
                    <h3>💬 Mensagem de Bloqueio das Cotas</h3>
                    <form action="/salvar_mensagem_concurso" method="POST">
                        <label>Texto que aparece para o cliente na tela de sucesso/meus bilhetes quando estão cobertas:</label>
                        <input type="text" name="msg_concurso" value="{{ msg_concurso }}">
                        <button type="submit">Salvar Mensagem</button>
                    </form>
                </div>

                <div class="card">
                    <h3>🚀 Liberação de Dezenas</h3>
                    <p>Libera as dezenas para todos os clientes, desativando a proteção de segurança ao sortear o concurso.</p>
                    <form action="/liberar_geral" method="POST">
                        {% if liberado_geral == 'sim' %}
                            <input type="hidden" name="estado" value="nao">
                            <button type="submit" class="btn-danger">Bloquear / Ocultar Dezenas Novamente</button>
                            <span style="color: #10b981; margin-left: 15px;">✓ As dezenas estão visíveis no momento.</span>
                        {% else %}
                            <input type="hidden" name="estado" value="sim">
                            <button type="submit" class="btn-success">Liberar Todas as Cotas (Dia do Sorteio)</button>
                            <span style="color: #ef4444; margin-left: 15px;">× As dezenas estão ocultas no momento.</span>
                        {% endif %}
                    </form>
                </div>

                <div class="card">
                    <h3>🌐 Regras do Sistema</h3>
                    <form action="/salvar_regras" method="POST">
                        <textarea name="regras_texto" rows="5">{{ regras }}</textarea>
                        <button type="submit">Salvar Regras</button>
                    </form>
                </div>

                <div class="card">
                    <h3>📊 Simulação e Auditoria do Resultado</h3>
                    <form action="/varredura" method="POST">
                        <label>Dezenas sorteadas (Ex: 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15):</label>
                        <input type="text" name="dezenas_oficiais" value="{{ resultado_oficial }}" placeholder="Digite 15 dezenas separadas por espaço">
                        <button type="submit" class="btn-success">Realizar Varredura/Processamento de Pontos</button>
                    </form>
                </div>

                <div class="card">
                    <h3>⚠️ Área de Risco</h3>
                    <form action="/zerar_vendas" method="POST" onsubmit="return confirm('Tem certeza que deseja apagar todas as vendas? Esta ação é irreversível!')">
                        <button type="submit" class="btn-danger">Zerar Todas as Vendas e Limpar Banco</button>
                    </form>
                </div>
            </div>
        </body>
        </html>
        '''
        return render_template_string(admin_template, 
                                      valor_cota=valor_cota, 
                                      regras=texto_regras, 
                                      msg_concurso=msg_concurso,
                                      liberado_geral=liberado_geral,
                                      resultado_oficial=resultado_oficial_str,
                                      ganhadores_15=ganhadores_15,
                                      ganhadores_14=ganhadores_14)
    
    return render_template()
        'index.html', 
=======
            "status": l[5]
        })
    
    caminho_html = "C:\\Users\\Prime Print\\Desktop\\loto\\templates\\index.html"
    with open(caminho_html, 'r', encoding='utf-8') as arquivo:
        conteudo_html = arquivo.read()

    return render_template_string(
        conteudo_html, 
>>>>>>> a7da25260dceea429f5eb518d6e1724241ceebfa
        admin=admin_mode, 
        valor_cota=valor_cota, 
        vendas=vendas_aprovadas,
        regras=texto_regras,
<<<<<<< HEAD
        resultado_oficial=resultado_oficial_str
    )

# --- ROTAS AJAX DE TELEFONE E BILHETES ---

@app.route('/buscar_por_telefone', methods=['POST'])
def buscar_por_telefone():
    contato = request.form.get('contato') or (request.json.get('contato') if request.is_json else None)
    
    if not contato:
        return jsonify({"sucesso": False, "mensagem": "Por favor, informe o número de telefone."})
    
    contato = str(contato).strip()
    
    conn = sqlite3.connect('primeprint.db')
    cursor = conn.cursor()
    cursor.execute("SELECT cliente, endereco, cidade FROM vendas WHERE contato = ? ORDER BY id DESC LIMIT 1", (contato,))
    resultado = cursor.fetchone()
    conn.close()
    
    if resultado:
        return jsonify({
            "sucesso": True,
            "nome": resultado[0],
            "endereco": resultado[1],
            "cidade": resultado[2]
        })
    return jsonify({"sucesso": False, "mensagem": "Nenhum cadastro localizado com este telefone."})


@app.route('/obter_meus_bilhetes', methods=['POST'])
def obter_meus_bilhetes():
    contato = request.form.get('contato') or (request.json.get('contato') if request.is_json else None)
    
    if not contato:
        return jsonify({"sucesso": False, "vendas": []})
        
    contato = str(contato).strip()
    liberado_geral = obter_config('liberado_geral') == 'sim'
    msg_concurso = obter_config('mensagem_concurso')
    
    conn = sqlite3.connect('primeprint.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id_combinacao, dezenas, pontos FROM vendas WHERE contato = ? AND status = 'aprovado' ORDER BY id DESC", (contato,))
    linhas = cursor.fetchall()
    conn.close()
    
    vendas_cliente = []
    for l in linhas:
        dezenas_mostradas = l[1] if liberado_geral else msg_concurso
        
        # ESPIÃO DE SEGURANÇA: Se o resultado oficial foi apagado (string vazia), garante que pontos fiquem em 0 na exibição
        res_oficial = obter_config('resultado_oficial')
        pontos_mostrados = l[2] if (res_oficial and res_oficial.strip()) else 0

        vendas_cliente.append({
            "id_combinacao": l[0],
            "dezenas": dezenas_mostradas, 
            "pontos": pontos_mostrados
        })
        
    return jsonify({"sucesso": True, "vendas": vendas_cliente})

# ------------------------------------------------------------------------

=======
        resultado_oficial=obter_config('resultado_oficial')
    )

>>>>>>> a7da25260dceea429f5eb518d6e1724241ceebfa
@app.route('/buscar_combinacao/<int:id_cota>')
def buscar_combinacao(id_cota):
    if id_cota < 1 or id_cota > 3268760:
        return jsonify({"sucesso": False, "mensagem": "ID fora dos limites da matriz (1 a 3.268.760)."})
<<<<<<< HEAD
    
=======
>>>>>>> a7da25260dceea429f5eb518d6e1724241ceebfa
    dezenas = gerar_dezenas_por_id(id_cota)
    dezenas_str = " ".join(f"{d:02d}" for d in dezenas)
    return jsonify({"sucesso": True, "dezenas": dezenas_str})

@app.route('/simular_resultado', methods=['POST'])
def simular_resultado():
    dezenas_input = request.form.get('dezenas_simuladas', '')
    jogo_teste = list(set([int(x) for x in dezenas_input.split() if x.isdigit()]))
<<<<<<< HEAD
    
    if len(jogo_teste) != 15:
        return jsonify({"sucesso": False, "mensagem": "Por favor, insira exatamente 15 números válidos."})
    
    jogo_teste.sort()
    id_real_15 = obter_id_por_combinacao(jogo_teste)

    estatisticas_gerais = { 13: 5475, 12: 87600, 11: 720720 }

    lista_14 = []
    fora_do_jogo = [n for n in range(1, 26) if n not in jogo_teste]
    
=======
    if len(jogo_teste) != 15:
        return jsonify({"sucesso": False, "mensagem": "Por favor, insira exatamente 15 números válidos."})
    jogo_teste.sort()
    id_real_15 = obter_id_por_combinacao(jogo_teste)
    estatisticas_gerais = { 13: 5475, 12: 87600, 11: 720720 }
    lista_14 = []
    fora_do_jogo = [n for n in range(1, 26) if n not in jogo_teste]
>>>>>>> a7da25260dceea429f5eb518d6e1724241ceebfa
    for i in range(15):
        for j in range(10):
            jogo_14 = list(jogo_teste)
            jogo_14[i] = fora_do_jogo[j]
            jogo_14.sort()
            id_real_14 = obter_id_por_combinacao(jogo_14)
            lista_14.append({
                "linha": id_real_14,
                "dezenas": " ".join(f"{d:02d}" for d in jogo_14)
            })
<<<<<<< HEAD

    lista_14 = sorted(lista_14, key=lambda x: x['linha'])

=======
    lista_14 = sorted(lista_14, key=lambda x: x['linha'])
>>>>>>> a7da25260dceea429f5eb518d6e1724241ceebfa
    return jsonify({
        "sucesso": True,
        "jogo_15": { "linha": id_real_15, "dezenas": " ".join(f"{d:02d}" for d in jogo_teste) },
        "lista_14": lista_14,
        "contagem_estatistica": estatisticas_gerais
    })

@app.route('/salvar_venda', methods=['POST'])
def salvar_venda():
    valor_cota = float(obter_config('valor_cota'))
<<<<<<< HEAD
    
=======
>>>>>>> a7da25260dceea429f5eb518d6e1724241ceebfa
    tipo_venda = request.form.get('tipo_venda')
    nome_cliente = request.form.get('nome_cliente', 'Cliente PRIME').strip()
    contato = request.form.get('contato', '').strip()
    cpf_cliente = request.form.get('cpf_cliente', '').strip()
    
<<<<<<< HEAD
    endereco = request.form.get('endereco', '').strip()
    cidade = request.form.get('cidade', '').strip()
    
=======
>>>>>>> a7da25260dceea429f5eb518d6e1724241ceebfa
    cpf_limpo = "".join(filter(str.isdigit, cpf_cliente))
    if not cpf_limpo:
        cpf_limpo = "00000000000"

<<<<<<< HEAD
    # --- SISTEMA ANTIDUPLICIDADE DE SEGURANÇA MÁXIMA ---
    conn = sqlite3.connect('primeprint.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id_combinacao FROM vendas WHERE status = 'aprovado'")
    cotas_vendidas = set(row[0] for row in cursor.fetchall())
    conn.close()

=======
>>>>>>> a7da25260dceea429f5eb518d6e1724241ceebfa
    ids_comprados = []
    if tipo_venda == 'unico':
        id_cota = request.form.get('id_combinacao')
        if id_cota:
<<<<<<< HEAD
            id_cota_int = int(id_cota)
            # Bloqueia na hora se a cota individual já possuir dono
            if id_cota_int in cotas_vendidas:
                return """
                <div style="font-family: 'Segoe UI', Tahoma, sans-serif; background: #0f172a; color: #f8fafc; height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; padding: 20px; box-sizing: border-box;">
                    <div style="background: #1e293b; padding: 40px; border-radius: 16px; border: 2px solid #f43f5e; max-width: 450px; box-shadow: 0 10px 25px rgba(0,0,0,0.3);">
                        <h2 style="color: #f43f5e; margin-top: 0; font-size: 26px;">⚠️ Cota Indisponível</h2>
                        <p style="color: #94a3b8; font-size: 16px; line-height: 1.6;">A cota número <b style="color: #f8fafc; font-size: 18px;">{}</b> acabou de ser comprada por outro participante.</p>
                        <p style="color: #64748b; font-size: 14px; margin-bottom: 25px;">Por favor, retorne e selecione outro número disponível na matriz.</p>
                        <a href="/" style="background: #3b82f6; color: white; padding: 14px 28px; text-decoration: none; border-radius: 8px; font-weight: bold; display: inline-block; transition: 0.2s; box-shadow: 0 4px 12px rgba(59,130,246,0.3);">Escolher Outra Cota</a>
                    </div>
                </div>
                """.format(id_cota_int), 200
            ids_comprados.append(id_cota_int)
            
=======
            ids_comprados.append(int(id_cota))
>>>>>>> a7da25260dceea429f5eb518d6e1724241ceebfa
    elif tipo_venda == 'lote':
        id_ini = int(request.form.get('id_inicial', 0))
        id_fim = int(request.form.get('id_final', 0))
        if id_ini > 0 and id_fim >= id_ini:
            limite_bloco = min(id_fim, id_ini + 99)
<<<<<<< HEAD
            intervalo_proposto = list(range(id_ini, limite_bloco + 1))
            
            # Verifica se há alguma cota vendida infiltrada no meio do lote solicitado
            cotas_conflitantes = [num for num in intervalo_proposto if num in cotas_vendidas]
            if cotas_conflitantes:
                return """
                <div style="font-family: 'Segoe UI', Tahoma, sans-serif; background: #0f172a; color: #f8fafc; height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; padding: 20px; box-sizing: border-box;">
                    <div style="background: #1e293b; padding: 40px; border-radius: 16px; border: 2px solid #f43f5e; max-width: 450px; box-shadow: 0 10px 25px rgba(0,0,0,0.3);">
                        <h2 style="color: #f43f5e; margin-top: 0; font-size: 26px;">⚠️ Conflito no Lote</h2>
                        <p style="color: #94a3b8; font-size: 16px; line-height: 1.6;">Não foi possível processar o lote. A cota número <b style="color: #f8fafc; font-size: 18px;">{}</b> (ou outras deste intervalo) já foi vendida.</p>
                        <p style="color: #64748b; font-size: 14px; margin-bottom: 25px;">Por favor, selecione um intervalo de cotas totalmente livres.</p>
                        <a href="/" style="background: #3b82f6; color: white; padding: 14px 28px; text-decoration: none; border-radius: 8px; font-weight: bold; display: inline-block; transition: 0.2s; box-shadow: 0 4px 12px rgba(59,130,246,0.3);">Revisar Intervalo</a>
                    </div>
                </div>
                """.format(cotas_conflitantes[0]), 200
            
            ids_comprados = intervalo_proposto
            
=======
            ids_comprados = list(range(id_ini, limite_bloco + 1))
>>>>>>> a7da25260dceea429f5eb518d6e1724241ceebfa
    elif tipo_venda == 'surpresinha':
        qtd = int(request.form.get('qtd_surpresinha', 1))
        if qtd > 100: 
            qtd = 100
<<<<<<< HEAD
            
        # Filtra automaticamente na geração, garantindo apenas números livres de forma transparente
        while len(ids_comprados) < qtd:
            num_random = random.randint(1, 3268760)
            if num_random not in cotas_vendidas and num_random not in ids_comprados:
                ids_comprados.append(num_random)
=======
        ids_comprados = [random.randint(1, 3268760) for _ in range(qtd)]
>>>>>>> a7da25260dceea429f5eb518d6e1724241ceebfa

    qtd_cotas = len(ids_comprados)
    if qtd_cotas == 0:
        return "Erro: Nenhuma cota válida selecionada ou intervalo inválido.", 400

    valor_total = float(valor_cota * qtd_cotas)
    chave_random = random.randint(100000, 999999)
    
    headers = {
        "Authorization": f"Bearer {MERCADOPAGO_TOKEN}",
        "Content-Type": "application/json",
        "X-Idempotency-Key": f"primeprint_{chave_random}"
    }

    nome_partes = nome_cliente.split()
    primeiro_nome = nome_partes[0] if nome_partes else "Cliente"
    sobrenome = nome_partes[-1] if len(nome_partes) > 1 else "PRIME"
    email_comprador = f"cliente.venda.{chave_random}@gmail.com"

    payment_data = {
        "transaction_amount": valor_total,
        "description": f"PRIME PRINT - {qtd_cotas} Cotas Lotofacil",
        "payment_method_id": "pix",
        "payer": {
            "email": email_comprador,
            "first_name": primeiro_nome,
            "last_name": sobrenome,
            "identification": { "type": "CPF", "number": cpf_limpo }
        }
    }

    try:
        url_mp = "https://api.mercadopago.com/v1/payments"
        resposta = requests.post(url_mp, json=payment_data, headers=headers, timeout=15)
        dados_retorno = resposta.json()
        mp_id = dados_retorno.get('id', 'Local')

        conn = sqlite3.connect('primeprint.db')
        cursor = conn.cursor()

        for id_venda in ids_comprados:
            dezenas_cota = gerar_dezenas_por_id(id_venda)
            dezenas_str = " ".join(f"{d:02d}" for d in dezenas_cota)
            cursor.execute(
<<<<<<< HEAD
                "INSERT INTO vendas (id_combinacao, dezenas, cliente, contato, endereco, cidade, mp_id, status) VALUES (?, ?, ?, ?, ?, ?, ?, 'pendente')",
                (id_venda, dezenas_str, nome_cliente, contato, endereco, cidade, str(mp_id))
=======
                "INSERT INTO vendas (id_combinacao, dezenas, cliente, contato, mp_id, status) VALUES (?, ?, ?, ?, ?, 'pendente')",
                (id_venda, dezenas_str, nome_cliente, contato, str(mp_id))
>>>>>>> a7da25260dceea429f5eb518d6e1724241ceebfa
            )
        
        conn.commit()
        conn.close()

        if resposta.status_code in [200, 201]:
            point_of_interaction = dados_retorno.get('point_of_interaction')
            if point_of_interaction:
                transaction_data = point_of_interaction.get('transaction_data')
                if transaction_data:
                    qr_code_base64 = transaction_data.get('qr_code_base64')
                    qr_code_copia_cola = transaction_data.get('qr_code')

                    if qr_code_copia_cola:
                        pix_template = """
                        <!DOCTYPE html>
                        <html lang="pt-BR">
                        <head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>PRIME PRINT - Pagamento Pix</title>
                        <style>
                            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0f172a; color: #f8fafc; margin: 0; padding: 20px; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
                            .card { background: #1e293b; border-radius: 16px; box-shadow: 0 10px 25px rgba(0,0,0,0.3); padding: 30px; max-width: 420px; width: 100%; text-align: center; border: 2px solid #3b82f6; }
                            .logo { font-weight: bold; font-size: 28px; color: #3b82f6; margin-bottom: 5px; letter-spacing: 1px; text-shadow: 0 0 10px rgba(59,130,246,0.5); }
                            .sub { color: #94a3b8; font-size: 14px; margin-bottom: 25px; }
                            .badge-pix { background: #10b981; color: white; padding: 6px 18px; border-radius: 20px; font-size: 13px; font-weight: bold; display: inline-block; margin-bottom: 20px; animation: pulse 2s infinite; }
                            .valor { font-size: 36px; font-weight: bold; color: #10b981; margin-bottom: 20px; }
                            .qr-box { background: white; padding: 15px; border-radius: 12px; display: inline-block; margin-bottom: 20px; border: 4px solid #3b82f6; }
                            .qr-box img { width: 200px; height: 200px; display: block; }
                            .instrucao { font-size: 14px; color: #cbd5e1; margin-bottom: 15px; padding: 0 10px; }
                            .input-copia { width: 100%; padding: 12px; border: 2px solid #334155; border-radius: 8px; font-size: 12px; background: #0f172a; text-align: center; box-sizing: border-box; margin-bottom: 12px; color: #94a3b8; font-weight: bold; }
                            .btn-copiar { background: #3b82f6; color: white; border: none; padding: 14px; width: 100%; border-radius: 8px; font-size: 16px; font-weight: bold; cursor: pointer; transition: 0.2s; box-shadow: 0 4px 12px rgba(59,130,246,0.3); }
                            .btn-copiar:hover { background: #2563eb; transform: translateY(-2px); }
                            .btn-voltar { display: block; margin-top: 20px; color: #94a3b8; text-decoration: none; font-size: 14px; font-weight: bold; }
                            .btn-voltar:hover { color: #f8fafc; }
                            .timer { font-size: 14px; color: #f43f5e; font-weight: bold; margin-top: 15px; }
                            @keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.05); } 100% { transform: scale(1); } }
                        </style>
                        </head>
                        <body>
                            <div class="card">
                                <div class="logo">PRIME PRINT</div>
                                <div class="sub">Sistema Automático de Cotas</div>
                                <span class="badge-pix">PAGAMENTO VIA PIX</span>
                                <div class="valor">R$ {{ "%.2f"|format(valor) }}</div>
                                <div class="qr-box">
                                    {% if img_base64 %}
                                        <img src="data:image/jpeg;base64,{{ img_base64 }}" alt="QR Code Pix">
                                    {% else %}
                                        <div style="width:200px; height:200px; display:flex; align-items:center; justify-content:center; background:#eee; font-size:12px; color:#666;">Utilize o Copia e Cola abaixo</div>
                                    {% endif %}
                                </div>
                                <div class="instrucao">Abra a aplicação do seu banco e escolha a opção <b>Pix Copia e Cola</b> para efetuar o pagamento.</div>
                                <input type="text" class="input-copia" id="pixCode" value="{{ copiacola }}" readonly>
                                <button class="btn-copiar" onclick="copiarPix()">Copiar Código Pix</button>
                                <div class="timer">Aguardando pagamento... Não feche esta página.</div>
                                <a href="/" class="btn-voltar">Cancelar e Voltar</a>
                            </div>
                            <script>
                                function copiarPix() {
                                    var copyText = document.getElementById("pixCode");
                                    copyText.select();
                                    copyText.setSelectionRange(0, 99999);
                                    navigator.clipboard.writeText(copyText.value);
                                    var btn = document.querySelector(".btn-copiar");
                                    btn.innerText = "✓ Código Copiado!";
                                    btn.style.background = "#10b981";
                                    setTimeout(function(){
                                        btn.innerText = "Copiar Código Pix";
                                        btn.style.background = "#3b82f6";
                                    }, 3000);
                                }
                                setInterval(function() {
                                    fetch('/status_pagamento/{{ payment_id }}')
                                    .then(response => response.json())
                                    .then(data => {
                                        if (data.status === 'aprovado') {
<<<<<<< HEAD
                                            window.location.href = '/sucesso?mp_id={{ payment_id }}&primeiro_acesso=true';
=======
                                            window.location.href = '/sucesso?mp_id={{ payment_id }}';
>>>>>>> a7da25260dceea429f5eb518d6e1724241ceebfa
                                        }
                                    });
                                }, 5000);
                            </script>
                        </body>
                        </html>
                        """
                        return render_template_string(
                            pix_template,
                            valor=valor_total,
                            copiacola=qr_code_copia_cola,
                            img_base64=qr_code_base64,
                            payment_id=mp_id
                        )
<<<<<<< HEAD

            return f"<h2>⚠️ Transação local</h2><a href='/'><button>Voltar</button></a>", 200
        else:
            return f"<h2>⚠️ Ajuste Requerido: {dados_retorno.get('message')}</h2><a href='/'><button>Voltar</button></a>", 200

=======
            return f"<h2>⚠️ Transação local</h2><a href='/'><button>Voltar</button></a>", 200
        else:
            return f"<h2>⚠️ Ajuste Requerido: {dados_retorno.get('message')}</h2><a href='/'><button>Voltar</button></a>", 200
>>>>>>> a7da25260dceea429f5eb518d6e1724241ceebfa
    except Exception as e:
        return f"Erro de comunicação no servidor local: '{str(e)}'", 500

@app.route('/status_pagamento/<mp_id>')
def status_pagamento(mp_id):
    headers = {"Authorization": f"Bearer {MERCADOPAGO_TOKEN}"}
    try:
        url = f"https://api.mercadopago.com/v1/payments/{mp_id}"
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            dados = resp.json()
            if dados.get("status") == "approved":
                conn = sqlite3.connect('primeprint.db')
                cursor = conn.cursor()
                cursor.execute("UPDATE vendas SET status = 'aprovado' WHERE mp_id = ?", (str(mp_id),))
<<<<<<< HEAD
                
=======
>>>>>>> a7da25260dceea429f5eb518d6e1724241ceebfa
                res_oficial_str = obter_config('resultado_oficial')
                if res_oficial_str:
                    res_oficial_lista = res_oficial_str.split()
                    cursor.execute("SELECT id, dezenas FROM vendas WHERE mp_id = ? AND status = 'aprovado'", (str(mp_id),))
                    cotas_aprovadas = cursor.fetchall()
<<<<<<< HEAD
                    
=======
>>>>>>> a7da25260dceea429f5eb518d6e1724241ceebfa
                    for cota in cotas_aprovadas:
                        dezenas_cota = cota[1].split()
                        pontos = len(set(dezenas_cota).intersection(set(res_oficial_lista)))
                        cursor.execute("UPDATE vendas SET pontos = ? WHERE id = ?", (pontos, cota[0]))
<<<<<<< HEAD

                conn.commit()
                conn.close()
                return jsonify({"status": "aprovado"})
    except Exception as e:
        print("Erro ao verificar pagamento:", e)
    
=======
                conn.commit()
                conn.close()
                return jsonify({"status": "aprovado"})
    except:
        pass
>>>>>>> a7da25260dceea429f5eb518d6e1724241ceebfa
    return jsonify({"status": "pendente"})

@app.route('/sucesso')
def sucesso():
    mp_id = request.args.get('mp_id')
<<<<<<< HEAD
    primeiro_acesso = request.args.get('primeiro_acesso') == 'true'
    
=======
>>>>>>> a7da25260dceea429f5eb518d6e1724241ceebfa
    conn = sqlite3.connect('primeprint.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id_combinacao, dezenas, pontos FROM vendas WHERE mp_id = ? AND status = 'aprovado'", (str(mp_id),))
    linhas = cursor.fetchall()
    conn.close()
    
    minhas_cotas = []
    for l in linhas:
        minhas_cotas.append({
            "id_combinacao": l[0],
            "dezenas": l[1],
            "pontos": l[2]
        })
<<<<<<< HEAD
    
    if not minhas_cotas:
        return redirect('/')

    # Pega o estado da chave mestra e a mensagem personalizada do Admin
    liberado_geral = obter_config('liberado_geral') == 'sim'
    msg_concurso = obter_config('mensagem_concurso')
        
    html_sucesso = '''
=======
    if not minhas_cotas:
        return redirect('/')
        
    html_sucesso = """
>>>>>>> a7da25260dceea429f5eb518d6e1724241ceebfa
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <title>Pagamento Aprovado!</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, sans-serif; background: #0f172a; color: #f8fafc; text-align: center; padding: 50px; }
            .box { background: #1e293b; padding: 40px; border-radius: 12px; max-width: 600px; margin: 0 auto; border: 2px solid #10b981; }
            h1 { color: #10b981; }
            .dezenas-box { font-size: 22px; font-weight: bold; background: #0f172a; padding: 15px; margin: 10px 0; border-radius: 8px; color: #3b82f6; letter-spacing: 2px; }
<<<<<<< HEAD
            .msg-bloqueio { font-size: 16px; background: #3b82f622; border: 1px dashed #3b82f6; padding: 15px; border-radius: 8px; color: #94a3b8; margin-top: 15px; line-height: 1.5; }
            .cota-oculta { background: #334155; color: #64748b; padding: 8px 15px; border-radius: 6px; font-size: 16px; letter-spacing: 0; display: block; margin-top: 5px; font-weight: normal; }
=======
>>>>>>> a7da25260dceea429f5eb518d6e1724241ceebfa
            .btn { display: inline-block; margin-top: 30px; padding: 15px 30px; background: #3b82f6; color: white; text-decoration: none; border-radius: 8px; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="box">
            <h1>🎉 Pagamento Aprovado!</h1>
            <p>Seus números foram gerados com sucesso e vinculados ao seu nome.</p>
            <p>Aqui estão as suas cotas oficiais:</p>
<<<<<<< HEAD
            
            {% for cota in cotas %}
                <div class="dezenas-box">
                    <span style="font-size: 14px; color: #94a3b8; display: block; letter-spacing: 0;">Linha/Cota: {{ cota.id_combinacao }}</span>
                    {% if primeiro_acesso or liberado_geral %}
                        {{ cota.dezenas }}
                    {% else %}
                        <span class="cota-oculta">{{ msg_concurso }}</span>
                    {% endif %}
                </div>
            {% endfor %}
            
            {% if primeiro_acesso %}
                <div class="msg-bloqueio" style="border-color: #eab308; color: #fde047;">
                    ⚠️ <b>ATENÇÃO:</b> Guarde ou tire um print desta tela agora. Por motivos de segurança, ao sair ou atualizar a página, os números serão cobertos e guardados em nosso sistema.
                </div>
            {% else %}
                {% if not liberado_geral %}
                    <div class="msg-bloqueio">
                        {{ msg_concurso }}
                    </div>
                {% endif %}
            {% endif %}
            
=======
            {% for cota in cotas %}
                <div class="dezenas-box">
                    <span style="font-size: 14px; color: #94a3b8; display: block; letter-spacing: 0;">Linha/Cota: {{ cota.id_combinacao }}</span>
                    {{ cota.dezenas }}
                </div>
            {% endfor %}
>>>>>>> a7da25260dceea429f5eb518d6e1724241ceebfa
            <a href="/" class="btn">Voltar ao Início</a>
        </div>
    </body>
    </html>
<<<<<<< HEAD
    '''
    return render_template_string(html_sucesso, 
                                  cotas=minhas_cotas, 
                                  primeiro_acesso=primeiro_acesso, 
                                  liberado_geral=liberado_geral,
                                  msg_concurso=msg_concurso)
=======
    """
    return render_template_string(html_sucesso, cotas=minhas_cotas)
>>>>>>> a7da25260dceea429f5eb518d6e1724241ceebfa

@app.route('/atualizar_valor_cota', methods=['POST'])
def atualizar_valor_cota():
    try:
        novo_valor = request.form.get('novo_valor', '10.00').replace(',', '.')
        atualizar_config('valor_cota', novo_valor)
    except: 
        pass
    return redirect('/?admin=true')

<<<<<<< HEAD
@app.route('/salvar_mensagem_concurso', methods=['POST'])
def salvar_mensagem_concurso():
    nova_msg = request.form.get('msg_concurso', '🔒 As cotas só serão liberadas no dia do concurso indicado.')
    atualizar_config('mensagem_concurso', nova_msg)
    return redirect('/?admin=true')

@app.route('/liberar_geral', methods=['POST'])
def liberar_geral():
    estado = request.form.get('estado', 'nao')
    atualizar_config('liberado_geral', estado)
    return redirect('/?admin=true')

=======
>>>>>>> a7da25260dceea429f5eb518d6e1724241ceebfa
@app.route('/salvar_regras', methods=['POST'])
def salvar_regras():
    novo_texto = request.form.get('regras_texto')
    if novo_texto is not None:
        atualizar_config('texto_regras', novo_texto)
    return redirect('/?admin=true')

@app.route('/varredura', methods=['POST'])
def varredura():
    dezenas_input = request.form.get('dezenas_oficiais', '')
<<<<<<< HEAD
    
    texto_limpo = dezenas_input.replace('-', ' ').replace(',', ' ').replace('.', ' ').replace('/', ' ')
    
    lista_resultado = []
    for x in texto_limpo.split():
        if x.isdigit():
            num = int(x)
            if 1 <= num <= 25:
                lista_resultado.append(num)
    
    lista_resultado = sorted(list(set(lista_resultado)))
    
    conn = sqlite3.connect('primeprint.db')
    cursor = conn.cursor()
    
=======
    lista_resultado = [int(x) for x in dezenas_input.split() if x.isdigit()]
>>>>>>> a7da25260dceea429f5eb518d6e1724241ceebfa
    if len(lista_resultado) == 15:
        res_oficial_str = " ".join(f"{d:02d}" for d in lista_resultado)
        atualizar_config('resultado_oficial', res_oficial_str)
        
<<<<<<< HEAD
        cursor.execute("SELECT id, dezenas FROM vendas WHERE status = 'aprovado'")
        cotas = cursor.fetchall()
        
=======
        conn = sqlite3.connect('primeprint.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, dezenas FROM vendas WHERE status = 'aprovado'")
        cotas = cursor.fetchall()
>>>>>>> a7da25260dceea429f5eb518d6e1724241ceebfa
        for cota in cotas:
            cota_id = cota[0]
            dezenas_cota = [int(x) for x in cota[1].split() if x.isdigit()]
            pontos = len(set(dezenas_cota).intersection(set(lista_resultado)))
            cursor.execute("UPDATE vendas SET pontos = ? WHERE id = ?", (pontos, cota_id))
<<<<<<< HEAD
    else:
        # SISTEMA ESPIÃO DE APURAÇÃO: Se o campo vier vazio (apagado) ou inválido, limpa o resultado oficial no banco e zera a pontuação de todos
        atualizar_config('resultado_oficial', '')
        cursor.execute("UPDATE vendas SET pontos = 0")
        
    conn.commit()
    conn.close()
        
=======
        conn.commit()
        conn.close()
>>>>>>> a7da25260dceea429f5eb518d6e1724241ceebfa
    return redirect('/?admin=true')

@app.route('/zerar_vendas', methods=['POST'])
def zerar_vendas():
    conn = sqlite3.connect('primeprint.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM vendas")
    conn.commit()
    conn.close()
    return redirect('/?admin=true')

if __name__ == '__main__':
<<<<<<< HEAD
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
=======
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
>>>>>>> a7da25260dceea429f5eb518d6e1724241ceebfa
