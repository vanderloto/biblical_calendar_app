# Documentação de API - [Nome da API]

<div align="center">

**Versão**: [X.Y.Z] | **Base URL**: `[https://api.exemplo.com]` | **Última Atualização**: [DD/MM/AAAA]

[![API Version](https://img.shields.io/badge/API-v1.0-blue)](link-api)
[![OpenAPI](https://img.shields.io/badge/OpenAPI-3.0-green)](link-swagger)
[![Status](https://img.shields.io/badge/status-stable-brightgreen)](link-status)

[🚀 Swagger UI](link-swagger) • [📋 Postman Collection](link-postman) • [🔑 Obter API Key](link-auth)

</div>

---

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Autenticação](#-autenticação)
- [Endpoints](#-endpoints)
- [Modelos de Dados](#-modelos-de-dados)
- [Códigos de Resposta](#-códigos-de-resposta)
- [Rate Limiting](#-rate-limiting)
- [Versionamento](#-versionamento)
- [SDKs e Bibliotecas](#-sdks-e-bibliotecas)
- [Exemplos](#-exemplos)
- [Changelog](#-changelog)

---

## 🎯 Visão Geral

### Descrição

[Descrição clara do propósito da API, funcionalidades principais e casos de uso]

### Características

- **🔒 Segura**: Autenticação JWT e HTTPS obrigatório
- **⚡ Rápida**: Tempo de resposta médio < 200ms
- **📊 Monitorada**: Logs completos e métricas em tempo real
- **🔄 Versionada**: Compatibilidade garantida entre versões

### Base URL

```
Produção:    https://api.[dominio].com/v1
Homologação: https://api-staging.[dominio].com/v1
```

### Formatos Suportados

- **Request**: `application/json`
- **Response**: `application/json`
- **Encoding**: `UTF-8`

---

## 🔐 Autenticação

### JWT Bearer Token

A API utiliza autenticação JWT (JSON Web Token) via header Authorization.

#### Obter Token

```http
POST /auth/login
Content-Type: application/json

{
  "email": "usuario@exemplo.com",
  "password": "senha123"
}
```

**Resposta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### Usar Token

```http
GET /api/v1/usuarios
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

#### Refresh Token

```http
POST /auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### API Key (Alternativa)

Para integrações server-to-server:

```http
GET /api/v1/dados
X-API-Key: sua-api-key-aqui
```

---

## 🔌 Endpoints

### Usuários

#### Listar Usuários

```http
GET /api/v1/usuarios
```

**Parâmetros de Query:**

| Parâmetro | Tipo | Obrigatório | Descrição | Exemplo |
|-----------|------|-------------|-----------|---------|
| `page` | `integer` | ❌ | Número da página (1-based) | `?page=2` |
| `limit` | `integer` | ❌ | Itens por página (max: 100) | `?limit=50` |
| `search` | `string` | ❌ | Busca por nome ou email | `?search=joão` |
| `status` | `string` | ❌ | Filtro por status | `?status=ativo` |
| `sort` | `string` | ❌ | Ordenação | `?sort=nome:asc` |

**Exemplo de Requisição:**
```bash
curl -X GET "https://api.exemplo.com/v1/usuarios?page=1&limit=10" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json"
```

**Resposta (200 OK):**
```json
{
  "data": [
    {
      "id": 1,
      "nome": "João Silva",
      "email": "joao@exemplo.com",
      "status": "ativo",
      "criado_em": "2024-01-15T10:30:00Z",
      "atualizado_em": "2024-01-15T10:30:00Z"
    }
  ],
  "meta": {
    "current_page": 1,
    "per_page": 10,
    "total": 150,
    "total_pages": 15
  },
  "links": {
    "first": "/api/v1/usuarios?page=1",
    "last": "/api/v1/usuarios?page=15",
    "prev": null,
    "next": "/api/v1/usuarios?page=2"
  }
}
```

#### Criar Usuário

```http
POST /api/v1/usuarios
```

**Body:**
```json
{
  "nome": "Maria Santos",
  "email": "maria@exemplo.com",
  "senha": "senha123",
  "status": "ativo",
  "perfil": "usuario"
}
```

**Validações:**

| Campo | Regras | Exemplo |
|-------|--------|---------|
| `nome` | Obrigatório, 2-100 caracteres | "João Silva" |
| `email` | Obrigatório, formato válido, único | "joao@exemplo.com" |
| `senha` | Obrigatório, mín. 8 caracteres | "senha123" |
| `status` | Opcional, enum: ativo/inativo | "ativo" |
| `perfil` | Opcional, enum: admin/usuario | "usuario" |

**Resposta (201 Created):**
```json
{
  "data": {
    "id": 2,
    "nome": "Maria Santos",
    "email": "maria@exemplo.com",
    "status": "ativo",
    "perfil": "usuario",
    "criado_em": "2024-01-15T11:00:00Z",
    "atualizado_em": "2024-01-15T11:00:00Z"
  },
  "message": "Usuário criado com sucesso"
}
```

#### Obter Usuário

```http
GET /api/v1/usuarios/{id}
```

**Parâmetros de Path:**

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `id` | `integer` | ID único do usuário |

**Resposta (200 OK):**
```json
{
  "data": {
    "id": 1,
    "nome": "João Silva",
    "email": "joao@exemplo.com",
    "status": "ativo",
    "perfil": "admin",
    "criado_em": "2024-01-15T10:30:00Z",
    "atualizado_em": "2024-01-15T10:30:00Z",
    "ultimo_login": "2024-01-15T14:20:00Z"
  }
}
```

#### Atualizar Usuário

```http
PUT /api/v1/usuarios/{id}
```

**Body (campos opcionais):**
```json
{
  "nome": "João Silva Santos",
  "status": "inativo"
}
```

**Resposta (200 OK):**
```json
{
  "data": {
    "id": 1,
    "nome": "João Silva Santos",
    "email": "joao@exemplo.com",
    "status": "inativo",
    "atualizado_em": "2024-01-15T15:00:00Z"
  },
  "message": "Usuário atualizado com sucesso"
}
```

#### Deletar Usuário

```http
DELETE /api/v1/usuarios/{id}
```

**Resposta (204 No Content):**
```
(Sem conteúdo)
```

### Recursos

#### Listar Recursos

```http
GET /api/v1/recursos
```

**Filtros Avançados:**
```http
GET /api/v1/recursos?categoria=tecnologia&data_inicio=2024-01-01&data_fim=2024-12-31
```

**Resposta (200 OK):**
```json
{
  "data": [
    {
      "id": 1,
      "titulo": "Recurso Exemplo",
      "descricao": "Descrição do recurso",
      "categoria": "tecnologia",
      "status": "publicado",
      "autor": {
        "id": 1,
        "nome": "João Silva"
      },
      "criado_em": "2024-01-15T10:30:00Z"
    }
  ],
  "meta": {
    "total": 25,
    "filtered": 10
  }
}
```

#### Upload de Arquivo

```http
POST /api/v1/recursos/{id}/upload
Content-Type: multipart/form-data
```

**Form Data:**
```
arquivo: (binary)
tipo: "imagem"
descricao: "Logo da empresa"
```

**Resposta (201 Created):**
```json
{
  "data": {
    "id": 1,
    "nome": "logo.png",
    "url": "https://cdn.exemplo.com/uploads/logo.png",
    "tamanho": 15360,
    "tipo": "image/png",
    "criado_em": "2024-01-15T16:00:00Z"
  }
}
```

---

## 📊 Modelos de Dados

### Usuario

```json
{
  "id": "integer",
  "nome": "string",
  "email": "string",
  "status": "enum[ativo, inativo]",
  "perfil": "enum[admin, usuario]",
  "criado_em": "datetime",
  "atualizado_em": "datetime",
  "ultimo_login": "datetime|null"
}
```

### Recurso

```json
{
  "id": "integer",
  "titulo": "string",
  "descricao": "string|null",
  "categoria": "string",
  "status": "enum[rascunho, publicado, arquivado]",
  "autor": {
    "id": "integer",
    "nome": "string"
  },
  "tags": ["string"],
  "metadados": "object|null",
  "criado_em": "datetime",
  "atualizado_em": "datetime"
}
```

### Paginação

```json
{
  "data": ["object"],
  "meta": {
    "current_page": "integer",
    "per_page": "integer",
    "total": "integer",
    "total_pages": "integer"
  },
  "links": {
    "first": "string|null",
    "last": "string|null",
    "prev": "string|null",
    "next": "string|null"
  }
}
```

### Erro

```json
{
  "error": {
    "code": "string",
    "message": "string",
    "details": "object|null"
  },
  "timestamp": "datetime",
  "path": "string"
}
```

---

## 📋 Códigos de Resposta

### Códigos de Sucesso

| Código | Descrição | Uso |
|--------|-----------|-----|
| `200` | OK | Requisição bem-sucedida |
| `201` | Created | Recurso criado com sucesso |
| `204` | No Content | Operação bem-sucedida sem conteúdo |

### Códigos de Erro do Cliente

| Código | Descrição | Exemplo |
|--------|-----------|---------|
| `400` | Bad Request | Dados inválidos na requisição |
| `401` | Unauthorized | Token ausente ou inválido |
| `403` | Forbidden | Sem permissão para o recurso |
| `404` | Not Found | Recurso não encontrado |
| `409` | Conflict | Conflito (ex: email já existe) |
| `422` | Unprocessable Entity | Erro de validação |
| `429` | Too Many Requests | Rate limit excedido |

### Códigos de Erro do Servidor

| Código | Descrição | Ação |
|--------|-----------|-------|
| `500` | Internal Server Error | Contate o suporte |
| `502` | Bad Gateway | Tente novamente em alguns minutos |
| `503` | Service Unavailable | Serviço em manutenção |

### Exemplos de Erro

**400 Bad Request:**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Dados de entrada inválidos",
    "details": {
      "email": ["Email é obrigatório"],
      "senha": ["Senha deve ter pelo menos 8 caracteres"]
    }
  },
  "timestamp": "2024-01-15T10:30:00Z",
  "path": "/api/v1/usuarios"
}
```

**401 Unauthorized:**
```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Token de acesso inválido ou expirado"
  },
  "timestamp": "2024-01-15T10:30:00Z",
  "path": "/api/v1/usuarios"
}
```

**404 Not Found:**
```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Usuário não encontrado"
  },
  "timestamp": "2024-01-15T10:30:00Z",
  "path": "/api/v1/usuarios/999"
}
```

---

## ⏱️ Rate Limiting

### Limites por Endpoint

| Endpoint | Limite | Janela | Escopo |
|----------|--------|--------|--------|
| `POST /auth/login` | 5 tentativas | 15 minutos | Por IP |
| `GET /api/v1/*` | 1000 requisições | 1 hora | Por usuário |
| `POST /api/v1/*` | 100 requisições | 1 hora | Por usuário |
| `PUT /api/v1/*` | 100 requisições | 1 hora | Por usuário |
| `DELETE /api/v1/*` | 50 requisições | 1 hora | Por usuário |

### Headers de Rate Limit

```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1642248000
```

### Resposta de Rate Limit Excedido

```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Muitas requisições. Tente novamente em 15 minutos."
  },
  "retry_after": 900
}
```

---

## 🔄 Versionamento

### Estratégia de Versionamento

- **URL Path**: `/api/v1/`, `/api/v2/`
- **Compatibilidade**: Mantida por 12 meses
- **Deprecação**: Aviso com 6 meses de antecedência

### Versões Disponíveis

| Versão | Status | Suporte até | Notas |
|--------|--------|-------------|-------|
| **v1** | ✅ Atual | 2025-12-31 | Versão estável |
| **v2** | 🔄 Beta | - | Em desenvolvimento |

### Header de Versão

```http
GET /api/v1/usuarios
API-Version: 1.0
```

### Deprecação

```http
HTTP/1.1 200 OK
Deprecation: true
Sunset: Wed, 31 Dec 2025 23:59:59 GMT
Link: </api/v2/usuarios>; rel="successor-version"
```

---

## 📚 SDKs e Bibliotecas

### JavaScript/TypeScript

```bash
npm install @empresa/api-client
```

```javascript
import { ApiClient } from '@empresa/api-client';

const client = new ApiClient({
  baseURL: 'https://api.exemplo.com/v1',
  token: 'seu-token-aqui'
});

// Listar usuários
const usuarios = await client.usuarios.list({ page: 1, limit: 10 });

// Criar usuário
const novoUsuario = await client.usuarios.create({
  nome: 'João Silva',
  email: 'joao@exemplo.com'
});
```

### Python

```bash
pip install empresa-api-client
```

```python
from empresa_api import ApiClient

client = ApiClient(
    base_url='https://api.exemplo.com/v1',
    token='seu-token-aqui'
)

# Listar usuários
usuarios = client.usuarios.list(page=1, limit=10)

# Criar usuário
novo_usuario = client.usuarios.create({
    'nome': 'João Silva',
    'email': 'joao@exemplo.com'
})
```

### cURL

```bash
# Definir variáveis
export API_BASE="https://api.exemplo.com/v1"
export TOKEN="seu-token-aqui"

# Listar usuários
curl -X GET "$API_BASE/usuarios" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json"

# Criar usuário
curl -X POST "$API_BASE/usuarios" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Silva",
    "email": "joao@exemplo.com",
    "senha": "senha123"
  }'
```

---

## 💡 Exemplos

### Fluxo Completo de Autenticação

```javascript
// 1. Login
const loginResponse = await fetch('/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'usuario@exemplo.com',
    password: 'senha123'
  })
});

const { access_token, refresh_token } = await loginResponse.json();

// 2. Usar token para acessar API
const usuariosResponse = await fetch('/api/v1/usuarios', {
  headers: {
    'Authorization': `Bearer ${access_token}`,
    'Content-Type': 'application/json'
  }
});

const usuarios = await usuariosResponse.json();

// 3. Refresh token quando necessário
const refreshResponse = await fetch('/auth/refresh', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ refresh_token })
});

const { access_token: newToken } = await refreshResponse.json();
```

### CRUD Completo

```python
import requests

class UsuarioAPI:
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
    
    def listar(self, page=1, limit=10):
        """Lista usuários com paginação."""
        response = requests.get(
            f'{self.base_url}/usuarios',
            headers=self.headers,
            params={'page': page, 'limit': limit}
        )
        return response.json()
    
    def criar(self, dados):
        """Cria novo usuário."""
        response = requests.post(
            f'{self.base_url}/usuarios',
            headers=self.headers,
            json=dados
        )
        return response.json()
    
    def obter(self, user_id):
        """Obtém usuário por ID."""
        response = requests.get(
            f'{self.base_url}/usuarios/{user_id}',
            headers=self.headers
        )
        return response.json()
    
    def atualizar(self, user_id, dados):
        """Atualiza usuário."""
        response = requests.put(
            f'{self.base_url}/usuarios/{user_id}',
            headers=self.headers,
            json=dados
        )
        return response.json()
    
    def deletar(self, user_id):
        """Deleta usuário."""
        response = requests.delete(
            f'{self.base_url}/usuarios/{user_id}',
            headers=self.headers
        )
        return response.status_code == 204

# Uso
api = UsuarioAPI('https://api.exemplo.com/v1', 'seu-token')

# Criar usuário
novo_usuario = api.criar({
    'nome': 'João Silva',
    'email': 'joao@exemplo.com',
    'senha': 'senha123'
})

# Listar usuários
usuarios = api.listar(page=1, limit=5)

# Atualizar usuário
api.atualizar(novo_usuario['data']['id'], {
    'nome': 'João Silva Santos'
})
```

### Tratamento de Erros

```javascript
async function criarUsuario(dadosUsuario) {
  try {
    const response = await fetch('/api/v1/usuarios', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(dadosUsuario)
    });

    if (!response.ok) {
      const errorData = await response.json();
      
      switch (response.status) {
        case 400:
          console.error('Dados inválidos:', errorData.error.details);
          break;
        case 401:
          console.error('Token inválido, redirecionando para login...');
          // Redirecionar para login
          break;
        case 409:
          console.error('Email já existe:', errorData.error.message);
          break;
        case 422:
          console.error('Erro de validação:', errorData.error.details);
          break;
        case 429:
          console.error('Rate limit excedido, aguarde...');
          // Implementar retry com backoff
          break;
        default:
          console.error('Erro inesperado:', errorData.error.message);
      }
      
      throw new Error(errorData.error.message);
    }

    return await response.json();
    
  } catch (error) {
    console.error('Erro na requisição:', error);
    throw error;
  }
}
```

---

## 📝 Changelog

### v1.2.0 - 2024-01-15

#### Adicionado
- Endpoint para upload de arquivos
- Filtros avançados em recursos
- Suporte a refresh tokens
- Rate limiting por endpoint

#### Alterado
- Formato de resposta de paginação
- Validação de senha mais rigorosa

#### Corrigido
- Bug na ordenação de usuários
- Escape de caracteres especiais em busca

### v1.1.0 - 2023-12-01

#### Adicionado
- Endpoint de recursos
- Autenticação via API Key
- Headers de rate limiting

#### Alterado
- Estrutura de resposta de erro padronizada

### v1.0.0 - 2023-10-15

#### Adicionado
- Endpoints básicos de usuários
- Autenticação JWT
- Documentação inicial

---

## 🔗 Links Úteis

- **[Swagger UI](link-swagger)** - Interface interativa da API
- **[Postman Collection](link-postman)** - Coleção para testes
- **[Status Page](link-status)** - Status dos serviços
- **[GitHub Repository](link-github)** - Código fonte
- **[Support Portal](link-support)** - Suporte técnico

---

<div align="center">

**Mantido por**: Equipe de API - [email-api]  
**Última Atualização**: [DD/MM/AAAA]  
**Versão da Documentação**: 1.2.0

---

**Para suporte técnico**: [email-suporte] | **Para reportar bugs**: [link-issues]

</div>