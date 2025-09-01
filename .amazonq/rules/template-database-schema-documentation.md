# Database Schema Documentation - [Nome do Banco]

<div align="center">

**Versão**: [X.Y.Z] | **SGBD**: [PostgreSQL/MySQL/Oracle] | **Última Atualização**: [DD/MM/AAAA]

[![Database](https://img.shields.io/badge/database-PostgreSQL-blue)](link-db)
[![Schema](https://img.shields.io/badge/schema-v1.0-green)](link-schema)
[![Migrations](https://img.shields.io/badge/migrations-current-brightgreen)](link-migrations)

[📊 ERD Diagram](link-erd) • [🔄 Migrations](link-migrations) • [📋 Data Dictionary](link-dictionary)

</div>

---

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Arquitetura do Banco](#-arquitetura-do-banco)
- [Diagrama ER](#-diagrama-er)
- [Tabelas](#-tabelas)
- [Relacionamentos](#-relacionamentos)
- [Índices](#-índices)
- [Views](#-views)
- [Stored Procedures](#-stored-procedures)
- [Triggers](#-triggers)
- [Migrations](#-migrations)
- [Performance](#-performance)
- [Backup e Recovery](#-backup-e-recovery)
- [Glossário](#-glossário)

---

## 🎯 Visão Geral

### Descrição

[Descrição do propósito do banco de dados, domínio de negócio e principais funcionalidades suportadas]

### Características

- **🗄️ SGBD**: [PostgreSQL 15.3]
- **📊 Tabelas**: [X] tabelas principais
- **🔗 Relacionamentos**: [X] foreign keys
- **📈 Índices**: [X] índices otimizados
- **💾 Tamanho**: ~[X] GB em produção

### Ambientes

| Ambiente | Host | Porta | Database | Schema |
|----------|------|-------|----------|--------|
| **Desenvolvimento** | localhost | 5432 | [db_dev] | public |
| **Homologação** | [host-hml] | 5432 | [db_hml] | public |
| **Produção** | [host-prod] | 5432 | [db_prod] | public |

### Conexão

```python
# SQLAlchemy connection string
DATABASE_URL = "postgresql://user:password@host:5432/database"

# Exemplo de configuração
from sqlalchemy import create_engine

engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    echo=False  # True para debug
)
```

---

## 🏗️ Arquitetura do Banco

### Estrutura Lógica

```mermaid
graph TB
    subgraph "Core Tables"
        A[usuarios]
        B[perfis]
        C[permissoes]
    end
    
    subgraph "Business Tables"
        D[projetos]
        E[tarefas]
        F[documentos]
    end
    
    subgraph "Audit Tables"
        G[audit_log]
        H[user_sessions]
    end
    
    A --> B
    B --> C
    A --> D
    D --> E
    E --> F
    A --> G
    A --> H
```

### Padrões de Nomenclatura

#### Tabelas
- **Formato**: `snake_case`, plural
- **Exemplos**: `usuarios`, `perfis_usuarios`, `log_auditoria`

#### Colunas
- **Formato**: `snake_case`, singular
- **Padrões**:
  - `id`: Chave primária (SERIAL/UUID)
  - `created_at`: Data de criação (TIMESTAMP)
  - `updated_at`: Data de atualização (TIMESTAMP)
  - `deleted_at`: Soft delete (TIMESTAMP NULL)

#### Índices
- **Formato**: `idx_[tabela]_[coluna(s)]`
- **Exemplos**: `idx_usuarios_email`, `idx_projetos_status_data`

#### Constraints
- **Primary Key**: `pk_[tabela]`
- **Foreign Key**: `fk_[tabela]_[tabela_referenciada]`
- **Unique**: `uk_[tabela]_[coluna(s)]`
- **Check**: `ck_[tabela]_[regra]`

---

## 📊 Diagrama ER

### Diagrama Conceitual

```mermaid
erDiagram
    USUARIOS {
        int id PK
        string nome
        string email UK
        string senha_hash
        enum status
        timestamp created_at
        timestamp updated_at
    }
    
    PERFIS {
        int id PK
        string nome UK
        string descricao
        boolean ativo
        timestamp created_at
    }
    
    USUARIOS_PERFIS {
        int usuario_id FK
        int perfil_id FK
        timestamp created_at
    }
    
    PROJETOS {
        int id PK
        string nome
        text descricao
        int owner_id FK
        enum status
        date data_inicio
        date data_fim
        timestamp created_at
        timestamp updated_at
    }
    
    TAREFAS {
        int id PK
        string titulo
        text descricao
        int projeto_id FK
        int assignee_id FK
        enum prioridade
        enum status
        timestamp created_at
        timestamp updated_at
    }
    
    USUARIOS ||--o{ USUARIOS_PERFIS : tem
    PERFIS ||--o{ USUARIOS_PERFIS : possui
    USUARIOS ||--o{ PROJETOS : possui
    PROJETOS ||--o{ TAREFAS : contem
    USUARIOS ||--o{ TAREFAS : executa
```

### Legenda

| Símbolo | Significado |
|---------|-------------|
| `||--o{` | Um para muitos |
| `||--||` | Um para um |
| `}o--o{` | Muitos para muitos |
| `PK` | Primary Key |
| `FK` | Foreign Key |
| `UK` | Unique Key |

---

## 📋 Tabelas

### usuarios

**Descrição**: Armazena informações dos usuários do sistema

**Estrutura**:
```sql
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    senha_hash VARCHAR(255) NOT NULL,
    status VARCHAR(20) DEFAULT 'ativo' CHECK (status IN ('ativo', 'inativo', 'bloqueado')),
    ultimo_login TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Colunas**:

| Coluna | Tipo | Nulo | Padrão | Descrição |
|--------|------|------|--------|-----------|
| `id` | SERIAL | ❌ | AUTO | Identificador único |
| `nome` | VARCHAR(100) | ❌ | - | Nome completo do usuário |
| `email` | VARCHAR(255) | ❌ | - | Email único para login |
| `senha_hash` | VARCHAR(255) | ❌ | - | Hash bcrypt da senha |
| `status` | VARCHAR(20) | ❌ | 'ativo' | Status do usuário |
| `ultimo_login` | TIMESTAMP | ✅ | NULL | Data do último login |
| `created_at` | TIMESTAMP | ❌ | NOW() | Data de criação |
| `updated_at` | TIMESTAMP | ❌ | NOW() | Data de atualização |

**Constraints**:
- `pk_usuarios`: PRIMARY KEY (id)
- `uk_usuarios_email`: UNIQUE (email)
- `ck_usuarios_status`: CHECK (status IN ('ativo', 'inativo', 'bloqueado'))

**Índices**:
- `idx_usuarios_email`: (email) - Para login
- `idx_usuarios_status`: (status) - Para filtros
- `idx_usuarios_created_at`: (created_at) - Para ordenação

**Triggers**:
- `tr_usuarios_updated_at`: Atualiza `updated_at` automaticamente

**Dados de Exemplo**:
```sql
INSERT INTO usuarios (nome, email, senha_hash, status) VALUES
('João Silva', 'joao@exemplo.com', '$2b$12$...', 'ativo'),
('Maria Santos', 'maria@exemplo.com', '$2b$12$...', 'ativo');
```

---

### projetos

**Descrição**: Armazena informações dos projetos gerenciados no sistema

**Estrutura**:
```sql
CREATE TABLE projetos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(200) NOT NULL,
    descricao TEXT,
    owner_id INTEGER NOT NULL REFERENCES usuarios(id),
    status VARCHAR(20) DEFAULT 'planejamento' CHECK (status IN ('planejamento', 'ativo', 'pausado', 'concluido', 'cancelado')),
    data_inicio DATE,
    data_fim DATE,
    orcamento DECIMAL(15,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Colunas**:

| Coluna | Tipo | Nulo | Padrão | Descrição |
|--------|------|------|--------|-----------|
| `id` | SERIAL | ❌ | AUTO | Identificador único |
| `nome` | VARCHAR(200) | ❌ | - | Nome do projeto |
| `descricao` | TEXT | ✅ | NULL | Descrição detalhada |
| `owner_id` | INTEGER | ❌ | - | ID do usuário responsável |
| `status` | VARCHAR(20) | ❌ | 'planejamento' | Status atual |
| `data_inicio` | DATE | ✅ | NULL | Data de início |
| `data_fim` | DATE | ✅ | NULL | Data de término |
| `orcamento` | DECIMAL(15,2) | ✅ | NULL | Orçamento do projeto |
| `created_at` | TIMESTAMP | ❌ | NOW() | Data de criação |
| `updated_at` | TIMESTAMP | ❌ | NOW() | Data de atualização |

**Relacionamentos**:
- `owner_id` → `usuarios.id` (Many-to-One)

---

### tarefas

**Descrição**: Armazena tarefas individuais dentro dos projetos

**Estrutura**:
```sql
CREATE TABLE tarefas (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    descricao TEXT,
    projeto_id INTEGER NOT NULL REFERENCES projetos(id) ON DELETE CASCADE,
    assignee_id INTEGER REFERENCES usuarios(id),
    prioridade VARCHAR(10) DEFAULT 'media' CHECK (prioridade IN ('baixa', 'media', 'alta', 'critica')),
    status VARCHAR(20) DEFAULT 'pendente' CHECK (status IN ('pendente', 'em_progresso', 'concluida', 'cancelada')),
    estimativa_horas INTEGER,
    horas_trabalhadas INTEGER DEFAULT 0,
    data_vencimento DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Relacionamentos**:
- `projeto_id` → `projetos.id` (Many-to-One, CASCADE DELETE)
- `assignee_id` → `usuarios.id` (Many-to-One, NULL allowed)

---

## 🔗 Relacionamentos

### Diagrama de Relacionamentos

```mermaid
graph LR
    A[usuarios] -->|1:N| B[projetos]
    A -->|1:N| C[tarefas]
    B -->|1:N| C
    A -->|N:M| D[perfis]
    A -->|1:N| E[audit_log]
    
    subgraph "Tabelas de Junção"
        F[usuarios_perfis]
    end
    
    A -.-> F
    D -.-> F
```

### Detalhamento dos Relacionamentos

#### usuarios → projetos (1:N)
- **Tipo**: One-to-Many
- **Chave**: `projetos.owner_id` → `usuarios.id`
- **Regra**: Um usuário pode ser dono de vários projetos
- **Cascade**: RESTRICT (não permite deletar usuário com projetos)

#### projetos → tarefas (1:N)
- **Tipo**: One-to-Many
- **Chave**: `tarefas.projeto_id` → `projetos.id`
- **Regra**: Um projeto pode ter várias tarefas
- **Cascade**: CASCADE (deletar projeto remove suas tarefas)

#### usuarios → tarefas (1:N)
- **Tipo**: One-to-Many (opcional)
- **Chave**: `tarefas.assignee_id` → `usuarios.id`
- **Regra**: Um usuário pode ser responsável por várias tarefas
- **Cascade**: SET NULL (deletar usuário não remove tarefas)

#### usuarios ↔ perfis (N:M)
- **Tipo**: Many-to-Many
- **Tabela de Junção**: `usuarios_perfis`
- **Chaves**: 
  - `usuarios_perfis.usuario_id` → `usuarios.id`
  - `usuarios_perfis.perfil_id` → `perfis.id`

---

## 📈 Índices

### Índices Primários

| Tabela | Índice | Tipo | Colunas | Propósito |
|--------|--------|------|---------|-----------|
| `usuarios` | `pk_usuarios` | PRIMARY | (id) | Chave primária |
| `projetos` | `pk_projetos` | PRIMARY | (id) | Chave primária |
| `tarefas` | `pk_tarefas` | PRIMARY | (id) | Chave primária |

### Índices Únicos

| Tabela | Índice | Colunas | Propósito |
|--------|--------|---------|-----------|
| `usuarios` | `uk_usuarios_email` | (email) | Login único |
| `perfis` | `uk_perfis_nome` | (nome) | Nome único |

### Índices de Performance

```sql
-- Índices para consultas frequentes
CREATE INDEX idx_usuarios_status ON usuarios(status);
CREATE INDEX idx_usuarios_created_at ON usuarios(created_at DESC);

CREATE INDEX idx_projetos_owner_status ON projetos(owner_id, status);
CREATE INDEX idx_projetos_data_inicio ON projetos(data_inicio);

CREATE INDEX idx_tarefas_projeto_status ON tarefas(projeto_id, status);
CREATE INDEX idx_tarefas_assignee_status ON tarefas(assignee_id, status) WHERE assignee_id IS NOT NULL;
CREATE INDEX idx_tarefas_vencimento ON tarefas(data_vencimento) WHERE data_vencimento IS NOT NULL;

-- Índice composto para relatórios
CREATE INDEX idx_tarefas_projeto_prioridade_status ON tarefas(projeto_id, prioridade, status);
```

### Análise de Performance

| Índice | Tamanho | Uso | Eficiência |
|--------|---------|-----|------------|
| `idx_usuarios_email` | 2.1 MB | 95% | ✅ Alto |
| `idx_projetos_owner_status` | 1.8 MB | 78% | ✅ Alto |
| `idx_tarefas_projeto_status` | 4.2 MB | 85% | ✅ Alto |
| `idx_tarefas_vencimento` | 1.2 MB | 45% | ⚠️ Médio |

---

## 👁️ Views

### vw_projetos_resumo

**Descrição**: View com resumo de projetos incluindo estatísticas de tarefas

```sql
CREATE VIEW vw_projetos_resumo AS
SELECT 
    p.id,
    p.nome,
    p.status,
    u.nome AS owner_nome,
    p.data_inicio,
    p.data_fim,
    COUNT(t.id) AS total_tarefas,
    COUNT(CASE WHEN t.status = 'concluida' THEN 1 END) AS tarefas_concluidas,
    COUNT(CASE WHEN t.status = 'pendente' THEN 1 END) AS tarefas_pendentes,
    ROUND(
        COUNT(CASE WHEN t.status = 'concluida' THEN 1 END) * 100.0 / 
        NULLIF(COUNT(t.id), 0), 2
    ) AS percentual_conclusao,
    p.created_at,
    p.updated_at
FROM projetos p
LEFT JOIN usuarios u ON p.owner_id = u.id
LEFT JOIN tarefas t ON p.id = t.projeto_id
GROUP BY p.id, p.nome, p.status, u.nome, p.data_inicio, p.data_fim, p.created_at, p.updated_at;
```

**Uso**:
```sql
-- Projetos com baixa conclusão
SELECT * FROM vw_projetos_resumo 
WHERE percentual_conclusao < 50 
ORDER BY percentual_conclusao;
```

### vw_usuarios_atividade

**Descrição**: View com estatísticas de atividade dos usuários

```sql
CREATE VIEW vw_usuarios_atividade AS
SELECT 
    u.id,
    u.nome,
    u.email,
    u.status,
    COUNT(DISTINCT p.id) AS projetos_owned,
    COUNT(DISTINCT t.id) AS tarefas_assigned,
    COUNT(CASE WHEN t.status = 'concluida' THEN 1 END) AS tarefas_concluidas,
    u.ultimo_login,
    u.created_at
FROM usuarios u
LEFT JOIN projetos p ON u.id = p.owner_id
LEFT JOIN tarefas t ON u.id = t.assignee_id
GROUP BY u.id, u.nome, u.email, u.status, u.ultimo_login, u.created_at;
```

---

## ⚙️ Stored Procedures

### sp_criar_projeto_completo

**Descrição**: Procedure para criar projeto com tarefas iniciais

```sql
CREATE OR REPLACE FUNCTION sp_criar_projeto_completo(
    p_nome VARCHAR(200),
    p_descricao TEXT,
    p_owner_id INTEGER,
    p_tarefas JSON
) RETURNS INTEGER AS $$
DECLARE
    v_projeto_id INTEGER;
    v_tarefa JSON;
BEGIN
    -- Criar projeto
    INSERT INTO projetos (nome, descricao, owner_id)
    VALUES (p_nome, p_descricao, p_owner_id)
    RETURNING id INTO v_projeto_id;
    
    -- Criar tarefas se fornecidas
    IF p_tarefas IS NOT NULL THEN
        FOR v_tarefa IN SELECT * FROM json_array_elements(p_tarefas)
        LOOP
            INSERT INTO tarefas (titulo, descricao, projeto_id, prioridade)
            VALUES (
                v_tarefa->>'titulo',
                v_tarefa->>'descricao',
                v_projeto_id,
                COALESCE(v_tarefa->>'prioridade', 'media')
            );
        END LOOP;
    END IF;
    
    RETURN v_projeto_id;
END;
$$ LANGUAGE plpgsql;
```

**Uso**:
```sql
SELECT sp_criar_projeto_completo(
    'Novo Sistema',
    'Sistema de gestão de projetos',
    1,
    '[
        {"titulo": "Análise de requisitos", "prioridade": "alta"},
        {"titulo": "Design da interface", "prioridade": "media"}
    ]'::json
);
```

### sp_relatorio_produtividade

**Descrição**: Gera relatório de produtividade por período

```sql
CREATE OR REPLACE FUNCTION sp_relatorio_produtividade(
    p_data_inicio DATE,
    p_data_fim DATE,
    p_usuario_id INTEGER DEFAULT NULL
) RETURNS TABLE (
    usuario_id INTEGER,
    usuario_nome VARCHAR(100),
    tarefas_concluidas INTEGER,
    horas_trabalhadas INTEGER,
    projetos_ativos INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        u.id,
        u.nome,
        COUNT(CASE WHEN t.status = 'concluida' 
              AND t.updated_at BETWEEN p_data_inicio AND p_data_fim 
              THEN 1 END)::INTEGER,
        COALESCE(SUM(CASE WHEN t.status = 'concluida' 
                     AND t.updated_at BETWEEN p_data_inicio AND p_data_fim 
                     THEN t.horas_trabalhadas END), 0)::INTEGER,
        COUNT(DISTINCT CASE WHEN p.status = 'ativo' THEN p.id END)::INTEGER
    FROM usuarios u
    LEFT JOIN tarefas t ON u.id = t.assignee_id
    LEFT JOIN projetos p ON u.id = p.owner_id
    WHERE (p_usuario_id IS NULL OR u.id = p_usuario_id)
    GROUP BY u.id, u.nome
    ORDER BY COUNT(CASE WHEN t.status = 'concluida' THEN 1 END) DESC;
END;
$$ LANGUAGE plpgsql;
```

---

## 🔄 Triggers

### tr_usuarios_updated_at

**Descrição**: Atualiza automaticamente o campo `updated_at`

```sql
CREATE OR REPLACE FUNCTION fn_update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tr_usuarios_updated_at
    BEFORE UPDATE ON usuarios
    FOR EACH ROW
    EXECUTE FUNCTION fn_update_timestamp();

CREATE TRIGGER tr_projetos_updated_at
    BEFORE UPDATE ON projetos
    FOR EACH ROW
    EXECUTE FUNCTION fn_update_timestamp();

CREATE TRIGGER tr_tarefas_updated_at
    BEFORE UPDATE ON tarefas
    FOR EACH ROW
    EXECUTE FUNCTION fn_update_timestamp();
```

### tr_audit_log

**Descrição**: Registra mudanças importantes para auditoria

```sql
CREATE TABLE audit_log (
    id SERIAL PRIMARY KEY,
    tabela VARCHAR(50) NOT NULL,
    operacao VARCHAR(10) NOT NULL,
    registro_id INTEGER NOT NULL,
    usuario_id INTEGER,
    dados_antigos JSONB,
    dados_novos JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE OR REPLACE FUNCTION fn_audit_trigger()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'DELETE' THEN
        INSERT INTO audit_log (tabela, operacao, registro_id, dados_antigos)
        VALUES (TG_TABLE_NAME, TG_OP, OLD.id, row_to_json(OLD));
        RETURN OLD;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO audit_log (tabela, operacao, registro_id, dados_antigos, dados_novos)
        VALUES (TG_TABLE_NAME, TG_OP, NEW.id, row_to_json(OLD), row_to_json(NEW));
        RETURN NEW;
    ELSIF TG_OP = 'INSERT' THEN
        INSERT INTO audit_log (tabela, operacao, registro_id, dados_novos)
        VALUES (TG_TABLE_NAME, TG_OP, NEW.id, row_to_json(NEW));
        RETURN NEW;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Aplicar trigger nas tabelas importantes
CREATE TRIGGER tr_usuarios_audit
    AFTER INSERT OR UPDATE OR DELETE ON usuarios
    FOR EACH ROW EXECUTE FUNCTION fn_audit_trigger();

CREATE TRIGGER tr_projetos_audit
    AFTER INSERT OR UPDATE OR DELETE ON projetos
    FOR EACH ROW EXECUTE FUNCTION fn_audit_trigger();
```

---

## 🔄 Migrations

### Estrutura de Migrations

```
migrations/
├── 001_initial_schema.sql
├── 002_add_audit_tables.sql
├── 003_add_user_profiles.sql
├── 004_add_project_budget.sql
└── rollback/
    ├── 001_rollback.sql
    ├── 002_rollback.sql
    └── ...
```

### Migration 001: Schema Inicial

```sql
-- migrations/001_initial_schema.sql
-- Criação das tabelas principais
-- Data: 2024-01-15
-- Autor: [Nome do Desenvolvedor]

BEGIN;

-- Tabela de usuários
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    senha_hash VARCHAR(255) NOT NULL,
    status VARCHAR(20) DEFAULT 'ativo' CHECK (status IN ('ativo', 'inativo', 'bloqueado')),
    ultimo_login TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de projetos
CREATE TABLE projetos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(200) NOT NULL,
    descricao TEXT,
    owner_id INTEGER NOT NULL REFERENCES usuarios(id),
    status VARCHAR(20) DEFAULT 'planejamento' CHECK (status IN ('planejamento', 'ativo', 'pausado', 'concluido', 'cancelado')),
    data_inicio DATE,
    data_fim DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de tarefas
CREATE TABLE tarefas (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    descricao TEXT,
    projeto_id INTEGER NOT NULL REFERENCES projetos(id) ON DELETE CASCADE,
    assignee_id INTEGER REFERENCES usuarios(id),
    prioridade VARCHAR(10) DEFAULT 'media' CHECK (prioridade IN ('baixa', 'media', 'alta', 'critica')),
    status VARCHAR(20) DEFAULT 'pendente' CHECK (status IN ('pendente', 'em_progresso', 'concluida', 'cancelada')),
    estimativa_horas INTEGER,
    horas_trabalhadas INTEGER DEFAULT 0,
    data_vencimento DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices básicos
CREATE INDEX idx_usuarios_email ON usuarios(email);
CREATE INDEX idx_usuarios_status ON usuarios(status);
CREATE INDEX idx_projetos_owner_id ON projetos(owner_id);
CREATE INDEX idx_tarefas_projeto_id ON tarefas(projeto_id);
CREATE INDEX idx_tarefas_assignee_id ON tarefas(assignee_id);

-- Triggers para updated_at
CREATE OR REPLACE FUNCTION fn_update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tr_usuarios_updated_at
    BEFORE UPDATE ON usuarios
    FOR EACH ROW
    EXECUTE FUNCTION fn_update_timestamp();

CREATE TRIGGER tr_projetos_updated_at
    BEFORE UPDATE ON projetos
    FOR EACH ROW
    EXECUTE FUNCTION fn_update_timestamp();

CREATE TRIGGER tr_tarefas_updated_at
    BEFORE UPDATE ON tarefas
    FOR EACH ROW
    EXECUTE FUNCTION fn_update_timestamp();

-- Inserir dados iniciais
INSERT INTO usuarios (nome, email, senha_hash) VALUES
('Administrador', 'admin@sistema.com', '$2b$12$...');

COMMIT;
```

### Migration 002: Auditoria

```sql
-- migrations/002_add_audit_tables.sql
-- Adiciona sistema de auditoria
-- Data: 2024-01-20

BEGIN;

-- Tabela de log de auditoria
CREATE TABLE audit_log (
    id SERIAL PRIMARY KEY,
    tabela VARCHAR(50) NOT NULL,
    operacao VARCHAR(10) NOT NULL,
    registro_id INTEGER NOT NULL,
    usuario_id INTEGER,
    dados_antigos JSONB,
    dados_novos JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para auditoria
CREATE INDEX idx_audit_log_tabela ON audit_log(tabela);
CREATE INDEX idx_audit_log_registro_id ON audit_log(registro_id);
CREATE INDEX idx_audit_log_created_at ON audit_log(created_at);

-- Função de auditoria
CREATE OR REPLACE FUNCTION fn_audit_trigger()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'DELETE' THEN
        INSERT INTO audit_log (tabela, operacao, registro_id, dados_antigos)
        VALUES (TG_TABLE_NAME, TG_OP, OLD.id, row_to_json(OLD));
        RETURN OLD;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO audit_log (tabela, operacao, registro_id, dados_antigos, dados_novos)
        VALUES (TG_TABLE_NAME, TG_OP, NEW.id, row_to_json(OLD), row_to_json(NEW));
        RETURN NEW;
    ELSIF TG_OP = 'INSERT' THEN
        INSERT INTO audit_log (tabela, operacao, registro_id, dados_novos)
        VALUES (TG_TABLE_NAME, TG_OP, NEW.id, row_to_json(NEW));
        RETURN NEW;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Aplicar triggers de auditoria
CREATE TRIGGER tr_usuarios_audit
    AFTER INSERT OR UPDATE OR DELETE ON usuarios
    FOR EACH ROW EXECUTE FUNCTION fn_audit_trigger();

CREATE TRIGGER tr_projetos_audit
    AFTER INSERT OR UPDATE OR DELETE ON projetos
    FOR EACH ROW EXECUTE FUNCTION fn_audit_trigger();

CREATE TRIGGER tr_tarefas_audit
    AFTER INSERT OR UPDATE OR DELETE ON tarefas
    FOR EACH ROW EXECUTE FUNCTION fn_audit_trigger();

COMMIT;
```

### Controle de Versão

```python
# migrations/version_control.py
class MigrationManager:
    def __init__(self, db_connection):
        self.db = db_connection
        self._ensure_migration_table()
    
    def _ensure_migration_table(self):
        """Cria tabela de controle de migrations se não existir."""
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS schema_migrations (
                version VARCHAR(50) PRIMARY KEY,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                rollback_sql TEXT
            )
        """)
    
    def apply_migration(self, version, sql_file, rollback_file=None):
        """Aplica uma migration."""
        with open(sql_file, 'r') as f:
            migration_sql = f.read()
        
        rollback_sql = None
        if rollback_file and os.path.exists(rollback_file):
            with open(rollback_file, 'r') as f:
                rollback_sql = f.read()
        
        try:
            self.db.execute(migration_sql)
            self.db.execute(
                "INSERT INTO schema_migrations (version, rollback_sql) VALUES (%s, %s)",
                (version, rollback_sql)
            )
            print(f"Migration {version} applied successfully")
        except Exception as e:
            print(f"Error applying migration {version}: {e}")
            raise
    
    def rollback_migration(self, version):
        """Faz rollback de uma migration."""
        result = self.db.execute(
            "SELECT rollback_sql FROM schema_migrations WHERE version = %s",
            (version,)
        ).fetchone()
        
        if not result or not result[0]:
            raise ValueError(f"No rollback available for migration {version}")
        
        try:
            self.db.execute(result[0])
            self.db.execute(
                "DELETE FROM schema_migrations WHERE version = %s",
                (version,)
            )
            print(f"Migration {version} rolled back successfully")
        except Exception as e:
            print(f"Error rolling back migration {version}: {e}")
            raise
```

---

## ⚡ Performance

### Análise de Consultas

#### Consultas Mais Frequentes

```sql
-- 1. Login de usuário (95% das consultas)
SELECT id, nome, email, status 
FROM usuarios 
WHERE email = $1 AND status = 'ativo';

-- Plano de execução:
-- Index Scan using idx_usuarios_email (cost=0.28..8.30 rows=1)

-- 2. Listar projetos do usuário (78% das consultas)
SELECT p.*, COUNT(t.id) as total_tarefas
FROM projetos p
LEFT JOIN tarefas t ON p.id = t.projeto_id
WHERE p.owner_id = $1
GROUP BY p.id
ORDER BY p.updated_at DESC;

-- 3. Dashboard de tarefas (65% das consultas)
SELECT t.*, p.nome as projeto_nome
FROM tarefas t
JOIN projetos p ON t.projeto_id = p.id
WHERE t.assignee_id = $1 AND t.status IN ('pendente', 'em_progresso')
ORDER BY t.prioridade DESC, t.data_vencimento ASC;
```

#### Otimizações Implementadas

```sql
-- Índice composto para dashboard
CREATE INDEX idx_tarefas_assignee_status_prioridade 
ON tarefas(assignee_id, status, prioridade, data_vencimento)
WHERE status IN ('pendente', 'em_progresso');

-- Índice parcial para projetos ativos
CREATE INDEX idx_projetos_owner_ativo 
ON projetos(owner_id, updated_at) 
WHERE status IN ('ativo', 'planejamento');

-- Estatísticas de tabela
ANALYZE usuarios;
ANALYZE projetos;
ANALYZE tarefas;
```

### Monitoramento de Performance

```sql
-- View para monitorar queries lentas
CREATE VIEW vw_slow_queries AS
SELECT 
    query,
    calls,
    total_time,
    mean_time,
    rows,
    100.0 * shared_blks_hit / nullif(shared_blks_hit + shared_blks_read, 0) AS hit_percent
FROM pg_stat_statements
WHERE mean_time > 100  -- queries com mais de 100ms
ORDER BY mean_time DESC;

-- Monitorar uso de índices
CREATE VIEW vw_index_usage AS
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_tup_read,
    idx_tup_fetch,
    idx_scan,
    CASE WHEN idx_scan = 0 THEN 'Unused' ELSE 'Used' END as status
FROM pg_stat_user_indexes
ORDER BY idx_scan;
```

### Configurações de Performance

```sql
-- postgresql.conf (principais configurações)
shared_buffers = 256MB                  # 25% da RAM
effective_cache_size = 1GB              # 75% da RAM
work_mem = 4MB                          # Para sorts e joins
maintenance_work_mem = 64MB             # Para VACUUM, CREATE INDEX
checkpoint_completion_target = 0.9     # Distribuir checkpoints
wal_buffers = 16MB                      # Write-ahead log buffers
random_page_cost = 1.1                  # Para SSDs
effective_io_concurrency = 200          # Para SSDs
```

---

## 💾 Backup e Recovery

### Estratégia de Backup

#### Backup Completo Diário
```bash
#!/bin/bash
# backup_daily.sh

DB_NAME="sistema_projetos"
BACKUP_DIR="/backups/daily"
DATE=$(date +%Y%m%d_%H%M%S)

# Backup completo
pg_dump -h localhost -U postgres -d $DB_NAME \
    --format=custom \
    --compress=9 \
    --file="$BACKUP_DIR/backup_$DATE.dump"

# Manter apenas 7 dias de backup
find $BACKUP_DIR -name "backup_*.dump" -mtime +7 -delete

# Log do backup
echo "$(date): Backup completed - backup_$DATE.dump" >> /var/log/backup.log
```

#### Backup Incremental
```bash
#!/bin/bash
# backup_incremental.sh

# Backup dos WAL files
pg_basebackup -h localhost -U postgres -D /backups/base -Ft -z -P

# Archive WAL files
archive_command = 'cp %p /backups/wal/%f'
```

### Scripts de Recovery

#### Recovery Point-in-Time
```bash
#!/bin/bash
# recovery_pit.sh

BACKUP_FILE="/backups/daily/backup_20240115_120000.dump"
TARGET_TIME="2024-01-15 14:30:00"

# Restaurar backup base
pg_restore -h localhost -U postgres -d sistema_projetos_recovery \
    --clean --create $BACKUP_FILE

# Aplicar WAL files até o ponto desejado
# (configurar recovery.conf)
echo "restore_command = 'cp /backups/wal/%f %p'" > recovery.conf
echo "recovery_target_time = '$TARGET_TIME'" >> recovery.conf
```

### Monitoramento de Backup

```sql
-- View para monitorar backups
CREATE VIEW vw_backup_status AS
SELECT 
    'daily' as backup_type,
    pg_size_pretty(pg_database_size(current_database())) as db_size,
    (SELECT modification FROM pg_stat_file('/backups/daily/latest.dump')) as last_backup,
    CASE 
        WHEN (SELECT modification FROM pg_stat_file('/backups/daily/latest.dump')) > CURRENT_TIMESTAMP - INTERVAL '25 hours'
        THEN 'OK'
        ELSE 'OUTDATED'
    END as status;
```

---

## 📚 Glossário

### Termos Técnicos

| Termo | Definição |
|-------|-----------|
| **ACID** | Atomicidade, Consistência, Isolamento, Durabilidade |
| **CASCADE** | Ação que se propaga para registros relacionados |
| **Constraint** | Regra que garante integridade dos dados |
| **Foreign Key** | Chave que referencia outra tabela |
| **Index** | Estrutura que acelera consultas |
| **Migration** | Script de alteração de schema |
| **Primary Key** | Chave única que identifica um registro |
| **Trigger** | Função executada automaticamente |
| **View** | Consulta salva como tabela virtual |
| **WAL** | Write-Ahead Log para recovery |

### Termos de Negócio

| Termo | Definição |
|-------|-----------|
| **Assignee** | Usuário responsável por uma tarefa |
| **Owner** | Usuário proprietário de um projeto |
| **Soft Delete** | Marcação de exclusão sem remoção física |
| **Status** | Estado atual de um registro |
| **Audit Trail** | Rastro de auditoria das alterações |

### Convenções

| Convenção | Exemplo | Uso |
|-----------|---------|-----|
| `snake_case` | `nome_usuario` | Nomes de tabelas e colunas |
| `pk_[tabela]` | `pk_usuarios` | Primary keys |
| `fk_[origem]_[destino]` | `fk_tarefas_usuarios` | Foreign keys |
| `idx_[tabela]_[coluna]` | `idx_usuarios_email` | Índices |
| `tr_[tabela]_[acao]` | `tr_usuarios_audit` | Triggers |
| `vw_[nome]` | `vw_projetos_resumo` | Views |
| `sp_[nome]` | `sp_criar_projeto` | Stored procedures |

---

<div align="center">

**Mantido por**: Equipe de Banco de Dados - [email-dba]  
**Última Atualização**: [DD/MM/AAAA]  
**Versão do Schema**: [X.Y.Z]

---

**Para suporte com banco de dados**: [email-suporte-db]

</div>