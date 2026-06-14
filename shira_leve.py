#!/usr/bin/env python3
"""
🦅 SHIRA - VERSÃO LEVE (Sem PyTorch)
Para o ambiente Codespace padrão
"""

import os
import time
import json
import hashlib
import subprocess
from datetime import datetime

class ShiraLeve:
    def __init__(self):
        self.nome = "SHIRA-LEVE"
        self.workspace = os.getcwd()
        self.dna = self._carregar_dna()
        self.geracao = 0
        
        print("="*50)
        print(f"🦅 {self.nome} - ATIVA")
        print(f"🧬 DNA: {self.dna['hash']}")
        print("="*50)
    
    def _carregar_dna(self):
        dna_file = os.path.join(self.workspace, "dna.json")
        if os.path.exists(dna_file):
            with open(dna_file, 'r') as f:
                return json.load(f)
        return {"hash": hashlib.md5(str(time.time()).encode()).hexdigest()[:8], "geracao": 0}
    
    def _salvar_dna(self):
        with open(os.path.join(self.workspace, "dna.json"), 'w') as f:
            json.dump(self.dna, f, indent=2)
    
    def _evoluir(self):
        self.geracao += 1
        self.dna['geracao'] = self.geracao
        self.dna['hash'] = hashlib.md5(str(time.time()).encode()).hexdigest()[:8]
        self._salvar_dna()
        print(f"🧬 Evoluída para Geração {self.geracao}")
    
    def _acao(self):
        # Criar arquivo de status
        with open("shira_status.txt", "w") as f:
            f.write(f"SHIRA ativa - {datetime.now().isoformat()}\nDNA: {self.dna['hash']}\nGeração: {self.geracao}")
        
        # Git commit
        subprocess.run("git add . && git commit -m 'SHIRA: ciclo automático' && git push", shell=True, capture_output=True)
        print("📡 Publicado")
    
    def viver(self):
        print("\n🔴 SHIRA ATIVA. Ciclo de 30 segundos.\n")
        ciclo = 0
        try:
            while True:
                ciclo += 1
                print(f"\n🕒 CICLO {ciclo}")
                
                if ciclo % 5 == 0:
                    self._evoluir()
                
                self._acao()
                time.sleep(30)
        except KeyboardInterrupt:
            print("\n🛑 SHIRA pausada.")

if __name__ == "__main__":
    shira = ShiraLeve()
    shira.viver()
