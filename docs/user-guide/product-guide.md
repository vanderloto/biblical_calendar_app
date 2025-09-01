# Guia do Produto - Biblical Calendar App

<div align="center">

**Versão**: 1.0.0 | **Última Atualização**: 27/01/2025

[![Produto](https://img.shields.io/badge/produto-ativo-green)](https://github.com/vanderloto/biblical_calendar_app)
[![Versão](https://img.shields.io/badge/versão-1.0.0-blue)](https://github.com/vanderloto/biblical_calendar_app)
[![Usuários](https://img.shields.io/badge/usuários-comunidade-orange)](https://github.com/vanderloto/biblical_calendar_app)

[🚀 Download](https://github.com/vanderloto/biblical_calendar_app) • [📊 Documentação](README.md) • [💬 Suporte](mailto:vander.loto@outlook.com)

</div>

---

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Primeiros Passos](#-primeiros-passos)
- [Funcionalidades Principais](#-funcionalidades-principais)
- [Guia do Usuário](#-guia-do-usuário)
- [Casos de Uso](#-casos-de-uso)
- [Configurações](#-configurações)
- [Exportação](#-exportação)
- [Troubleshooting](#-troubleshooting)
- [FAQ](#-faq)
- [Suporte](#-suporte)

---

## 🎯 Visão Geral

### O que é o Biblical Calendar App?

O Biblical Calendar App é um calendário bíblico-lunissolar dinâmico que calcula com precisão astronômica o início de cada mês baseado nas luas novas observáveis em Jerusalém. O sistema oferece uma interface visual intuitiva para explorar festivais bíblicos, fases lunares e estações astronômicas.

### Para quem é este produto?

- **👤 Estudantes de Teologia**: Pesquisadores e acadêmicos interessados em cronologia bíblica
- **👥 Comunidades Religiosas**: Grupos que seguem o calendário bíblico para observância de festivais
- **🏢 Educadores**: Professores de história, astronomia e estudos religiosos
- **🔬 Pesquisadores**: Especialistas em calendários antigos e astronomia histórica

### Principais Benefícios

| Benefício | Descrição | Impacto |
|-----------|-----------|---------|
| **⚡ Precisão Astronômica** | Cálculos baseados em efemérides DE421 | Dados confiáveis para pesquisa |
| **📊 Interface Visual** | Calendário interativo com navegação intuitiva | Facilita compreensão e uso |
| **🔒 Flexibilidade** | Opção entre métodos astronômico e observacional | Atende diferentes necessidades |

---

## 🚀 Primeiros Passos

### Requisitos do Sistema

- **Sistema Operacional**: Windows 10+, macOS 10.15+, Linux Ubuntu 20.04+
- **Python**: 3.11 ou superior
- **Memória**: 1 GB RAM recomendado
- **Espaço**: 200 MB disponível
- **Internet**: Para download inicial de efemérides

### Instalação Rápida

```bash
# 1. Clone o repositório
git clone https://github.com/vanderloto/biblical_calendar_app.git
cd biblical_calendar_app

# 2. Instale Poetry (se necessário)
curl -sSL https://install.python-poetry.org | python3 -

# 3. Instale dependências
poetry install

# 4. Execute a aplicação
poetry run biblical-calendar
```

### Primeiro Uso

1. **Inicialização**: A aplicação baixará automaticamente os dados astronômicos (de421.bsp)
2. **Configuração**: Defina o ano de referência (padrão: ano atual)
3. **Método**: Escolha entre lua nova astronômica ou primeira crescente visível
4. **Geração**: Clique em "Gerar" para calcular o calendário
5. **Exploração**: Navegue pelas abas e explore as funcionalidades

---

## ⚡ Funcionalidades Principais

### Calendário Visual Interativo

**Descrição**: Interface principal com visualização mensal estilo calendário gregoriano

**Como usar**:
1. Acesse a aba "Calendário Visual"
2. Use os botões de navegação (◀ Anterior, Hoje, Próximo ▶)
3. Clique em qualquer dia para ver eventos detalhados
4. Observe as anotações visuais: ★ (festivais), 🌑 (fases lunares), 🌍 (estações)

**Dicas**:
- 💡 O dia atual é destacado com fundo azul
- ⚠️ A navegação é contínua entre anos (1-2100)

### Festivais Bíblicos Completos

**Descrição**: 10 festivais bíblicos principais com nomes hebraicos e traduções

**Localização**: Aba "Festas & Yeshua"

**Festivais incluídos**:
- **Primavera**: Pessach, Chag HaMatzot, Omer Reshit
- **Verão**: Shavuot
- **Outono**: Rosh Hashaná, Yom Kippur, Sukkot
- **Outros**: Chanucá, Purim

### Cálculos Astronômicos

**Descrição**: Precisão científica baseada em Skyfield e efemérides DE421

**Exemplo prático**:
```
Cenário: Calcular Nissan 1 para 2024
Ação: Definir ano 2024 e gerar calendário
Resultado: Nissan 1 = 09/04/2024 (baseado na lua nova após equinócio)
```

---

## 📖 Guia do Usuário

### Interface Principal

#### Barra de Controles (Superior)
- **Ano referência**: Campo para inserir o ano desejado
- **Heurística**: Checkbox para usar primeira crescente visível
- **Gerar**: Botão para calcular o calendário
- **Exportar**: Botões para CSV e ICS

#### Abas de Navegação
- **🗓️ Calendário Visual**: Visualização principal interativa
- **📋 Meses (lista)**: Tabela com todos os meses e durações
- **🎉 Festas & Yeshua**: Lista de festivais e eventos relacionados
- **🌍 Estações**: Informações astronômicas para Jerusalém e São Paulo

### Navegação no Calendário

#### Controles de Navegação
| Botão | Função |
|-------|--------|
| **◀ Anterior** | Mês anterior (com transição automática de ano) |
| **Hoje** | Navega para o mês atual |
| **Próximo ▶** | Próximo mês (com transição automática de ano) |

#### Painel "Eventos do Dia"
- **Localização**: Lado direito da tela
- **Conteúdo**: Eventos do dia selecionado com descrições
- **Formato**: Nomes em negrito, descrições em texto normal
- **Informações**: Estação astronômica atual para ambas localidades

### Símbolos e Legendas

#### Anotações Visuais
- **★**: Festival bíblico (nome hebraico)
- **🌑**: Lua Nova (início do mês)
- **🌓**: Quarto Crescente
- **🌕**: Lua Cheia
- **🌗**: Quarto Minguante
- **🌍**: Estação astronômica (equinócios/solstícios)
- **Fundo azul**: Dia atual

---

## 💼 Casos de Uso

### Caso de Uso 1: Pesquisa Acadêmica

**Objetivo**: Determinar datas precisas de festivais bíblicos para um ano específico

**Persona**: Professor de Teologia

**Cenário**:
> "Como professor, preciso das datas exatas dos festivais bíblicos para 2024 para preparar meu cronograma de aulas sobre o calendário hebraico"

**Solução**:
1. Abrir a aplicação
2. Definir ano como 2024
3. Manter método astronômico (padrão)
4. Clicar em "Gerar"
5. Acessar aba "Festas & Yeshua"
6. Exportar dados em CSV para análise

**Tempo estimado**: 3 minutos

### Caso de Uso 2: Observância Religiosa

**Objetivo**: Planejar observância de festivais baseada na primeira crescente visível

**Persona**: Líder de comunidade religiosa

**Pré-requisitos**:
- Conhecimento sobre diferença entre métodos astronômico e observacional
- Acesso à aplicação

**Processo**:
```
Input: Ano da observância desejada
Processo: Ativar heurística de visibilidade + gerar calendário
Output: Datas ajustadas para primeira crescente visível em Jerusalém
```

### Caso de Uso 3: Educação Astronômica

**Objetivo**: Demonstrar relação entre astronomia e calendários antigos

**Variações**:
- **Cenário A**: Comparar fases lunares com início dos meses
- **Cenário B**: Mostrar diferenças sazonais entre hemisférios

---

## ⚙️ Configurações

### Métodos de Cálculo

#### Lua Nova Astronômica (Padrão)
- **Descrição**: Baseado no momento exato da conjunção Sol-Lua
- **Uso**: Estudos acadêmicos e pesquisa científica
- **Precisão**: Máxima (baseado em efemérides DE421)

#### Primeira Crescente Visível (Heurística)
- **Descrição**: Simula observação visual em Jerusalém
- **Critérios**: Elongação ≥ 10° e altitude ≥ 3°
- **Uso**: Prática religiosa tradicional

### Localidades de Referência

#### Jerusalém (Principal)
- **Coordenadas**: 31.7683°N, 35.2137°E
- **Timezone**: Asia/Jerusalem
- **Uso**: Cálculos principais e heurística de visibilidade

#### São Paulo (Comparação)
- **Coordenadas**: 23.5505°S, 46.6333°W
- **Timezone**: America/Sao_Paulo
- **Uso**: Comparação sazonal (Hemisfério Sul)

### Personalização da Interface

#### Navegação
- **Range de Anos**: 1-2100 (transição automática)
- **Idioma**: Português (nomes hebraicos + traduções)
- **Formato de Data**: DD/MM/AAAA (gregoriano)

---

## 📤 Exportação

### Exportação CSV (Meses)

**Descrição**: Dados tabulares dos meses calculados

**Como exportar**:
1. Gere o calendário para o ano desejado
2. Clique em "Exportar CSV (meses)"
3. Escolha local para salvar o arquivo

**Formato do arquivo**:
```csv
index,name,start,end,days
1,Nissan,2024-04-09,2024-05-07,29
2,Iyar,2024-05-08,2024-06-05,29
...
```

**Uso**: Análise de dados, planilhas, pesquisa

### Exportação ICS (Festivais)

**Descrição**: Calendário compatível com aplicações padrão

**Como exportar**:
1. Gere o calendário com festivais
2. Clique em "Exportar ICS (festas)"
3. Salve o arquivo .ics

**Compatibilidade**:
- Google Calendar
- Microsoft Outlook
- Apple Calendar
- Thunderbird
- Outros aplicativos compatíveis com iCalendar

**Conteúdo**: Todos os festivais bíblicos e eventos de Yeshua

---

## 🔧 Troubleshooting

### Problemas Comuns

#### Aplicação não inicia
**Sintomas**: Erro ao executar `poetry run biblical-calendar`

**Soluções**:
1. **Verificar Python**: Confirme versão 3.11+
   ```bash
   python --version
   ```
2. **Reinstalar dependências**:
   ```bash
   poetry install --no-cache
   ```
3. **Verificar Poetry**: Atualize se necessário
   ```bash
   poetry --version
   poetry self update
   ```

#### Download de efemérides falha
**Sintomas**: Erro "Failed to download de421.bsp"

**Soluções**:
1. **Verificar conexão**: Teste acesso à internet
2. **Proxy/Firewall**: Configure se necessário
3. **Download manual**: Baixe de421.bsp do site da NASA
4. **Espaço em disco**: Verifique 200MB+ disponível

#### Cálculos inconsistentes
**Sintomas**: Datas diferentes do esperado

**Soluções**:
1. **Verificar método**: Confirme se está usando o método correto
2. **Ano válido**: Use anos entre 1-2100
3. **Comparar fontes**: Verifique com outras referências astronômicas

### Códigos de Erro

| Código | Descrição | Solução |
|--------|-----------|---------|
| **ImportError** | Dependência não encontrada | `poetry install` |
| **FileNotFoundError** | Arquivo de efemérides ausente | Aguardar download automático |
| **ValueError** | Ano inválido | Usar ano entre 1-2100 |

### Logs e Diagnóstico

#### Verificação do Sistema
```bash
# Verificar instalação
poetry run python -c "from biblical_calendar import BiblicalCalendarApp; print('OK')"

# Testar importações
poetry run python -c "import skyfield, pandas, icalendar; print('Dependências OK')"
```

---

## ❓ FAQ

### Geral

**P: O que torna este calendário diferente de outros calendários hebraicos?**
R: Usa cálculos astronômicos precisos baseados em efemérides científicas (DE421) e oferece opção de heurística de visibilidade da primeira crescente, simulando a observação histórica em Jerusalém.

**P: Posso usar para anos muito antigos ou futuros?**
R: Sim, suporta anos de 1 a 2100 com precisão astronômica. Para anos anteriores a 1900, a precisão pode ser ligeiramente reduzida.

### Funcionalidades

**P: Como funciona a heurística de visibilidade?**
R: Simula a observação da primeira crescente em Jerusalém, considerando elongação ≥ 10° e altitude ≥ 3° no pôr do sol. Verifica até 3 noites após a lua nova astronômica.

**P: Por que alguns anos têm 13 meses?**
R: Anos embolísmicos ocorrem quando há 13 luas novas em aproximadamente 370 dias. O sistema detecta automaticamente e adiciona Adar I e Adar II.

### Uso Prático

**P: Posso integrar com meu calendário pessoal?**
R: Sim, exporte em formato ICS e importe no Google Calendar, Outlook ou qualquer aplicativo compatível com iCalendar.

**P: Os horários são em que timezone?**
R: Cálculos astronômicos são em UTC. Horários de nascer/pôr do sol são no timezone local de cada cidade (Jerusalém/São Paulo).

### Técnico

**P: Qual a precisão dos cálculos?**
R: Usa efemérides DE421 da NASA/JPL, com precisão de segundos para posições planetárias. Heurística de visibilidade tem margem de ±1 dia.

**P: Funciona offline?**
R: Após o download inicial das efemérides (de421.bsp ~17MB), funciona completamente offline.

---

## 🆘 Suporte

### Canais de Atendimento

#### Suporte Técnico
- **📧 Email**: vander.loto@outlook.com
- **🐛 Issues**: [GitHub Issues](https://github.com/vanderloto/biblical_calendar_app/issues)
- **💬 Discussões**: [GitHub Discussions](https://github.com/vanderloto/biblical_calendar_app/discussions)

#### Recursos de Autoajuda
- **📚 Documentação**: [README.md](README.md)
- **📖 Código Fonte**: [GitHub Repository](https://github.com/vanderloto/biblical_calendar_app)
- **📋 Changelog**: [CHANGELOG.md](CHANGELOG.md)

### Como Reportar Problemas

1. **Acesse**: [GitHub Issues](https://github.com/vanderloto/biblical_calendar_app/issues)
2. **Categoria**: Selecione Bug Report ou Feature Request
3. **Descrição**: Seja específico sobre o problema
4. **Ambiente**: Inclua SO, versão Python, versão da aplicação
5. **Reprodução**: Passos para reproduzir o problema
6. **Anexos**: Screenshots se relevante

### Informações Úteis para Suporte

Sempre inclua:
- **Sistema Operacional**: Windows/macOS/Linux + versão
- **Versão Python**: `python --version`
- **Versão Poetry**: `poetry --version`
- **Versão da Aplicação**: 1.0.0
- **Comando executado**: Comando que causou o erro
- **Mensagem de erro**: Texto completo do erro

---

## 📊 Recursos Adicionais

### Documentação Técnica

- **📋 README Completo**: [README.md](README.md)
- **🔧 Configuração Poetry**: [pyproject.toml](pyproject.toml)
- **📊 Histórico de Mudanças**: [CHANGELOG.md](CHANGELOG.md)

### Referências Astronômicas

- **🌙 Skyfield**: [rhodesmill.org/skyfield](https://rhodesmill.org/skyfield/)
- **🌍 Efemérides DE421**: NASA/JPL Development Ephemeris
- **📅 Calendário Hebraico**: Referências históricas e religiosas

### Comunidade

- **👥 GitHub**: [Repositório Principal](https://github.com/vanderloto/biblical_calendar_app)
- **📧 Contato Direto**: vander.loto@outlook.com
- **🏢 DATAMETRIA**: Empresa desenvolvedora

---

<div align="center">

**Mantido por**: Vander Loto - DATAMETRIA  
**Última Atualização**: 27/01/2025  
**Versão do Guia**: 1.0.0

---

**Precisa de ajuda?** [📧 Entre em Contato](mailto:vander.loto@outlook.com)

</div>