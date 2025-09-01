# Fix para Erro Mobile - Biblical Calendar Web

## Problema Identificado

O erro "Erro ao gerar calendário" no mobile é causado por:

1. **URLs hardcoded**: Frontend estava usando `http://localhost:5000` que não funciona em produção
2. **Configuração de ambiente**: Variáveis de ambiente não configuradas corretamente

## Correções Aplicadas

### 1. Frontend - URLs Dinâmicas
- ✅ Substituído `http://localhost:5000/api` por variável de ambiente
- ✅ Fallback para `/api` em produção
- ✅ Configuração separada para desenvolvimento local

### 2. Backend - Melhor Error Handling
- ✅ Adicionado traceback detalhado para debug
- ✅ Logs mais informativos

### 3. Configuração de Ambiente
```bash
# Desenvolvimento (.env.local)
VITE_API_BASE_URL=http://localhost:5000/api

# Produção (.env.production)
VITE_API_BASE_URL=/api
```

## Deploy no Render.com

### Passo 1: Build do Frontend
```bash
cd web/frontend
npm run build
```

### Passo 2: Copiar arquivos para static/
```bash
cd ..
cp -r frontend/dist/* static/
```

### Passo 3: Deploy
- Commit e push para GitHub
- Render.com fará deploy automático

## Teste Local

```bash
# Terminal 1 - Backend
cd web/backend
python app.py

# Terminal 2 - Frontend (dev)
cd web/frontend
npm run dev

# Ou teste produção local
cd web
python server.py
```

## Verificação

1. **Desktop**: Deve funcionar normalmente
2. **Mobile**: Deve carregar calendário sem erro
3. **API**: Endpoints devem responder com URLs relativas

## URLs de Teste

- **Health**: `/api/health`
- **Calendário**: `/api/calendar/2025`
- **Com heurística**: `/api/calendar/2025?visibility=true`