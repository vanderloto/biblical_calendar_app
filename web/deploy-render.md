# Deploy no Render.com - Biblical Calendar Web

Este guia detalha como fazer o deploy da aplicação web no Render.com.

## 🌐 Sobre o Render.com

O Render.com é uma plataforma de cloud moderna que oferece:
- **Deploy automático** a partir do GitHub
- **Tier gratuito** com 750 horas/mês
- **HTTPS automático** com certificados SSL
- **Builds automáticos** com Docker
- **Logs em tempo real**

---

## 🚀 Processo de Deploy

### 1. Preparação do Repositório

#### Estrutura Necessária
```
biblical_calendar_app/
├── web/
│   ├── Dockerfile          # Build unificado
│   ├── render.yaml         # Configuração Render
│   ├── server.py           # Servidor unificado
│   ├── backend/            # API Flask
│   ├── frontend/           # App Vue.js
│   └── .dockerignore       # Otimização build
└── src/                    # Código fonte compartilhado
```

#### Arquivos Criados para Render
- ✅ `Dockerfile` - Build multi-stage (frontend + backend)
- ✅ `render.yaml` - Configuração de serviço
- ✅ `server.py` - Servidor Flask unificado
- ✅ `.dockerignore` - Otimização de build
- ✅ `.env.production` - Variáveis de ambiente

### 2. Deploy Manual

#### Opção A: Via Dashboard Render

1. **Acesse**: [render.com](https://render.com)
2. **Conecte GitHub**: Autorize acesso ao repositório
3. **Novo Web Service**: 
   - Repository: `biblical_calendar_app`
   - Branch: `main`
   - Root Directory: `web`
   - Environment: `Docker`
   - Dockerfile Path: `./Dockerfile`

4. **Configurações**:
   - Name: `biblical-calendar-web`
   - Plan: `Free`
   - Region: `Oregon`
   - Auto-Deploy: `Yes`

5. **Variáveis de Ambiente**:
   ```
   FLASK_ENV=production
   PORT=10000
   ```

6. **Deploy**: Clique em "Create Web Service"

#### Opção B: Via render.yaml (Recomendado)

1. **Commit arquivos**:
   ```bash
   git add web/
   git commit -m "feat: add Render.com deployment config"
   git push origin main
   ```

2. **Blueprint Deploy**:
   - Acesse Render Dashboard
   - "New" → "Blueprint"
   - Conecte repositório
   - Selecione `render.yaml`
   - Deploy automático

### 3. Configuração Avançada

#### Variáveis de Ambiente
```bash
# Produção
FLASK_ENV=production
PORT=10000

# Opcional - Modo Acadêmico padrão
DEFAULT_ACADEMIC_MODE=false

# Opcional - Cache
CACHE_TIMEOUT=3600
```

#### Health Check
- **Endpoint**: `/api/health`
- **Timeout**: 30 segundos
- **Interval**: 60 segundos

---

## 🔧 Arquitetura no Render

### Servidor Unificado
```python
# server.py - Serve frontend + backend
Flask App
├── /api/*          → Backend API (Flask)
├── /               → Frontend SPA (Vue.js)
└── /<spa-routes>   → SPA Routing (index.html)
```

### Build Process
```dockerfile
# Multi-stage build
Stage 1: Frontend Build (Node.js)
├── npm install
├── npm run build
└── Generate dist/

Stage 2: Production (Python)
├── Install Python deps
├── Copy backend code
├── Copy built frontend
└── Start unified server
```

---

## 📊 Monitoramento

### Logs
```bash
# Render Dashboard → Service → Logs
# Ou via CLI
render logs -s biblical-calendar-web
```

### Métricas
- **CPU Usage**: Monitorado automaticamente
- **Memory Usage**: Limite 512MB (free tier)
- **Response Time**: Disponível no dashboard
- **Uptime**: 99.9% SLA

### Health Checks
```bash
# Verificar status
curl https://your-app.onrender.com/api/health

# Resposta esperada
{
  "status": "healthy",
  "timestamp": "2025-01-03T...",
  "version": "1.0.0"
}
```

---

## 🔄 Atualizações

### Deploy Automático
- **Trigger**: Push para branch `main`
- **Build Time**: ~5-10 minutos
- **Downtime**: ~30 segundos durante deploy

### Deploy Manual
```bash
# Via Render CLI
render deploy -s biblical-calendar-web

# Ou via Dashboard
# Service → Manual Deploy → Deploy Latest Commit
```

### Rollback
```bash
# Via Dashboard
# Service → Deploys → Previous Deploy → Redeploy
```

---

## 🐛 Troubleshooting

### Problemas Comuns

#### Build Falha
```bash
# Verificar logs de build
# Comum: Dependências incompatíveis
# Solução: Verificar requirements.txt e package.json
```

#### App não Inicia
```bash
# Verificar PORT environment variable
# Render usa PORT dinâmica
# server.py deve usar: os.environ.get('PORT', 10000)
```

#### API não Responde
```bash
# Verificar se rotas /api/* estão funcionando
# Testar: https://your-app.onrender.com/api/health
```

#### Frontend não Carrega
```bash
# Verificar se arquivos estão em /static
# Verificar se SPA routing está configurado
```

### Performance

#### Otimizações
- **Cold Start**: ~10-30 segundos (free tier)
- **Keep Alive**: Configurar health check
- **Cache**: Implementar cache Redis (paid tier)

#### Limites Free Tier
- **Memory**: 512MB
- **CPU**: Compartilhado
- **Bandwidth**: 100GB/mês
- **Build Time**: 500 minutos/mês

---

## 🔒 Segurança

### HTTPS
- **Automático**: Certificado SSL gratuito
- **Custom Domain**: Suportado (paid tier)
- **Headers**: Configurar no Flask app

### Environment Variables
```python
# Nunca commitar secrets
# Usar Render Environment Variables
import os

SECRET_KEY = os.environ.get('SECRET_KEY')
DATABASE_URL = os.environ.get('DATABASE_URL')
```

---

## 💰 Custos

### Free Tier
- **750 horas/mês**: Suficiente para 1 app 24/7
- **Sleep após 15min**: Inatividade
- **Cold start**: ~30 segundos

### Starter Plan ($7/mês)
- **Sem sleep**: Always-on
- **Mais recursos**: CPU/Memory
- **Custom domains**: Incluído

---

## 📞 Suporte

### Recursos
- **Documentação**: [render.com/docs](https://render.com/docs)
- **Status**: [status.render.com](https://status.render.com)
- **Community**: [community.render.com](https://community.render.com)

### Comandos Úteis
```bash
# Instalar Render CLI
npm install -g @render/cli

# Login
render auth login

# Listar serviços
render services list

# Ver logs
render logs -s biblical-calendar-web -f
```

---

## 🎉 Resultado Final

Após o deploy bem-sucedido:

- **URL**: `https://biblical-calendar-web.onrender.com`
- **API**: `https://biblical-calendar-web.onrender.com/api/health`
- **SSL**: Automático
- **Deploy**: Automático via Git push

### Exemplo de URL
```
https://biblical-calendar-web-xyz123.onrender.com
```

---

<div align="center">

**Deploy realizado com sucesso no Render.com! 🚀**

**Sua aplicação está online e acessível globalmente!**

</div>