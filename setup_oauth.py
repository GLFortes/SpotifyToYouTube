#!/usr/bin/env python3
"""
Setup YouTube Music OAuth authentication (recommended method)
This creates a token that auto-refreshes, so you don't need to regenerate headers
"""

import os
import json
import sys

def setup_oauth():
    """Setup OAuth authentication for YouTube Music"""
    
    print("""
╔════════════════════════════════════════════════════════════════╗
║          YouTube Music OAuth Setup (Auto-Refresh)             ║
╚════════════════════════════════════════════════════════════════╝

Este método é MELHOR que headers porque:
✅ Token se renova automaticamente
✅ Não precisa regerar quando expira
✅ Mais seguro e estável

PASSO A PASSO:

1. Você precisa de credenciais OAuth do Google Cloud Console
   
2. Se já tem o arquivo client_secret_*.json baixado:
   → Coloque na pasta do projeto
   → Pressione ENTER para continuar
   
3. Se NÃO tem, siga estes passos:
   → Acesse: https://console.cloud.google.com/
   → Crie um projeto (ou use existente)
   → Ative "YouTube Data API v3"
   → Vá em APIs & Services > Credentials
   → Create Credentials > OAuth client ID
   → Escolha "Desktop app" (IMPORTANTE!)
   → Baixe o JSON
   → Coloque na pasta do projeto
""")
    
    input("Pressione ENTER quando o arquivo client_secret_*.json estiver na pasta...")
    
    # Find client_secret file
    import glob
    json_files = glob.glob('client_secret_*.json')
    
    if not json_files:
        print("\n❌ Arquivo client_secret_*.json não encontrado!")
        print("Por favor, baixe do Google Cloud Console e coloque na pasta do projeto.")
        sys.exit(1)
    
    client_file = json_files[0]
    print(f"\n✅ Encontrado: {client_file}")
    
    # Read credentials
    with open(client_file, 'r') as f:
        credentials = json.load(f)
    
    if 'installed' in credentials:
        client_id = credentials['installed']['client_id']
        client_secret = credentials['installed']['client_secret']
    elif 'web' in credentials:
        client_id = credentials['web']['client_id']
        client_secret = credentials['web']['client_secret']
    else:
        print("❌ Formato de JSON inválido!")
        sys.exit(1)
    
    print(f"🔑 Client ID: {client_id[:30]}...")
    
    # Setup OAuth using ytmusicapi
    print("\n🌐 Iniciando autenticação OAuth...")
    print("Um navegador vai abrir. Faça login e autorize o acesso.\n")
    
    from ytmusicapi.setup import setup_oauth
    
    try:
        setup_oauth(
            filepath='oauth.json',
            client_id=client_id,
            client_secret=client_secret,
            open_browser=True
        )
        
        print("\n✅ Autenticação OAuth concluída com sucesso!")
        print("📁 Arquivo criado: oauth.json")
        print("\n🎵 Agora você pode usar o script normalmente!")
        print("   O token será renovado automaticamente quando expirar.")
        
    except Exception as e:
        print(f"\n❌ Erro durante autenticação: {e}")
        print("\n💡 Verifique se:")
        print("   1. YouTube Data API v3 está habilitada")
        print("   2. As credenciais são do tipo 'Desktop app'")
        print("   3. Você autorizou o acesso no navegador")
        sys.exit(1)

if __name__ == '__main__':
    setup_oauth()
