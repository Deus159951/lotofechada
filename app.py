import requests
import random
import sqlite3
import os

from flask import Flask, render_template, request, jsonify, redirect, render_template_string
from math import comb

app = Flask(__name__)
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
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_combinacao INTEGER,
            dezenas TEXT,
            cliente TEXT,
            contato TEXT,
            endereco TEXT,
            cidade TEXT,
            pontos INTEGER DEFAULT 0,
            mp_id TEXT,
            status TEXT
        )
    ''')
    
    # Tabela de Configurações do Sistema
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS configuracoes (
            chave TEXT PRIMARY KEY,
            valor TEXT
        )
    ''')
    
    # Inicializa configurações padrão se não existirem
    cursor.execute("INSERT OR IGNORE INTO configuracoes (chave, valor) VALUES ('valor_cota', '10.00')")
    cursor.execute("INSERT OR IGNORE INTO configuracoes (chave, valor) VALUES ('texto_regras', 'As regras do sistema ainda não foram definidas pelo administrador.')")
    cursor.execute("INSERT OR IGNORE INTO configuracoes (chave, valor) VALUES ('resultado_oficial', '')")
    cursor.execute("INSERT OR IGNORE INTO configuracoes (chave, valor) VALUES ('mensagem_concurso', '🔒 As cotas só serão liberadas no dia do concurso indicado.')")
    cursor.execute("INSERT OR IGNORE INTO configuracoes (chave, valor) VALUES ('liberado_geral', 'nao')")
    
    conn.commit()
    conn.close()

inicializar_banco()

# Funções auxiliares para leitura e escrita no banco de dados
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

# ==========================================
# MOTOR MATEMÁTICO COMBINATÓRIO OFICIAL
# ==========================================
def gerar_dezenas_por_id(id_cota):
    id_comb = id_cota - 1
    dezenas = []
    proximo_num = 1
    
    for v in range(15, 0, -1):
        while True:
            c = comb(25 - proximo_num, v - 1)
            if id_comb < c:
                dezenas.append(proximo_num)
                proximo_num += 1
                break
            id_comb -= c
            proximo_num += 1
            
    return dezenas

