# Biblical Calendar Web Version

<div align="center">

**Versão Web do Calendário Bíblico Lunissolar**

[![Vue.js](https://img.shields.io/badge/Vue.js-3.4+-green)](https://vuejs.org)
[![Flask](https://img.shields.io/badge/Flask-3.0+-blue)](https://flask.palletsprojects.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://docker.com)

</div>

---

## 🌐 Visão Geral

Esta é a versão web do Biblical Calendar App, oferecendo toda a funcionalidade do aplicativo desktop através de uma interface web moderna e responsiva.

### ✨ Funcionalidades

- **Interface Web Responsiva**: Funciona em desktop, tablet e mobile
- **API REST Completa**: Backend Flask com endpoints para todos os cálculos
- **Calendário Visual Interativo**: Navegação mensal com eventos
- **Exportações**: CSV e ICS via download direto
- **Modo Acadêmico**: Suporte a efemérides DE440 para máxima precisão
- **Multi-usuário**: Suporte a múltiplos usuários simultâneos

---

## 🏗️ Arquitetura

```
web/
├── backend/           # Flask API
│   ├── app.py        # Aplicação principal
│   └── requirements.txt
├── frontend/         # Vue.js 3 SPA
│   ├── src/
│   │   ├── App.vue   # Componente principal
│   │   └── main.js   # Entry point
│   ├── package.json
│   └── vite.config.js
└── docker/           # Containerização
    ├── docker-compose.yml
    ├── Dockerfile.backend
    ├── Dockerfile.frontend
    └── nginx.conf
```

---

## 🚀 Instalação e Execução

### Desenvolvimento Local

#### Backend (Flask)
```bash
cd web/backend

# Opção 1: Script rápido (Recomendado)
# Windows:
start.bat
# Linux/macOS:
./start.sh

# Opção 2: Script Python
python run.py

# Opção 3: Manual com venv
python -m venv venv
# Windows: venv\Scripts\activate.bat
# Linux/macOS: source venv/bin/activate
pip install "numpy<2.0" --upgrade
pip install -r requirements.txt
set PYTHONPATH=..\..\src  # Windows
# export PYTHONPATH="../../src"  # Linux/macOS
python app.py

# Servidor rodando em http://localhost:5000
```

#### Frontend (Vue.js)
```bash
cd web/frontend

# Opção 1: Script rápido (Recomendado)
# Windows:
start.bat
# Linux/macOS:
./start.sh

# Opção 2: Desenvolvimento
npm install
npm run dev
# Servidor de desenvolvimento em http://localhost:3000

# Opção 3: Build + Servidor estático
npm install
npm run build
cd dist
python -m http.server 3000
# Servidor estático em http://localhost:3000
```

### Build de Produção (Manual)

#### 1. Build do Frontend
```bash
cd web/frontend
npm install
npm run build
# Arquivos gerados em dist/
```

#### 2. Servir Frontend Estático
```bash
# Opção 1: Python HTTP Server
cd web/frontend/dist
python -m http.server 3000

# Opção 2: Node.js serve
npm install -g serve
serve -s dist -l 3000

# Opção 3: Nginx (configuração manual)
# Copiar arquivos dist/ para /var/www/html
```

#### 3. Backend em Produção
```bash
cd web/backend
pip install -r requirements.txt gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

#### 4. Proxy Reverso (Nginx)
```nginx
server {
    listen 80;
    
    location / {
        root /path/to/frontend/dist;
        try_files $uri $uri/ /index.html;
    }
    
    location /api/ {
        proxy_pass http://localhost:5000;
    }
}
```

### Produção com Docker

```bash
cd web/docker
docker-compose up -d
# Aplicação disponível em http://localhost
```

---

## 📡 API Endpoints

### Calendário
- `GET /api/health` - Health check
- `GET /api/calendar/{year}` - Gerar calendário para um ano
  - Query params: `visibility`, `academic`

### Exportações
- `GET /api/export/csv/{year}` - Exportar CSV
- `GET /api/export/ics/{year}` - Exportar ICS

### Exemplo de Uso
```javascript
// Gerar calendário para 2025 com modo acadêmico
const response = await fetch('/api/calendar/2025?academic=true')
const data = await response.json()
```

---

## 🎨 Interface

### Características
- **Design Moderno**: Interface limpa com gradientes e blur effects
- **Responsiva**: Adaptável a diferentes tamanhos de tela
- **Interativa**: Clique nos dias para ver eventos detalhados
- **Navegação Intuitiva**: Botões Anterior/Próximo/Hoje
- **Feedback Visual**: Estados de loading e erro

### Componentes Principais
- **Header de Controles**: Configuração de ano e opções
- **Calendário Visual**: Grid mensal com eventos
- **Painel de Eventos**: Detalhes dos eventos selecionados
- **Botões de Exportação**: Download direto de CSV/ICS

---

## 🔧 Configuração

### Variáveis de Ambiente

#### Backend
```bash
FLASK_ENV=production
FLASK_APP=app.py
```

#### Frontend
```bash
VITE_API_BASE_URL=http://localhost:5000/api
```

### Personalização
- **Cores**: Editar CSS no `index.html`
- **API Base URL**: Configurar no componente Vue
- **Portas**: Ajustar no docker-compose.yml

---

## 🧪 Testes

### Backend
```bash
cd web/backend
python -m pytest tests/
```

### Frontend
```bash
cd web/frontend
npm run test
```

### E2E (Planejado)
```bash
npm run test:e2e
```

---

## 📦 Deploy

### Docker Compose (Recomendado)
```bash
# Produção
docker-compose -f docker-compose.yml up -d

# Desenvolvimento
docker-compose -f docker-compose.dev.yml up
```

### Manual
1. **Backend**: Deploy Flask em servidor Python
2. **Frontend**: Build e servir arquivos estáticos
3. **Proxy**: Configurar Nginx para roteamento

---

## 🔍 Monitoramento

### Health Checks
- Backend: `GET /api/health`
- Frontend: Verificar carregamento da página

### Logs
```bash
# Docker logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Aplicação local
tail -f backend.log
```

---

## 🤝 Contribuição

### Desenvolvimento
1. Fork o repositório
2. Crie branch para feature: `git checkout -b feature/nova-funcionalidade`
3. Desenvolva e teste localmente
4. Commit: `git commit -m "feat: adiciona nova funcionalidade"`
5. Push: `git push origin feature/nova-funcionalidade`
6. Abra Pull Request

### Estrutura de Commits
- `feat:` Nova funcionalidade
- `fix:` Correção de bug
- `docs:` Documentação
- `style:` Formatação
- `refactor:` Refatoração
- `test:` Testes

---

## 📋 Roadmap

### Versão 1.1 (Próxima)
- [ ] PWA (Progressive Web App)
- [ ] Notificações push para festivais
- [ ] Temas claro/escuro
- [ ] Gestos touch para navegação

### Versão 1.2
- [ ] Múltiplas localidades
- [ ] Comparação de métodos de cálculo
- [ ] Gráficos e visualizações
- [ ] API de terceiros

---

## 📞 Suporte

- **Issues**: [GitHub Issues](https://github.com/vanderloto/biblical_calendar_app/issues)
- **Email**: vander.loto@outlook.com
- **Documentação**: [Docs](../docs/)

---

<div align="center">

**Desenvolvido com ❤️ por Vander Loto - DATAMETRIA**

**Acesse a versão web e experimente o calendário bíblico no seu navegador!**

</div>