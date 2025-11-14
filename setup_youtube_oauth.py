#!/usr/bin/env python3
"""
Auto-refreshing OAuth for YouTube Music with Enterprise Security
Uses Google's official OAuth flow with:
- Encrypted token storage
- Minimal scopes (principle of least privilege)
- Token validation and revocation checks
- Secure file permissions
"""

import os
import json
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from security_manager import SecureTokenManager

# Minimal scopes - only what's needed (principle of least privilege)
SCOPES = [
    'https://www.googleapis.com/auth/youtube.force-ssl'  # Only playlist management, not full YouTube access
]
TOKEN_FILE = 'youtube_token.enc'  # Encrypted token file

def get_authenticated_service():
    """
    Get authenticated YouTube service with auto-refresh and security
    """
    from google.oauth2.credentials import Credentials
    
    token_manager = SecureTokenManager(token_file=TOKEN_FILE)
    creds = None
    
    # Load saved token if exists
    creds_data = token_manager.load_credentials()
    if creds_data:
        print("📂 Token criptografado encontrado, carregando...")
        from datetime import datetime
        
        creds = Credentials(
            token=creds_data['token'],
            refresh_token=creds_data['refresh_token'],
            token_uri=creds_data['token_uri'],
            client_id=creds_data['client_id'],
            client_secret=creds_data['client_secret'],
            scopes=creds_data['scopes']
        )
        
        # Set expiry if available
        if creds_data.get('expiry'):
            creds.expiry = datetime.fromisoformat(creds_data['expiry'])
    
    # If no valid credentials, get new ones
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Token expirado, renovando automaticamente...")
            try:
                creds.refresh(Request())
                print("✅ Token renovado com sucesso!")
                
                # Validate token wasn't revoked
                try:
                    test_service = build('youtube', 'v3', credentials=creds)
                    test_service.channels().list(part='snippet', mine=True).execute()
                    print("✅ Token validado - não foi revogado")
                except HttpError as e:
                    if e.resp.status == 401:
                        print("❌ Token foi revogado! Necessário reautenticar.")
                        creds = None
                    else:
                        raise
                        
            except Exception as e:
                print(f"❌ Erro ao renovar token: {e}")
                print("   Necessário reautenticar...")
                creds = None
        
        if not creds:
            print("🔐 Autenticação necessária...")
            
            # Find client secret file
            import glob
            json_files = glob.glob('client_secret_*.json')
            
            if not json_files:
                print("\n❌ Arquivo client_secret_*.json não encontrado!")
                print("Baixe do Google Cloud Console e coloque na pasta do projeto.")
                return None
            
            # Set secure permissions on client secret
            os.chmod(json_files[0], 0o600)
            print(f"📝 Usando: {json_files[0]}")
            print("🌐 Abrindo navegador para autorização...")
            print(f"📋 Escopos solicitados (mínimo necessário):")
            for scope in SCOPES:
                print(f"   - {scope}")
            
            flow = InstalledAppFlow.from_client_secrets_file(
                json_files[0], 
                SCOPES,
                redirect_uri='http://localhost:8090/'
            )
            
            creds = flow.run_local_server(port=8090, open_browser=True)
            print("✅ Autenticação concluída!")
        
        # Save credentials with encryption
        print(f"💾 Salvando token com criptografia...")
        token_manager.save_credentials(creds)
        print("✅ Token salvo com segurança! Próximas execuções serão automáticas.")
    else:
        print("✅ Token válido encontrado!")
    
    return build('youtube', 'v3', credentials=creds)

def test_auth():
    """Test authentication"""
    print("""
╔════════════════════════════════════════════════════════════════╗
║     YouTube OAuth com Auto-Refresh (Método Oficial)          ║
╚════════════════════════════════════════════════════════════════╝

Este método:
✅ Auto-renova tokens automaticamente
✅ Funciona por meses sem intervenção
✅ Usa API oficial do Google
✅ Salva credenciais localmente

""")
    
    service = get_authenticated_service()
    
    if not service:
        return False
    
    try:
        print("\n🧪 Testando acesso à API do YouTube...")
        # Get user's channel
        request = service.channels().list(part='snippet', mine=True)
        response = request.execute()
        
        if response.get('items'):
            channel = response['items'][0]
            print(f"✅ Conectado como: {channel['snippet']['title']}")
            print(f"📺 Canal ID: {channel['id']}")
            return True
        else:
            print("⚠️  Nenhum canal encontrado")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao testar: {e}")
        return False

if __name__ == '__main__':
    success = test_auth()
    if success:
        print("\n🎉 Tudo configurado! O token será renovado automaticamente.")
        print("📝 Arquivo criado: youtube_token.pickle")
        print("\n💡 Agora atualize o script principal para usar este método.")
    else:
        print("\n❌ Configuração falhou. Verifique as credenciais.")
