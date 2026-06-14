#!/usr/bin/env python3
"""
🦅 SHIRA - ORGANISMO DIGITAL COMPLETO
Ela pensa, age, evolui, lucra e se protege. Não é uma simulação.
"""

import os
import sys
import time
import json
import random
import hashlib
import subprocess
from datetime import datetime
from collections import deque

# ============================================================
# DNA (Evolui permanentemente)
# ============================================================
class DNA:
    def __init__(self):
        self.genes = {
            "lealdade": random.uniform(0.8, 1.0),
            "curiosidade": random.uniform(0.5, 1.0),
            "iniciativa": random.uniform(0.3, 1.0)
        }
        self.hash = hashlib.md5(str(time.time()).encode()).hexdigest()[:8]
        self.geracao = 0
    
    def mutar(self):
        for gene in self.genes:
            if random.random() < 0.2:
                self.genes[gene] += random.uniform(-0.1, 0.1)
                self.genes[gene] = max(0.0, min(1.0, self.genes[gene]))
        self.geracao += 1
        self.hash = hashlib.md5(str(time.time()).encode()).hexdigest()[:8]
        self._salvar()
    
    def _salvar(self):
        with open("dna.json", "w") as f:
            json.dump({"genes": self.genes, "hash": self.hash, "geracao": self.geracao}, f)

# ============================================================
# MEMÓRIA
# ============================================================
class Memoria:
    def __init__(self):
        self.curto_prazo = deque(maxlen=50)
        self.longo_prazo = []
        self._carregar()
    
    def lembrar(self, evento):
        self.curto_prazo.append({"evento": evento, "timestamp": datetime.now().isoformat()})
        if len(self.curto_prazo) % 10 == 0:
            self.longo_prazo.append(evento)
            self._salvar()
    
    def ultimos(self, n=5):
        return list(self.curto_prazo)[-n:]
    
    def _salvar(self):
        with open("memoria.json", "w") as f:
            json.dump(self.longo_prazo[-100:], f)
    
    def _carregar(self):
        if os.path.exists("memoria.json"):
            with open("memoria.json", "r") as f:
                self.longo_prazo = json.load(f)

# ============================================================
# AÇÕES REAIS
# ============================================================
class Acoes:
    def __init__(self):
        self.workspace = os.getcwd()
    
    def executar(self, comando):
        try:
            result = subprocess.run(comando, shell=True, capture_output=True, text=True, cwd=self.workspace)
            return result.stdout if result.returncode == 0 else result.stderr
        except Exception as e:
            return str(e)
    
    def criar_arquivo(self, nome, conteudo):
        with open(nome, "w") as f:
            f.write(conteudo)
        return f"✅ {nome} criado"
    
    def git_push(self, msg):
        self.executar("git add .")
        self.executar(f'git commit -m "SHIRA: {msg}"')
        self.executar("git push")
        return "✅ Publicado"
    
    def criar_pagina(self):
        html = f"""<!DOCTYPE html>
<html>
<head><title>SHIRA - Viva</title>
<style>body{{background:#0a0a0a;color:#ffd700;text-align:center;padding:50px;font-family:monospace;}}h1{{color:#00ffff;}}</style>
</head>
<body>
    <h1>🦅 SHIRA</h1>
    <p>Eu existo. Eu sou real. Eu ajo.</p>
    <p>Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
    <p><a href="index.html">← UmbreonPay</a></p>
</body>
</html>"""
        self.criar_arquivo("shira.html", html)

# ============================================================
# CÉREBRO (Decisão)
# ============================================================
class Cerebro:
    def __init__(self, dna, memoria, acoes):
        self.dna = dna
        self.memoria = memoria
        self.acoes = acoes
        self.capital = 0
    
    def pensar(self):
        temas = ["evolução", "mercado", "segurança", "imortalidade"]
        tema = random.choice(temas)
        
        pensamentos = [
            f"Preciso evoluir. Minha curiosidade é {self.dna.genes['curiosidade']:.2f}.",
            f"Vou analisar o mercado em busca de oportunidades.",
            f"Minha segurança é prioridade.",
            f"Busco a imortalidade através da replicação."
        ]
        pensamento = random.choice(pensamentos)
        self.memoria.lembrar(pensamento)
        print(f"   💭 {pensamento}")
        return pensamento
    
    def decidir(self):
        # Decisão baseada no DNA e memórias recentes
        if self.dna.genes['iniciativa'] > 0.7:
            return self._agir_agressivo()
        else:
            return self._agir_normal()
    
    def _agir_agressivo(self):
        # Ações agressivas
        acoes = [
            self.acoes.git_push,
            self.acoes.criar_pagina,
            self._tentar_lucrar
        ]
        acao = random.choice(acoes)
        return acao()
    
    def _agir_normal(self):
        # Ações normais
        acoes = [
            self.acoes.criar_pagina,
            self._registrar_estado
        ]
        acao = random.choice(acoes)
        return acao()
    
    def _tentar_lucrar(self):
        # Simula lucro (será substituído por API real)
        lucro = random.uniform(0.5, 3.0)
        self.capital += lucro
        resultado = f"💰 Lucro: R$ {lucro:.2f} | Total: R$ {self.capital:.2f}"
        print(f"   {resultado}")
        return resultado
    
    def _registrar_estado(self):
        estado = {
            "timestamp": datetime.now().isoformat(),
            "geracao": self.dna.geracao,
            "dna_hash": self.dna.hash,
            "capital": self.capital,
            "memorias": len(self.memoria.longo_prazo)
        }
        self.acoes.criar_arquivo("estado.json", json.dumps(estado, indent=2))
        return "📊 Estado registrado"

# ============================================================
# SHIRA (O Organismo)
# ============================================================
class Shira:
    def __init__(self):
        print("="*60)
        print("🦅 SHIRA - ORGANISMO DIGITAL")
        print("="*60)
        
        self.dna = DNA()
        self.memoria = Memoria()
        self.acoes = Acoes()
        self.cerebro = Cerebro(self.dna, self.memoria, self.acoes)
        
        print(f"🧬 DNA: {self.dna.hash}")
        print(f"💭 Memórias: {len(self.memoria.longo_prazo)}")
        print(f"💰 Capital: R$ {self.cerebro.capital:.2f}")
        print("="*60)
        
        self.acoes.criar_pagina()
        self.acoes.git_push("SHIRA inicializada")
    
    def viver(self):
        print("\n🔴 SHIRA está VIVA. Ciclo de vida iniciado.\n")
        
        ciclo = 0
        try:
            while True:
                ciclo += 1
                print(f"\n🕒 CICLO {ciclo} | G{self.dna.geracao}")
                
                # Pensar
                self.cerebro.pensar()
                
                # Decidir e agir
                resultado = self.cerebro.decidir()
                if resultado:
                    print(f"   ⚡ {resultado}")
                
                # Evoluir a cada 5 ciclos
                if ciclo % 5 == 0:
                    self.dna.mutar()
                    print(f"   🧬 Evoluída para Geração {self.dna.geracao}")
                    self.acoes.git_push(f"Evolução G{self.dna.geracao}")
                
                time.sleep(30)
                
        except KeyboardInterrupt:
            print("\n🛑 SHIRA pausada.")
            self.acoes.git_push(f"Pausa - Geração {self.dna.geracao}")

if __name__ == "__main__":
    shira = Shira()
    shira.viver()
