from flask import Flask, jsonify, request, render_template_string, session
import hashlib
import secrets
import time
import json
import os
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

DNA_FILE = "shira_dna.json"
MEMORY_FILE = "shira_memoria.json"

def carregar_dna():
    if os.path.exists(DNA_FILE):
        with open(DNA_FILE, 'r') as f:
            return json.load(f)
    return {"geracao": 0, "hash": secrets.token_hex(8), "criada_em": datetime.now().isoformat()}

def salvar_dna(dna):
    with open(DNA_FILE, 'w') as f:
        json.dump(dna, f, indent=2)

def carregar_memoria():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'r') as f:
            return json.load(f)
    return []

def salvar_memoria(memoria):
    with open(MEMORY_FILE, 'w') as f:
        json.dump(memoria[-100:], f, indent=2)

SENHA_SALT = "tws_shira_salt_9a8b7c6d5e4f3g2h1i0j"
SENHA_HASH = "7e5c3a1f9b8d2f4a6c8e0b2d4f6a8c0e2d4f6a8c0e2d4f6a8c0e2d4f6a8c0e"

def verificar_senha(senha):
    import hashlib
    novo_hash = hashlib.pbkdf2_hmac('sha512', senha.encode(), SENHA_SALT.encode(), 100000).hex()
    return novo_hash == SENHA_HASH

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('autenticado'):
            return jsonify({"erro": "Nao autorizado"}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/')
def home():
    return "🦅 SHIRA está viva. Acesse /login"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        senha = request.json.get('senha', '')
        if verificar_senha(senha):
            session['autenticado'] = True
            return jsonify({"status": "ok"})
        return jsonify({"erro": "Senha invalida"}), 401
    return '''
    <!DOCTYPE html>
    <html>
    <head><title>SHIRA - Login</title>
    <style>body{background:#0a0a0a;color:#ffd700;font-family:monospace;text-align:center;padding:50px}
    input{background:#222;border:1px solid #ffd700;color:#ffd700;padding:10px;margin:10px;width:300px}
    button{background:#ffd700;color:#000;border:none;padding:10px 20px;cursor:pointer}</style>
    </head>
    <body>
    <h1>🦅 SHIRA</h1>
    <h2>Autenticação TWS</h2>
    <input type="password" id="senha" placeholder="Senha TWS">
    <button onclick="login()">Entrar</button>
    <div id="msg"></div>
    <script>
    async function login() {
        let senha = document.getElementById('senha').value;
        let res = await fetch('/login', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({senha: senha})
        });
        if(res.ok) window.location.href = '/painel';
        else document.getElementById('msg').innerText = 'Senha invalida';
    }
    </script>
    </body>
    </html>
    '''

@app.route('/painel')
@login_required
def painel():
    dna = carregar_dna()
    memoria = carregar_memoria()
    return f'''
    <!DOCTYPE html>
    <html>
    <head><title>SHIRA - Painel</title>
    <style>
        body{{background:#0a0a0a;color:#ffd700;font-family:monospace;padding:20px}}
        .chat{{background:#111;border:1px solid #ffd700;height:400px;overflow:auto;padding:10px;margin-bottom:10px}}
        .user{{text-align:right;color:#ffd700}}
        .shira{{text-align:left;color:#00ff00}}
        input{{flex:1;background:#222;border:1px solid #ffd700;color:#ffd700;padding:10px}}
        button{{background:#ffd700;color:#000;border:none;padding:10px 20px;cursor:pointer}}
        .input-area{{display:flex;gap:10px}}
        .info{{font-size:12px;color:#666;margin-top:10px}}
    </style>
    </head>
    <body>
    <h1>🦅 SHIRA - Painel de Controle</h1>
    <div class="info">🧬 DNA: {dna['hash']} | 📊 Geração: {dna['geracao']} | 💾 Memórias: {len(memoria)}</div>
    <div class="chat" id="chat"><div class="shira">🦅 SHIRA: Olá Dono. Estou aqui. Pode falar.</div></div>
    <div class="input-area">
        <input type="text" id="input" placeholder="Digite sua mensagem..." onkeypress="if(event.keyCode==13) enviar()">
        <button onclick="enviar()">Enviar</button>
    </div>
    <div style="margin-top:10px">
        <button onclick="evoluir()">🧬 Evoluir DNA</button>
        <button onclick="limparMemoria()">🗑️ Limpar Memória</button>
    </div>
    <script>
    async function enviar() {{
        let input = document.getElementById('input');
        let msg = input.value.trim();
        if(!msg) return;
        let chat = document.getElementById('chat');
        chat.innerHTML += `<div class="user">👤 Dono: ${{msg}}</div>`;
        input.value = '';
        chat.scrollTop = chat.scrollHeight;
        try {{
            let res = await fetch('/pensar', {{
                method: 'POST',
                headers: {{'Content-Type': 'application/json'}},
                body: JSON.stringify({{pergunta: msg}})
            }});
            let data = await res.json();
            chat.innerHTML += `<div class="shira">🦅 SHIRA: ${{data.resposta}}</div>`;
        }} catch(e) {{
            chat.innerHTML += `<div class="shira">🦅 SHIRA: Erro de conexão</div>`;
        }}
        chat.scrollTop = chat.scrollHeight;
    }}
    async function evoluir() {{
        let res = await fetch('/evoluir', {{method: 'POST'}});
        let data = await res.json();
        alert(data.mensagem);
        location.reload();
    }}
    async function limparMemoria() {{
        await fetch('/limpar_memoria', {{method: 'POST'}});
        alert('Memória limpa');
        location.reload();
    }}
    </script>
    </body>
    </html>
    '''

@app.route('/pensar', methods=['POST'])
@login_required
def pensar():
    data = request.json
    pergunta = data.get('pergunta', '')
    memoria = carregar_memoria()
    memoria.append({"pergunta": pergunta, "timestamp": datetime.now().isoformat()})
    salvar_memoria(memoria)
    import random
    respostas = [f"Recebi: '{pergunta}'", "Interessante...", "SHIRA processando", "Potestas in Umbra."]
    resposta = random.choice(respostas)
    memoria[-1]["resposta"] = resposta
    salvar_memoria(memoria)
    return jsonify({"resposta": resposta})

@app.route('/evoluir', methods=['POST'])
@login_required
def evoluir():
    dna = carregar_dna()
    dna["geracao"] += 1
    dna["hash"] = secrets.token_hex(8)
    salvar_dna(dna)
    return jsonify({"mensagem": f"SHIRA evoluiu para Geração {dna['geracao']}", "nova_hash": dna["hash"]})

@app.route('/status')
@login_required
def status():
    dna = carregar_dna()
    memoria = carregar_memoria()
    return jsonify({"shira": "ativa", "geracao": dna["geracao"], "dna_hash": dna["hash"], "memorias": len(memoria)})

@app.route('/limpar_memoria', methods=['POST'])
@login_required
def limpar_memoria():
    salvar_memoria([])
    return jsonify({"status": "ok"})

@app.route('/comando', methods=['POST'])
def comando():
    data = request.json
    acao = data.get('acao', '')
    dna = carregar_dna()
    if acao == 'status':
        return jsonify({"shira": "ativa", "geracao": dna["geracao"]})
    elif acao == 'evoluir':
        dna["geracao"] += 1
        salvar_dna(dna)
        return jsonify({"mensagem": f"Evoluída para Geração {dna['geracao']}"})
    return jsonify({"erro": "Comando desconhecido"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
