#!/usr/bin/env python3
"""Alternative setup for YouTube Music using browser headers"""

print("""
╔═══════════════════════════════════════════════════════════════╗
║     YouTube Music - Autenticação Alternativa (Mais Simples)  ║
╚═══════════════════════════════════════════════════════════════╝

O método OAuth está apresentando problemas. Vamos usar o método de headers
que é mais simples e confiável.

PASSO A PASSO:

1. Abra o YouTube Music no seu navegador (Chrome/Firefox)
   → https://music.youtube.com

2. Faça login na sua conta

3. Pressione F12 para abrir o DevTools

4. Vá na aba "Network" (Rede)

5. Na página do YouTube Music, clique em qualquer playlist sua

6. No DevTools, procure por uma requisição que comece com "browse"
   (pode filtrar digitando "browse" no campo de busca)

7. Clique nessa requisição "browse"

8. No painel direito, vá na aba "Headers" (Cabeçalhos)

9. Role até encontrar "Request Headers" (Cabeçalhos da requisição)

10. Copie TODO o conteúdo dos Request Headers

11. Cole abaixo quando solicitado

══════════════════════════════════════════════════════════════════

Pressione ENTER quando estiver pronto para colar os headers...
""")

input()

print("\nCole os Request Headers completos aqui e pressione ENTER duas vezes:")
print("(Cole tudo que estiver em Request Headers, incluindo Cookie, etc)\n")

headers_lines = []
while True:
    try:
        line = input()
        if line.strip() == "" and headers_lines:
            break
        if line.strip():
            headers_lines.append(line)
    except EOFError:
        break

if not headers_lines:
    print("❌ Nenhum header fornecido!")
    exit(1)

# Parse headers
headers_dict = {}
for line in headers_lines:
    if ':' in line:
        key, value = line.split(':', 1)
        headers_dict[key.strip()] = value.strip()

# Save to headers_auth.json in ytmusicapi format
import json

ytmusic_headers = {
    "User-Agent": headers_dict.get("User-Agent", ""),
    "Accept": "*/*",
    "Accept-Language": headers_dict.get("Accept-Language", "en-US,en;q=0.5"),
    "Content-Type": "application/json",
    "X-Goog-AuthUser": "0",
    "x-origin": "https://music.youtube.com",
    "Cookie": headers_dict.get("Cookie", "")
}

# Filter out empty values
ytmusic_headers = {k: v for k, v in ytmusic_headers.items() if v}

with open('headers_auth.json', 'w') as f:
    json.dump(ytmusic_headers, f, indent=2)

print("\n✅ Arquivo headers_auth.json criado com sucesso!")
print("🎵 Agora você pode executar: python3 spotify_to_youtube.py")
