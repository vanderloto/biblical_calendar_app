# Gerenciamento de Efemérides - Biblical Calendar App

<div align="center">

**Documentação técnica sobre arquivos de efemérides astronômicas**

[![Skyfield](https://img.shields.io/badge/Skyfield-1.45+-blue)](https://rhodesmill.org/skyfield/)
[![DE421](https://img.shields.io/badge/Ephemeris-DE421-green)](https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/)

</div>

---

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Arquivo DE421.bsp](#-arquivo-de421bsp)
- [Implementação Atual](#-implementação-atual)
- [Atualizações Futuras](#-atualizações-futuras)
- [Troubleshooting](#-troubleshooting)

---

## 🎯 Visão Geral

### O que são Efemérides

Efemérides são arquivos que contêm dados precisos sobre posições de corpos celestes (Sol, Lua, planetas) ao longo do tempo. O Biblical Calendar App usa estes dados para calcular:

- **Luas Novas**: Conjunções Sol-Lua precisas
- **Fases Lunares**: Crescente, Cheia, Minguante
- **Estações**: Equinócios e solstícios
- **Posições**: Elongação e altitude da Lua

### Biblioteca Skyfield

O projeto usa a biblioteca **Skyfield** que:
- Carrega automaticamente arquivos de efemérides
- Fornece interface Python para cálculos astronômicos
- Suporta múltiplos formatos de efemérides da NASA/JPL

---

## 📊 Arquivo DE421.bsp

### Características Técnicas

| Propriedade | Valor | Descrição |
|-------------|-------|-----------|
| **Nome** | `de421.bsp` | Desenvolvimento Ephemeris 421 |
| **Período** | 1900-2050 | 150 anos de cobertura |
| **Precisão** | Sub-arcsegundo | Precisão astronômica profissional |
| **Tamanho** | ~17 MB | Download único |
| **Origem** | NASA/JPL | Jet Propulsion Laboratory |

### Cobertura Temporal

```python
# Período coberto pelo DE421
INICIO = date(1900, 1, 1)
FIM = date(2050, 12, 31)

# Para o Biblical Calendar App
ANO_MINIMO = 1900  # Limite inferior
ANO_MAXIMO = 2050  # Limite superior
```

### Adequação para o Projeto

✅ **Suficiente para uso normal**: Cobre período 1900-2050
✅ **Precisão adequada**: Sub-arcsegundo para cálculos lunares
✅ **Tamanho razoável**: 17 MB é aceitável para download
✅ **Padrão da indústria**: Usado por software astronômico profissional

---

## 🔧 Implementação Atual

### Código de Carregamento

```python
# src/biblical_calendar/calendar.py
from skyfield import api

# Carregamento automático do DE421
TS = api.load.timescale()
Eph = api.load('de421.bsp')  # Download automático se não existir
```

### Localização do Arquivo

O Skyfield armazena o arquivo em:

**Windows:**
```
%USERPROFILE%\.skyfield\de421.bsp
```

**Linux/macOS:**
```
~/.skyfield/de421.bsp
```

### Verificação de Status

```python
def check_ephemeris_status():
    """Verifica status do arquivo de efemérides."""
    import os
    from skyfield.api import load
    
    # Caminho do arquivo
    loader = load
    ephemeris_path = loader.path_to('de421.bsp')
    
    if os.path.exists(ephemeris_path):
        size_mb = os.path.getsize(ephemeris_path) / (1024 * 1024)
        print(f"✅ DE421.bsp encontrado: {ephemeris_path}")
        print(f"📊 Tamanho: {size_mb:.1f} MB")
        return True
    else:
        print("❌ DE421.bsp não encontrado - será baixado automaticamente")
        return False
```

---

## 🔄 Atualizações Futuras

### Quando Atualizar

| Cenário | Ação Recomendada | Nova Efeméride |
|---------|------------------|----------------|
| **Uso até 2050** | Manter DE421 | Não necessário |
| **Uso após 2050** | Atualizar obrigatório | DE430 ou DE440 |
| **Maior precisão** | Opcional | DE430/DE440 |
| **Pesquisa acadêmica** | Recomendado | DE440 (mais recente) |

### Opções de Atualização

#### DE430 (Recomendado para futuro)
```python
# Substitua na linha de carregamento
Eph = api.load('de430.bsp')  # Cobre 1550-2650
```

**Características:**
- **Período**: 1550-2650 (1100 anos)
- **Tamanho**: ~128 MB
- **Precisão**: Melhorada vs DE421

#### DE440 (Mais recente)
```python
# Para máxima precisão
Eph = api.load('de440.bsp')  # Cobre 1550-2650
```

**Características:**
- **Período**: 1550-2650
- **Tamanho**: ~128 MB  
- **Precisão**: Estado da arte (2020+)

### Implementação de Atualização

```python
def load_best_ephemeris():
    """Carrega a melhor efeméride disponível."""
    from skyfield.api import load
    
    # Tentar DE440 primeiro (mais recente)
    try:
        return load('de440.bsp')
    except Exception:
        pass
    
    # Fallback para DE430
    try:
        return load('de430.bsp')
    except Exception:
        pass
    
    # Fallback para DE421 (atual)
    return load('de421.bsp')

# Uso futuro
# Eph = load_best_ephemeris()
```

---

## 🔧 Troubleshooting

### Problemas Comuns

#### 1. Falha no Download
```
ConnectionError: Failed to download de421.bsp
```

**Soluções:**
- Verificar conexão com internet
- Tentar novamente (download pode ser interrompido)
- Download manual do arquivo

#### 2. Arquivo Corrompido
```
ValueError: Invalid SPK file
```

**Soluções:**
- Deletar arquivo existente
- Forçar novo download
- Verificar espaço em disco

#### 3. Permissões de Escrita
```
PermissionError: Cannot write to ~/.skyfield/
```

**Soluções:**
- Verificar permissões da pasta
- Executar como administrador (Windows)
- Criar pasta manualmente

### Download Manual

Se o download automático falhar:

1. **Baixar manualmente:**
   ```
   https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/de421.bsp
   ```

2. **Colocar na pasta Skyfield:**
   - Windows: `%USERPROFILE%\.skyfield\`
   - Linux/macOS: `~/.skyfield/`

3. **Verificar integridade:**
   ```python
   from skyfield.api import load
   eph = load('de421.bsp')  # Deve carregar sem erro
   ```

### Limpeza de Cache

```python
def clear_skyfield_cache():
    """Remove arquivos de cache do Skyfield."""
    import os
    import shutil
    from skyfield.api import load
    
    cache_dir = load.directory
    if os.path.exists(cache_dir):
        shutil.rmtree(cache_dir)
        print(f"Cache limpo: {cache_dir}")
```

---

## 📈 Recomendações

### Para Uso Atual (2025)
- ✅ **Manter DE421**: Adequado para período 1900-2050
- ✅ **Monitorar performance**: Verificar se download ocorre corretamente
- ✅ **Documentar limitações**: Informar usuários sobre período coberto

### Para Uso Futuro (2050+)
- 🔄 **Planejar migração**: DE430 ou DE440 antes de 2050
- 📊 **Avaliar impacto**: Arquivo maior (128 MB vs 17 MB)
- 🧪 **Testar compatibilidade**: Verificar se não quebra funcionalidades

### Para Pesquisa Acadêmica
- 🎯 **Considerar DE440**: Máxima precisão disponível
- 📝 **Documentar escolha**: Justificar efeméride usada
- 🔬 **Validar resultados**: Comparar com outras fontes

---

## 📚 Referências

### Documentação Oficial
- **[Skyfield Documentation](https://rhodesmill.org/skyfield/)** - Biblioteca Python
- **[NASA/JPL Ephemeris](https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/)** - Arquivos oficiais
- **[DE421 Specification](https://ipnpr.jpl.nasa.gov/progress_report/42-178/178C.pdf)** - Especificação técnica

### Comparações
- **[Ephemeris Comparison](https://rhodesmill.org/skyfield/planets.html)** - Diferenças entre versões
- **[Accuracy Analysis](https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/aareadme_de430-de431.txt)** - Análise de precisão

---

<div align="center">

**Mantido por**: Equipe de Desenvolvimento DATAMETRIA  
**Última Atualização**: 31/08/2025  
**Versão**: 1.1.0

---

**Para questões técnicas**: vander.loto@outlook.com

</div>