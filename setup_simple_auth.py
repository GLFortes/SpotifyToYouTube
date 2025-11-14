#!/usr/bin/env python3
"""
Simple OAuth setup using browser cookie method
More reliable for YouTube Music
"""

print("""
╔════════════════════════════════════════════════════════════════╗
║     YouTube Music - Configuração de Autenticação Simples     ║
╚════════════════════════════════════════════════════════════════╝

🔄 ATENÇÃO: Este método usa browser headers, mas vamos torná-lo mais fácil!

OPÇÃO 1 - Usar biblioteca ytmusicapi browser (Recomendado):
════════════════════════════════════════════════════════════════

Este método é mais simples e funciona melhor!

Vamos instalar uma extensão para facilitar...
""")

import subprocess
import sys

# Install ytmusicapi with browser support
print("📦 Instalando suporte a browser...")
try:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', 'ytmusicapi[browser]'])
    print("✅ Instalado!\n")
except:
    print("⚠️  Falhou, mas podemos continuar...\n")

print("""
PASSO A PASSO SIMPLES:

1. Instale a extensão do navegador:
   Chrome: https://chrome.google.com/webstore/detail/ytmusicapi-browser/bdcjjaacmgogjkcnnhcknnfpomjjlhne
   Firefox: Em breve

2. Ou use o método manual (mais universal):
   
   a) Abra: https://music.youtube.com
   
   b) Pressione F12 (DevTools)
   
   c) Vá na aba "Application" ou "Storage"
   
   d) Em "Cookies" → "https://music.youtube.com"
   
   e) Copie APENAS estes cookies:
      - SAPISID
      - __Secure-1PAPISID  
      - __Secure-3PAPISID
   
   f) Cole abaixo no formato:
      SAPISID=valor; __Secure-1PAPISID=valor; __Secure-3PAPISID=valor

══════════════════════════════════════════════════════════════════

Deseja continuar com o método manual de cookies? (s/n): """)

choice = input().strip().lower()

if choice != 's':
    print("\n👋 Processo cancelado. Execute novamente quando estiver pronto!")
    sys.exit(0)

print("\nCole os cookies no formato especificado:")
print("SAPISID=xxx; __Secure-1PAPISID=xxx; __Secure-3PAPISID=xxx\n")

cookies = input("Cookies: ").strip()

if not cookies:
    print("❌ Nenhum cookie fornecido!")
    sys.exit(1)

# Parse cookies
cookie_dict = {}
for cookie in cookies.split(';'):
    if '=' in cookie:
        key, value = cookie.split('=', 1)
        cookie_dict[key.strip()] = value.strip()

# Create auth JSON
import json

auth_data = {
    "Cookie": cookies.strip(),
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Content-Type": "application/json",
    "X-Goog-AuthUser": "0",
    "x-origin": "https://music.youtube.com"
}

with open('headers_auth.json', 'w') as f:
    json.dump(auth_data, f, indent=2)

print("\n✅ Arquivo headers_auth.json criado!")
print("🎵 Teste executando: python3 test_youtube.py")
print("\n💡 Quando os cookies expirarem, execute este script novamente!")
