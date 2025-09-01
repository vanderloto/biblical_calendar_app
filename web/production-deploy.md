# Deploy Manual de Produção - Biblical Calendar Web

Este guia detalha como fazer o deploy da versão web do Biblical Calendar sem usar Docker.

## 📋 Pré-requisitos

### Software Necessário
- **Python 3.11+** - [Download](https://python.org/downloads/)
- **Node.js 18+** - [Download](https://nodejs.org/)
- **Nginx** (opcional, para proxy reverso)

### Verificação
```bash
python --version  # 3.11+
node --version    # 18+
npm --version     # 9+
```

---

## 🏗️ Build da Aplicação

### Opção 1: Script Automatizado

#### Linux/macOS:
```bash
chmod +x build.sh
./build.sh
```

#### Windows:
```cmd
build.bat
```

### Opção 2: Build Manual

#### 1. Frontend
```bash
cd web/frontend
npm install
npm run build
# Arquivos gerados em dist/
```

#### 2. Backend
```bash
cd web/backend
pip install -r requirements.txt
# Teste: python -c "import app; print('OK')"
```

---

## 🚀 Deploy de Produção

### Cenário 1: Servidor Único (Simples)

#### 1. Servir Frontend
```bash
# Opção A: Python HTTP Server
cd web/frontend/dist
python -m http.server 3000

# Opção B: Node.js serve
npm install -g serve
serve -s dist -l 3000

# Opção C: Nginx (ver configuração abaixo)
```

#### 2. Executar Backend
```bash
cd web/backend

# Desenvolvimento
python app.py

# Produção com Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

#### 3. Acessar
- Frontend: http://localhost:3000
- Backend: http://localhost:5000/api/health

### Cenário 2: Nginx como Proxy Reverso

#### 1. Configurar Nginx
```bash
# Copiar configuração
sudo cp nginx-production.conf /etc/nginx/sites-available/biblical-calendar
sudo ln -s /etc/nginx/sites-available/biblical-calendar /etc/nginx/sites-enabled/

# Editar caminhos no arquivo
sudo nano /etc/nginx/sites-available/biblical-calendar
# Alterar: root /path/to/biblical_calendar_app/web/frontend/dist;

# Testar e recarregar
sudo nginx -t
sudo systemctl reload nginx
```

#### 2. Executar Backend
```bash
cd web/backend
gunicorn -w 4 -b 127.0.0.1:5000 app:app
```

#### 3. Acessar
- Aplicação: http://localhost (porta 80)

---

## 🔧 Configurações de Produção

### Backend (Flask)

#### Variáveis de Ambiente
```bash
export FLASK_ENV=production
export FLASK_APP=app.py
```

#### Gunicorn com Configuração
```bash
# gunicorn.conf.py
bind = "0.0.0.0:5000"
workers = 4
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 2
```

```bash
gunicorn -c gunicorn.conf.py app:app
```

### Frontend (Vue.js)

#### Configuração de Produção
```javascript
// vite.config.js
export default defineConfig({
  plugins: [vue()],
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    minify: 'terser',
    sourcemap: false
  },
  server: {
    proxy: {
      '/api': 'http://localhost:5000'
    }
  }
})
```

---

## 🔒 Segurança

### HTTPS (Recomendado)

#### 1. Certificado SSL
```bash
# Let's Encrypt (gratuito)
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d seu-dominio.com
```

#### 2. Configuração Nginx SSL
```nginx
server {
    listen 443 ssl http2;
    server_name seu-dominio.com;
    
    ssl_certificate /etc/letsencrypt/live/seu-dominio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/seu-dominio.com/privkey.pem;
    
    # Resto da configuração...
}
```

### Firewall
```bash
# Ubuntu/Debian
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable

# CentOS/RHEL
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

---

## 📊 Monitoramento

### Health Checks
```bash
# Backend
curl http://localhost:5000/api/health

# Frontend
curl http://localhost:3000
```

### Logs
```bash
# Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Gunicorn
gunicorn --access-logfile - --error-logfile - app:app
```

### Processo Management (Systemd)

#### Backend Service
```ini
# /etc/systemd/system/biblical-calendar-api.service
[Unit]
Description=Biblical Calendar API
After=network.target

[Service]
Type=exec
User=www-data
WorkingDirectory=/path/to/biblical_calendar_app/web/backend
ExecStart=/usr/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable biblical-calendar-api
sudo systemctl start biblical-calendar-api
sudo systemctl status biblical-calendar-api
```

---

## 🔄 Atualizações

### Processo de Atualização
```bash
# 1. Backup (se necessário)
cp -r web/frontend/dist web/frontend/dist.backup

# 2. Atualizar código
git pull origin main

# 3. Rebuild
./build.sh

# 4. Restart services
sudo systemctl restart biblical-calendar-api
sudo systemctl reload nginx
```

---

## 🐛 Troubleshooting

### Problemas Comuns

#### Frontend não carrega
```bash
# Verificar se arquivos foram gerados
ls -la web/frontend/dist/

# Verificar permissões
chmod -R 755 web/frontend/dist/
```

#### API não responde
```bash
# Verificar se backend está rodando
curl http://localhost:5000/api/health

# Verificar logs
journalctl -u biblical-calendar-api -f
```

#### CORS errors
```bash
# Verificar configuração do Flask CORS
# Ou configurar no Nginx (ver nginx-production.conf)
```

### Performance

#### Otimizações
- **Gzip**: Habilitado no Nginx
- **Cache**: Headers de cache para assets estáticos
- **CDN**: Considerar para assets (futuro)
- **Database**: Cache Redis (planejado)

---

## 📞 Suporte

- **Documentação**: [README.md](README.md)
- **Issues**: [GitHub Issues](https://github.com/vanderloto/biblical_calendar_app/issues)
- **Email**: vander.loto@outlook.com

---

<div align="center">

**Deploy realizado com sucesso! 🎉**

**Acesse sua aplicação e desfrute do calendário bíblico web!**

</div>