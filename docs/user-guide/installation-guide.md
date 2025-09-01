# Guia de Instalação - Biblical Calendar App

## Pré-requisitos

### Sistema Operacional
- Windows 10+ / macOS 10.15+ / Linux Ubuntu 20.04+
- 1 GB RAM (recomendado)
- 200 MB espaço em disco
- Conexão com internet (para download inicial)

### Software Necessário
- Python 3.11 ou superior
- Poetry (gerenciador de dependências)

## Instalação Passo a Passo

### 1. Verificar Python
```bash
python --version
# Deve mostrar 3.11 ou superior
```

### 2. Instalar Poetry
```bash
# Windows/macOS/Linux
curl -sSL https://install.python-poetry.org | python3 -
```

### 3. Clonar Repositório
```bash
git clone https://github.com/vanderloto/biblical_calendar_app.git
cd biblical_calendar_app
```

### 4. Instalar Dependências
```bash
poetry install
```

### 5. Executar Aplicação
```bash
poetry run biblical-calendar
```

## Verificação da Instalação

### Teste Básico
```bash
poetry run python -c "from biblical_calendar import BiblicalCalendarApp; print('OK')"
```

### Teste de Dependências
```bash
poetry run python -c "import skyfield, pandas, icalendar; print('Dependências OK')"
```

## Troubleshooting

### Erro: Python não encontrado
**Solução**: Instalar Python 3.11+ do site oficial

### Erro: Poetry não encontrado
**Solução**: Adicionar Poetry ao PATH do sistema

### Erro: Dependências não instaladas
**Solução**: Executar `poetry install --no-cache`