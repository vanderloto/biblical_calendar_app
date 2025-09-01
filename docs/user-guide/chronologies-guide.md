# Guia de Cronologias - Biblical Calendar App

<div align="center">

**Sistemas Cronológicos Comparativos**

[![Ussher](https://img.shields.io/badge/Ussher-4004%20AC-blue)](https://en.wikipedia.org/wiki/Ussher_chronology)
[![Hebrew](https://img.shields.io/badge/Hebrew-AM-green)](https://en.wikipedia.org/wiki/Hebrew_calendar)
[![Gregorian](https://img.shields.io/badge/Gregorian-DC-orange)](https://en.wikipedia.org/wiki/Gregorian_calendar)

</div>

---

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Cronologia de Ussher](#-cronologia-de-ussher)
- [Calendário Hebraico](#-calendário-hebraico)
- [Calendário Gregoriano](#-calendário-gregoriano)
- [Comparações](#-comparações)
- [Uso na Interface](#-uso-na-interface)

---

## 🎯 Visão Geral

### O que são Cronologias

O Biblical Calendar App exibe três sistemas cronológicos diferentes para fornecer contexto histórico e educacional completo:

1. **Cronologia de Ussher**: Baseada na criação do mundo em 4004 AC
2. **Calendário Hebraico**: Sistema judaico tradicional (Anno Mundi)
3. **Calendário Gregoriano**: Sistema padrão mundial moderno

### Por que Três Sistemas?

- **Contexto Histórico**: Diferentes tradições de contagem de tempo
- **Valor Educacional**: Compreensão de perspectivas cronológicas
- **Referência Acadêmica**: Facilita estudos bíblicos e históricos
- **Comparação Visual**: Entendimento das diferenças entre sistemas

---

## 📜 Cronologia de Ussher

### História

A Cronologia de Ussher foi desenvolvida pelo Arcebispo James Ussher (1581-1656) baseada em:
- **Genealogias Bíblicas**: Cálculos a partir de Adão
- **Eventos Históricos**: Correlação com história secular
- **Textos Antigos**: Análise de manuscritos hebraicos e gregos

### Características

| Aspecto | Detalhes |
|---------|----------|
| **Criação** | 4004 AC (23 de outubro) |
| **Base** | Genealogias do Antigo Testamento |
| **Método** | Soma de idades patriarcais |
| **Uso** | Tradição cristã protestante |

### Cálculo no App

```python
def calculate_ussher_year(gregorian_year: int) -> int:
    """Cronologia de Ussher: Criação em 4004 AC"""
    return gregorian_year + 4004
```

**Exemplo**: 2025 DC = 6029 AM (Ussher)

### Eventos Principais

- **4004 AC**: Criação do mundo
- **2348 AC**: Dilúvio de Noé
- **2016 AC**: Nascimento de Abraão
- **1491 AC**: Êxodo do Egito
- **1012 AC**: Reinado de Davi

---

## 🕎 Calendário Hebraico

### História

O calendário hebraico (Anno Mundi) é o sistema cronológico oficial do judaísmo:
- **Origem**: Tradição rabínica antiga
- **Base**: Cálculos talmúdicos
- **Uso**: Comunidades judaicas mundiais
- **Precisão**: Refinado ao longo dos séculos

### Características

| Aspecto | Detalhes |
|---------|----------|
| **Criação** | 3761 AC (aproximadamente) |
| **Base** | Tradição rabínica |
| **Método** | Cálculos talmúdicos |
| **Uso** | Judaísmo mundial |

### Cálculo no App

```python
def calculate_hebrew_year(gregorian_year: int) -> int:
    """Calendário hebraico: Anno Mundi"""
    return gregorian_year + 3760
```

**Exemplo**: 2025 DC = 5785 AM (Hebraico)

### Eventos Principais

- **1 AM**: Criação do mundo
- **1656 AM**: Dilúvio de Noé
- **2048 AM**: Nascimento de Abraão
- **2448 AM**: Êxodo do Egito
- **2924 AM**: Construção do Primeiro Templo

---

## ⛪ Calendário Gregoriano

### História

O calendário gregoriano é o sistema padrão mundial:
- **Origem**: Papa Gregório XIII (1582)
- **Base**: Era Cristã (Anno Domini)
- **Reforma**: Correção do calendário juliano
- **Uso**: Padrão internacional

### Características

| Aspecto | Detalhes |
|---------|----------|
| **Marco Zero** | Nascimento de Cristo |
| **Base** | Era Cristã (AD/DC) |
| **Método** | Cálculo solar |
| **Uso** | Mundial |

### Eventos Principais

- **1 DC**: Nascimento de Jesus Cristo
- **70 DC**: Destruição do Segundo Templo
- **313 DC**: Édito de Milão
- **1582 DC**: Reforma gregoriana
- **1948 DC**: Criação de Israel

---

## 📊 Comparações

### Tabela Comparativa

| Ano Gregoriano | Ussher (AM) | Hebraico (AM) | Diferença |
|----------------|-------------|---------------|-----------|
| **2025 DC** | 6029 | 5785 | 244 anos |
| **2000 DC** | 6004 | 5760 | 244 anos |
| **1000 DC** | 5004 | 4760 | 244 anos |
| **1 DC** | 4005 | 3761 | 244 anos |

### Diferenças Principais

#### Ussher vs Hebraico
- **Diferença**: ~244 anos
- **Causa**: Métodos de cálculo diferentes
- **Genealogias**: Interpretações distintas
- **Tradições**: Cristã vs Judaica

#### Ambos vs Gregoriano
- **Ussher**: +4004 anos
- **Hebraico**: +3760 anos
- **Referência**: Criação vs Nascimento de Cristo

### Gráfico Temporal

```
Criação (Ussher)    Criação (Hebraico)    Nascimento Cristo    Hoje
     |                      |                     |              |
  4004 AC               3761 AC                1 DC          2025 DC
     |<------ 6029 AM (Ussher) ----------------------->|
     |         |<------ 5785 AM (Hebraico) ----------->|
     |         |              |<-- 2025 DC -->|
```

---

## 🖥️ Uso na Interface

### Localização das Cronologias

#### 1. Cabeçalho do Calendário Visual
```
Mês 1 - Nissan (start 2025-03-30, 29 dias)
Ussher: 6029 AM | Hebraico: 5785 | Gregoriano: 2025
```

#### 2. Painel de Eventos do Dia
```
📅 Cronologias do Ano:
   Ussher: 6029 AM (desde Criação)
   Hebraico: 5785 AM (Anno Mundi)
   Gregoriano: 2025 DC (Era Cristã)
```

#### 3. Legenda do Painel Direito
```
Cronologias:
Ussher: Desde Criação (4004 AC)
Hebraico: Anno Mundi (AM)
Gregoriano: Era Cristã (DC)
```

### Atualização Dinâmica

- **Navegação**: Cronologias atualizam ao mudar mês/ano
- **Clique no Dia**: Mostra cronologias da data específica
- **Contexto**: Sempre relacionado ao ano sendo visualizado

---

## 📚 Valor Educacional

### Para Estudantes

- **Perspectiva Histórica**: Diferentes formas de contar tempo
- **Contexto Bíblico**: Cronologias usadas em estudos bíblicos
- **Comparação**: Entendimento das diferenças metodológicas

### Para Pesquisadores

- **Referência Múltipla**: Três sistemas em uma interface
- **Contexto Acadêmico**: Facilita citações e referências
- **Análise Comparativa**: Base para estudos cronológicos

### Para Curiosos

- **Cultura Geral**: Conhecimento sobre sistemas de tempo
- **História**: Compreensão de tradições cronológicas
- **Religião**: Perspectivas judaica e cristã

---

## 🔍 Detalhes Técnicos

### Implementação

```python
# Funções de cálculo
def calculate_ussher_year(gregorian_year: int) -> int:
    """Cronologia de Ussher: Criação em 4004 AC"""
    return gregorian_year + 4004

def calculate_hebrew_year(gregorian_year: int) -> int:
    """Calendário hebraico: Anno Mundi"""
    return gregorian_year + 3760

# Uso na interface
gregorian_year = date.year
ussher_year = calculate_ussher_year(gregorian_year)
hebrew_year = calculate_hebrew_year(gregorian_year)
```

### Precisão

- **Ussher**: Baseado em 4004 AC exato
- **Hebraico**: Aproximação de +3760 anos
- **Gregoriano**: Ano civil padrão

### Limitações

- **Simplificação**: Cálculos aproximados
- **Variações**: Diferentes tradições podem variar
- **Contexto**: Fins educacionais, não definitivos

---

## 📖 Referências

### Fontes Acadêmicas

- **Ussher Chronology**: "Annales Veteris Testamenti" (1650)
- **Hebrew Calendar**: Talmud Babilônico, Tratado Rosh Hashaná
- **Gregorian Calendar**: Bula "Inter gravissimas" (1582)

### Estudos Modernos

- **Finegan, Jack**: "Handbook of Biblical Chronology" (1998)
- **Thiele, Edwin**: "The Mysterious Numbers of the Hebrew Kings" (1983)
- **Hughes, David**: "The Star of Bethlehem Mystery" (1979)

### Recursos Online

- **[Ussher Chronology](https://en.wikipedia.org/wiki/Ussher_chronology)** - Wikipedia
- **[Hebrew Calendar](https://www.hebcal.com/)** - HebCal
- **[Gregorian Calendar](https://www.timeanddate.com/)** - Time and Date

---

<div align="center">

**Mantido por**: Equipe de Desenvolvimento DATAMETRIA  
**Última Atualização**: 31/08/2025  
**Versão**: 1.0.0

---

**Para questões sobre cronologias**: vander.loto@outlook.com

</div>