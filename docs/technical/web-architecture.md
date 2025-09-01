# Arquitetura da Versão Web - Biblical Calendar App

<div align="center">

**Especificação Técnica da Plataforma Web**

[![Flask](https://img.shields.io/badge/Backend-Flask-green)](https://flask.palletsprojects.com/)
[![Vue.js](https://img.shields.io/badge/Frontend-Vue.js%203-brightgreen)](https://vuejs.org/)
[![Docker](https://img.shields.io/badge/Deploy-Docker-blue)](https://docker.com/)

</div>

---

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Arquitetura do Sistema](#-arquitetura-do-sistema)
- [Stack Tecnológico](#-stack-tecnológico)
- [API REST](#-api-rest)
- [Frontend Vue.js](#-frontend-vuejs)
- [Deploy e Infraestrutura](#-deploy-e-infraestrutura)
- [Segurança](#-segurança)
- [Performance](#-performance)

---

## 🎯 Visão Geral

### Objetivo

Criar uma versão web completa do Biblical Calendar App que mantenha todas as funcionalidades da versão desktop, oferecendo:

- **Acessibilidade Universal**: Acesso via navegador em qualquer dispositivo
- **Interface Responsiva**: Otimizada para desktop, tablet e mobile
- **API REST**: Integração com outras aplicações
- **Performance**: Carregamento rápido e experiência fluida
- **Escalabilidade**: Suporte a múltiplos usuários simultâneos

### Benefícios

- ✅ **Sem Instalação**: Acesso direto via navegador
- ✅ **Multiplataforma**: Windows, macOS, Linux, iOS, Android
- ✅ **Compartilhamento**: URLs diretas para calendários específicos
- ✅ **Integração**: API para desenvolvedores externos
- ✅ **Manutenção**: Deploy centralizado e atualizações automáticas

---

## 🏗️ Arquitetura do Sistema

### Diagrama de Arquitetura

```mermaid
graph TB
    subgraph "Cliente"
        A[Navegador Web]
        B[Mobile App]
    end
    
    subgraph "Frontend"
        C[Vue.js 3 SPA]
        D[Nginx Static]
    end
    
    subgraph "Backend"
        E[Flask API]
        F[Celery Workers]
    end
    
    subgraph "Dados"
        G[Redis Cache]
        H[PostgreSQL]
        I[Ephemeris Files]
    end
    
    A --> C
    B --> C
    C --> D
    D --> E
    E --> F
    E --> G
    E --> H
    F --> I
```

### Componentes Principais

| Componente | Tecnologia | Responsabilidade |
|------------|------------|------------------|
| **Frontend SPA** | Vue.js 3 | Interface do usuário |
| **API Backend** | Flask-RESTX | Lógica de negócio e cálculos |
| **Cache Layer** | Redis | Cache de cálculos astronômicos |
| **Database** | PostgreSQL | Persistência de dados |
| **Task Queue** | Celery | Processamento assíncrono |
| **Web Server** | Nginx | Proxy reverso e assets estáticos |

---

## 🛠️ Stack Tecnológico

### Backend (Flask)

```python
# requirements.txt
flask==2.3.3
flask-restx==1.1.0
flask-cors==4.0.0
celery==5.3.1
redis==4.6.0
psycopg2-binary==2.9.7
skyfield==1.45
pandas==2.1.0
gunicorn==21.2.0
```

#### Estrutura do Backend
```
backend/
├── app/
│   ├── __init__.py          # Factory pattern
│   ├── api/
│   │   ├── calendar.py      # Endpoints do calendário
│   │   ├── festivals.py     # Endpoints de festivais
│   │   └── ephemeris.py     # Endpoints de efemérides
│   ├── core/
│   │   ├── astronomy.py     # Lógica astronômica
│   │   ├── cache.py         # Gerenciamento de cache
│   │   └── config.py        # Configurações
│   ├── models/
│   │   └── calendar.py      # Modelos de dados
│   └── tasks/
│       └── calculations.py  # Tarefas Celery
├── tests/
├── Dockerfile
└── requirements.txt
```

### Frontend (Vue.js 3)

```json
{
  "dependencies": {
    "vue": "^3.3.4",
    "vue-router": "^4.2.4",
    "pinia": "^2.1.6",
    "axios": "^1.5.0",
    "@vueuse/core": "^10.4.1",
    "tailwindcss": "^3.3.3"
  },
  "devDependencies": {
    "vite": "^4.4.9",
    "typescript": "^5.2.2",
    "cypress": "^13.2.0"
  }
}
```

#### Estrutura do Frontend
```
frontend/
├── src/
│   ├── components/
│   │   ├── Calendar/
│   │   │   ├── CalendarGrid.vue
│   │   │   ├── MonthNavigation.vue
│   │   │   └── DayEvents.vue
│   │   ├── UI/
│   │   │   ├── Button.vue
│   │   │   └── Modal.vue
│   │   └── Layout/
│   │       └── AppHeader.vue
│   ├── composables/
│   │   ├── useCalendar.js
│   │   └── useEphemeris.js
│   ├── services/
│   │   └── api.js
│   ├── stores/
│   │   ├── calendar.js
│   │   └── settings.js
│   ├── views/
│   │   ├── Calendar.vue
│   │   └── About.vue
│   ├── App.vue
│   └── main.js
├── public/
├── Dockerfile
└── package.json
```

---

## 🔌 API REST

### Endpoints Principais

#### Calendário
```http
GET /api/v1/calendar/{year}
GET /api/v1/calendar/{year}/months
GET /api/v1/calendar/{year}/festivals
GET /api/v1/calendar/{year}/moon-phases
```

#### Configurações
```http
GET /api/v1/ephemeris/status
POST /api/v1/settings/academic-mode
GET /api/v1/locations
```

### Exemplo de Resposta

```json
{
  "year": 2025,
  "ephemeris": "DE421 (Padrão)",
  "embolismic": false,
  "months": [
    {
      "index": 1,
      "name": "Nissan",
      "start": "2025-03-30",
      "end": "2025-04-28",
      "days": 29
    }
  ],
  "festivals": [
    {
      "name": "Pessach",
      "hebrew": "פסח",
      "date": "2025-04-13",
      "description": "Celebra a libertação do povo de Israel do Egito."
    }
  ]
}
```

### Documentação OpenAPI

```python
# app/api/calendar.py
from flask_restx import Namespace, Resource, fields

api = Namespace('calendar', description='Biblical Calendar operations')

calendar_model = api.model('Calendar', {
    'year': fields.Integer(required=True, description='Year'),
    'ephemeris': fields.String(description='Ephemeris used'),
    'embolismic': fields.Boolean(description='Is embolismic year'),
    'months': fields.List(fields.Nested(month_model))
})

@api.route('/<int:year>')
class CalendarResource(Resource):
    @api.marshal_with(calendar_model)
    def get(self, year):
        """Get biblical calendar for specific year"""
        return generate_calendar_data(year)
```

---

## 🎨 Frontend Vue.js

### Composable para Calendário

```javascript
// composables/useCalendar.js
import { ref, computed } from 'vue'
import { useCalendarStore } from '@/stores/calendar'

export function useCalendar() {
  const store = useCalendarStore()
  const currentYear = ref(new Date().getFullYear())
  const currentMonth = ref(0)
  
  const currentMonthData = computed(() => {
    return store.months[currentMonth.value]
  })
  
  const navigateMonth = (direction) => {
    if (direction === 'next') {
      if (currentMonth.value < store.months.length - 1) {
        currentMonth.value++
      } else {
        // Navigate to next year
        currentYear.value++
        currentMonth.value = 0
        store.loadYear(currentYear.value)
      }
    } else {
      if (currentMonth.value > 0) {
        currentMonth.value--
      } else {
        // Navigate to previous year
        currentYear.value--
        currentMonth.value = 11 // or 12 for embolismic
        store.loadYear(currentYear.value)
      }
    }
  }
  
  return {
    currentYear,
    currentMonth,
    currentMonthData,
    navigateMonth
  }
}
```

### Componente de Calendário

```vue
<template>
  <div class="calendar-container">
    <!-- Navigation -->
    <div class="calendar-header">
      <button @click="navigateMonth('prev')" class="nav-btn">
        ← Anterior
      </button>
      <h2 class="month-title">
        {{ currentMonthData?.name }} {{ currentYear }}
      </h2>
      <button @click="navigateMonth('next')" class="nav-btn">
        Próximo →
      </button>
    </div>
    
    <!-- Calendar Grid -->
    <div class="calendar-grid">
      <div v-for="day in weekDays" :key="day" class="day-header">
        {{ day }}
      </div>
      
      <div
        v-for="day in calendarDays"
        :key="day.date"
        :class="dayClasses(day)"
        @click="selectDay(day)"
      >
        <div class="day-number">{{ day.number }}</div>
        <div class="day-gregorian">{{ day.gregorian }}</div>
        <div class="day-events">
          <span v-for="event in day.events" :key="event.name" class="event-icon">
            {{ event.icon }}
          </span>
        </div>
      </div>
    </div>
    
    <!-- Events Panel -->
    <div v-if="selectedDay" class="events-panel">
      <h3>Eventos do Dia {{ selectedDay.number }}</h3>
      <div v-for="event in selectedDay.events" :key="event.name" class="event-item">
        <strong>{{ event.name }}</strong>
        <p>{{ event.description }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useCalendar } from '@/composables/useCalendar'

const { currentYear, currentMonth, currentMonthData, navigateMonth } = useCalendar()
const selectedDay = ref(null)

const weekDays = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb']

const calendarDays = computed(() => {
  // Generate calendar days with events
  return generateCalendarDays(currentMonthData.value)
})

const dayClasses = (day) => ({
  'calendar-day': true,
  'today': day.isToday,
  'selected': selectedDay.value?.date === day.date,
  'has-events': day.events.length > 0
})

const selectDay = (day) => {
  selectedDay.value = day
}
</script>

<style scoped>
.calendar-container {
  @apply max-w-4xl mx-auto p-4;
}

.calendar-header {
  @apply flex items-center justify-between mb-6;
}

.calendar-grid {
  @apply grid grid-cols-7 gap-1 mb-6;
}

.calendar-day {
  @apply border border-gray-200 p-2 min-h-20 cursor-pointer hover:bg-gray-50;
}

.calendar-day.today {
  @apply bg-blue-100 border-blue-300;
}

.calendar-day.has-events {
  @apply bg-yellow-50;
}

.events-panel {
  @apply bg-white border border-gray-200 rounded-lg p-4;
}
</style>
```

---

## 🚀 Deploy e Infraestrutura

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    depends_on:
      - backend
    environment:
      - VITE_API_BASE_URL=http://backend:5000/api/v1

  backend:
    build: ./backend
    ports:
      - "5000:5000"
    depends_on:
      - redis
      - postgres
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=postgresql://user:pass@postgres:5432/biblical_calendar
      - REDIS_URL=redis://redis:6379/0
    volumes:
      - ephemeris_data:/app/ephemeris

  celery:
    build: ./backend
    command: celery -A app.celery worker --loglevel=info
    depends_on:
      - redis
      - postgres
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres:5432/biblical_calendar
      - REDIS_URL=redis://redis:6379/0
    volumes:
      - ephemeris_data:/app/ephemeris

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=biblical_calendar
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - frontend
      - backend

volumes:
  postgres_data:
  ephemeris_data:
```

### GitHub Actions CI/CD

```yaml
# .github/workflows/deploy.yml
name: Deploy Web App

on:
  push:
    branches: [main]
    paths: ['web/**']

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Test Backend
        run: |
          cd web/backend
          pip install -r requirements.txt
          pytest
      
      - name: Test Frontend
        run: |
          cd web/frontend
          npm install
          npm run test:unit
          npm run build

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      
      - name: Deploy to Production
        run: |
          docker-compose -f docker-compose.prod.yml up -d --build
```

---

## 🔒 Segurança

### Autenticação e Autorização

```python
# app/core/auth.py
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

jwt = JWTManager()

@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    # Simple API key authentication for now
    api_key = request.json.get('api_key')
    if validate_api_key(api_key):
        access_token = create_access_token(identity=api_key)
        return {'access_token': access_token}
    return {'error': 'Invalid API key'}, 401

@app.route('/api/v1/calendar/<int:year>')
@jwt_required(optional=True)  # Optional for public access
def get_calendar(year):
    # Rate limiting based on authentication
    return generate_calendar(year)
```

### Rate Limiting

```python
# app/core/rate_limit.py
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/v1/calendar/<int:year>')
@limiter.limit("10 per minute")
def get_calendar(year):
    return generate_calendar(year)
```

---

## ⚡ Performance

### Cache Strategy

```python
# app/core/cache.py
import redis
import json
from functools import wraps

redis_client = redis.Redis.from_url(os.getenv('REDIS_URL'))

def cache_result(expiration=3600):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
            
            # Try to get from cache
            cached = redis_client.get(cache_key)
            if cached:
                return json.loads(cached)
            
            # Calculate and cache
            result = func(*args, **kwargs)
            redis_client.setex(cache_key, expiration, json.dumps(result, default=str))
            return result
        return wrapper
    return decorator

@cache_result(expiration=86400)  # 24 hours
def generate_biblical_months(year, use_visibility=False):
    # Expensive astronomical calculations
    return calculate_months(year, use_visibility)
```

### Frontend Performance

```javascript
// Lazy loading de componentes
const CalendarView = defineAsyncComponent(() =>
  import('@/views/Calendar.vue')
)

// Virtual scrolling para listas grandes
import { RecycleScroller } from 'vue-virtual-scroller'

// Service Worker para cache
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/sw.js')
}
```

---

## 📊 Métricas e Monitoramento

### Prometheus Metrics

```python
# app/core/metrics.py
from prometheus_client import Counter, Histogram, generate_latest

REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration')

@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request
def after_request(response):
    REQUEST_COUNT.labels(method=request.method, endpoint=request.endpoint).inc()
    REQUEST_DURATION.observe(time.time() - request.start_time)
    return response

@app.route('/metrics')
def metrics():
    return generate_latest()
```

---

<div align="center">

**Mantido por**: Equipe de Desenvolvimento DATAMETRIA  
**Última Atualização**: 31/08/2025  
**Versão**: 1.0.0

---

**Para questões técnicas**: vander.loto@outlook.com

</div>