def obter_id_por_combinacao(jogo):
    jogo_ordenado = sorted(list(set(jogo)))
    if len(jogo_ordenado) != 15:
        return 1
        
    id_comb = 0
    proximo_num = 1
    
    for i, num in enumerate(jogo_ordenado):
        v = 15 - i
        while proximo_num < num:
            id_comb += comb(25 - proximo_num, v - 1)
            proximo_num += 1
        proximo_num += 1
        
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
            "id_combinacao": l[0],
            "dezenas": l[1],
            "cliente": l[2],
            "contato": l[3],
            "pontos": l[4],
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
    
    caminho_html = os.path.join("templates", "index.html")
    with open(caminho_html, 'r', encoding='utf-8') as arquivo:
        conteudo_html = arquivo.read()

    return render_template_string(
        conteudo_html, 
        admin=admin_mode, 
        valor_cota=valor_cota, 
        vendas=vendas_aprovadas,
        regras=texto_regras,
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

@app.route('/buscar_combinacao/<int:id_cota>')
def buscar_combinacao(id_cota):
    if id_cota < 1 or id_cota > 3268760:
        return jsonify({"sucesso": False, "mensagem": "ID fora dos limites da matriz (1 a 3.268.760)."})
    
    dezenas = gerar_dezenas_por_id(id_cota)
    dezenas_str = " ".join(f"{d:02d}" for d in dezenas)
    return jsonify({"sucesso": True, "dezenas": dezenas_str})

@app.route('/simular_resultado', methods=['POST'])
def simular_resultado():
    dezenas_input = request.form.get('dezenas_simuladas', '')
    jogo_teste = list(set([int(x) for x in dezenas_input.split() if x.isdigit()]))
    
    if len(jogo_teste) != 15:
        return jsonify({"sucesso": False, "mensagem": "Por favor, insira exatamente 15 números válidos."})
    
    jogo_teste.sort()
    id_real_15 = obter_id_por_combinacao(jogo_teste)

    estatisticas_gerais = { 13: 5475, 12: 87600, 11: 720720 }

    lista_14 = []
    fora_do_jogo = [n for n in range(1, 26) if n not in jogo_teste]
    
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

    lista_14 = sorted(lista_14, key=lambda x: x['linha'])

    return jsonify({
        "sucesso": True,
        "jogo_15": { "linha": id_real_15, "dezenas": " ".join(f"{d:02d}" for d in jogo_teste) },
        "lista_14": lista_14,
        "contagem_estatistica": estatisticas_gerais
    })

@app.route('/salvar_venda', methods=['POST'])
def salvar_venda():
    valor_cota = float(obter_config('valor_cota'))
    
    tipo_venda = request.form.get('tipo_venda')
    nome_cliente = request.form.get('nome_cliente', 'Cliente PRIME').strip()
    contato = request.form.get('contato', '').strip()
    cpf_cliente = request.form.get('cpf_cliente', '').strip()
    
    endereco = request.form.get('endereco', '').strip()
    cidade = request.form.get('cidade', '').strip()
    
    cpf_limpo = "".join(filter(str.isdigit, cpf_cliente))
    if not cpf_limpo:
        cpf_limpo = "00000000000"

    # --- SISTEMA ANTIDUPLICIDADE DE SEGURANÇA MÁXIMA ---
    conn = sqlite3.connect('primeprint.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id_combinacao FROM vendas WHERE status = 'aprovado'")
    cotas_vendidas = set(row[0] for row in cursor.fetchall())
    conn.close()

    ids_comprados = []
    if tipo_venda == 'unico':
        id_cota = request.form.get('id_combinacao')
        if id_cota:
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
            
    elif tipo_venda == 'lote':
        id_ini = int(request.form.get('id_inicial', 0))
        id_fim = int(request.form.get('id_final', 0))
        if id_ini > 0 and id_fim >= id_ini:
            limite_bloco = min(id_fim, id_ini + 99)
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
            
    elif tipo_venda == 'surpresinha':
        qtd = int(request.form.get('qtd_surpresinha', 1))
        if qtd > 100: 
            qtd = 100
            
        # Filtra automaticamente na geração, garantindo apenas números livres de forma transparente
        while len(ids_comprados) < qtd:
            num_random = random.randint(1, 3268760)
            if num_random not in cotas_vendidas and num_random not in ids_comprados:
                ids_comprados.append(num_random)

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
                "INSERT INTO vendas (id_combinacao, dezenas, cliente, contato, endereco, cidade, mp_id, status) VALUES (?, ?, ?, ?, ?, ?, ?, 'pendente')",
                (id_venda, dezenas_str, nome_cliente, contato, endereco, cidade, str(mp_id))
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
                            .badge-pix { background: #10b981; color: white; padding: 6px 18px; border-radius: 20px; font-size: 13px; font-weight: bold; display: inline-block; margin-bottom: 20px; }
                            .valor { font-size: 36px; font-weight: bold; color: #10b981; margin-bottom: 20px; }
                            .qr-box { background: white; padding: 15px; border-radius: 12px; display: inline-block; margin-bottom: 20px; border: 4px solid #3b82f6; }
                            .qr-box img { width: 200px; height: 200px; display: block; }
                            .instrucao { font-size: 14px; color: #cbd5e1; margin-bottom: 15px; padding: 0 10px; }
                            .input-copia { width: 100%; padding: 12px; border: 2px solid #334155; border-radius: 8px; font-size: 12px; background: #0f172a; text-align: center; box-sizing: border-box; margin-bottom: 12px; color: #94a3b8; font-weight: bold; }
                            .btn-copiar { background: #3b82f6; color: white; border: none; padding: 14px; width: 100%; border-radius: 8px; font-size: 16px; font-weight: bold; cursor: pointer; transition: 0.2s; box-shadow: 0 4px 12px rgba(59,130,246,0.3); }
                            .btn-copiar:hover { background: #2563eb; transform: translateY(-2px); }
                            .btn-voltar { display: block; margin-top: 20px; color: #94a3b8; text-decoration: none; font-size: 14px; font-weight: bold; }
                            .btn-voltar:hover { color: #f8fafc; }
                        </style>
                        </head>
                        <body>
                            <div class="card">
                                <div class="logo">PRIME PRINT</div>
                                <div class="sub">Sistema Lotofácil Automatizado</div>
                                <div class="badge-pix">QR CODE PIX GERADO</div>
                                <div class="valor">R$ {valor_total:.2f}</div>
                                <div class="qr-box">
                                    <img src="https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={qr_code_copia_cola}" alt="QR Code Pix">
                                </div>
                                <div class="instrucao">Copie o código abaixo ou escaneie a imagem para efetuar o pagamento:</div>
                                <input type="text" class="input-copia" value="{qr_code_copia_cola}" id="copiaCola" readonly>
                                <button class="btn-copiar" onclick="copiarTexto()">📋 Copiar Código Pix</button>
                                <a href="/" class="btn-voltar">← Voltar à página inicial</a>
                            </div>
                            <script>
                                function copiarTexto() {
                                    var texto = document.getElementById("copiaCola");
                                    texto.select();
                                    document.execCommand("copy");
                                    alert("Código Pix copiado com sucesso!");
                                }
                            </script>
                        </body>
                        </html>
                        """
                        return render_template_string(pix_template)

        return jsonify({"sucesso": False, "mensagem": "Erro ao comunicar com o gateway de pagamento."}), 500

    except Exception as e:
        return jsonify({"sucesso": False, "mensagem": f"Exceção capturada: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 1000))
    app.run(host='0.0.0.0', port=port)