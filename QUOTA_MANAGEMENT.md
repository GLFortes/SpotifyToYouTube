# 📊 YouTube API Quota Management

## 🎯 Entendendo a Cota do YouTube

A YouTube Data API v3 tem um limite de **10.000 units por dia**. Cada operação consome uma quantidade diferente:

### Custos por Operação:
- 🔍 **search()**: 100 units
- ➕ **playlist.insert()** (criar): 50 units
- 📝 **playlistItems.insert()** (adicionar música): 50 units

### Exemplo Prático:
Para uma playlist com **100 músicas**:
- Buscar 100 músicas: 100 × 100 = **10.000 units** ❌
- Criar 1 playlist: **50 units**
- Adicionar 100 músicas: 100 × 50 = **5.000 units**
- **TOTAL: 15.050 units** (150% do limite diário!)

---

## ✅ Otimizações Implementadas

### 1️⃣ **Cache de Buscas** 
Se você buscar a mesma música duas vezes, ela vem do cache (0 units na 2ª vez).

```python
# Antes: Buscar "Bohemian Rhapsody" = 100 units
# Depois: Primeira vez = 100 units, segunda vez = 0 units
```

### 2️⃣ **Limite de Resultados Reduzido**
Mudamos de `limit=5` para `limit=1` na busca (pega só o melhor resultado).

### 3️⃣ **Estimativa Automática de Cota**
Antes de iniciar, o programa mostra:
```
📊 Estimated YouTube API Quota Usage:
   Search: 10,000 units (100 tracks × 100)
   Create playlist: 50 units
   Add tracks: 5,000 units (100 tracks × 50)
   ─────────────────────────
   TOTAL: 15,050 units (150.5% of daily limit)
   ⚠️  WARNING: Exceeds daily quota limit!
   💡 Recommendation: Transfer max 66 tracks per day
```

### 4️⃣ **Proteção Automática**
Se ultrapassar a cota, o programa pergunta:
```
Limit to 66 tracks? (s/n):
```

### 5️⃣ **Progress em Batches**
Mostra progresso a cada 50 músicas (não a cada 10).

---

## 🎓 Cálculo de Limite Seguro

**Fórmula:**
```
max_tracks = (10.000 - 50) / 150
max_tracks = 9.950 / 150
max_tracks = 66 músicas por dia
```

Onde:
- 10.000 = limite diário
- 50 = criar playlist
- 150 = buscar (100) + adicionar (50) por música

---

## 💡 Estratégias para Playlists Grandes

### Opção 1: Dividir em Múltiplos Dias
Playlist com 200 músicas:
- **Dia 1**: 66 músicas (9.900 units)
- **Dia 2**: 66 músicas (9.900 units)
- **Dia 3**: 68 músicas (10.200 units - ligeiramente acima)

### Opção 2: Criar Várias Playlists Menores
```bash
# Transferir em partes
python3 spotify_to_youtube.py  # Selecionar "limitar a 66"
# Esperar 24h
python3 continue_transfer.py   # Continuar de onde parou
```

### Opção 3: Usar o Script `continue_transfer.py`
Este script detecta músicas já adicionadas e pula elas (economiza cota).

---

## 🔧 Comandos Úteis

### Ver Estimativa Antes de Transferir
O programa mostra automaticamente antes de iniciar.

### Transferir com Limite Manual
```python
# No código, adicione:
transferer.transfer_playlist(playlist_id, name, max_tracks=50)
```

### Verificar Cota Restante
Visite: https://console.cloud.google.com/apis/api/youtube.googleapis.com/quotas

---

## ❓ FAQ

**P: Por que não fazer batch add (adicionar várias de uma vez)?**
R: A YouTube Music API não suporta batch insert para playlistItems. Cada música = 1 chamada = 50 units.

**P: Posso aumentar meu limite de cota?**
R: Sim! Você pode solicitar aumento em: https://support.google.com/youtube/contact/yt_api_form

**P: E se eu já estourei a cota hoje?**
R: Aguarde até 00:00 UTC (20:00 BRT) quando o contador reseta.

**P: Headers method usa cota?**
R: Não! Headers extraídos do navegador não contam na cota oficial, mas podem expirar.

---

## 🎯 Recomendações

✅ **DO:**
- Use o estimador de cota antes de transferir
- Transfira playlists grandes em múltiplos dias
- Use `continue_transfer.py` para retomar
- Considere headers method para playlists muito grandes (menos seguro)

❌ **DON'T:**
- Não tente transferir 200+ músicas de uma vez
- Não ignore os avisos de cota
- Não crie múltiplas contas só pra ter mais cota (viola ToS)

---

## 📈 Comparação Antes vs Depois

### Antes das Otimizações:
- ❌ Sem estimativa de cota
- ❌ Sem cache de buscas
- ❌ Sem proteção contra estouro
- ❌ limit=5 nas buscas (desnecessário)

### Depois das Otimizações:
- ✅ Estimativa automática
- ✅ Cache de buscas repetidas
- ✅ Proteção automática com sugestão
- ✅ limit=1 (mais eficiente)
- ✅ Progress em batches
- ✅ Relatório de cota usada no final

**Economia estimada: ~10-15% em playlists com músicas repetidas**

---

**Dúvidas?** Abra uma issue no GitHub!
