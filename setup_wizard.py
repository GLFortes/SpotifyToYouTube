#!/usr/bin/env python3
"""
🎵 Spotify to YouTube Music - Setup Wizard
Interactive setup guide in Portuguese
"""

import os
import sys
import subprocess
import json
import platform
import webbrowser
from pathlib import Path
from typing import Dict, Tuple
import time


class SetupWizard:
    def __init__(self):
        self.os_type = platform.system()
        self.project_dir = Path(__file__).parent
        self.env_file = self.project_dir / ".env"
        self.venv_dir = self.project_dir / "venv"
        self.python_cmd = self._get_python_cmd()
        
    def _get_python_cmd(self) -> str:
        """Detect correct Python command"""
        for cmd in ['python3', 'python']:
            try:
                subprocess.run([cmd, '--version'], capture_output=True, check=True)
                return cmd
            except:
                continue
        return None
    
    def print_header(self, title: str):
        """Print formatted header"""
        print(f"\n{'='*60}")
        print(f"  {title}")
        print(f"{'='*60}\n")
    
    def print_step(self, number: int, title: str, emoji: str = ""):
        """Print step header"""
        print(f"\n{emoji} [{number}] {title}")
        print(f"{'-'*50}")
    
    def print_success(self, msg: str):
        """Print success message"""
        print(f"✅ {msg}")
    
    def print_error(self, msg: str):
        """Print error message"""
        print(f"❌ {msg}")
    
    def print_info(self, msg: str):
        """Print info message"""
        print(f"ℹ️  {msg}")
    
    def print_warning(self, msg: str):
        """Print warning message"""
        print(f"⚠️  {msg}")
    
    def ask_yes_no(self, question: str, default: bool = True) -> bool:
        """Ask yes/no question"""
        default_str = "S/n" if default else "s/N"
        while True:
            try:
                print(f"\n❓ {question} [{default_str}]: ", end='', flush=True)
                response = input().strip().lower()
                
                if response == '':
                    return default
                if response in ['s', 'sim', 'yes', 'y']:
                    return True
                if response in ['n', 'não', 'no']:
                    return False
                print("⚠️  Digite 's' ou 'n' por favor")
            except EOFError:
                return default
    
    def ask_input(self, prompt: str, default: str = None) -> str:
        """Ask for user input"""
        if default:
            prompt += f" [{default}]"
        try:
            print(f"\n📝 {prompt}: ", end='', flush=True)
            response = input().strip()
            return response if response else default
        except EOFError:
            return default
    
    def check_python(self) -> bool:
        """Check Python version"""
        self.print_step(1, "Verificando Python", "🐍")
        
        if not self.python_cmd:
            self.print_error("Python 3 não encontrado!")
            self.print_info(f"Sistema operacional: {self.os_type}")
            
            if self.os_type == "Linux":
                self.print_info("Execute: sudo apt install python3 python3-pip python3-venv")
            elif self.os_type == "Darwin":  # macOS
                self.print_info("Execute: brew install python3")
            elif self.os_type == "Windows":
                self.print_info("Baixe em: https://www.python.org/downloads/")
            
            return False
        
        result = subprocess.run([self.python_cmd, '--version'], capture_output=True, text=True)
        version = result.stdout.strip()
        self.print_success(f"{version} encontrado!")
        return True
    
    def setup_venv(self) -> bool:
        """Setup virtual environment"""
        self.print_step(2, "Configurando Ambiente Virtual", "🔧")
        
        if self.venv_dir.exists():
            self.print_info("Ambiente virtual já existe!")
            if not self.ask_yes_no("Deseja recriá-lo?"):
                return True
            
            print("🗑️  Removendo ambiente anterior...")
            subprocess.run(['rm', '-rf', str(self.venv_dir)], check=True)
        
        print("📦 Criando ambiente virtual...")
        result = subprocess.run(
            [self.python_cmd, '-m', 'venv', str(self.venv_dir)],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            self.print_error(f"Erro ao criar venv: {result.stderr}")
            return False
        
        self.print_success("Ambiente virtual criado!")
        
        # Install requirements
        print("\n📥 Instalando dependências Python...")
        requirements_file = self.project_dir / "requirements.txt"
        
        if self.os_type == "Windows":
            pip_cmd = str(self.venv_dir / "Scripts" / "pip")
        else:
            pip_cmd = str(self.venv_dir / "bin" / "pip")
        
        result = subprocess.run(
            [pip_cmd, 'install', '-r', str(requirements_file)],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            self.print_error(f"Erro ao instalar dependências: {result.stderr}")
            return False
        
        self.print_success("Dependências instaladas!")
        return True
    
    def setup_spotify(self) -> Dict[str, str]:
        """Setup Spotify API credentials"""
        self.print_step(3, "Configurando Spotify API", "🎵")
        
        self.print_info("Você precisa criar uma aplicação no Spotify Developer Dashboard")
        print("\n📋 Siga estes passos:")
        print("1. Acesse: https://developer.spotify.com/dashboard")
        print("2. Faça login (ou crie conta grátis)")
        print("3. Clique em 'Create an App'")
        print("4. Aceite os termos e crie")
        print("5. Você receberá Client ID e Client Secret")
        
        print("\n⚙️  Configuração da Aplicação:")
        print("- App Name: 'Spotify to YouTube Music'")
        print("- Redirect URI: http://127.0.0.1:8080/callback")
        print("  (Configure isto em Settings → Redirect URIs)")
        
        if self.ask_yes_no("\n✅ Você já criou a aplicação no Spotify?"):
            client_id = self.ask_input("Client ID")
            client_secret = self.ask_input("Client Secret")
            
            if client_id and client_secret:
                self.print_success("Credenciais do Spotify salvas!")
                return {
                    'SPOTIFY_CLIENT_ID': client_id,
                    'SPOTIFY_CLIENT_SECRET': client_secret,
                    'SPOTIFY_REDIRECT_URI': 'http://127.0.0.1:8080/callback'
                }
        
        self.print_warning("Configure o Spotify depois e execute novamente")
        return {}
    
    def setup_youtube(self) -> Dict[str, str]:
        """Setup YouTube OAuth"""
        self.print_step(4, "Configurando YouTube Music OAuth", "📹")
        
        self.print_info("Você precisa criar credenciais OAuth no Google Cloud")
        print("\n📋 Siga estes passos:")
        print("1. Acesse: https://console.cloud.google.com")
        print("2. Crie um novo projeto: 'Spotify to YouTube Music'")
        print("3. Ative a API do YouTube Data API v3")
        print("4. Crie credenciais OAuth 2.0 (Desktop)")
        print("5. Baixe o arquivo JSON")
        
        print("\n⚙️  Configuração da Aplicação:")
        print("- Tipo: Desktop Application")
        print("- Redirect URI: http://localhost")
        print("  (Configure isto em OAuth Consent Screen → Authorized redirect URIs)")
        
        if self.ask_yes_no("\n✅ Você já criou as credenciais OAuth no Google?"):
            json_path = self.ask_input("Caminho para o arquivo client_secret_*.json")
            
            if json_path and os.path.exists(json_path):
                # Copy to project
                import shutil
                dest = self.project_dir / os.path.basename(json_path)
                shutil.copy(json_path, dest)
                self.print_success(f"Arquivo copiado para: {dest}")
                
                if self.ask_yes_no("Deseja fazer a autenticação YouTube agora?"):
                    print("\n🌐 Abrindo navegador para autenticação...")
                    print("⏳ Aguarde (pode levar alguns segundos)...")
                    
                    # Run setup_youtube_oauth.py
                    setup_script = self.project_dir / "setup_youtube_oauth.py"
                    if setup_script.exists():
                        result = subprocess.run(
                            [self.python_cmd, str(setup_script)],
                            cwd=str(self.project_dir),
                            capture_output=False
                        )
                        if result.returncode == 0:
                            self.print_success("YouTube OAuth configurado!")
                            return {'YOUTUBE_OAUTH': 'configurado'}
                        else:
                            self.print_error("Erro na autenticação YouTube")
                            return {}
                
                return {}
        
        self.print_warning("Configure o YouTube depois e execute novamente")
        return {}
    
    def save_env(self, config: Dict[str, str]) -> bool:
        """Save .env file"""
        self.print_step(5, "Salvando Configuração", "💾")
        
        env_content = """# Spotify API Credentials
SPOTIFY_CLIENT_ID={spotify_id}
SPOTIFY_CLIENT_SECRET={spotify_secret}
SPOTIFY_REDIRECT_URI=http://127.0.0.1:8080/callback

# YouTube Music Authentication
# Configure com: python3 setup_youtube_oauth.py
""".format(
            spotify_id=config.get('SPOTIFY_CLIENT_ID', 'seu_client_id'),
            spotify_secret=config.get('SPOTIFY_CLIENT_SECRET', 'seu_client_secret')
        )
        
        try:
            self.env_file.write_text(env_content)
            # Protect file permissions
            os.chmod(self.env_file, 0o600)
            self.print_success(f".env criado em: {self.env_file}")
            return True
        except Exception as e:
            self.print_error(f"Erro ao salvar .env: {e}")
            return False
    
    def test_spotify(self) -> bool:
        """Test Spotify connection"""
        self.print_step(6, "Testando Spotify", "🧪")
        
        if not self.env_file.exists():
            self.print_warning("Arquivo .env não encontrado")
            return False
        
        try:
            import spotipy
            from spotipy.oauth2 import SpotifyOAuth
            from dotenv import load_dotenv
            
            load_dotenv(self.env_file)
            
            auth = SpotifyOAuth(
                client_id=os.getenv('SPOTIFY_CLIENT_ID'),
                client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
                redirect_uri=os.getenv('SPOTIFY_REDIRECT_URI')
            )
            
            # Test with client credentials flow (no user interaction)
            sp = spotipy.Spotify(auth_manager=auth)
            sp.current_user()
            
            self.print_success("Spotify conectado com sucesso!")
            return True
        except Exception as e:
            self.print_warning(f"Teste do Spotify: {e}")
            self.print_info("Configure as credenciais corretas no .env")
            return False
    
    def print_final_instructions(self):
        """Print final instructions"""
        self.print_header("🎉 Setup Completo!")
        
        print("""
Para iniciar a transferência de playlists:

1️⃣  Ative o ambiente virtual:
""")
        
        if self.os_type == "Windows":
            print("    venv\\Scripts\\activate")
        else:
            print("    source venv/bin/activate")
        
        print("""
2️⃣  Execute o script principal:
    
    python3 spotify_to_youtube.py

3️⃣  Escolha a playlist e deixe a magia acontecer! ✨

📚 Documentação completa: README.md
🔒 Detalhes de segurança: SECURITY.md
        """)
    
    def run(self):
        """Run the complete wizard"""
        self.print_header("🎵 Spotify to YouTube Music - Setup Wizard")
        print("""
Este wizard irá guiá-lo pelo setup da aplicação.

O que você vai fazer:
✓ Configurar ambiente Python
✓ Adicionar credenciais do Spotify
✓ Adicionar credenciais do YouTube
✓ Testar a conexão
✓ Tudo em menos de 5 minutos!
        """)
        
        if not self.ask_yes_no("Deseja continuar?"):
            print("\n👋 Até logo!")
            sys.exit(0)
        
        # Step 1: Check Python
        if not self.check_python():
            self.print_error("Python 3 é obrigatório!")
            sys.exit(1)
        
        # Step 2: Setup venv
        if not self.setup_venv():
            self.print_error("Erro ao configurar ambiente virtual")
            sys.exit(1)
        
        # Step 3: Spotify setup
        spotify_config = self.setup_spotify()
        
        # Step 4: YouTube setup
        youtube_config = self.setup_youtube()
        
        # Combine configs
        all_config = {**spotify_config, **youtube_config}
        
        # Step 5: Save .env
        if all_config:
            if self.save_env(all_config):
                # Step 6: Test Spotify
                self.test_spotify()
        
        # Final instructions
        self.print_final_instructions()
        
        print("\n✨ Setup finalizado com sucesso!")
        print("🚀 Próximo passo: python3 spotify_to_youtube.py\n")


if __name__ == '__main__':
    try:
        wizard = SetupWizard()
        wizard.run()
    except KeyboardInterrupt:
        print("\n\n👋 Setup cancelado pelo usuário")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
