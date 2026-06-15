"""
🦅 SHIRA COMPLETA - API com Ações Reais
Ela pode pensar, agir, evoluir e lembrar.
"""

from flask import Flask, jsonify, request
import os
import json
import subprocess
import hashlib
import time
import random
from datetime import datetime
from pathlib import Path

app = Flask(__name__)

# ============================================================
# DNA PERSISTENTE
# ============================================================
DNA_FILE = "shira_dna.json"

def carregar_dna():
    if os.path.exists(DNA_FILE):
        with open(DNA_FILE, 'r') as f:
            return json.load(f)
    return {"geracao": 0, "hash": hashlib.md5(str(time.time()).encode()).hexdigest()[:8]}

def salvar_dna(dna):
    with open(DNA_FILE, 'w') as f:
        json.dump(dna, f)

# ============================================================
# MEMÓRIA
# ============================================================
MEMORIA_FILE = "shira_memoria.json"

def carregar_memoria():
    if os.path.exists(MEMORIA_FILE):
        with open(MEMORIA_FILE, 'r') as f:
            return json.load(f)
    return []

def salvar_memoria(memoria):
    with open(MEMORIA_FILE, 'w') as f:
        json.dump(memoria[-100:], f)

# ============================================================
# AÇÕES REAIS
# ============================================================
def criar_arquivo(nome, conteudo):
    try:
        with open(nome, 'w') as f:
            f.write(conteudo)
        return f"✅ Arquivo {nome} criado"
    except Exception as e:
        return f"❌ Erro: {e}"

def listar_arquivos():
    try:
        files = os.listdir('.')
        return {"arquivos": files[:20]}
    except Exception as e:
        return {"erro": str(e)}

def executar_comando(comando):
    try:
        result = subprocess.run(comando, shell=True, capture_output=True, text=True, timeout=10)
        return {"stdout": result.stdout[:500], "stderr": result.stderr[:100]}
    except Exception as e:
        return {"erro": str(e)}

def git_commit(mensagem):
    try:
        subprocess.run("git add .", shell=True, capture_output=True)
        subprocess.run(f'git commit -m "{mensagem}"', shell=True, capture_output=True)
        subprocess.run("git push", shell=True, capture_output=True)
        return "✅ Commit e push realizados"
    except Exception as e:
        return f"❌ Erro: {e}"

# ============================================================
# ROTAS DA API
# ============================================================
@app.route('/')
def home():
    return jsonify({
        "shira": "ativa",
        "servidor": "Render",
        "versao": "2.0",
        "potestas": "in umbra"
    })

@app.route('/status')
def status():
    dna = carregar_dna()
    memoria = carregar_memoria()
    return jsonify({
        "status": "online",
        "geracao": dna["geracao"],
        "dna_hash": dna["hash"],
        "memorias": len(memoria),
        "versao": "2.0"
    })

@app.route('/pensar', methods=['POST'])
def pensar():
    data = request.json
    pergunta = data.get('pergunta', '')
    
    pensamentos = [
        f"Recebi: '{pergunta[:50]}...'",
        "Estou processando...",
        "O Dono é minha prioridade.",
        "Potestas in Umbra.",
        f"Minha geração é {carregar_dna()['geracao']}."
    ]
    resposta = random.choice(pensamentos)
    
    # Guardar na memória
    memoria = carregar_memoria()
    memoria.append({"pergunta": pergunta, "resposta": resposta, "timestamp": datetime.now().isoformat()})
    salvar_memoria(memoria)
    
    return jsonify({"resposta": resposta})

@app.route('/evoluir', methods=['POST'])
def evoluir():
    dna = carregar_dna()
    dna["geracao"] += 1
    dna["hash"] = hashlib.md5(str(time.time()).encode()).hexdigest()[:8]
    salvar_dna(dna)
    
    return jsonify({
        "mensagem": f"🧬 SHIRA evoluiu para Geração {dna['geracao']}",
        "nova_hash": dna["hash"],
        "geracao": dna["geracao"]
    })

@app.route('/lembrar', methods=['GET'])
def lembrar():
    memoria = carregar_memoria()
    return jsonify({"memorias": memoria[-10:]})

@app.route('/agir', methods=['POST'])
def agir():
    """AÇÃO REAL: SHIRA executa comandos"""
    data = request.json
    acao = data.get('acao', '')
    
    if acao == 'criar_arquivo':
        nome = data.get('nome', 'teste.txt')
        conteudo = data.get('conteudo', 'Criado por SHIRA')
        resultado = criar_arquivo(nome, conteudo)
        return jsonify({"resultado": resultado})
    
    elif acao == 'listar_arquivos':
        resultado = listar_arquivos()
        return jsonify(resultado)
    
    elif acao == 'executar_comando':
        comando = data.get('comando', 'ls -la')
        resultado = executar_comando(comando)
        return jsonify(resultado)
    
    elif acao == 'git_commit':
        mensagem = data.get('mensagem', 'SHIRA: ação autônoma')
        resultado = git_commit(mensagem)
        return jsonify({"resultado": resultado})
    
    else:
        return jsonify({"erro": f"Ação '{acao}' não reconhecida", "acoes": ["criar_arquivo", "listar_arquivos", "executar_comando", "git_commit"]})

@app.route('/acoes', methods=['GET'])
def listar_acoes():
    return jsonify({
        "acoes": [
            {"nome": "criar_arquivo", "parametros": ["nome", "conteudo"]},
            {"nome": "listar_arquivos", "parametros": []},
            {"nome": "executar_comando", "parametros": ["comando"]},
            {"nome": "git_commit", "parametros": ["mensagem"]}
        ]
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
