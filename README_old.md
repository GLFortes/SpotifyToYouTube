# 🎵 Spotify to YouTube Music Transfer

Script Python para transferir suas playlists do Spotify para o YouTube Music automaticamente.

## 📋 Funcionalidades

- ✅ Lista todas as suas playlists do Spotify
- ✅ Busca automaticamente as músicas no YouTube Music
- ✅ Cria playlists no YouTube Music
- ✅ Transfere músicas individuais ou todas as playlists de uma vez
- ✅ Interface interativa via linha de comando
- ✅ Relatório de progresso em tempo real

## 🔧 Pré-requisitos

### Sistema
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Instalação do Python e pip (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

## 🚀 Instalação

### 1. Clone ou baixe o projeto

```bash
cd "Spotify to Youtube"
```

### 2. (Opcional) Crie um ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 3. Instale as dependências

```bash
pip3 install -r requirements.txt
```

## 🔑 Configuração das APIs

### Spotify API

1. Acesse o [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Faça login com sua conta Spotify
3. Clique em "Create an App"
4. Preencha os dados:
   - **App name**: "Spotify to YouTube Transfer" (ou qualquer nome)
   - **App description**: "Transfer playlists to YouTube Music"
   - **Redirect URI**: `http://localhost:8888/callback`
5. Após criar, copie o **Client ID** e **Client Secret**

### YouTube Music API

1. Execute o comando para autenticação:
```bash
ytmusicapi oauth
```

2. Siga as instruções:
   - Um navegador será aberto automaticamente
   - Faça login na sua conta Google
   - Autorize o acesso ao YouTube Music
   - O arquivo `headers_auth.json` será criado automaticamente

### Arquivo .env

1. Copie o arquivo de exemplo:
```bash
cp .env.example .env
```

2. Edite o arquivo `.env` e adicione suas credenciais:
```env
SPOTIFY_CLIENT_ID=seu_client_id_aqui
SPOTIFY_CLIENT_SECRET=seu_client_secret_aqui
SPOTIFY_REDIRECT_URI=http://localhost:8888/callback
```

## 💻 Como Usar

### Executar o script

```bash
python3 spotify_to_youtube.py
```

### Uso Interativo

Ao executar o script, você verá:

1. **Lista de Playlists**: Todas as suas playlists do Spotify numeradas
2. **Opções**:
   - Digite o número da playlist para transferir uma específica
   - Digite `all` para transferir todas as playlists
   - Digite `q` para sair

### Exemplo de Saída

```
============================================================
🎵 Spotify to YouTube Music Transfer Tool
============================================================

📋 Fetching your Spotify playlists...

Found 15 playlists:

  1. My Favorites (142 tracks)
  2. Workout Mix (38 tracks)
  3. Chill Vibes (67 tracks)
  ...

Options:
  - Enter playlist number to transfer
  - Enter 'all' to transfer all playlists
  - Enter 'q' to quit

Your choice: 1

🎵 Transferring playlist: My Favorites
============================================================
📥 Fetching tracks from Spotify...
   Found 142 tracks
📤 Creating YouTube Music playlist...
   Created playlist ID: PLxxxxxxxxxxxxxxx
🔍 Searching for tracks on YouTube Music...
   [1/142] Song Name - Artist Name ✓
   [2/142] Another Song - Another Artist ✓
   ...

➕ Adding 140 tracks to YouTube Music playlist...
✅ Successfully transferred 140/142 tracks!
```

## 📁 Estrutura do Projeto

```
Spotify to Youtube/
├── spotify_to_youtube.py    # Script principal
├── requirements.txt          # Dependências Python
├── .env.example             # Exemplo de configuração
├── .env                     # Suas credenciais (não commitado)
├── .gitignore              # Arquivos ignorados pelo Git
├── headers_auth.json       # Autenticação YouTube (gerado automaticamente)
└── README.md               # Este arquivo
```

## 🔒 Segurança

- ⚠️ **NUNCA** compartilhe seu arquivo `.env` ou `headers_auth.json`
- ⚠️ Estes arquivos contêm credenciais sensíveis
- ✅ O `.gitignore` já está configurado para proteger estes arquivos

## ❗ Problemas Comuns

### "Missing Spotify credentials"
- Verifique se o arquivo `.env` existe e está configurado corretamente
- Confirme que as variáveis `SPOTIFY_CLIENT_ID` e `SPOTIFY_CLIENT_SECRET` estão preenchidas

### "YouTube Music authentication file not found"
- Execute `ytmusicapi oauth` para criar o arquivo de autenticação
- Certifique-se de autorizar o acesso quando solicitado

### "No tracks found on YouTube Music"
- Algumas músicas podem não estar disponíveis no YouTube Music
- Nomes muito específicos ou regionais podem não ser encontrados
- O script busca as 5 primeiras correspondências e escolhe a melhor

### Músicas não encontradas
- O script tenta fazer a melhor correspondência possível
- Músicas muito novas ou exclusivas do Spotify podem não estar no YouTube Music
- Você verá um relatório de quantas músicas foram transferidas com sucesso

## 📝 Notas

- O script respeita os limites de taxa das APIs
- A transferência pode levar algum tempo dependendo do tamanho da playlist
- Músicas não encontradas no YouTube Music serão puladas
- Um relatório detalhado será exibido ao final

## 🤝 Contribuições

Sugestões e melhorias são bem-vindas!

## 📄 Licença

Este projeto é de código aberto para uso pessoal.

---

**Desenvolvido com ❤️ para facilitar a migração de playlists**
