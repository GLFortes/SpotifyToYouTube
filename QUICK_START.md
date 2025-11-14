# ⚡ Quick Start - Começar Agora

Se você quer começar rapidinho, sem ler tudo:

## 1️⃣ Clone ou baixe o projeto

```bash
cd ~/Documents
git clone https://github.com/GLFortes/SpotifyToYouTube.git
# ou extraia o ZIP se baixou
cd SpotifyToYouTube
```

## 2️⃣ Execute o wizard (tudo automático!)

```bash
python3 setup_wizard.py
```

Ele vai:
- ✅ Verificar Python
- ✅ Criar ambiente virtual
- ✅ Instalar dependências
- ✅ Pedir credenciais do Spotify e YouTube
- ✅ Testar tudo automaticamente

## 3️⃣ Transferir sua playlist

```bash
# Ative o ambiente virtual
source venv/bin/activate  # Linux/macOS
# ou
venv\Scripts\activate     # Windows

# Execute a transferência
python3 spotify_to_youtube.py
```

Escolha sua playlist e deixa rodar! 🚀

---

## ❓ Preciso criar credenciais?

Sim, mas é super fácil (5 minutos):

### Spotify (gratuito)
1. https://developer.spotify.com/dashboard
2. Clique "Create an App"
3. Copie: **Client ID** e **Client Secret**

### YouTube (gratuito)
1. https://console.cloud.google.com
2. Crie projeto novo
3. Ative "YouTube Data API v3"
4. Crie credencial OAuth
5. Baixe arquivo JSON

O wizard pede essas informações e configura tudo! 🎉

---

## 🆘 Problema?

- **Python não encontrado?** → [Instale Python 3](https://www.python.org/downloads/)
- **Credenciais não funcionam?** → Veja [README.md](README.md) seção "Troubleshooting"
- **Precisa de mais info?** → Leia [README.md](README.md) completo

---

**É isso! Boa sorte! 🎵**
