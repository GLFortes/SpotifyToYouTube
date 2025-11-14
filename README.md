# 🎵 Spotify to YouTube Music Transfer

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Security](https://img.shields.io/badge/Security-Enterprise%20Grade-brightgreen.svg)](SECURITY.md)

> 🚀 Transfira suas playlists do Spotify para o YouTube Music de forma automatizada, inteligente e **segura**!

## ✨ Funcionalidades

- 🎼 Lista todas as suas playlists do Spotify
- 🔍 Busca automaticamente músicas no YouTube Music
- ➕ Cria playlists no YouTube Music com OAuth2
- 🔒 **Tokens criptografados com AES-128** (Enterprise-grade security)
- 🔄 **Auto-refresh de tokens** (funciona por meses sem relogar)
- 🔐 **Integração com OS keyring** (chaves protegidas pelo sistema)
- 🛡️ **Escopos OAuth mínimos** (princípio do menor privilégio)
- 📊 Relatório detalhado de progresso
- 🎯 100% via linha de comando

---

## 🔒 Segurança Enterprise-Grade

Este projeto implementa segurança de nível corporativo:

✅ **Criptografia de tokens** (AES-128 via Fernet)  
✅ **Keyring do sistema operacional** (chaves protegidas)  
✅ **Validação de revogação de tokens**  
✅ **Permissões seguras** (chmod 600 em arquivos sensíveis)  
✅ **Escopos OAuth mínimos** (youtube.force-ssl apenas)  
✅ **Auditoria de segurança integrada**

📖 **Leia mais:** [SECURITY.md](SECURITY.md)

---

## 📋 Pré-requisitos

### 🐍 Python
- **Python 3.8+** instalado
- **pip** (gerenciador de pacotes)
- **venv** (ambiente virtual)

### 💻 Sistema Operacional
- ✅ Linux (testado no Ubuntu/Debian)
- ✅ macOS
- ✅ Windows

---

## 🛠️ Setup do Ambiente

### 1️⃣ Instalar Dependências do Sistema

#### 🐧 Ubuntu/Debian
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

#### 🍎 macOS
```bash
brew install python3
```

#### 🪟 Windows
Baixe Python em: https://www.python.org/downloads/

---

### 2️⃣ Clonar/Baixar o Projeto

```bash
cd ~/Documents
# Se baixou em ZIP, extraia aqui
cd "Spotify to Youtube"
```

---

### 3️⃣ Criar Ambiente Virtual

```bash
# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual
source venv/bin/activate  # Linux/macOS
# ou
venv\Scripts\activate     # Windows
```

💡 **Dica:** Você verá `(venv)` no início do prompt quando ativado!

---

### 4️⃣ Instalar Dependências Python

```bash
pip install -r requirements.txt
```

📦 **Pacotes instalados:**
- `spotipy` - Cliente Spotify API
- `ytmusicapi` - Cliente YouTube Music API
- `python-dotenv` - Gerenciamento de variáveis de ambiente
- `google-auth` - Autenticação Google

---

## 🔐 Configuração das APIs

### 🎧 Spotify API

#### Passo 1: Criar Aplicação
1. Acesse: [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Faça login na sua conta Spotify
3. Clique em **"Create app"**

#### Passo 2: Configurar Aplicação
- **App name:** `Spotify to YouTube Transfer`
- **App description:** `Transfer playlists to YouTube Music`
- **Redirect URI:** `http://localhost:8080/callback` ⚠️ **IMPORTANTE!**
- **APIs/SDKs:** Selecione **Web API**

#### Passo 3: Obter Credenciais
1. Após criar, copie o **Client ID**
2. Clique em **"Show Client Secret"** e copie
3. Guarde essas informações para o próximo passo

---

### 🎬 YouTube Music API (OAuth2)

#### Método Recomendado: OAuth com Auto-Refresh ✅ **SEGURO**

Este método usa autenticação oficial do Google com renovação automática de tokens:

**Passo 1: Criar Projeto no Google Cloud Console**

1. Acesse: [Google Cloud Console](https://console.cloud.google.com/)
2. Clique em **"Novo Projeto"**
3. Nome: `spotify-to-youtube` (ou qualquer nome)
4. Clique em **"Criar"**

**Passo 2: Ativar YouTube Data API v3**

1. No menu lateral, vá em **"APIs e Serviços"** → **"Biblioteca"**
2. Busque por **"YouTube Data API v3"**
3. Clique nela e depois em **"Ativar"**

**Passo 3: Configurar Tela de Consentimento OAuth**

1. No menu lateral, **"APIs e Serviços"** → **"Tela de consentimento OAuth"**
2. Selecione **"External"** (Externo) → **"Criar"**
3. Preencha:
   - **Nome do app:** `Spotify to YouTube Transfer`
   - **E-mail de suporte:** seu email
   - **E-mail do desenvolvedor:** seu email
4. Clique em **"Salvar e Continuar"**
5. Em **"Escopos"**, clique em **"Salvar e Continuar"** (sem adicionar nada)
6. Em **"Público-alvo"** (ou "Audience"):
   - ⚠️ **IMPORTANTE:** Adicione seu e-mail aqui
   - Clique em **"+ ADICIONAR USUÁRIOS"**
   - Digite seu email do Google
   - Clique em **"Adicionar"**
7. Clique em **"Salvar e Continuar"**

**Passo 4: Criar Credenciais OAuth**

1. No menu lateral, **"APIs e Serviços"** → **"Credenciais"**
2. Clique em **"+ Criar Credenciais"** → **"ID do cliente OAuth 2.0"**
3. Tipo: **"Aplicativo para computador"**
4. Nome: `Spotify to YouTube Desktop`
5. Clique em **"Criar"**
6. **Baixe o arquivo JSON** das credenciais
7. Renomeie para `client_secret_XXXXX.json` (mantenha o nome original)
8. Coloque na pasta do projeto

**Passo 5: Configurar Redirect URIs**

1. Clique no cliente OAuth que você criou
2. Em **"URIs de redirecionamento autorizados"**, adicione:
   ```
   http://localhost:8090/
   ```
3. Clique em **"Salvar"**

**Passo 6: Executar Setup OAuth**

```bash
python3 setup_youtube_oauth.py
```

✅ Isso vai:
- Abrir navegador para autorização
- Salvar token criptografado
- Token renova automaticamente (nunca expira!)

#### Método Alternativo: Headers do Navegador (Menos Seguro)

Se preferir não configurar OAuth:

1. **Abra o YouTube Music:** https://music.youtube.com
2. **Faça login** na sua conta
3. **Pressione F12** para abrir DevTools
4. **Vá na aba "Network"** (Rede)
5. **Clique em qualquer playlist** sua no YouTube Music
6. **No DevTools**, procure por requisição **"browse"**
7. **Clique nela** → Aba **"Headers"** → Role até **"Request Headers"**
8. **Copie TODO o conteúdo** dos Request Headers
9. **Execute:**
   ```bash
   python3 setup_youtube_headers.py
   ```
10. **Cole os headers** quando solicitado

⚠️ **Desvantagens:**
- Headers expiram após algumas semanas
- Precisa reconfigurar manualmente
- Menos seguro (cookies em plaintext)

**💡 Recomendação:** Use OAuth para segurança e conveniência!

---

### 5️⃣ Configurar Variáveis de Ambiente

```bash
# Copiar arquivo de exemplo
cp .env.example .env

# Editar com suas credenciais
nano .env  # ou use seu editor favorito
```

**Conteúdo do arquivo `.env`:**
```env
SPOTIFY_CLIENT_ID=seu_client_id_aqui
SPOTIFY_CLIENT_SECRET=seu_client_secret_aqui
SPOTIFY_REDIRECT_URI=http://localhost:8080/callback
```

---

## 🚀 Como Usar

### ▶️ Primeira Execução

```bash
# 1. Ativar ambiente virtual
source venv/bin/activate

# 2. Configurar YouTube OAuth (uma vez)
python3 setup_youtube_oauth.py

# 3. Executar transferência
python3 spotify_to_youtube.py
```

### 🔄 Execuções Subsequentes

```bash
# Apenas execute (token renova automaticamente!)
source venv/bin/activate
python3 spotify_to_youtube.py
```

### 🔐 Auditoria de Segurança

```bash
# Verificar status de segurança do projeto
python3 security_manager.py
```

---

## 📝 Estrutura do Projeto

```
Spotify to Youtube/
├── 📄 spotify_to_youtube.py      # Script principal de transferência
├── 📄 continue_transfer.py       # Continuar transferência parcial
├── 📄 setup_youtube_oauth.py     # Setup OAuth com criptografia
├── 📄 setup_youtube_headers.py   # Setup alternativo (headers)
├── 🔒 security_manager.py        # Módulo de segurança enterprise
├── 📦 requirements.txt           # Dependências Python
├── 🔐 .env                       # Credenciais Spotify (NÃO commitar!)
├── 🔐 .env.example               # Template de configuração
├── 🔐 youtube_token.enc          # Token OAuth criptografado (gerado)
├── 🔐 client_secret_*.json       # Credenciais Google (NÃO commitar!)
├── 🚫 .gitignore                 # Arquivos ignorados
├── 📖 README.md                  # Este arquivo
└── 📖 SECURITY.md                # Documentação de segurança
```

---

## 🎮 Fluxo de Uso

```
📋 Listar Playlists Spotify
    ↓
🎯 Escolher Playlist
    ↓
🔍 Buscar Músicas no YouTube
    ↓
➕ Criar Playlist
    ↓
🎵 Adicionar Músicas
    ↓
✅ Concluído!
```

---

## 🐛 Troubleshooting

### ❌ "Token criptografado não encontrado"
**Solução:** Execute `python3 setup_youtube_oauth.py` para configurar OAuth

### ❌ "Access blocked: has not completed Google verification process"
**Solução:** Adicione seu email em **"Público-alvo"** (Audience) no Google Cloud Console OAuth consent screen

### ❌ "INVALID_CLIENT: Insecure redirect URI"
**Solução:** Use `http://localhost:8080/callback` (não `https`) no Spotify Dashboard

### ❌ "Address already in use" (porta 8080)
**Solução:** A porta está ocupada. Mude para 8081 no `.env` e no Spotify Dashboard

### ❌ "Address already in use" (porta 8090)
**Solução:** 
```bash
# Matar processo na porta 8090
lsof -ti:8090 | xargs kill -9
```

### ❌ "Keyring não disponível"
**Solução:** O sistema vai usar fallback com senha. Digite uma senha quando solicitado.

### ❌ Token foi revogado
**Solução:** Execute `python3 setup_youtube_oauth.py` novamente para reautenticar

---

## 🔒 Segurança

### ✅ Implementações de Segurança

Este projeto implementa segurança enterprise-grade:

1. **Criptografia AES-128** - Todos os tokens são criptografados
2. **OS Keyring** - Chaves armazenadas no keyring do sistema
3. **OAuth2 com Auto-Refresh** - Tokens renovam automaticamente
4. **Escopos Mínimos** - Apenas permissões necessárias (youtube.force-ssl)
5. **Permissões 600** - Arquivos sensíveis protegidos
6. **Validação de Revogação** - Detecta tokens revogados

### ⚠️ NUNCA compartilhe:
- ❌ Arquivo `.env`
- ❌ Arquivo `youtube_token.enc`
- ❌ Arquivo `client_secret_*.json`
- ❌ Client Secret do Spotify

### ✅ Proteção Automática
O `.gitignore` já protege todos estes arquivos automaticamente!

### 📋 Auditoria
Execute `python3 security_manager.py` para verificar o status de segurança.

📖 **Documentação completa:** [SECURITY.md](SECURITY.md)

---

## 💡 Dicas

- 🔄 **Playlists grandes:** Use `continue_transfer.py` se houver timeout
- 🎯 **Teste primeiro:** Comece com uma playlist pequena
- ⏱️ **Seja paciente:** Músicas são adicionadas uma por vez (mais confiável)
- 🔍 **Músicas não encontradas:** Algumas podem não estar no YouTube Music
- 📱 **Refresh:** Atualize o YouTube Music no celular para ver as playlists

---

## 📊 Exemplo de Saída

```
============================================================
🎵 Spotify to YouTube Music Transfer Tool
============================================================

📋 Fetching your Spotify playlists...

Found 12 playlists:
  1. My Favorites (142 tracks)
  2. Workout Mix (38 tracks)
  3. Chill Vibes (67 tracks)

Your choice: 1

🎵 Transferring playlist: My Favorites
============================================================
📥 Fetching tracks from Spotify...
   Found 142 tracks
📤 Creating YouTube Music playlist...
   Created playlist ID: PLxxx
🔍 Searching for tracks on YouTube Music...
   [1/142] Song Name - Artist ✓
   [2/142] Another Song - Artist ✓
   Progress: 10/142 tracks added...
   ...
➕ Adding tracks to YouTube Music playlist...
✅ Successfully added 140/142 tracks to the playlist!
```

---

## 🤝 Contribuindo

Encontrou um bug ou tem uma sugestão? Sinta-se à vontade para:
- 🐛 Reportar issues
- 💡 Sugerir melhorias
- 🔧 Enviar pull requests

---

## 📜 Licença

Este projeto é de código aberto para uso pessoal.

---

## 👨‍💻 Autor

Criado com ❤️ para facilitar a migração de playlists do Spotify para YouTube Music.

---

## 🙏 Agradecimentos

- [Spotipy](https://github.com/plamere/spotipy) - Excelente wrapper para Spotify API
- [ytmusicapi](https://github.com/sigma67/ytmusicapi) - API não oficial para YouTube Music
- Comunidade open source! 🌟

---

**🎵 Boas transferências!**
