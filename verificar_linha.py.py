<<<<<<< HEAD
import requests
import random
import sqlite3
from flask import Flask, render_template, request, jsonify, redirect
from math import comb

app = Flask(__name__)

# ==========================================
# CONFIGURAÇÕES DO SISTEMA (PRIME PRINT)
# ==========================================
MERCADOPAGO_TOKEN = "APP_USR-2030455237914285-061213-49091f47d2a141002ac73f272feabe0a-193922692"

# ==========================================
# CONFIGURAÇÃO DO BANCO DE DADOS (SQLITE)
# ==========================================
def inicializar_banco():
    conn = sqlite3.connect('primeprint.db')
    cursor = conn.cursor()
    
    # Tabela de Vendas/Cotas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_combinacao INTEGER,
            dezenas TEXT,
            cliente TEXT,
            contato TEXT,
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
    
    conn = sqlite3.connect('primeprint.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id_combinacao, dezenas, cliente, contato, pontos, status FROM vendas WHERE status = 'aprovado'")
    linhas = cursor.fetchall()
    conn.close()
    
    vendas_aprovadas = []
    for l in linhas:
        vendas_aprovadas.append({
            "id_combinacao": l[0],
            "dezenas": l[1],
            "cliente": l[2],
            "contato": l[3],
            "pontos": l[4],
            "status": l[5]
        })
    
    return render_template(
        'index.html', 
        admin=admin_mode, 
        valor_cota=valor_cota, 
        vendas=vendas_aprovadas,
        regras=texto_regras
    )

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
    
    cpf_limpo = "".join(filter(str.isdigit, cpf_cliente))
    if not cpf_limpo:
        cpf_limpo = "00000000000"

    ids_comprados = []
    if tipo_venda == 'unico':
        id_cota = request.form.get('id_combinacao')
        if id_cota:
            ids_comprados.append(int(id_cota))
    elif tipo_venda == 'lote':
        id_ini = int(request.form.get('id_inicial', 0))
        id_fim = int(request.form.get('id_final', 0))
        if id_ini > 0 and id_fim >= id_ini:
            limite_bloco = min(id_fim, id_ini + 99)
            ids_comprados = list(range(id_ini, limite_bloco + 1))
    elif tipo_venda == 'surpresinha':
        qtd = int(request.form.get('qtd_surpresinha', 1))
        if qtd > 100: 
            qtd = 100
        ids_comprados = [random.randint(1, 3268760) for _ in range(qtd)]

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

        # Já salva no banco como pendente
        for id_venda in ids_comprados:
            dezenas_cota = gerar_dezenas_por_id(id_venda)
            dezenas_str = " ".join(f"{d:02d}" for d in dezenas_cota)
            cursor.execute(
                "INSERT INTO vendas (id_combinacao, dezenas, cliente, contato, mp_id, status) VALUES (?, ?, ?, ?, ?, 'pendente')",
                (id_venda, dezenas_str, nome_cliente, contato, str(mp_id))
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
                        from flask import render_template_string
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
                                            window.location.href = '/sucesso?mp_id={{ payment_id }}';
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

            return f"<h2>⚠️ Transação local</h2><a href='/'><button>Voltar</button></a>", 200
        else:
            return f"<h2>⚠️ Ajuste Requerido: {dados_retorno.get('message')}</h2><a href='/'><button>Voltar</button></a>", 200

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
                # Atualiza o status no banco de dados SQLite
                conn = sqlite3.connect('primeprint.db')
                cursor = conn.cursor()
                cursor.execute("UPDATE vendas SET status = 'aprovado' WHERE mp_id = ?", (str(mp_id),))
                
                # Após aprovar, aplica os pontos caso o resultado oficial já exista
                res_oficial_str = obter_config('resultado_oficial')
                if res_oficial_str:
                    res_oficial_lista = res_oficial_str.split()
                    cursor.execute("SELECT id, dezenas FROM vendas WHERE mp_id = ? AND status = 'aprovado'", (str(mp_id),))
                    cotas_aprovadas = cursor.fetchall()
                    
                    for cota in cotas_aprovadas:
                        dezenas_cota = cota[1].split()
                        pontos = len(set(dezenas_cota).intersection(set(res_oficial_lista)))
                        cursor.execute("UPDATE vendas SET pontos = ? WHERE id = ?", (pontos, cota[0]))

                conn.commit()
                conn.close()
                return jsonify({"status": "aprovado"})
    except Exception as e:
        print("Erro ao verificar pagamento:", e)
        pass
    
    return jsonify({"status": "pendente"})

@app.route('/sucesso')
def sucesso():
    mp_id = request.args.get('mp_id')
    
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
    
    if not minhas_cotas:
        return redirect('/')
        
    html_sucesso = """
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
            .btn { display: inline-block; margin-top: 30px; padding: 15px 30px; background: #3b82f6; color: white; text-decoration: none; border-radius: 8px; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="box">
            <h1>🎉 Pagamento Aprovado!</h1>
            <p>Seus números foram gerados com sucesso e vinculados ao seu nome.</p>
            <p>Aqui estão as suas cotas oficiais:</p>
            
            {% for cota in cotas %}
                <div class="dezenas-box">
                    <span style="font-size: 14px; color: #94a3b8; display: block; letter-spacing: 0;">Linha/Cota: {{ cota.id_combinacao }}</span>
                    {{ cota.dezenas }}
                </div>
            {% endfor %}
            
            <a href="/" class="btn">Voltar ao Início</a>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_sucesso, cotas=minhas_cotas)

@app.route('/atualizar_valor_cota', methods=['POST'])
def atualizar_valor_cota():
    try:
        novo_valor = request.form.get('novo_valor', '10.00').replace(',', '.')
        atualizar_config('valor_cota', novo_valor)
    except: 
        pass
    return redirect('/?admin=true')

@app.route('/salvar_regras', methods=['POST'])
def salvar_regras():
    novo_texto = request.form.get('regras_texto')
    if novo_texto is not None:
        atualizar_config('texto_regras', novo_texto)
    return redirect('/?admin=true')

@app.route('/varredura', methods=['POST'])
def varredura():
    dezenas_input = request.form.get('dezenas_oficiais', '')
    lista_resultado = [int(x) for x in dezenas_input.split() if x.isdigit()]
    
    if len(lista_resultado) == 15:
        # Salva o resultado oficial no banco
        res_oficial_str = " ".join(f"{d:02d}" for d in lista_resultado)
        atualizar_config('resultado_oficial', res_oficial_str)
        
        # Faz o cruzamento de todos os bilhetes vendidos e aprovados
        conn = sqlite3.connect('primeprint.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, dezenas FROM vendas WHERE status = 'aprovado'")
        cotas = cursor.fetchall()
        
        for cota in cotas:
            cota_id = cota[0]
            dezenas_cota = [int(x) for x in cota[1].split() if x.isdigit()]
            
            # Calcula os acertos (intersecção)
            pontos = len(set(dezenas_cota).intersection(set(lista_resultado)))
            
            # Atualiza a pontuação no banco
            cursor.execute("UPDATE vendas SET pontos = ? WHERE id = ?", (pontos, cota_id))
            
        conn.commit()
        conn.close()
        
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
    app.run(host='0.0.0.0', port=5000, debug=True)
=======
# Lista de 15 números de um resultado real da Lotofácil
# (Exemplo: concurso 3110)
resultado_oficial = [1, 2, 4, 5, 8, 9, 10, 11, 13, 14, 18, 19, 21, 22, 23]
resultado_oficial.sort() # Organiza em ordem crescente

print("Procurando o resultado no arquivo...")

with open("todas_combinacoes.txt", "r") as f:
    for i, linha in enumerate(f, 1):
        # Transforma a linha do arquivo em lista de números
        jogo = sorted(list(map(int, linha.strip().split(','))))
        
        # Compara com o resultado oficial
        if jogo == resultado_oficial:
            print(f"ENCONTRADO! O sorteio está na linha {i} do seu arquivo.")
            break
    else:
        print("Resultado não encontrado (isso não deveria acontecer se o arquivo estiver completo).")
def encontrar_linha():
    # Pergunta os números ao usuário
    entrada = input("Digite os 15 números sorteados, separados por vírgula (ex: 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15): ")
    try:
        # Transforma a entrada em uma lista de inteiros e ordena
        numeros_sorteados = sorted([int(n.strip()) for n in entrada.split(',')])
    except ValueError:
        print("Erro: Por favor, digite apenas números separados por vírgula.")
        return

    print("Procurando no arquivo, aguarde...")
    
    with open("todas_combinacoes.txt", "r") as f:
        # Percorre o arquivo linha por linha
        for i, linha in enumerate(f, 1):
            jogo_arquivo = sorted([int(n) for n in linha.strip().split(',')])
            
            if jogo_arquivo == numeros_sorteados:
                print(f"SUCESSO! O sorteio está na LINHA {i} do seu arquivo.")
                return
                
    print("Resultado não encontrado no arquivo.")

encontrar_linha()
def encontrar_linha():
    entrada = input("Digite os 15 números sorteados, separados por vírgula: ")
    try:
        # Remove espaços e converte para números, garantindo que não tenham zeros à esquerda
        numeros_sorteados = sorted([int(n.strip()) for n in entrada.split(',')])
    except ValueError:
        print("Erro: Digite apenas números separados por vírgula.")
        return

    print("Procurando no arquivo, aguarde...")
    
    with open("todas_combinacoes.txt", "r") as f:
        for i, linha in enumerate(f, 1):
            jogo_arquivo = [int(n) for n in linha.strip().split(',')]
            if jogo_arquivo == numeros_sorteados:
                print(f"SUCESSO! O sorteio está na LINHA {i} do seu arquivo.")
                return
                
    print("Resultado não encontrado no arquivo.")

encontrar_linha()
>>>>>>> a7da25260dceea429f5eb518d6e1724241ceebfa
